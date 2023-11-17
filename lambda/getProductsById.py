import json
import boto3

s3_client = boto3.client("s3")
S3_BUCKET = 'dz-task-3'

def lambda_handler(event, context):
    print(event)
    object_key = "data.json"  
    file_content = s3_client.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read().decode('utf-8')
    list_data = json.loads(file_content)
    
    for record in list_data:
        print(record)
        if record["id"] == "1":
            return {
                'statusCode': 200,
                'body': json.dumps(event)
            }

    return {
        'statusCode': 200,
        'body': json.dumps(event["pathParameters"]["productId"])
    }