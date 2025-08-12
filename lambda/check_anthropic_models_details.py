import boto3
import json
from tabulate import tabulate

def get_anthropic_model_details(region_name="us-east-1"):
    """
    Lists all Anthropic models in AWS Bedrock and their throughput requirements.
    
    Args:
        region_name (str): AWS region where Bedrock is available
        
    Returns:
        list: Details of Anthropic models
    """
    try:
        # Create a Bedrock client
        bedrock_client = boto3.client(
            service_name='bedrock',
            region_name=region_name
        )
        
        # Get list of foundation models
        response = bedrock_client.list_foundation_models()
        
        # Extract Anthropic models and their details
        anthropic_models = []
        
        for model in response.get('modelSummaries', []):
            provider_name = model.get('providerName', '')
            
            if 'anthropic' in provider_name.lower():
                model_id = model.get('modelId', '')
                model_name = model.get('modelName', '')
                
                # Check if on-demand throughput is supported
                on_demand_supported = model.get('inferenceTypesSupported', [])
                requires_provisioned = 'ON_DEMAND' not in on_demand_supported
                
                anthropic_models.append({
                    "Model ID": model_id,
                    "Model Name": model_name,
                    "Requires Provisioned": "Yes" if requires_provisioned else "No",
                    "Inference Types": ", ".join(on_demand_supported)
                })
        
        return anthropic_models
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def main():
    region = "us-east-1"  # Common region for Bedrock
    
    print(f"Fetching Anthropic model details from AWS Bedrock in {region}...")
    anthropic_models = get_anthropic_model_details(region)
    
    if not anthropic_models:
        print("No Anthropic models found or couldn't access AWS Bedrock.")
        return
    
    print("\nAnthropic Models in AWS Bedrock:")
    print(tabulate(anthropic_models, headers="keys", tablefmt="grid"))
    
    # List models requiring provisioned throughput
    provisioned_models = [m for m in anthropic_models if m["Requires Provisioned"] == "Yes"]
    
    if provisioned_models:
        print("\nAnthropic Models Requiring Provisioned Throughput:")
        for model in provisioned_models:
            print(f"- {model['Model Name']} ({model['Model ID']})")

if __name__ == "__main__":
    main()