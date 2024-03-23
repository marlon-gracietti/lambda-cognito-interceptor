
import boto3
import base64

# Configuração do cliente do Cognito
cognito_client = boto3.client('cognito-idp')
user_pool_id = 'us-east-1_vnrPcWJ2I'  # Substitua pelo seu User Pool ID

def lambda_handler(event, context):  # Renomeado de handler para lambda_handler
    print("START2")
    
    # Extrai o token do evento de autorização
    auth_header = event.get('authorizationToken')
    if not auth_header:
        print("Authorization header is missing")
        return generate_policy('user', 'Deny', event['methodArn'])

    encoded_token = auth_header.split(' ')[1]
    if not encoded_token:
        print("Invalid Authorization token format")
        return generate_policy('user', 'Deny', event['methodArn'])

    # Decodifica o token para obter o valor
    decoded_value = base64.b64decode(encoded_token).decode('utf-8')
    print("Decoded value:", decoded_value)

    # Exemplo: extrai o username do valor decodificado
    username = decoded_value.split(':')[0]  # Ajuste conforme necessário

    try:
        user_attributes = get_user_attributes(username)
        print("User Attributes:", user_attributes)
    except Exception as e:
        print("Error fetching user attributes:", str(e))
        return generate_policy('user', 'Deny', event['methodArn'])

    return generate_policy('user', 'Allow', event['methodArn'])

def get_user_attributes(username):
    response = cognito_client.admin_get_user(
        UserPoolId=user_pool_id,
        Username=username
    )
    # Transforma os atributos do usuário em um dicionário mais amigável
    attributes = {attr['Name']: attr['Value'] for attr in response['UserAttributes']}
    return attributes

def generate_policy(principal_id, effect, resource):
    policy_document = {
        'Version': '2012-10-17',
        'Statement': [{
            'Action': 'execute-api:Invoke',
            'Effect': effect,
            'Resource': resource,
        }]
    }
    return {
        'principalId': principal_id,
        'policyDocument': policy_document,
        # Opcional: inclua um contexto de autenticação se necessário
    }
