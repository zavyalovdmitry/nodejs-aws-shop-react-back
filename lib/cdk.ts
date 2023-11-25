import { Duration, Stack, StackProps } from 'aws-cdk-lib';
// import * as sns from 'aws-cdk-lib/aws-sns';
// import * as subs from 'aws-cdk-lib/aws-sns-subscriptions';
// import * as sqs from 'aws-cdk-lib/aws-sqs';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';

const lambda_envs =       {
  dynamo_table_products: "products",
  dynamo_table_stocks: "stocks",
}

export class AwsStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const api = new apigateway.RestApi(this, 'api', {
      description: 'task 3 : api gateway',
      deployOptions: {
        stageName: 'dev',
      },

      defaultCorsPreflightOptions: {
        allowHeaders: [
          'Content-Type',
          'X-Amz-Date',
          'Authorization',
          'X-Api-Key',
        ],
        allowMethods: ['OPTIONS', 'GET'],
        allowCredentials: true,
        allowOrigins: apigateway.Cors.ALL_ORIGINS
      },
    });

    new cdk.CfnOutput(this, 'apiUrl', { value: api.url });
    
    const s3ListBucketsPolicy = new iam.PolicyStatement({
      actions: ['s3:*'],
      resources: ['arn:aws:s3:::*'],
    });

    const getProductsList_lambda = new lambda.Function(this, "getProductsList", {
      runtime: lambda.Runtime.PYTHON_3_11, 
      code: lambda.Code.fromAsset("lambda/getProductsList"), 
      handler: 'lambda_function.lambda_handler', 
      environment: lambda_envs
    });

    const productsList = api.root.addResource('products');

    productsList.addMethod(
      'GET',
      new apigateway.LambdaIntegration(getProductsList_lambda, {proxy: true}),
    );

    getProductsList_lambda.role?.attachInlinePolicy(
      new iam.Policy(this, 'list-buckets-policy-getProductsList', {
        statements: [s3ListBucketsPolicy],
      }),
    );

    const getProductsById_lambda = new lambda.Function(this, "getProductsById", {
      runtime: lambda.Runtime.PYTHON_3_11, 
      code: lambda.Code.fromAsset("lambda/getProductsById"), 
      handler: 'lambda_function.lambda_handler', 
      environment: lambda_envs
    });
  
    const productsBuId = productsList.addResource('{productId}');

    productsBuId.addMethod(
      'GET',
      new apigateway.LambdaIntegration(getProductsById_lambda, {proxy: true}),
    );

    getProductsById_lambda.role?.attachInlinePolicy(
      new iam.Policy(this, 'list-buckets-policy-getProductsById', {
        statements: [s3ListBucketsPolicy],
      }),
    );
  }
}
