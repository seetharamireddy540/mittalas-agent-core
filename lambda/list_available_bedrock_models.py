import boto3
import json
from botocore.exceptions import ClientError

def list_available_bedrock_models(region_name="us-west-2"):
    """
    Lists all AWS Bedrock models that the current AWS credentials have access to.
    
    Args:
        region_name (str): AWS region where Bedrock is available
        
    Returns:
        list: A list of model IDs available to the user
    """
    try:
        # Create a Bedrock client
        bedrock_client = boto3.client(
            service_name='bedrock',
            region_name=region_name
        )
        
        # Get list of foundation models
        response = bedrock_client.list_foundation_models()
        
        # Extract model IDs and organize by provider
        available_models = {}
        
        for model in response.get('modelSummaries', []):
            model_id = model.get('modelId')
            provider_name = model.get('providerName')
            
            if provider_name not in available_models:
                available_models[provider_name] = []
            
            available_models[provider_name].append(model_id)
        
        return available_models
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')
        error_msg = e.response.get('Error', {}).get('Message')
        
        if error_code == 'AccessDeniedException':
            print(f"Access denied: {error_msg}")
            print("Make sure your AWS credentials have proper permissions to access Bedrock.")
        else:
            print(f"AWS Error: {error_code} - {error_msg}")
        
        return {}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {}

def main():
    # You can change the region to where you have Bedrock access
    region = "us-east-1"  # Common regions for Bedrock include us-east-1, us-west-2
    
    print(f"Fetching available Bedrock models in {region}...")
    models_by_provider = list_available_bedrock_models(region)
    
    if not models_by_provider:
        print("No models found or couldn't access AWS Bedrock.")
        print("Check your AWS credentials and permissions.")
        return
    
    print("\nAvailable AWS Bedrock models:")
    print("===========================\n")
    
    for provider, models in models_by_provider.items():
        print(f"Provider: {provider}")
        print("-" * (len(provider) + 10))
        
        for i, model_id in enumerate(models, 1):
            print(f"{i}. {model_id}")
        
        print()  # Add empty line between providers
    
    print(f"Total providers: {len(models_by_provider)}")
    print(f"Total models: {sum(len(models) for models in models_by_provider.values())}")

if __name__ == "__main__":
    main()