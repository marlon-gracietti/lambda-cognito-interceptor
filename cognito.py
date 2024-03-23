# cognito.py
import boto3

cognito_client = boto3.client("cognito-idp")

def get_user_attributes(username, user_pool_id):
    response = cognito_client.admin_get_user(
        UserPoolId=user_pool_id,
        Username=username
    )
    attributes = {attr["Name"]: attr["Value"] for attr in response["UserAttributes"]}
    return attributes
