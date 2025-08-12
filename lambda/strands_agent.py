from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from strands_tools import http_request
from mcp import stdio_client, StdioServerParameters

model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

# Bedrock
bedrock_model = BedrockModel(
  model_id=model_id,
  temperature=0.3,
  streaming=True, # Enable/disable streaming
  region_name="us-east-1"
)
agent = Agent(model=bedrock_model)
response = agent("Tell me about Agentic AI")

print(response)