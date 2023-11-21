import boto3
import logging
import botocore
import json
import uuid
import os

tableProducts = 'products'
tableStocks = 'stocks'

# print("environment variable : " + os.environ['env_variable'])

def lambda_handler(event, context):
    dynamo = boto3.client('dynamodb')
    logger = logging.getLogger()
    s3_client = boto3.client("s3")
    S3_BUCKET = 'dz-task-3' 
    
    object_key = "data.json"  
    file_content = s3_client.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read().decode('utf-8')
    list_data = json.loads(file_content)
    
    print(list_data)
    
    for record in list_data:
        productsItem = {}
        stocksItem = {}
        
        productId = str(uuid.uuid4())
        stockId = str(uuid.uuid4())
    
        productsItem['id'] = {'S': productId}
        productsItem['title'] = {'S': record["title"]}
        productsItem['description'] = {'S': record["description"]}
        productsItem['price'] = {'N': str(record["price"])}
        
        stocksItem['id'] = {'S': stockId}
        stocksItem['product_id'] = {'S': productId}
        stocksItem['count'] = {'N': str(13)}
        
        try:        
            dynamo.put_item(            
                TableName=tableProducts,            
                Item=productsItem)    
            dynamo.put_item(            
                TableName=tableStocks,            
                Item=stocksItem)    
            
        except botocore.exceptions.ClientError as err:        
            logger.error(            
                "Couldn't put stats %s into table %s. Here's why: %s: %s",            
                'on users', 'userstats-prod',            
                err.response['Error']['Code'], err.response['Error']['Message'])        
            raise
        
    return {
        'statusCode': 200,
        'body': json.dumps('All good!')
    }
