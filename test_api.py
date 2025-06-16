import requests
import json
import random
import string
import sys

API_URL = 'https://fte-backend-prod.ew.r.appspot.com'

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_register():
    try:
        random_user = f'test_user_{generate_random_string()}'
        url = f'{API_URL}/api/auth/register/'
        data = {
            'username': random_user,
            'password': 'test123',
            'email': f'{random_user}@example.com',
            'cedula': f'{random.randint(1000000000, 9999999999)}',
            'correo': f'{random_user}@example.com',
            'nombre_completo': f'Test User {random_user}'
        }
        print('Sending registration request...', flush=True)
        response = requests.post(url, json=data)
        print('=== Test Register ===', flush=True)
        print(f'Status Code: {response.status_code}', flush=True)
        print('Response:', response.text, flush=True)
        return data if response.status_code == 201 else None
    except Exception as e:
        print(f'Error during registration: {e}', flush=True)
        return None

def test_login(credentials=None):
    try:
        if not credentials:
            credentials = {
                'username': 'test_user',
                'password': 'test123'
            }
        
        url = f'{API_URL}/api/auth/login/'
        data = {
            'username': credentials['username'],
            'password': credentials['password']
        }
        print('Sending login request...', flush=True)
        response = requests.post(url, json=data)
        print('\n=== Test Login ===', flush=True)
        print(f'Status Code: {response.status_code}', flush=True)
        print('Response:', response.text, flush=True)
    except Exception as e:
        print(f'Error during login: {e}', flush=True)

if __name__ == '__main__':
    print('Starting tests...', flush=True)
    credentials = test_register()
    if credentials:
        test_login(credentials)
    print('Tests completed.', flush=True) 