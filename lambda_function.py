import boto3
import praw
import os
import datetime
import logging
import asyncio
from decimal import Decimal
from tenacity import retry, wait_fixed, stop_after_attempt

# Initialize AWS resources
dynamodb = boto3.resource("dynamodb", region_name=os.environ["REGION"])
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])
comprehend = boto3.client("comprehend", region_name=os.environ["REGION"])


# Configure Reddit client
reddit = praw.Reddit(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    user_agent=os.environ["USER_AGENT"],
)

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# convert float to decimal because dynamodb doesnt underdant floats
def convert_floats_to_decimal(data):
    if isinstance(data, list):
        return [convert_floats_to_decimal(item) for item in data]
    if isinstance(data, dict):
        return {k: convert_floats_to_decimal(v) for k, v in data.items()}
    if isinstance(data, float):
        return Decimal(str(data))
    return data

#function to analyze sentiment in batches to improve performance
@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
async def analyze_sentiment_batch(texts):
    texts = list(texts)  # Convert generators to lists
    if not texts:
        return []
    
    try:
        # Process in 25s
        results = []
        for i in range(0, len(texts), 25):
            batch = texts[i:i+25]
            response = comprehend.batch_detect_sentiment(
                TextList=batch,
                LanguageCode='es'
            )
            results.extend([item['Sentiment'] for item in response['ResultList']])
        return results
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {str(e)}")
        return ['NEUTRAL'] * len(texts)  # Fallback 

# Fetch posts from reddit, exceptions included
@retry(wait=wait_fixed(5), stop=stop_after_attempt(3))
async def fetch_reddit_posts(subreddit_name, limit=10):
    try:
        subreddit = await asyncio.to_thread(reddit.subreddit, subreddit_name)
        posts = await asyncio.to_thread(lambda: list(subreddit.hot(limit=limit)))
        return posts
    except praw.exceptions.APIException as e:
        logger.error(f"Reddit API error: {str(e)}")
        raise

async def process_post(post):
    try:
        # Get top 2 comments (convert first CommentForest to list)
        all_comments = await asyncio.to_thread(lambda: list(post.comments))
        comments = [
            c.body for c in all_comments[:2]
            if not c.distinguished and isinstance(c, praw.models.Comment)
        ]
        
        # Analyze sentiments
        post_sentiment = (await analyze_sentiment_batch([post.title]))[0]
        comment_sentiments = await analyze_sentiment_batch(comments)
        
        # Build DynamoDB item with correct S key structure
        item = {
            "post_id": post.id,
            "timestamp": int(datetime.datetime.utcnow().timestamp()),
            "title": post.title,
            "score": post.score,
            "url": post.url,
            "sentiment": post_sentiment,
            "comments_sentiment": [{"S": s} for s in comment_sentiments]
        }
        
        return convert_floats_to_decimal(item)
        
    except Exception as e:
        logger.error(f"Failed processing post {post.id}: {str(e)}")
        return None

# Async processing loop
async def main_handler(event, context):
    try:
        posts = await fetch_reddit_posts("mexico", limit=10)
        processed_items = await asyncio.gather(*(process_post(p) for p in posts))
        
        # Filter out failed items
        valid_items = [item for item in processed_items if item is not None]
        
        # Batch write with error handling
        with table.batch_writer() as writer:
            for item in valid_items:
                try:
                    writer.put_item(Item=item)
                    logger.info(f"Inserted post ID: {item.get('post_id', 'Unknown')}")
                except Exception as e:
                    logger.error(f"Failed to write {item['post_id']}: {str(e)}")
        
        return {
            "statusCode": 200,
            "body": f"Processed {len(valid_items)}/{len(posts)} posts"
        }
        
    except Exception as e:
        logger.error(f"Critical failure: {str(e)}")
        return {"statusCode": 500, "body": "Processing failed"}

# Entry to lambda
def lambda_handler(event, context):
    return asyncio.run(main_handler(event, context))
