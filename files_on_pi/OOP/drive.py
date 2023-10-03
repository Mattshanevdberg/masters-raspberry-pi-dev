import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
#from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
import os
import json
### OWN FUNCTIONS ###
from owntime import Timer
from telegram import TelegramBot

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
destination_folder_id = 'folder_id'


class DriveAuth:
    def __init__(self):
        self.refresh_token = None 
        self.start_time = None
        self.device_verification_code = None 
        self.verification_url = None 
        self.expires_in = None 
        self.interval = None 
        self.device_code = None 
        self.access_token = None 
        self.not_expired = True
        self.timer = Timer()

    def retrieve_refresh_token(self):
        '''retreives the refresh token from a file named refresh_token 
            Returns: refresh_token (returns None if there is no file called refresh_token)'''
        try:
            with open('refresh_token', 'r') as file:
                self.refresh_token = file.read().strip()
                print('Refresh token retrieved successfully.')
                return self.refresh_token
        except FileNotFoundError:
            print('Refresh token file not found.')
            return None
        except Exception as e:
            print(f"An error occurred while retrieving the refresh token: {e}")
            return None 
        
    def save_refresh_token(self):
        try:
            with open('refresh_token', 'w') as file:
                file.write(self.refresh_token)
                print('Refresh token saved successfully.')
        except Exception as e:
            print(f"An error occurred while saving the refresh token: {e}")
    
    def request_device_authorization(self):
        ''' Request device authorization - to be used only when refresh token is not available
            Returns: device_verfication_code, verification_url, expires_in, interval, device_code'''
        response = requests.post(DEVICE_AUTH_URL, data={
            'client_id': CLIENT_ID,
            'scope': SCOPES
        })
        print(response)
        if response.status_code == 200:
            data = response.json()
            print('Please go to', data['verification_url'], 'and enter code', data['user_code'], data['device_code'])
            self.user_code = data['user_code']
            self.verification_url = data['verification_url'] 
            self.expires_in = data['expires_in'] 
            self.interval = data['interval'] 
            self.device_code = data['device_code']
            #return data['user_code'], data['verification_url'],  data['expires_in'], data['interval'], data['device_code']
        else:
            print('Device authorization request failed.')
            #return None, None, None, None
    
    def request_access_token(self):
        '''Requests an access token and refresh token using the device_verification_token - to be used only once after request_device_authorisation, 
        if request_token is available use this to obtain a access token rather
            Parm: device_verfication_code
            Return: access_token, refresh_token'''
        #client = BackendApplicationClient(client_id=CLIENT_ID)
        token_url = TOKEN_URL
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'device_code': self.device_code,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
        }
        # Request access token
        response = requests.post(token_url,headers=headers, data=data)
        #original
        '''
        response = requests.post(token_url, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), data={
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'device_code': device_code
        })
        '''
        if response.status_code == 200:
            tokens = response.json()
            print(tokens)
            print('Access token:', tokens['access_token'])
            print('Refresh token:', tokens['refresh_token'])
            self.access_token = tokens['access_token']
            self.refresh_token = tokens['refresh_token']            
            #return tokens['access_token'], tokens['refresh_token']
        else:
            error_code = str(response.status_code)
            print('Access token request failed.' + 'error: ' + error_code)
            #return None, None

    def poll_for_token(self):
        '''pole the server to check if the token has been input, while the code has not expired
            Params: device_verification_code, start_time, expires_in, interval
            Returns: access_token, refresh_token'''
        # pole the server to check if the token has been input
        not_expired = True
        # loop while waiting for person to access...
        while not self.access_token and not_expired:
            #poll every specified interval
            self.timer.sleep(self.interval)

            #get the elapsed time and check that the token has not expired
            self.elapsed_time = self.timer.check_elapsed_time(self.start_time)
            
            if self.elapsed_time > (self.expires_in - 100):
                not_expired = False
            else:
                self.request_access_token()

        #return access_token, refresh_token
    
    def get_new_refresh_token(self):
        '''the full overview function that retrieves a new refresh token and saves it
            Returns: access_token, refresh_token'''
        while (not self.refresh_token):
            # loop to keep getting verification code each time it expires
            # get authorisation code and url
            self.request_device_authorization()

            # keep track of expired code
            self.start_time = self.timer.start_timer()
            # send message with these codes to be used for authorisation to telegram
            telegram_bot = TelegramBot(USER_NAME)
            telegram_bot.send_telegram('verification url: ' + self.verification_url)
            telegram_bot.send_telegram('device verification code: ' + self.user_code)

            # pole the server to check if the token has been input
            self.poll_for_token(self.device_code, self.start_time, self.expires_in, self.interval)

        # now have a refresh token and access token, so we must save the refresh token to be reused
        self.save_refresh_token(self.refresh_token)
        #return access_token, refresh_token
    


drive = DriveAuth()
drive.get_new_refresh_token()

#drive.request_device_authorization()
