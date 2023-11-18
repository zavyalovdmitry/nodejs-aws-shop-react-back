#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { AwsStack } from '../lib/cdk';

const region = process.env.AWS_REGION
const account = process.env.AWS_ACCOUNT

const app = new cdk.App();
new AwsStack(app, 'AwsStack',
  {
    env: {
      region, account
    }
  }
);
