import json
import boto3
import os
import botocore

from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

tableProducts = os.environ['dynamo_table_products']
tableStocks = os.environ['dynamo_table_stocks']

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource("dynamodb")
        products = dynamodb.Table(tableProducts)
        stocks = dynamodb.Table(tableStocks)
        all_products = []
    
        try:
            # Loop through subscribers in DynamoDB
            response = products.scan()
            all_products = response['Items']
            print("all_products: ",all_products)
    
            # Paginate through DynamoDB response
            while 'LastEvaluatedKey' in response:
                response = products.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                all_products.extend(response['Items'])
            
        except botocore.exceptions.ClientError as e:
            print(e.response['Error']['Message'])
        
        print("all_products: ",all_products)
        
        joined_data = []
        
        for product in all_products:
            count = stocks.get_item(Key={"product_id": product["id"]})['Item']['count']
            product["count"] = count
            joined_data.append(product)
      
        return {
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'statusCode': 200,
            'body': json.dumps(joined_data, cls=DecimalEncoder)
        }
    except:
        return {
            'statusCode': 500,
            'body': json.dumps('Something went wrong :(')
        }