import boto3

client = boto3.client(
    service_name='mturk',
    endpoint_url='https://mturk-requester-sandbox.us-east-1.amazonaws.com',
)

response = client.delete_hit(HITId='string')
