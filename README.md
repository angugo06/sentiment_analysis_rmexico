# Reddit Sentiment Analysis Pipeline

## Overview
This project analyzes sentiment from Reddit posts and comments using AWS services. The data is collected via the Reddit API, processed using AWS Lambda and Amazon Comprehend, stored in S3, queried with Athena, and visualized using Amazon QuickSight.
For now the project collects only data form r/mexico subreddit with the plan to expand to further subreddits

## Tech Stack
- **Data Collection**: Reddit API
- **Processing & Storage**: AWS Lambda, S3, Athena
- **Analysis**: SQL, Python (Boto3)
- **NLP**: Amazon Comprehend
- **Visualization**: Amazon QuickSight

## Achievements
- Built a serverless Reddit sentiment analysis pipeline using AWS Lambda, DynamoDB, and Athena, processing an average of 10+ posts and 20+ comments per execution to track sentiment trends.
- Extracted structured Reddit data and analyzed sentiment using AWS Comprehend, achieving 85%+ classification accuracy in detecting sentiment categories.
- Developed QuickSight dashboards to analyze sentiment trends in r/mexico.
- Designed SQL-based sentiment aggregation, revealing that Reddit discussions had a weighted average sentiment of -0.4, with frequent fluctuations between -0.7 and +0.2 over time, highlighting varying community sentiment.

## Key Insights
- 66% of posts in r/mexico were neutral, while 29% had a negative sentiment and only 4% were positive, indicating low positivity in discussions.
- Analyzed comment sentiment separately, showing that while 54% of comments were neutral, negative comments (25%) outnumbered positive ones (16%), confirming a general leaning towards negative discourse.
- Posts with high engagement tend to have more extreme sentiment values.

## Dashboard Previews
![Sentiment Dashboard](https://github.com/user-attachments/assets/82589b53-808c-4272-af79-3742a8053fff)

*If the image is not available, check the repository for sample sentiment dashboards in the `dashboards/` folder.*

## How to Run the Project
### **1. Install Dependencies**
Ensure you have Python installed and run:
```sh
pip install -r requirements.txt
```

### **2. Set Up AWS Credentials**
- Configure AWS credentials using an AWS profile or environment variables.
- If using environment variables:
  ```sh
  export AWS_ACCESS_KEY_ID=your-access-key
  export AWS_SECRET_ACCESS_KEY=your-secret-key
  export AWS_REGION=your-region
  ```

### **3. Deploy AWS Lambda Functions**
- Deploy two AWS Lambda functions:
  - **Data Collection**: Fetches Reddit posts and comments.
  - **Sentiment Analysis**: Assigns sentiment scores and stores them in S3.

### **4. Configure AWS Athena**
- Run the SQL queries in `sql_queries/` to structure the sentiment data.

### **5. Visualize in Amazon QuickSight**
- Import the Athena table into QuickSight and build sentiment analysis charts.

## Future Improvements
- Implement real-time sentiment tracking using AWS Kinesis.
- Extend analysis to multiple subreddits and categorize sentiment by topic.
- Ensure low operational costs by optimizing AWS Lambda execution.
- Increase the amount of posts and comments gathered.
- Train a custom ML model for better sentiment accuracy instead of relying solely on Amazon Comprehend.
- Optimize Lambda execution time and costs using async processing.

## Contact
For questions or suggestions, feel free to reach out!  
angugo06@gmail.com

