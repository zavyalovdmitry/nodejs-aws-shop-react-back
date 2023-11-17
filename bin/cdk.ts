#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { NodejsAwsShopReactBackStack } from '../lib/cdk';

const app = new cdk.App();
new NodejsAwsShopReactBackStack(app, 'NodejsAwsShopReactBackStack');
