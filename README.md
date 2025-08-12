# Lambda API Service with CDK

A containerized Lambda web service with API Gateway and IAM authentication.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Bootstrap CDK (first time only):
```bash
npx cdk bootstrap
```

3. Deploy the stack:
```bash
npm run deploy
npm run deploy:arm64
npm run deploy:x86_64
or 
LAMBDA_ARCH=x86_64 cdk deploy




```

## Architecture

- **Lambda Function**: Containerized Python function
- **API Gateway**: REST API with IAM authentication
- **Docker**: Lambda runs in a container for better dependency management

## Testing

The API requires IAM authentication. Use AWS CLI or SDK with proper credentials:

```bash
aws apigateway test-invoke-method \
  --rest-api-id <API_ID> \
  --resource-id <RESOURCE_ID> \
  --http-method GET
```

## Cleanup

```bash
npx cdk destroy
```

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install Strands and tools
pip install strands-agents strands-agents-tools