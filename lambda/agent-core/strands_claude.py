from ast import mod
from strands import Agent, tool
from strands_tools import calculator
import argparse
import json
from strands.models import BedrockModel
import requests 
import os

@tool
def weather():
    """ Get weather """ # Dummy implementation
    return "sunny"


@tool
def weather():
    """ Get weather """ # Dummy implementation
    return "sunny"

model = BedrockModel(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
                     region_name="us-east-1"
                     )


agent = Agent(model=model, 
            tools=[calculator, calculator],
            system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather."
)    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, default="What is the weather in New York?")
    args = parser.parse_args()
    response = agent(args.prompt)
    print(response)