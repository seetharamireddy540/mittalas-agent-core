import boto3
import json

class BedrockAgent:
    def __init__(self, region_name="us-east-1"):
        """
        Initialize the Bedrock agent with AWS credentials and region.
        
        Args:
            region_name (str): AWS region where Bedrock is available
        """
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=region_name
        )
        
    def invoke_model(self, model_id, prompt, max_tokens=512, temperature=0.7):
        """
        Invoke a model on AWS Bedrock.
        
        Args:
            model_id (str): The model ID to use
            prompt (str): The prompt to send to the model
            max_tokens (int): Maximum number of tokens to generate
            temperature (float): Controls randomness (0.0 to 1.0)
            
        Returns:
            dict: The model's response
        """
        try:
            # Use Messages API for Claude 3.5 models
            if "claude-3" in model_id:
                body = json.dumps({
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "anthropic_version": "bedrock-2023-05-31"
                })
            # Legacy format for older Claude models
            elif "anthropic" in model_id:
                body = json.dumps({
                    "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                    "max_tokens_to_sample": max_tokens,
                    "temperature": temperature
                })
            elif "amazon.titan" in model_id:
                body = json.dumps({
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": max_tokens,
                        "temperature": temperature
                    }
                })
            else:
                body = json.dumps({
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                })
                
            response = self.client.invoke_model(
                modelId=model_id,
                body=body
            )
            
            response_body = json.loads(response.get('body').read())
            
            # Parse response based on model type
            if "claude-3" in model_id:
                return {"text": response_body.get("content")[0].get("text")}
            elif "anthropic" in model_id:
                return {"text": response_body.get("completion")}
            elif "amazon.titan" in model_id:
                return {"text": response_body.get("results")[0].get("outputText")}
            else:
                return response_body
                
        except Exception as e:
            return {"error": str(e)}


# Example usage
if __name__ == "__main__":
    # Create an instance of the agent
    agent = BedrockAgent(region_name="us-east-1")  # Use a region where Bedrock is available
    
    # Define parameters
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    prompt = "Explain how machine learning works in simple terms."
    
    # Invoke the model
    response = agent.invoke_model(model_id, prompt)
    
    # Print the response
    if "error" in response:
        print(f"Error: {response['error']}")
    else:
        print(f"Response: {response['text']}")