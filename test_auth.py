import requests
import json
import random
import string

BASE_URL = 'https://fte-backend-prod.ew.r.appspot.com'

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_register():
    username = f'test_user_{generate_random_string()}'
    data = {
        'username': username,
        'password': 'TestPass123!',
        'email': f'{username}@test.com',
        'cedula': f'TEST{generate_random_string(8)}',
        'nombre_completo': f'Test User {username}'
    }
    
    print("\n=== Testing Registration ===")
    print(f"Sending registration data:\n{json.dumps(data, indent=2)}")
    
    response = requests.post(f'{BASE_URL}/api/auth/register/', json=data)
    print(f"Registration Status Code: {response.status_code}")
    print(f"Registration Response:\n{json.dumps(response.json(), indent=2) if response.content else 'No content'}")
    
    if response.status_code == 201:
        print("\n=== Testing Login with New User ===")
        login_data = {
            'username': username,
            'password': 'TestPass123!'
        }
        print(f"Sending login data:\n{json.dumps(login_data, indent=2)}")
        
        login_response = requests.post(f'{BASE_URL}/api/auth/login/', json=login_data)
        print(f"Login Status Code: {login_response.status_code}")
        print(f"Login Response:\n{json.dumps(login_response.json(), indent=2) if login_response.content else 'No content'}")

def test_login(credentials=None):
    print("\n=== Testing Login ===")
    if not credentials:
        credentials = {
            'username': input("Enter username: "),
            'password': input("Enter password: ")
        }
    
    print(f"\nAttempting login with:\n{json.dumps(credentials, indent=2)}")
    
    response = requests.post(f'{BASE_URL}/api/auth/login/', json=credentials)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2) if response.content else 'No content'}")
    
    return response.json() if response.status_code == 200 else None

def test_protected_endpoint(token):
    print("\n=== Testing Protected Endpoint ===")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/api/materias/', headers=headers)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2) if response.content else 'No content'}")

if __name__ == '__main__':
    test_register() 