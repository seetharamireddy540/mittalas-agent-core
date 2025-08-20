from ast import mod
from strands import Agent, tool
from strands_tools import calculator
import argparse
import json
from strands.models import BedrockModel
import requests 
import os
from bedrock_agentcore.runtime import BedrockAgentCoreApp


app = BedrockAgentCoreApp()

@tool
def weather():
    """ Get weather """ # Dummy implementation
    return "sunny"


@tool
def weather():
    """ Get weather """ # Dummy implementation
    return "sunny"

model = BedrockModel(model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                     region_name="us-east-1"
                     )


agent = Agent(model=model, 
            tools=[calculator, calculator],
            system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather."
)    


@app.entrypoint
def strands_agent_bedrock(payload):
    """
    Invoke the agent with a payload from Bedrock Agent Core.
    """
    user_input = payload.get("prompt")
    print(f"User input {user_input}")
    response = agent(user_input)
    return response.message['content'][0]['text']
    
if __name__ == "__main__":
    app.run()