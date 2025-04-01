import boto3
import json
import os
from datetime import datetime
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer
from decimal import Decimal

def lambda_handler(event, context):
    # Initialize clients
    dynamodb = boto3.client('dynamodb')
    s3 = boto3.client('s3')
    table_name = os.environ.get('DYNAMODB_TABLE', 'default-table')
    bucket_name = os.environ.get('S3_BUCKET', 'default-bucket')
    deserializer = TypeDeserializer()

    def convert_decimals(obj):
        if isinstance(obj, Decimal):
            return float(obj) if '.' in str(obj) else int(obj)
        if isinstance(obj, dict):
            return {k: convert_decimals(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [convert_decimals(v) for v in obj]
        return obj

    try:
        paginator = dynamodb.get_paginator('scan')
        iterator = paginator.paginate(
            TableName=table_name,
            PaginationConfig={'PageSize': 100}
        )
        
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        s3_key = f'exports/{timestamp}/data.json'
        
        record_count = 0
        json_lines = []

        for page in iterator:
            for item in page['Items']:
                python_item = {k: deserializer.deserialize(v) for k, v in item.items()}
                converted_item = convert_decimals(python_item)
                json_lines.append(json.dumps(converted_item))
                record_count += 1

                if len(json_lines) >= 100:
                    write_to_s3(s3, bucket_name, s3_key, '\n'.join(json_lines))
                    json_lines = []

        if json_lines:
            write_to_s3(s3, bucket_name, s3_key, '\n'.join(json_lines))

        return {
            'statusCode': 200,
            'body': f"Exported {record_count} records to {s3_key}"
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': f"AWS Error: {e.response['Error']['Message']}"
        }

def write_to_s3(s3_client, bucket, key, content):
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=content,
            ContentType='application/json'
        )
    except ClientError as e:
        raise Exception(f"S3 upload failed: {e}")
