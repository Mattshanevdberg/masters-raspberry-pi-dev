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
SOURCE_FOLDER_PATH = '/home/' + USER_NAME + '/Desktop'
# time as an integer, !!!6:30am = 630 THERE IS NO ZERO IN FRONT!!! ,  8pm = 2000, 8:05pm = 2005, etc.
# if the sleep/upload period falls over over midnight (is over 2 days) please seperate the time into period1 ending at 2359 and period2 starting at 1 
SLEEP_PERIOD_START = 1930 
SLEEP_PERIOD_END = 2359
SLEEP_PERIOD_START2 = 1 # time as an integer, !!!6:30am = 630 THERE IS NO ZERO IN FRONT!!! ,  8pm = 2000, 8:05pm = 2005, etc.
SLEEP_PERIOD_END2 = 630
UPLOAD_PERIOD_START = 1930
UPLOAD_PERIOD_END = 2359
UPLOAD_PERIOD_START2 = 1
UPLOAD_PERIOD_END2 = 630

#Exception catching in declarations
tele_bot0 = TelegramBot(USER_NAME)

### MAIN LOOP ###
def main():
    try:
        # Instantiate your custom classes and objects and variables
        access_token_timer = Timer(USER_NAME)
        drive_auth1 = DriveAuth(USER_NAME, access_token_timer)
        drive_upload1 = DriveUpload(USER_NAME, drive_auth1, access_token_timer)
        pi_camera = Camera(USER_NAME)
        maintenance = Maintenance(USER_NAME)
        tele_bot1 = TelegramBot(USER_NAME)
        mode = 'video' # default mode on start up
        require_refresh_token = False
        sleep_mode = False # set to True if in sleep mode
        upload_mode = False
        #set_sleep_mode = False # this is set by the user if the forces sleep mode
        #set_upload_mode = False
        set_get_new_refresh_token = False

        # Set the system time to the time found on the web
        access_token_timer.sleep(60)
        access_token_timer.set_system_clock_from_web()

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
            if access_token_timer.is_current_time_in_window(SLEEP_PERIOD_START, SLEEP_PERIOD_END) or access_token_timer.is_current_time_in_window(SLEEP_PERIOD_START2, SLEEP_PERIOD_END2):
                sleep_mode = True
            else: 
                sleep_mode = False
            
            # if current time is in upload period or upload mode
            if access_token_timer.is_current_time_in_window(UPLOAD_PERIOD_START, UPLOAD_PERIOD_END) or access_token_timer.is_current_time_in_window(UPLOAD_PERIOD_START2, UPLOAD_PERIOD_END2):
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
            if mode not in ('sleep', 'maintenance', 'upload', 'image', 'video', 'ping', 'refresh_token', 'reboot', 'vid_frame_rate', 'img_frame_rate'):
                message = "please send a valid mode. The valid modes are 'sleep', 'maintenance', 'upload', 'image', 'video', 'ping', 'refresh_token', 'reboot', 'vid_frame_rate', 'img_frame_rate' and the format is 'user_name:mode' if sending a message to a specific pi and 'all:mode' if setting all pi's"
                tele_bot1.send_telegram(message)
                access_token_timer.sleep(60)
                # update the mode variable
        
            # if mode is maintenance
            if mode == 'maintenance':
                #TESTED: 06-10-2023 - except teamviewer

                # get ip address to use in the VNC
                #ip_address = maintenance.get_ip_address()
                #tele_bot1.send_telegram(f'IP address: {ip_address}. This is not actually required for VNC... going into sleep loop now...')
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
            
            if mode == 'vid_frame_rate':
                #TESTED: 06-10-2023 - except teamviewer
                #changing the frame rate in the capture video function
                while (mode == 'vid_frame_rate'):
                    tele_bot1.send_telegram('Please select input a frame rate (frames/sec) using the following format "username:frame_rate"')
                    access_token_timer.sleep(60)
                    # receiveing frame rate
                    new_mode = tele_bot1.receive_message(mode)
                    # if frame rate has been selected update framerate, else continue requesting
                    if new_mode != mode:
                        tele_bot1.send_telegram(f'frame rate is being changed to : {new_mode}')
                        pi_camera.update_vid_frame_rate(new_mode)
                        print(new_mode)
                        mode = new_mode
                        tele_bot1.send_telegram(f'frame rate has been updated. Please select new mode. Mode will automatically change to video mode if no mode is selected.')
                        access_token_timer.sleep(60)
                        new_mode = tele_bot1.receive_message(mode)
                        #check if mode has been changed else return to video mode
                        if new_mode != mode:
                            tele_bot1.send_telegram(f'mode has been changed to : {new_mode}')
                            mode = new_mode
                        else:
                            mode = 'video'

            if mode == 'img_frame_rate':
                #TESTED: 06-10-2023 - except teamviewer
                #changing the frame rate in the capture video function
                while (mode == 'img_frame_rate'):
                    tele_bot1.send_telegram('Please select input a frame rate (frames/sec) using the following format "username:frame_rate"')
                    access_token_timer.sleep(60)
                    # receiveing frame rate
                    new_mode = tele_bot1.receive_message(mode)
                    # if frame rate has been selected update framerate, else continue requesting
                    if new_mode != mode:
                        tele_bot1.send_telegram(f'frame rate is being changed to : {new_mode}')
                        pi_camera.update_img_frame_rate(new_mode)

                        print(new_mode)
                        mode = new_mode
                        tele_bot1.send_telegram(f'frame rate has been updated. Please select new mode. Mode will automatically change to video mode if no mode is selected.')
                        access_token_timer.sleep(60)
                        new_mode = tele_bot1.receive_message(mode)
                        #check if mode has been changed else return to video mode
                        if new_mode != mode:
                            tele_bot1.send_telegram(f'mode has been changed to : {new_mode}')
                            mode = new_mode
                        else:
                            mode = 'video'

            
            # if mode is video and not sleep or upload = True 
            if mode == 'video' and not sleep_mode and not upload_mode:
                # check if the system is running out of memory and skip taking videos if this is the case
                if not drive_upload1.check_for_low_memory():
                    # take videos
                    pi_camera.capture_video()
                    print('take video')
                else: 
                    tele_bot1.send_telegram("there is less than 1GB of memory left on the device. More videos will not be taken. Please change to upload mode or VNC into the pi and delete some videos manually")
                    access_token_timer.sleep(180) 

            # if mode is image and not sleep or upload = True 
            if mode == 'image' and not sleep_mode and not upload_mode:
                # check if the system is running out of memory and skip taking images if this is the case
                if not drive_upload1.check_for_low_memory():
                    # take pictures
                    pi_camera.capture_images()
                    print('take image')
                    # take images
                else: 
                    tele_bot1.send_telegram("there is less than 1GB of memory left on the device. More videos will not be taken. Please change to upload mode or VNC into the pi and delete some videos manually")
                    access_token_timer.sleep(180)            

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

                # call upload folders function
                drive_upload1.upload_folders_to_drive()
                # set upload_mode to False
                #upload_mode = False
            
            if mode == 'sleep' or sleep_mode and not upload_mode:
            #TESTED            
                access_token_timer.sleep(60)
                print('sleeping')

    except Exception as e:
        # Handle exceptions or errors gracefully
        e = str(e)
        print(f'If there is not a message after this, then an error occurred in the declarations in main: {e}, otherwise it occured in main')
        tele_bot0.send_telegram(f"An error occurred in main: {e}")
        print(f"An error occurred in main: {e}")
        tele_bot1.send_telegram(f"An error occurred in main: {e}")
        #check if maintenance mode is activated then just sleep
        traceback.print_exc()
        access_token_timer.sleep(900)
        while tele_bot1.receive_message(mode) == 'maintenance':
            access_token_timer.sleep(60)
        #force restart of pi
        os.system('sudo reboot')

if __name__ == "__main__":
    # Call the main function when the script is run
    main()
