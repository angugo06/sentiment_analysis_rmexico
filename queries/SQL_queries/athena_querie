WITH exploded AS (
    SELECT 
        a.post_id,
        FROM_UNIXTIME(a.timestamp) AS formatted_date, -- Convert UNIX timestamp to date
        a.score,
        -- Map post sentiment to numerical value
        CASE 
            WHEN a.sentiment = 'POSITIVE' THEN 1
            WHEN a.sentiment = 'NEUTRAL' THEN 0
            WHEN a.sentiment = 'NEGATIVE' THEN -1
            ELSE 0
        END AS post_sentiment_score,
        -- Exploding the comments_sentiment array
        t.comment_sentiment
    FROM 
        reddit_sentiment_db.reddit_sentiment_analysis a
    CROSS JOIN UNNEST(a.comments_sentiment) AS t (comment_sentiment) -- Unnest the array to separate comments sentiment
),
comment_sentiment_score AS (
    SELECT
        post_id,
        formatted_date,
        score,
        post_sentiment_score,
        -- Map each comment sentiment to a numerical value
        CASE 
            WHEN comment_sentiment = 'POSITIVE' THEN 1
            WHEN comment_sentiment = 'NEUTRAL' THEN 0
            WHEN comment_sentiment = 'NEGATIVE' THEN -1
            ELSE 0
        END AS comment_sentiment_score
    FROM exploded
),
-- Calculate average comment sentiment per post
average_comment_sentiment AS (
    SELECT
        post_id,
        AVG(comment_sentiment_score) AS avg_comment_sentiment
    FROM comment_sentiment_score
    GROUP BY post_id
)
-- Now, we calculate the overall sentiment as the average of the post sentiment and the average comment sentiment
SELECT 
    c.post_id,
    c.formatted_date,
    c.score,
    c.post_sentiment_score,
    ac.avg_comment_sentiment,
    -- Calculate overall sentiment
    (c.post_sentiment_score + ac.avg_comment_sentiment) / 2 AS overall_sentiment_score
FROM 
    comment_sentiment_score c
JOIN 
    average_comment_sentiment ac ON c.post_id = ac.post_id
GROUP BY 
    c.post_id, c.formatted_date, c.score, c.post_sentiment_score, ac.avg_comment_sentiment
ORDER BY 
    c.formatted_date
