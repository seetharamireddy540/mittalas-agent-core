import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

export class LambdaApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Lambda function with Docker container
    const architecture = process.env.LAMBDA_ARCH === 'x86_64' ? lambda.Architecture.X86_64 : lambda.Architecture.ARM_64;
    const targetArch = process.env.LAMBDA_ARCH === 'x86_64' ? 'x86_64' : 'arm64';
    
    const lambdaFunction = new lambda.DockerImageFunction(this, 'WebServiceFunction', {
      code: lambda.DockerImageCode.fromImageAsset('./lambda', {
        buildArgs: {
          TARGETARCH: targetArch
        }
      }),
      timeout: cdk.Duration.seconds(30),
      memorySize: 512,
      architecture: architecture,
    });

    // Add Strands AI framework permissions
    lambdaFunction.addToRolePolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        'bedrock:InvokeModel',
        'bedrock:InvokeModelWithResponseStream',
        'strands:*'
      ],
      resources: ['*']
    }));

    // API Gateway with IAM authentication
    const api = new apigateway.RestApi(this, 'WebServiceApi', {
      restApiName: 'RAM Strands Agent API',
      defaultMethodOptions: {
        authorizationType: apigateway.AuthorizationType.IAM,
      },
    });

    // Lambda integration
    const lambdaIntegration = new apigateway.LambdaIntegration(lambdaFunction);

    // Add routes
    api.root.addMethod('GET', lambdaIntegration);
    api.root.addMethod('POST', lambdaIntegration);
    
    // Add specific endpoints
    const analyzeResource = api.root.addResource('analyze');
    analyzeResource.addMethod('POST', lambdaIntegration);
    
    const recommendResource = api.root.addResource('recommend');
    recommendResource.addMethod('POST', lambdaIntegration);

    // Output API URL
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: api.url,
      description: 'RAM Strands Agent API Gateway URL',
    });
  }
}
