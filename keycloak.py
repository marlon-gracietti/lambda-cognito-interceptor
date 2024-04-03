import urllib.request
import urllib.parse
import json
import os

# Carregando variáveis de ambiente
CLIENT_SECRET = os.getenv('KEYCLOAK_CLIENT_SECRET')
CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID')
KEYCLOAK_BASE_URL = os.getenv('KEYCLOAK_BASE_URL')
REALM_NAME = os.getenv('KEYCLOAK_REALM_NAME')
GROUP_ID = os.getenv('KEYCLOAK_GROUP_ID')

def get_keycloak_access_token():
    url = f"{KEYCLOAK_BASE_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    data = urllib.parse.urlencode(payload).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req) as response:
        response_body = response.read()
        return json.loads(response_body.decode())["access_token"]

def get_user_id(username, access_token):
    url = f"{KEYCLOAK_BASE_URL}/admin/realms/{REALM_NAME}/users?username={username}"
    headers = {"Authorization": f"Bearer {access_token}"}
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req) as response:
        response_body = response.read()
        users = json.loads(response_body.decode())
        if users:
            return users[0]['id']
    return None

def add_user_to_keycloak(user_data, access_token):
    url = f"{KEYCLOAK_BASE_URL}/admin/realms/{REALM_NAME}/users"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, data=json.dumps(user_data).encode(), headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 201:
                print(f"User added: {user_data['username']}")
            else:
                print(f"Unexpected status code received when adding user: {response.status}")
    except urllib.error.HTTPError as e:
        if e.code == 409:
            print(f"User already exists: {user_data['username']}")
        else:
            raise

def update_user_in_keycloak(user_id, user_data, access_token):
    url = f"{KEYCLOAK_BASE_URL}/admin/realms/{REALM_NAME}/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, data=json.dumps(user_data).encode(), headers=headers, method='PUT')
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 204:
                print(f"User updated: {user_data['username']}")
            else:
                print(f"Unexpected status code received when updating user: {response.status}")
    except urllib.error.HTTPError as e:
        raise Exception(f"Failed to update user: {e}")

def add_or_update_user_in_keycloak(user_data, access_token):
    user_id = get_user_id(user_data['username'], access_token)
    if user_id:
        update_user_in_keycloak(user_id, user_data, access_token)
        add_user_into_group(user_id, access_token)
    else:
        add_user_to_keycloak(user_data, access_token)
        user_id = get_user_id(user_data['username'], access_token)
        add_user_into_group(user_id, access_token)

def add_user_into_group(user_id, access_token):    
    url = f"{KEYCLOAK_BASE_URL}/admin/realms/{REALM_NAME}/users/{user_id}/groups/{GROUP_ID}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    req = urllib.request.Request(url, headers=headers, method='PUT')
    try:
        with urllib.request.urlopen(req) as response:
            # Verificando o código de status 204 para sucesso
            if response.status == 204:
                print(f"User {user_id} successfully added to group {GROUP_ID}")
            else:
                print(f"Unexpected status code received when adding user to group: {response.status}")
    except urllib.error.HTTPError as e:
        raise Exception(f"Failed to add user into group: {e}")
