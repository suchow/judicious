import os

import boto3

mode = os.environ.get("JUDICIOUS_MTURK_MODE", "sandbox")

if mode == "sandbox":
    client = boto3.client(
        service_name='mturk',
        endpoint_url='https://mturk-requester-sandbox.us-east-1.amazonaws.com',
        region_name="us-east-1",
    )
elif mode == "live":
    client = boto3.client(
        service_name='mturk',
        region_name="us-east-1",
    )
# Test that you can connect to the API by checking your account balance
user_balance = client.get_account_balance()

# In Sandbox this always returns $10,000
print("Your account balance is {}".format(user_balance['AvailableBalance']))

# Create the HIT
response = client.create_hit_with_hit_type(
    HITTypeId=os.environ["JUDICIOUS_MTURK_HIT_TYPE_ID"],
    MaxAssignments=1,
    LifetimeInSeconds=os.environ.get("JUDICIOUS_MTURK_LIFETIME",
                                     1 * 24 * 60 * 60),
    Question=open("external.xml", "r").read(),
)

# The response included several fields that will be helpful later
hit_type_id = response['HIT']['HITTypeId']
hit_id = response['HIT']['HITId']
print("Your HIT has been created. You can see it at this link:")
print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(
    hit_type_id))
print("Your HIT ID is: {}".format(hit_id))
