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
        productId = event["pathParameters"]["productId"]
        
        dynamodb = boto3.resource("dynamodb")
        products = dynamodb.Table(tableProducts)
        stocks = dynamodb.Table(tableStocks)
        
        product = products.get_item(Key={"id": productId})['Item']
        count = stocks.get_item(Key={"product_id": productId})['Item']['count']
        product['count'] = count
      
        return {
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'statusCode': 200,
            'body': json.dumps(product, cls=DecimalEncoder)
        }

    except:
        return {
            'statusCode': 500,
            'body': json.dumps('Something went wrong :(')
        }