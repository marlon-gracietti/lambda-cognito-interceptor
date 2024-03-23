# keycloak.py
import urllib.request
import urllib.parse
import json
import os

CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')
KEYCLOAK_BASE_URL = os.getenv('KEYCLOAK_BASE_URL')
REALM_NAME = os.getenv('REALM_NAME')

def get_keycloak_access_token():
    url = f"{KEYCLOAK_BASE_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    data = urllib.parse.urlencode(payload).encode()
    req = urllib.request.Request(url, data=data)  # Dados devem ser codificados
    with urllib.request.urlopen(req) as response:
        response_body = response.read()
        return json.loads(response_body.decode())["access_token"]

def add_user_to_keycloak(user_data, access_token):
    url = f"{KEYCLOAK_BASE_URL}/admin/realms/{REALM_NAME}/users"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, data=json.dumps(user_data).encode(), headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        response_body = response.read()
        if response.status != 201:
            raise Exception(f"Failed to add user: {response_body.decode()}")

# Nota: urllib não lança exceções para códigos de status HTTP fora do range 200-299,
# então você pode precisar verificar response.status manualmente para códigos de erro.
