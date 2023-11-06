import requests
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
#from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
import os
import json
import shutil
import psutil #this is for checking momory
### OWN FUNCTIONS ###
from owntime import Timer
from telegram import TelegramBot

### DRIVE ###
# OAuth 2.0 endpoint URLs
TOKEN_URL = 'https://oauth2.googleapis.com/token'
DEVICE_AUTH_URL = 'https://oauth2.googleapis.com/device/code'
REFRESH_URL = 'https://oauth2.googleapis.com/token'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
# OAuth 2.0 client credentials
CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
# Sample folder to upload from the desktop
DESTINATION_FOLDER_ID = 'folder_id'


class DriveAuth:
    def __init__(self, user_name, access_token_timer):
        self.user_name = user_name
        self.access_token_timer = access_token_timer
        self.access_token_expires_in = None
        self.refresh_token = None 
        self.start_time = None
        self.device_verification_code = None 
        self.verification_url = None 
        self.expires_in = None 
        self.interval = None 
        self.device_code = None 
        self.access_token = None 
        self.not_expired = True
        self.refresh_token_timer = Timer()
        self.telegram_bot = TelegramBot(self.user_name)
        self.tokens = None # this is potentially to be used later in the uploading of images

    def retrieve_refresh_token(self):
        #TESTED: 06-10-2023
        '''retreives the refresh token from a file named refresh_token 
            Returns: refresh_token (returns None if there is no file called refresh_token)'''
        try:
            with open('refresh_token', 'r') as file:
                self.refresh_token = file.read().strip()
                #print('Refresh token retrieved successfully.')
                return True
        except FileNotFoundError:
            #print('Refresh token file not found.')
            self.telegram_bot.send_telegram('Refresh token file not found.')
            return False
        except Exception as e:
            e = str(e)
            self.refresh_token_timer.sleep(120)
            function_name = 'DriveAuth.retrieve_refresh_token:'
            self.telegram_bot.send_telegram(f"{function_name}: {e}")
            return False 
        
    def save_refresh_token(self):
        # TESTED: 06-10-2023
        try:
            with open('refresh_token', 'w') as file:
                file.write(self.refresh_token)
                self.telegram_bot.send_telegram('Refresh token saved successfully.')
        except Exception as e:
            e = str(e)
            self.refresh_token_timer.sleep(120)
            function_name = 'DriveAuth.save_refresh_token:'
            self.telegram_bot.send_telegram(f"{function_name}: {e}")            
    
    def update_dictionary_values(self):
        # TESTED: 06-10-2023 
        """
        Updates token dictionary to be saved
        """
        self.tokens = {
            "token": self.access_token,
            "refresh_token": self.refresh_token,
            "token_uri": TOKEN_URL,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scopes": SCOPES
        }

    def save_token_creds(self):
        # TESTED: 06-10-2023
        try:
            self.update_dictionary_values()
            with open('token.json', 'w') as file:
                json.dump(self.tokens, file)
                #self.telegram_bot.send_telegram('Token Creds saved successfully.')
        except Exception as e:  
            e = str(e)
            self.refresh_token_timer.sleep(120)       
            function_name = 'DriveAuth.save_token_creds:'
            self.telegram_bot.send_telegram(f"{function_name}: An error occurred while saving the Token Creds: {e}")
    
    def request_device_authorization(self):
        ''' Request device authorization - to be used only when refresh token is not available
            Returns: device_verfication_code, verification_url, expires_in, interval, device_code'''
        #TESTED: 06-10-2023
        try:
            response = requests.post(DEVICE_AUTH_URL, data={
                'client_id': CLIENT_ID,
                'scope': SCOPES
            })
            #print(response)
            if response.status_code == 200:
                data = response.json()
                #print('Please go to', data['verification_url'], 'and enter code', data['user_code'], data['device_code'])
                self.user_code = data['user_code']
                self.verification_url = data['verification_url'] 
                self.expires_in = data['expires_in'] 
                self.interval = data['interval'] 
                self.device_code = data['device_code']
                #return data['user_code'], data['verification_url'],  data['expires_in'], data['interval'], data['device_code']
            else:
                error_code = str(response.status_code)
                #print('Access token request failed.' + 'error: ' + error_code + response.text)
                self.telegram_bot.send_telegram('function: DriveAuth.request_device_authorization: Device authorization request failed.'+ 'error: ' + error_code + response.text)
                #return None, None, None, None
        except Exception as e:
            e = str(e)
            self.refresh_token_timer.sleep(120)
            function_name = 'DriveAuth.request_device_authorization:'
            self.telegram_bot.send_telegram(function_name + e)        
    
    def request_access_token(self):
        #TESTED: 06-10-2023
        '''Requests an access token and refresh token using the device_verification_token - to be used only once after request_device_authorisation, 
        if request_token is available use this to obtain a access token rather
            Parm: device_verfication_code
            Return: access_token, refresh_token'''
        #client = BackendApplicationClient(client_id=CLIENT_ID)
        try:
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
            response = requests.post(TOKEN_URL,headers=headers, data=data)

            if response.status_code == 200:
                self.tokens = response.json()
                #print(self.tokens)
                #print('Access token:', self.tokens['access_token'])
                #print('Refresh token:', self.tokens['refresh_token'])
                self.access_token = self.tokens['access_token']
                self.refresh_token = self.tokens['refresh_token']
                self.save_token_creds()
                #return tokens['access_token'], tokens['refresh_token']
            else:
                error_code = str(response.status_code)
                self.telegram_bot.send_telegram('function:DriveAuth.request_access_token: Access token request failed.' + 'error: ' + error_code + response.text)
                #return None, None
        except Exception as e:
            e = str(e)
            self.refresh_token_timer.sleep(120)
            function_name = 'DriveAuth.request_access_token:'
            self.telegram_bot.send_telegram(function_name + e)           

    def poll_for_token(self):
        #TESTED: 06-10-2023 
        '''pole the server to check if the token has been input, while the code has not expired
            sets the access_token and refresh_token'''
        # pole the server to check if the token has been input
        not_expired = True
        # loop while waiting for person to access...
        try:
            while not self.access_token and not_expired:
                #poll every specified interval
                self.refresh_token_timer.sleep(self.interval)

                #get the elapsed time and check that the token has not expired
                self.elapsed_time = self.refresh_token_timer.check_elapsed_time()
                
                if self.elapsed_time > (self.expires_in - 100):
                    not_expired = False
                else:
                    self.request_access_token()

        except Exception as e:
            e = str(e)
            self.refresh_token_timer.sleep(120)
            function_name = 'DriveAuth.poll_for_token:'
            self.telegram_bot.send_telegram(function_name + e)    

        #return access_token, refresh_token
    
    def get_new_refresh_token(self):
        '''the full overview function that retrieves a new refresh token and saves it to a file
            and to a variable'''
        #TESTED 09-10-2023
        try: 
            while (not self.refresh_token):
                # loop to keep getting verification code each time it expires
                # get authorisation code and url
                self.request_device_authorization()

                # keep track of expired code
                self.refresh_token_timer.start_timer()
                # send message with these codes to be used for authorisation to telegram
                
                self.telegram_bot.send_telegram('verification url: ' + self.verification_url)
                self.telegram_bot.send_telegram('device verification code: ' + self.user_code)

                # pole the server to check if the token has been input
                self.poll_for_token()

            # now have a refresh token and access token, so we must save the refresh token to be reused
            self.save_refresh_token()
            #return access_token, refresh_token
        except Exception as e: 
            e = str(e)
            self.refresh_token_timer.sleep(120)
            function_name = 'DriveAuth.get_new_refresh_token'
            self.telegram_bot.send_telegram(function_name + e)

    def refresh_access_token(self):
        ''' Request a new access token using the refresh token 
            '''
        #TESTED 09-10-2023

        try:
            #start timer to determine when the access token will expire
            self.access_token_timer.start_timer
            #request the access token using the refresh token 
            response = requests.post(REFRESH_URL, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), data={
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token
            })

            if response.status_code == 200:
                tokens = response.json()
                #print('Access token:', tokens['access_token'])
                self.access_token = tokens['access_token']
                self.access_token_expires_in = tokens['expires_in']
                self.save_token_creds()
                #return tokens['access_token']
            else:
                self.telegram_bot.send_telegram('Access token refresh failed. there is likely something wrong with the refresh token. try deleting it and restarting the pi. Otherwise see the error below..')
                error_code = str(response.status_code)
                self.telegram_bot.send_telegram('function:DriveAuth.refresh_access_token: Access token refresh failed.' + 'error: ' + error_code + response.text)
                return None 
        
        except Exception as e:         
            e = str(e)
            self.refresh_token_timer.sleep(120)      
            function_name = 'DriveAuth.refresh_access_token'
            self.telegram_bot.send_telegram(function_name + e) 

    def check_access_token_expired(self):
        '''checks if the access token has expiered and if it has requests a new one'''
        try:
            elapsed_time = self.access_token_timer.check_elapsed_time 

            if elapsed_time > (self.access_token_expires_in - 3):
                self.request_access_token()

        except Exception as e:         
            e = str(e)
            self.refresh_token_timer.sleep(120)      
            function_name = 'DriveAuth.check_access_token_expired'
            self.telegram_bot.send_telegram(function_name + e) 

