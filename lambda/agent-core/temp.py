import re
from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session
import boto3
import time
boto_session = Session()
region = boto_session.region_name

agentcore_runtime = Runtime()
agent_name = "strands_claude_getting_started"
response = agentcore_runtime.configure(
    entrypoint="strands_claude.py",
    auto_create_execution_role=True,
    auto_create_ecr=True,
    requirements_file="requirements.txt",
    region="us-east-1",
    agent_name=agent_name
)
response

launch_result = agentcore_runtime.launch()
status_response = agentcore_runtime.status()
status = status_response.endpoint['status']
end_status = ['READY', 'CREATE_FAILED', 'DELETE_FAILED', 'UPDATE_FAILED']
while status not in end_status:
    time.sleep(10)
    status_response = agentcore_runtime.status()
    status = status_response.endpoint['status']
    print(status)
status

launch_result.ecr_uri, launch_result.agent_id, launch_result.ecr_uri.split('/')[1]

invoke_response = agentcore_runtime.invoke({"prompt": "How is the weather now?"})
print(invoke_response)

# agentcore_control_client = boto3.client(
#     'bedrock-agentcore-control',
#     region_name="us-east-1"
# )
# ecr_client = boto3.client(
#     'ecr',
#     region_name="us-east-1"
    
# )

# runtime_delete_response = agentcore_control_client.delete_agent_runtime(
#     agentRuntimeId=launch_result.agent_id,
    
# )

# response = ecr_client.delete_repository(
#     repositoryName=launch_result.ecr_uri.split('/')[1],
#     force=True
# )

# print(response)