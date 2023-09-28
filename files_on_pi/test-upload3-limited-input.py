
############## IMPORTS ##############
### Drive
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
import os
from pydrive.drive import GoogleDrive
### Telegram
import telepot
import pprint
### General
import time
import sys

######### GLOBAL VARIABLES #############
### DRIVE ###
# OAuth 2.0 endpoint URLs
TOKEN_URL = 'https://oauth2.googleapis.com/token'
DEVICE_AUTH_URL = 'https://oauth2.googleapis.com/device/code'
REFRESH_URL = 'https://oauth2.googleapis.com/token'
# OAuth 2.0 client credentials
CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
# Sample folder to upload from the desktop
user_name = 'matthew'
source_folder_path = '/home/' + user_name + '/Desktop/I LOVE YOU.jpg'
destination_folder_name = 'Test'
destination_folder_id = '1vJgmXrr0CaPnVdkE1_mYz-zPS6OIY7ii'
### TELEGRAM ###
TELE_TOKEN = 'token'
TELE_SEND_ADDRESS = 'send_address'
device_name =  'matt_test_computer: '

######### FUNCTIONS #####################

### DRIVE ###

def request_device_authorization():
    ''' Request device authorization - to be used only when refresh token is not available
        Returns: device_verfication_code, verification_url'''
    response = requests.post(DEVICE_AUTH_URL, data={
        'client_id': CLIENT_ID,
        'scope': 'https://www.googleapis.com/auth/drive.file'
    })
    print(response)
    if response.status_code == 200:
        data = response.json()
        print('Please go to', data['verification_url'], 'and enter code', data['user_code'])
        return data['user_code'], data['verification_url'],  data['expires_in'], data['interval'],
    else:
        print('Device authorization request failed.')
        return None, None, None, None

def request_access_token(device_code):
    '''Requests an access token and refresh token using the device_verification_token - to be used only once after request_device_authorisation, 
    if request_token is available use this to obtain a access token rather
        Parm: device_verfication_code
        Return: access_token, refresh_token'''
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
        return tokens['access_token'], tokens['refresh_token']
    else:
        print('Access token request failed.')
        return None, None

def refresh_access_token(refresh_token):
    ''' Request a new access token using the refresh token 
        Param: refresh_token 
        Return: access_token'''
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
    
def save_refresh_token(refresh_token):
    try:
        with open('refresh_token', 'w') as file:
            file.write(refresh_token)
            print('Refresh token saved successfully.')
    except Exception as e:
        print(f"An error occurred while saving the refresh token: {e}")

def retrieve_refresh_token():
    '''retreives the refresh token from a file named refresh_token 
        Returns: refresh_token'''
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
        
### TELEGRAM ###

def initialise_tele_bot():
    bot = telepot.Bot(TELE_TOKEN)
    return bot

def receive_message(bot):
    response = bot.getUpdates(limit=1, offset=-1)
    if response and 'message' in response[0]:
        message_text = response[0]['message']['text']
        print('Received message:', message_text)
        return message_text
    else:
        print('No messages received.')
        return 'No new messages in the last 24 hours'


def send_telegram(bot, message, device_name):
    bot.sendMessage(TELE_SEND_ADDRESS, device_name + message)
    print('message sent to ' + device_name + message)
    return None

### TIMER ###

def start_timer():
    start_time = time.time()
    return start_time

def check_elapsed_time(start_time):
    elapsed_time = time.time() - start_time
    return elapsed_time


if __name__ == '__main__':

    # initialise the telegram bot
    tele_bot = initialise_tele_bot()

    # start-up message
    send_telegram(tele_bot, 'restarting' , device_name)

    # try retreive the refresh token
    refresh_token = retrieve_refresh_token()

    # if there is no refresh token present then this is a first time start up or refresh token is missing 
    # and we need to authorise device to access the drive

    while (not refresh_token):
        # loop to keep getting verification code each time it expires
        # get authorisation code and url
        device_verification_code, verification_url, expires_in, interval = request_device_authorization()

        # keep track of expired code
        start_time = start_timer()
        # send message with these codes to be used for authorisation to telegram
        send_telegram(tele_bot, 'verification url: ' + verification_url, device_name)
        send_telegram(tele_bot, 'device verification code: ' + device_verification_code, device_name)

        # pole the server to check if the token has been input
        access_token = None #initialise access token
        # loop while waiting for person to access...
        while(not access_token):
            time.sleep(5)



    '''
    refresh_token = 'test'
    save_refresh_token(refresh_token)
    refresh_token2 = retrieve_refresh_token()
    print(refresh_token2)
    '''
    '''
    tele_bot = initialise_tele_bot()
    message_received = receive_message(tele_bot)
    print(message_received)
    #send_telegram(tele_bot, 'send message test', device_name)
    '''
    '''   
    device_code, interval, verification_url = request_device_authorization()
    if device_code:
        while True:
            tokens = request_access_token(device_code)
            if tokens:
                upload_to_drive(tokens['access_token'], source_folder_path, destination_folder_name, destination_folder_id)
                time.sleep(interval)  # Wait for the specified interval
                device_code = None  # Stop requesting new tokens for this session
            else:
                break  # Stop if token request failed
    '''