class DriveUpload:
    def __init__(self, user_name, drive_auth, access_token_timer):
        self.desired_folder_name = None
        self.user_name = user_name
        self.list_of_folders = []
        self.drive_auth = drive_auth
        self.access_token_timer = access_token_timer
        self.parent_folder_id = None
        self.telegram_bot = TelegramBot(self.user_name)
        self.upload_timer = Timer()        
    
    def collect_folder_paths_to_upload(self):
        '''create a list containing strings of the paths to the folders 
        on the Desktop '''
        # TESTED 09-10-2023
        try:
            desktop_path = f'/home/{self.user_name}/Desktop'
            folder_counter = 0
            #test
            #desktop_path = f'/home/{self.user_name}/Desktop/test_upload (copy)'
            #end test
            # empty the list of folders attribute
            self.list_of_folders = []
            # fill the  list with the paths to all folders on the desktop (only folders)
            for item in os.listdir(desktop_path):
                if item  not in ('__pycache__', 'masters-raspberry-pi-dev'):
                    item_path = os.path.join(desktop_path, item)
                    if os.path.isdir(item_path):
                        self.list_of_folders.append(item_path)
                        folder_counter += 1

                        if folder_counter == 20:
                            break
                
            #print(self.list_of_folders)


        except Exception as e: 
            e = str(e)
            self.upload_timer.sleep(120)    
            function_name = 'DriveUpload.collect_folder_paths_to_upload'
            self.telegram_bot.send_telegram(function_name + e)
    
    def delete_folders(self):
        '''deletes all the folders in the self.list_of_folders attribute'''
        for folder_path in self.list_of_folders:
            try:
                shutil.rmtree(folder_path)
                print(f'Deleted folder: {folder_path}')
            except Exception as e:
                e = str(e)
                self.upload_timer.sleep(120)    
                print(f'Failed to delete folder {folder_path}: {e}')
                function_name = 'DriveUpload.delete_folders'
                self.telegram_bot.send_telegram(function_name + e)

    def drive_create_folder(self, desired_folder_name):
        ''' Create a folder and stores the id of this folder'''
        # refresh the access token 
        #TESTED 09-10-2023
        try:
            #refresh the access token before uploading
            self.drive_auth.refresh_access_token()

            creds = Credentials.from_authorized_user_file('token.json', SCOPES)


            # create drive api client
            service = build('drive', 'v3', credentials=creds)
            file_metadata = {
                'name': desired_folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [DESTINATION_FOLDER_ID]
            }

            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, fields='id'
                                        ).execute()
            print(F'Folder ID: "{file.get("id")}".')

            self.parent_folder_id = file.get('id')
            #return file.get('id')

        except HttpError as error:
            function_name = 'DriveUpload.drive_create_folder'
            error = str(error)
            self.upload_timer.sleep(120)    
            self.telegram_bot.send_telegram(function_name + error)
                
        except Exception as e:  
            e = str(e)
            function_name = 'DriveAuth.drive_create_folder'
            self.telegram_bot.send_telegram(function_name + e)       
    
    def drive_upload_image(self, file_name, file_path):
        '''uploads an image to the drive'''
        #TESTED 09-10-2023

        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # create drive api client
            service = build('drive', 'v3', credentials=creds)

            file_metadata = {
                'name': file_name,
                'parents': [self.parent_folder_id]
                }
            media = MediaFileUpload(file_path)#,
                                    #mimetype='image/jpeg')
            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, media_body=media,
                                        fields='id').execute()
            #print(F'File ID: {file.get("id")}')

        except Exception as e:  
            e = str(e)
            self.upload_timer.sleep(120)    
            function_name = 'DriveUpload.drive_upload_image'
            self.telegram_bot.send_telegram(function_name + e) 

    def drive_upload_video(self, file_name, file_path):
        '''uploads a video to the drive'''
        #TESTED 09-10-2023
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # create drive api client
            service = build('drive', 'v3', credentials=creds)

            file_metadata = {
                'name': file_name,
                'parents': [self.parent_folder_id]
                }
            media = MediaFileUpload(file_path)#,
                                    #mimetype='image/jpeg')
            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, media_body=media,
                                        fields='id').execute()
            #print(F'File ID: {file.get("id")}')

        except Exception as e: 
            e = str(e) 
            self.upload_timer.sleep(120)    
            function_name = 'DriveUpload.drive_upload_video'
            self.telegram_bot.send_telegram(function_name + e)
        
    def upload_folders_to_drive(self):
        '''uploads all folders on the desktop to the drive and deletes
        the folders from the desktop'''
        # TESTED 09-10-2023
        
        try:
            #get list of folders to upload
            self.collect_folder_paths_to_upload()

            for folder in self.list_of_folders:
                # create a folder on the drive
                #test
                #folder = '/home/matthew/Desktop/Test_upload_video'
                #end test
                #print(folder)
                self.drive_create_folder(os.path.basename(folder))

                # List files in the local folder
                files_to_upload = os.listdir(folder)

                if 'image' in folder:
                    for file_name in files_to_upload:
                        file_path = os.path.join(folder, file_name)
                    
                        # Upload each file to the created subfolder on Google Drive
                        self.drive_upload_image(file_name, file_path)

                        #print(f"Uploaded {file_name} to Google Drive")
                
                if 'video' in folder:
                    for file_name in files_to_upload:
                        file_path = os.path.join(folder, file_name)
                    
                        # Upload each file to the created subfolder on Google Drive
                        self.drive_upload_video(file_name, file_path)
                
                #pause for 3 seconds before uploading next folder
                self.upload_timer.sleep(3)

                        #print(f"Uploaded {file_name} to Google Drive")
            # send a message to inform the upload is finished
            self.telegram_bot.send_telegram('upload complete... deleting folders on desktop..')
            self.delete_folders()
            self.telegram_bot.send_telegram('folders have been deleted')
            self.upload_timer.sleep(60)
                                            
        except Exception as e:  
            e = str(e)
            self.upload_timer.sleep(120)    
            function_name = 'DriveUpload.upload_folders_to_drive'
            self.telegram_bot.send_telegram(function_name + e)

    def check_for_low_memory(self):
        '''checks the memory available on the local system and if it is less than 1GB, returns true\
            param: 
            Returns: True is less than 1GB memory remains, false more than 1 GB remains'''
        #TESTED 09-10-2023
        try:
            threshold = 1 * 1024 * 1024 * 1024  # 1 GB in bytes
            available_memory = psutil.virtual_memory().available
            return available_memory < threshold

        except Exception as e: 
            e = str(e) 
            self.upload_timer.sleep(120)    
            function_name = 'DriveUpload.check_for_low_memory'
            self.telegram_bot.send_telegram(function_name + e)
            return False




### TESTING ###
#access_token_timer = Timer()

#drive_auth = DriveAuth('matthew', access_token_timer)

#drive_upload = DriveUpload('matthew', drive_auth, access_token_timer)
#print(drive_auth.retrieve_refresh_token)
#drive_upload.collect_folder_paths_to_upload()
#drive_upload.delete_folders()
#drive_upload.upload_folders_to_drive()
#drive.request_device_authorization()
