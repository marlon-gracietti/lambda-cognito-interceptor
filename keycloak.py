# keycloak.py
import requests

KEYCLOAK_BASE_URL = "https://keycloak.hml.propagandistanc.com/auth"
REALM_NAME = "NHUB"
CLIENT_ID = "nhub-users"
CLIENT_SECRET = "5u3Q94TvigM9kt4BncFYTwoqyqZSGKak"

def get_keycloak_access_token():
    url = f"{KEYCLOAK_BASE_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]

def add_user_to_keycloak(user_data, access_token):
    url = f"{KEYCLOAK_BASE_URL}/admin/realms/{REALM_NAME}/users"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=user_data, headers=headers)
    response.raise_for_status()
