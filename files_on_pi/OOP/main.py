### OTHER FUNCTION IMPORT ###
import os
import traceback
### OWN FUNCTION IMPORT ###
from drive import DriveAuth
from drive import DriveUpload
from camera import Camera
from owntime import Timer
from telegram import TelegramBot
from maintenance import Maintenance

### GLOBALS ###
USER_NAME = 'matthew' #ensure this is user computer user name
SOURCE_FOLDER_PATH = '/home/' + USER_NAME + '/Desktop/Test_upload_folder'
SLEEP_PERIOD_START = 2000 # time as an integer, 8pm = 2000, 8:05pm = 2005, 06:35am = 0635, etc.
SLEEP_PERIOD_END = 2005
UPLOAD_PERIOD_START = 2000
UPLOAD_PERIOD_END = 2005

### MAIN LOOP ###
def main():
    try:
        # Instantiate your custom classes and objects and variables
        access_token_timer = Timer()
        drive_auth1 = DriveAuth(USER_NAME, access_token_timer)
        drive_upload1 = DriveUpload(USER_NAME, drive_auth1, access_token_timer)
        pi_camera = Camera(USER_NAME)
        maintenance = Maintenance(USER_NAME)
        tele_bot1 = TelegramBot(USER_NAME)
        mode = 'video' # default mode on start up
        require_refresh_token = False
        sleep_mode = False # set to True if in sleep mode
        #set_sleep_mode = False # this is set by the user if the forces sleep mode
        #set_upload_mode = False
        set_get_new_refresh_token = False

        # send start up message (User_name)
        tele_bot1.send_telegram("Finished my nap, back to work!")

        # Start while loop (1)
        while(1):
            # check that the refresh token is present and retreive it
            refresh_token_present = drive_auth1.retrieve_refresh_token()
            
            # check there is a refresh token present OR require new refresh token OR not mode maintenance
            if not refresh_token_present or require_refresh_token or set_get_new_refresh_token: 
                # send message to inform that device authorisation is happening
                tele_bot1.send_telegram("Okay, I looked everywhere and I can't seem find the refresh token anywhere... Damn, Gonna have to reauthenticate to get a new one...")
                # redo device device authorisation and save refresh token to file
                drive_auth1.get_new_refresh_token()
                # set set_get_new_refresh_token back to false
                if set_get_new_refresh_token == True:
                    set_get_new_refresh_token = False
                    mode = 'video' # setting mode back to default
                # wait 1 min to set to different mode if required
                access_token_timer.sleep(60)
            
            # if current time is in sleep period or user has set the sleep mode
            if access_token_timer.is_current_time_in_window(SLEEP_PERIOD_START, SLEEP_PERIOD_END):
                sleep_mode = True
            else: 
                sleep_mode = False
            
            # if current time is in upload period or upload mode
            if access_token_timer.is_current_time_in_window(UPLOAD_PERIOD_START, UPLOAD_PERIOD_END):
                upload_mode = True       
            else: 
                upload_mode = False

            #BELOW HAS BEEN TESTED
            # check if there is a new message stating that the mode should change
            # if no message, it will maintain the mode it is currently in
            new_mode = tele_bot1.receive_message(mode)
            # send a message if the mode has changed
            if new_mode != mode:
                tele_bot1.send_telegram(f'mode has been changed from {mode} to {new_mode}')
                mode = new_mode
            #check that a valid mode has been entered and send a message if not
            if mode not in ('sleep', 'maintenance', 'upload', 'image', 'video', 'ping', 'refresh_token', 'reboot'):
                message = "please send a valid mode. The valid modes are 'sleep', 'maintenance', 'upload', 'image', 'video', 'ping', 'refresh_token', 'reboot' and the format is 'user_name:mode' if sending a message to a specific pi and 'all:mode' if setting all pi's"
                tele_bot1.send_telegram(message)
                access_token_timer.sleep(60)
                # update the mode variable
        
            # if mode is maintenance
            if mode == 'maintenance':
                #TESTED: 06-10-2023 - except teamviewer

                # get ip address to use in the VNC
                ip_address = maintenance.get_ip_address()
                tele_bot1.send_telegram(f'IP address: {ip_address}. This is not actually required for VNC... going into sleep loop now...')
                # send Telegram reminding that must set mode at end and that
                # must change sleep and upload period if during that time and testing
                # is taking place
                # send telegram to remind to set mode again or restart  
                # while loop waiting for command to continue (set mode) or restart
                while (mode == 'maintenance'):
                    tele_bot1.send_telegram('please remember to change mode back once done with maintence or send a message "user_name:reboot" or "all:reboot" if you want to reboot all pis')
                    new_mode = tele_bot1.receive_message(mode)
                    if new_mode != mode:
                        tele_bot1.send_telegram(f'mode has been changed from {mode} to {new_mode}')
                        mode = new_mode
                    access_token_timer.sleep(60)
            
            # if mode is video and not sleep or upload = True 
            if mode == 'video' and not sleep_mode and not upload_mode:
                # take videos
                pi_camera.capture_video()
                #print('take video')

            # if mode is image and not sleep or upload = True 
            if mode == 'image' and not sleep_mode and not upload_mode:
                # take pictures
                pi_camera.capture_images()
                #print('take image')
                # take images
            

            # if mode is ping
            if mode == 'ping': 
            #TESTED
                # send a message saying ping until mode is changed
                tele_bot1.send_telegram('PING')
                access_token_timer.sleep(5)

            # if mode is refresh_token 
            if mode == 'refresh_token':
            #TESTED 
                # set_get_new_refresh_token = True
                set_get_new_refresh_token = True
            
            if mode == 'reboot':
            #TESTED 
                print('reboot')
                os.system('sudo reboot')
            
            # if mode is upload
            if mode == 'upload' or upload_mode:
            #TESTED
                # send message that uploading files
                tele_bot1.send_telegram('uploading files...')
                # call upload folders function
                drive_upload1.upload_folders_to_drive()
                # set upload_mode to False
                upload_mode = False
            
            if mode == 'sleep' or sleep_mode:
            #TESTED            
                access_token_timer.sleep(60)
                print('sleeping')

    except Exception as e:
        # Handle exceptions or errors gracefully
        e = str(e)
        print(f"An error occurred in main: {e}")
        tele_bot1.send_telegram(f"An error occurred in main: {e}")
        #force restart of pi
        traceback.print_exc()
        os.system('sudo reboot')

if __name__ == "__main__":
    # Call the main function when the script is run
    main()
