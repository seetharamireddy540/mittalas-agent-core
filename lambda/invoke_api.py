import boto3
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

def invoke_api():
    url = "https://8k1q6pjzhe.execute-api.us-east-1.amazonaws.com/prod/"
    
    session = boto3.Session()
    credentials = session.get_credentials()
    
    request = AWSRequest(method='GET', url=url)
    SigV4Auth(credentials, 'execute-api', 'us-east-1').add_auth(request)
    
    response = requests.get(url, headers=dict(request.headers))
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    invoke_api()