import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
import os
import time
import sys
from pydrive.drive import GoogleDrive

# OAuth 2.0 endpoint URLs
TOKEN_URL = 'https://oauth2.googleapis.com/token'
DEVICE_AUTH_URL = 'https://oauth2.googleapis.com/device/code'
REFRESH_URL = 'https://oauth2.googleapis.com/token'

# OAuth 2.0 client credentials
CLIENT_ID = '88517990399-uik94v200989ffi42ksehp93ouv0hu1q.apps.googleusercontent.com'
CLIENT_SECRET = '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'

# Sample folder to upload from the desktop
user_name = 'matthew'
source_folder_path = '/home/' + user_name + '/Desktop/I LOVE YOU.jpg'
destination_folder_name = 'Test'
destination_folder_id = '1vJgmXrr0CaPnVdkE1_mYz-zPS6OIY7ii'

def request_device_authorization():
    # Request device authorization
    response = requests.post(DEVICE_AUTH_URL, data={
        'client_id': CLIENT_ID,
        'scope': 'https://www.googleapis.com/auth/drive.file'
    })
    print(response)
    if response.status_code == 200:
        data = response.json()
        print('Please go to', data['verification_url'], 'and enter code', data['user_code'])
        return data['device_code'], data['interval'], data['verification_url']
    else:
        print('Device authorization request failed.')
        return None, None, None

def request_access_token(device_code):
    client = BackendApplicationClient(client_id=CLIENT_ID)
    token_url = TOKEN_URL

    # Request access token
    response = requests.post(token_url, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), data={
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code
    })

    if response.status_code == 200:
        tokens = response.json()
        print('Access token:', tokens['access_token'])
        print('Refresh token:', tokens['refresh_token'])
        return tokens
    else:
        print('Access token request failed.')

def refresh_access_token(refresh_token):
    # Request a new access token using the refresh token
    response = requests.post(REFRESH_URL, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    })

    if response.status_code == 200:
        tokens = response.json()
        print('Access token:', tokens['access_token'])
        return tokens['access_token']
    else:
        print('Access token refresh failed.')
        return None
    
def upload_to_drive(access_token, source_folder_path, destination_folder_name, destination_folder_id):
    try:
        # Create a GoogleDrive instance using the provided access token
        drive = GoogleDrive(None, auth_method='Bearer', auth_token=access_token)

        # List files in the local folder
        files_to_upload = os.listdir(source_folder_path)

        # Create a new subfolder within the destination folder
        subfolder_metadata = {
            'title': destination_folder_name,
            'parents': [{'id': destination_folder_id}],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        subfolder = drive.CreateFile(subfolder_metadata)
        subfolder.Upload()

        for file_name in files_to_upload:
            file_path = os.path.join(source_folder_path, file_name)

            # Upload each file to the created subfolder on Google Drive
            file_metadata = {
                'title': file_name,
                'parents': [{'id': subfolder['id']}]
            }
            file = drive.CreateFile(file_metadata)
            file.SetContentFile(file_path)
            file.Upload()

            print(f"Uploaded {file_name} to Google Drive")

    except Exception as e:
        print(f"An error occurred: {e}")
def save_refresh_token(refresh_token):
    try:
        with open('refresh_token', 'w') as file:
            file.write(refresh_token)
            print('Refresh token saved successfully.')
    except Exception as e:
        print(f"An error occurred while saving the refresh token: {e}")

def retrieve_refresh_token():
    try:
        with open('refresh_token', 'r') as file:
            refresh_token = file.read().strip()
            print('Refresh token retrieved successfully.')
            return refresh_token
    except FileNotFoundError:
        print('Refresh token file not found.')
        return None
    except Exception as e:
        print(f"An error occurred while retrieving the refresh token: {e}")
        return None


if __name__ == '__main__':
    device_code, interval = request_device_authorization()
    if device_code:
        while True:
            tokens = request_access_token(device_code)
            if tokens:
                upload_to_drive(tokens['access_token'], source_folder_path, destination_folder_name, destination_folder_id)
                time.sleep(interval)  # Wait for the specified interval
                device_code = None  # Stop requesting new tokens for this session
            else:
                break  # Stop if token request failed
