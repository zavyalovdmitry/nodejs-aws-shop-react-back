import boto3
import logging
import botocore
import json
import uuid
import os
import random
import string

tableProducts = os.environ['dynamo_table_products']
tableStocks = os.environ['dynamo_table_stocks']

def lambda_handler(event, context):
    print('Got incoming request: ', event)
    try: 
        
        if (event.get("body") == None):
            letters = string.ascii_lowercase
    
            title = ''.join(random.choice(letters) for i in range(5))
            description = ''.join(random.choice(letters) for i in range(20))
            price = random.randint(0, 555)
            count = random.randint(0, 55)
        else:
            try:
                body = json.loads(event["body"])
    
                title = body["title"]
                description = body["description"]
                price = body["price"]
                count = body["count"]
                
                if not price.isdigit() or not count.isdigit():
                    return {
                        'statusCode': 400,
                        'body': json.dumps('Incorrect product data!')
                    } 
            except:
                return {
                    'statusCode': 400,
                    'body': json.dumps('Incorrect product data!')
                }
    
        dynamo = boto3.client('dynamodb')
        logger = logging.getLogger()
        
        #title = event['title']
        #description = event['description']
        #price = event['price']
        #count = event['count']
    
        productsItem = {}
        stocksItem = {}
        
        productId = str(uuid.uuid4())
    
        productsItem['id'] = {'S': productId}
        productsItem['title'] = {'S': title}
        productsItem['description'] = {'S': description}
        productsItem['price'] = {'N': str(price)}
        
        stocksItem['product_id'] = {'S': productId}
        stocksItem['count'] = {'N': str(count)}
        
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
    except:
        return {
            'statusCode': 500,
            'body': json.dumps('Something went wrong :(')
        }
