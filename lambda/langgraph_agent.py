
from typing import Annotated

from typing_extensions import TypedDict
from dotenv import load_dotenv
# Ensure your AWS credentials are configured

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

model = init_chat_model("anthropic.claude-3-5-sonnet-20240620-v1:0", model_provider="bedrock_converse",
                          region_name="us-east-1")

messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]

model.invoke(messages)