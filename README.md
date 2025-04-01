# Reddit Sentiment Analysis Pipeline

## Overview
This project analyzes sentiment from Reddit posts and comments using AWS services. The data is collected via the Reddit API, processed using AWS Lambda, stored in S3, queried with Athena, and visualized using Amazon QuickSight.

## Tech Stack
- **Data Collection**: Reddit API
- **Processing & Storage**: AWS Lambda, S3, Athena
- **Analysis**: SQL, Python (Pandas, Boto3)
- **Visualization**: Amazon QuickSight

## Key Insights
- The sentiment of Reddit comments varies significantly based on discussion topics.
- Community sentiment trends can be tracked over time using aggregated scores.
- Posts with high engagement tend to have more extreme sentiment values.

## Dashboard Previews
*(Insert images of QuickSight dashboards here)*

## How to Run the Project
### **1. Set Up AWS Lambda Functions**
- Deploy two AWS Lambda functions:
  - **Data Collection**: Fetches Reddit posts and comments.
  - **Sentiment Analysis**: Assigns sentiment scores and stores them in S3.

### **2. Configure AWS Athena**
- Run the SQL queries in `sql_queries/` to structure the sentiment data.

### **3. Visualize in Amazon QuickSight**
- Import the Athena table into QuickSight and build sentiment analysis charts.

## Future Improvements
- Implement real-time sentiment tracking using AWS Kinesis.
- Extend analysis to multiple subreddits for broader insights.

## Contact
For questions or suggestions, feel free to reach out!

