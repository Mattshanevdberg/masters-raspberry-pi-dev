import picamera2
import os
#own functions
from owntime import Timer

# GLOBALS
IMG_SEC_INTERVAL_BETWEEN_IMAGES = 1
IMG_SEC_BETWEEN_FOLDER_UPLOAD = 60

class Camera:
    def __init__(self, user_name, source_folder_path):
        self.user_name = user_name
        self.source_folder_path = source_folder_path
        self.output_folder = None
        self.timer = Timer()
        self.camera = picamera2.Picamera2()

    def create_folder(self, path):
        '''Create folder at the path with folder name
            Param: path including folder name'''
        # Create the output folder on the desktop if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)
    
    def capture_images(self):
        '''captures images at a set interval for a set amount of time
        then saves them to a folder on the desktop in a folder named the time, date, camera'''

        #set folder name to the current time
        self.output_folder = self.timer.get_date_time()

        # set path to desktop and create folder there 
        desktop_path = f'/home/{self.user_name}/Desktop/{self.user_name}_{self.output_folder}'
        self.create_folder(desktop_path)

        #start timer
        start_time = self.timer.start_timer()

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
            
            print(f'Captured image: {image_path}')
            
            # check if time has expired 
            elapsed_time = self.timer.check_elapsed_time()
            if elapsed_time > (IMG_SEC_BETWEEN_FOLDER_UPLOAD):
                not_expired = False
            
            # iterate counter
            image_counter += 1

        self.camera.close()

    def capture_video(self):
        '''captures videos at of a set length for a set 
        amount of time'''

        #set folder name to the current time
        self.output_folder = self.timer.get_date_time()

        # set path to desktop and create folder there 
        desktop_path = f'/home/{self.user_name}/Desktop/{self.user_name}_{self.output_folder}'
        self.create_folder(desktop_path)

        #start timer
        start_time = self.timer.start_timer()

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
            image_path = os.path.join(desktop_path, f'{self.user_name}_vid_{current_time}_{image_counter + 1:03d}.mov')
            self.camera.capture_file(image_path)
            
            print(f'Captured image: {image_path}')
            
            # check if time has expired 
            elapsed_time = self.timer.check_elapsed_time()
            if elapsed_time > (IMG_SEC_BETWEEN_FOLDER_UPLOAD):
                not_expired = False
            
            # iterate counter
            image_counter += 1

        self.camera.close()