import requests
import getpass

IP = "http://10.180.3.152:3001"

def getHeader(token):
    """Return a dictionary containing headers for a HTTP request with the specified authorization token."""
    config = {
        'headers': {
            'Content-Type': 'application/json'
        }
    }

    config['headers']['Authorization'] = f'Token {token}'
    return config['headers']

def login(username=None, password=None):
    """Authenticate a user with a server and return an access token.

    Parameters:
    username (str, optional): The username to use for authentication. If None, the user is prompted to enter it.
    password (str, optional): The password to use for authentication. If None, the user is prompted to enter it.

    Returns:
    str or None: An access token if authentication was successful, None otherwise.
    """
    if username is None:
        username = input("Username: ")
    if password is None:
        password = getpass.getpass("Password: ")

    IP = "http://10.180.3.152:3001"
    url = f"{IP}/reduction/auth/login"  # Replace {IP} with the IP address of the server

    payload = {"username": username, "password": password}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Authentication successful!")
        return response.json()["token"]
    else:
        print("Authentication failed.")
        return None