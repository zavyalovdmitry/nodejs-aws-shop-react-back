import json
import boto3

s3_client = boto3.client("s3")
S3_BUCKET = 'dz-task-3'

def lambda_handler(event, context):
    object_key = "data.json"  
    file_content = s3_client.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read().decode('utf-8')
  
    return {
        'statusCode': 200,
        'body': json.dumps(file_content)
    }
