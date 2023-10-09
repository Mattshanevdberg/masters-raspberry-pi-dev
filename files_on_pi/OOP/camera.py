import picamera2
import os
#own functions
from owntime import Timer
from telegram import TelegramBot

# GLOBALS
IMG_SEC_INTERVAL_BETWEEN_IMAGES = 1
IMG_SEC_BETWEEN_FOLDER_UPLOAD = 60
VID_SEC_LENGTH_OF_VIDEO = 60

class Camera:
    def __init__(self, user_name): #source_folder_path):    REMOVED
        self.user_name = user_name
#        self.source_folder_path = source_folder_path       REMOVED
        self.output_folder = None
        self.timer = Timer()
        self.camera = picamera2.Picamera2()
        self.tele_bot_cam = TelegramBot(self.user_name)

    def create_folder(self, path):
        '''Create folder at the path with folder name
            Param: path including folder name'''
        # Create the output folder on the desktop if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)
   
    def capture_images(self):
        '''captures images at a set interval for a set amount of time
        then saves them to a folder on the desktop in a folder named the time, date, camera'''
        try:
            #set folder name to the current time
            self.output_folder = self.timer.get_date_time()

            # set path to desktop and create folder there 
            desktop_path = f'/home/{self.user_name}/Desktop/{self.user_name}_image_{self.output_folder}'
            self.create_folder(desktop_path)

            #start timer
            self.timer.start_timer()

            #configure camera and take pictures for upload time
            config = self.camera.create_still_configuration()
            self.camera.configure(config)
            not_expired = True
            self.camera.start()
            image_counter = 1
            while (not_expired):

                # Sleep for set inteval
                self.timer.sleep(IMG_SEC_INTERVAL_BETWEEN_IMAGES)

                # Get the current time for naming the image
                current_time = self.timer.get_date_time()
                
                # Capture an image
                image_path = os.path.join(desktop_path, f'{self.user_name}_image_{current_time}_{image_counter + 1:03d}.jpg')
                self.camera.capture_file(image_path)
                
                #print(f'Captured image: {image_path}')
                
                # check if time has expired 
                elapsed_time = self.timer.check_elapsed_time()
                if elapsed_time > (IMG_SEC_BETWEEN_FOLDER_UPLOAD):
                    not_expired = False
                
                # iterate counter
                image_counter += 1

            self.camera.close()

        except Exception as e:  
            function_name = 'DriveAuth.capture_images'
            self.tele_bot_cam.send_telegram(function_name + e) 

    def capture_video(self):
        '''captures videos at of a set length for a set amount of time 
        then saves them to a folder on the desktop in a folder named the time, date, camera'''

        try:

            #set folder name to the current time
            self.output_folder = self.timer.get_date_time()

            # set path to desktop and create folder there 
            desktop_path = f'/home/{self.user_name}/Desktop/{self.user_name}_video_{self.output_folder}'
            self.create_folder(desktop_path)

            # Get the current time for naming the image
            current_time = self.timer.get_date_time()

            #take video of set length of time
            self.camera.start_and_record_video(f'{self.user_name}_video_{current_time}.mp4', quality=Quality.VERY_HIGH, duration=VID_SEC_LENGTH_OF_VIDEO)

        except Exception as e:  
            function_name = 'DriveAuth.capture_video'
            self.tele_bot_cam.send_telegram(function_name + e) 
            
#####TEST
'''
    def save_refresh_token(self, image_path):
        try:
            with open(image_path, 'w') as file:
                file.write('Test')
                print('Refresh token saved successfully.')
        except Exception as e:
            print(f"An error occurred while saving the refresh token: {e}")

    def capture_images_test(self):
            captures images at a set interval for a set amount of time
            then saves them to a folder on the desktop in a folder named the time, date, camera

            #set folder name to the current time
            self.output_folder = self.timer.get_date_time()

            # set path to desktop and create folder there 
            desktop_path = f'/home/{self.user_name}/Desktop/{self.user_name}_image_{self.output_folder}'
            self.create_folder(desktop_path)

            #start timer
            start_time = self.timer.start_timer()

            #configure camera and take pictures for upload time
            #config = self.camera.create_still_configuration()
            #self.camera.configure(config)
            not_expired = True
            #self.camera.start()
            image_counter = 0
            while (not_expired):

                # Sleep for set inteval
                self.timer.sleep(IMG_SEC_INTERVAL_BETWEEN_IMAGES)

                # Get the current time for naming the image
                current_time = self.timer.get_date_time()
                
                # Capture an image
                image_path = os.path.join(desktop_path, f'{self.user_name}_image_{current_time}_{image_counter:03d}.jpg')
                #self.camera.capture_file(image_path)
                print(image_path)
                self.save_refresh_token(image_path)
                
                print(f'Captured image: {image_path}')

                #iterate image counter
                image_counter += 1
                
                # check if time has expired 
                elapsed_time = self.timer.check_elapsed_time()
                if elapsed_time > (IMG_SEC_BETWEEN_FOLDER_UPLOAD):
                    not_expired = False

#            self.camera.close()

    def capture_video_test(self):
        captures videos at of a set length for a set amount of time 
        then saves them to a folder on the desktop in a folder named the time, date, camera

        #set folder name to the current time
        self.output_folder = self.timer.get_date_time()

        # set path to desktop and create folder there 
        desktop_path = f'/home/{self.user_name}/Desktop/{self.user_name}_video_{self.output_folder}'
        self.create_folder(desktop_path)

        # Get the current time for naming the image
        current_time = self.timer.get_date_time()

        #take video of set length of time
        video_path = os.path.join(desktop_path, f'{self.user_name}_video_{current_time}.mp4')
        #self.camera.start_and_record_video(video_path, quality=Quality.VERY_HIGH, duration=VID_SEC_LENGTH_OF_VIDEO)
        print(video_path)
'''
#camera = Camera('matthew')
#camera.capture_images_test()
#camera.capture_video_test()