# lambda_function.py
import os
import base64
from cognito import get_user_attributes
from keycloak import get_keycloak_access_token, add_or_update_user_in_keycloak

USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')

def lambda_handler(event, context):
       
    auth_header = event.get("authorizationToken")
    if not auth_header:
        print("Authorization header is missing")
        return generate_policy("user", "Deny", event["methodArn"])

    encoded_token = auth_header.split(" ")[1]
    decoded_value = base64.b64decode(encoded_token).decode("utf-8")    
    username, password = decoded_value.split(":")
    
    try:
        user_attributes = get_user_attributes(username, USER_POOL_ID)
        print("User Attributes:", user_attributes)
        
        access_token = get_keycloak_access_token()

        user_data = {
            "username": username,
            "enabled": True,
            "firstName": username,   
            "lastName": username,      
            "email": user_attributes.get("email", "default"),      
            "attributes": user_attributes,
            "credentials": [{
                "type": "password",
                "value": password,
                "temporary": False  
            }]                        
        }
        add_or_update_user_in_keycloak(user_data, access_token)
        
    except Exception as e:
        print("Error:", str(e))
        return generate_policy("user", "Deny", event["methodArn"])

    return generate_policy("user", "Allow", event["methodArn"])

def generate_policy(principal_id, effect, resource):
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "execute-api:Invoke",
            "Effect": effect,
            "Resource": resource,
        }]
    }
    return {
        "principalId": principal_id,
        "policyDocument": policy_document,
    }
