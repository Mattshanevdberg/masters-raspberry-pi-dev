
import picamera2
import os
from picamera2.encoders import JpegEncoder, H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput
#own functions
from owntime import Timer
from telegram import TelegramBot
import math

# GLOBALS

# VIDEO RELATED GLOBAL VARIABLES

# for the video resolution you have a finite number of options. Technically you can make the resolution anything and the 
# camera will select the resolution closest to that. However, different formats, encoders and framerates work for differ
# resolutions. 
# I have chosen the following resolutions and linked them to the relevant formats and encoders to create optimum outputs 
# when running on a raspberry pi zero. If you force a different resolution that is not listed here. It is possible but please
# go look at the relevant capture function and ensure that the correct encoder works for that format (H264 is the best encoder 
# but onlty works up till 1920x1080, after that you will have to use the JpegEncoder). The H264 creates far smaller files.
# different maximum frame rates will change when using different pi models (faster frame rates with more processing power).
# However, there are limits on frame rates at different resolutions from the camera module itself. There are 3 sensors on the 
# camera module 3 that operate in the following resolutions and can handle the following max frame rates:
# sensor 1: up to (1536x864), max fps = 120
# sensor 2: (1536x864) to (2304x1296), max fps = 56
# sensor 3: (2304x1296) to (4608x2592), max fps = 12
# note that when operating close to any of the limits (high res or high fps at a res), the system can become unstable and not
# provide the exact frame rate that you have requested. It is always good to check these.
# if, for whatever reason, there is a memory issue at any of the resolutions. Try reducing the buffer_count when configuring the video
# The aspect ratio is fixed at 16:9, for the fixed resoltions provided. 
# Note that the codec information on these videos is not captured correctly by the pi and video encoders (except the resolution) 
# and has to be found manually. There is a function in the test.py file that finds the actual number of frames in the video. 
# WARNING: mjpeg videos cannot be played by regular video players and must be converted to mp4 before they can be viewed. Even then, 
# the codec info is missing or incorrect, so the video will not play at the correct speed. These formats are primarily if you need higher
# resolutions and are going to be using the videos for a project where you will ultimately be extracting frames from the video.
#
# If you want videos that are viewable using standard video software, you should use resolutions lower than 1920x1080 
# and choose the mp4 format. 
#
# choose a video resolution:
# 1 = 1280x720 (mjpeg)(h264Encoder)
# 2 = 1280x720 (mp4)(max fps = 64)(h264Encoder)
# 3 = 1536x864 (mjpeg)(max fps = 37)(h264Encoder) note this is maximum ratio for sensor 1 in the camera module 3
# 4 = 1536x864 (mp4)(max fps = 37)(h264Encoder) note this is maximum ratio for sensor 1 in the camera module 3
# 5 = 1920x1080 (mjpeg)(max fps = 37)(h264Encoder) note that this is the maximum resolution for the h264Encoder, videos will become much larger using the JpegEncoder
# 6 = 1920x1080 (mp4)(max fps = 37)(h264Encoder) note that this is the maximum resolution for the h264Encoder, videos will become much larger using the JpegEncoder
# 7 = 2304x1296 (mjpeg)(max fps = 17)(JpegEncoder) note this is maximum ratio for sensor 2 in the camera module 3
# 8 = 2752x1550 (mjpeg)(max fps = 11)(JpegEncoder) note this is the last resolution that you can have 6 buffers
# 9 = 2992x1800 (mjpeg)(max fps = 8)(JpegEncoder) note this uses only 5 buffers and may be unstable
# 10 = 3792x2132 (mjpeg)(max fps = 3)(JpegEncoder) note this uses only 3 buffers and may be unstable
# 11 = 4608x2592 (mjpeg)(max fps = 1)(JpegEncoder) note this uses only 1 buffers and may be unstable
VID_RESOLUTION_INPUT = 8 # an interger from 1 to 11
# set the default frame rate (please take into account the max frame rates mentioned above for the possible resolutions)
VID_FRAME_RATE = 11
# set the video length to take in seconds
VID_SEC_LENGTH_OF_VIDEO = 60 # I would potentially move this into an option to be set through telegram and make this just setting the default value

# do not alter the below variable unless you would like to add new resolutions and know how to adjust the encoders in the capture function
VID_RESOLUTION_OPTIONS = {1: (1280, 720), 2: (1280, 720), 3: (1536, 864), 4: (1536, 864), 5: (1920, 1080), 6: (1920, 1080), 7: (2304, 1296), 8: (2752, 1550), 9: (2992, 1800), 10: (3792, 2132), 11: (4608, 2592)}


# CAMERA RELATED GLOBAL VARIABLES
# less research has gone into optimum resolutions and acheivable photos per second 
# the max number of pictures per sec @ 1920x1080 is around 4 and @2752x1550 it is around 2.2 (these are the only tested resolutions)
# if you try take more pictures per burst than is possible, the maximum number of pictures will simply be taken
# use higher buffer count (up to 6) for more images at a lower resolution and a lower buffer count for higher resolution lower frame rate
# if your buffer count is too high for a specified resolution, you will get a memory error. Lower the buffer count. At a buffer count of 
# 1 you should still be able to capture 1 image per second
# you can choose:
# the length of time in seconds that images will be taken and saved to a single folder in seconds (image burst)
IMG_SEC_BURST_LENGTH = 10
# number of pictures to take per the picture taking period (images per burst)
IMG_NUM_PER_BURST = 10 # I would potentially move this into an option to be set through telegram and make this just setting the default value
# resolution
IMG_RESOLUTION = VID_RESOLUTION_OPTIONS.get(VID_RESOLUTION_INPUT) # the default is making the image resolution equal to the video resolution
# select the buffer count (leave this at 1 unless you would like to capture more than a image per second then you can make it up to six, more buffers means you can capture images faster)
IMG_BUFFER_COUNT = 1

class Camera:
    def __init__(self, user_name): #source_folder_path):    REMOVED
        self.user_name = user_name
        self.not_configured = True
#        self.source_folder_path = source_folder_path       REMOVED
        self.output_folder = None
        self.timer = Timer(self.user_name)
        self.camera = picamera2.Picamera2()
        self.tele_bot_cam = TelegramBot(self.user_name)
        self.img_burst_length = IMG_SEC_BURST_LENGTH
        self.img_num_per_burst = IMG_NUM_PER_BURST
        self.img_resolution = IMG_RESOLUTION
        self.img_buffer_count = IMG_BUFFER_COUNT
        self.vid_length_of_vid = VID_SEC_LENGTH_OF_VIDEO
        self.vid_frame_rate = VID_FRAME_RATE
        self.vid_resolution = VID_RESOLUTION_OPTIONS.get(VID_RESOLUTION_INPUT)

    def create_folder(self, path):
        '''Create folder at the path with folder name
            Param: path including folder name'''
        # Create the output folder on the desktop if it doesn't exist
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            
        except Exception as e:  
            function_name = 'Camera.create_folder'
            e = str(e)
            self.timer.sleep(120)
            self.tele_bot_cam.send_telegram(function_name + e) 

   
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

            # get frame duration from fps for input into config
            frame_duration = (math.ceil(1000000/self.vid_frame_rate)-1, math.ceil(1000000/self.vid_frame_rate))


            #configure camera and take pictures for upload time
            if self.not_configured:
                config = self.camera.create_still_configuration({"size": self.img_resolution}, buffer_count=self.img_buffer_count, controls={"FrameDurationLimits": frame_duration})
                # align resolution with an optimum resolution
                self.camera.align_configuration(config)
                self.camera.configure(config)
                #self.not_configured = False

            self.camera.start()
            image_counter = 1
            #start timer
            self.timer.start_timer()
            while self.timer.check_elapsed_time() < self.img_burst_length:

                # Get the current time for naming the image
                current_time = self.timer.get_date_time()
                
                # Capture an image
                image_path = os.path.join(desktop_path, f'{self.user_name}_image_res_{self.img_resolution}_{current_time}_{image_counter + 1:03d}.jpg')
                self.camera.capture_file(image_path)
                
                # iterate counter
                image_counter += 1

            self.camera.stop()

        except Exception as e:  
            function_name = 'Camera.capture_images:'
            e = str(e)
            self.timer.sleep(120)
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

            # Get the current time for naming the video
            current_time = self.timer.get_date_time()
            # get the resolution, duration, fps for naming the video
            vid_width = str(self.vid_resolution[0])
            vid_height = str(self.vid_resolution[1])
            vid_duration = str(self.vid_length_of_vid)
            vid_fps = str(self.vid_frame_rate)

            # get frame duration from fps for input into config
            frame_duration = (math.ceil(1000000/self.vid_frame_rate)-1, math.ceil(1000000/self.vid_frame_rate))

            # choose the configuration and output type based on desired resoltuion and specified output type
            if VID_RESOLUTION_INPUT == 2 or 4 or 6:
                # set video path 
                vid_path = os.path.join(desktop_path, (f'{self.user_name}_video_res_{vid_width}_{vid_height}_duration_{vid_duration}_fps_{vid_fps}_{current_time}.mp4'))
                # set the video configuration
                video_config = self.camera.create_video_configuration({"size": self.vid_resolution}, buffer_count=6, controls={"FrameDurationLimits": frame_duration})
                # the following line will select an optimim resolution that is closest to the desired resolution
                self.camera.configure(video_config)
                # select the appropriate encoder for the resolution and output 
                encoder = H264Encoder()
                # select the appropriate output
                output = FfmpegOutput(vid_path)
                # start the camera capturing frames
                self.camera.start()
                # start the encoder recording video (this is, frames are thrown away. Now they are stored)
                self.camera.start_encoder(encoder, output)
                # sleep for the length of the video
                self.timer.sleep(self.vid_length_of_vid)
                # stop the video recording
                self.camera.stop_encoder()
                # stopping camera so can reconfigure if resolution changes
                self.camera.stop()
            
            # choose the configuration and output type based on desired resoltuion and specified output type
            elif VID_RESOLUTION_INPUT == 1 or 3 or 5:
                # set video path 
                vid_path = os.path.join(desktop_path, (f'{self.user_name}_video_res_{vid_width}_{vid_height}_duration_{vid_duration}_fps_{vid_fps}_{current_time}.mjpeg'))
                # set the video configuration
                video_config = self.camera.create_video_configuration({"size": self.vid_resolution}, buffer_count=6, controls={"FrameDurationLimits": frame_duration})
                # the following line will select an optimim resolution that is closest to the desired resolution
                self.camera.configure(video_config)
                # select the appropriate encoder for the resolution and output 
                encoder = H264Encoder()
                # select the appropriate output
                output = vid_path
                # start the camera capturing frames
                self.camera.start()
                # start the encoder recording video (this is, frames are thrown away. Now they are stored)
                self.camera.start_encoder(encoder, output)
                # sleep for the length of the video
                self.timer.sleep(self.vid_length_of_vid)
                # stop the video recording
                self.camera.stop_encoder()
                # stopping camera so can reconfigure if resolution changes
                self.camera.stop()

            # choose the configuration and output type based on desired resoltuion and specified output type
            elif VID_RESOLUTION_INPUT == 7 or 8:
                # set video path 
                vid_path = os.path.join(desktop_path, (f'{self.user_name}_video_res_{vid_width}_{vid_height}_duration_{vid_duration}_fps_{vid_fps}_{current_time}.mjpeg'))
                # set the video configuration
                video_config = self.camera.create_video_configuration({"size": self.vid_resolution}, buffer_count=6, controls={"FrameDurationLimits": frame_duration})
                # the following line will select an optimim resolution that is closest to the desired resolution
                self.camera.configure(video_config)
                # select the appropriate encoder for the resolution and output 
                encoder = JpegEncoder()
                # select the appropriate output
                output = vid_path
                # start the camera capturing frames
                self.camera.start()
                # start the encoder recording video (this is, frames are thrown away. Now they are stored)
                self.camera.start_encoder(encoder, output)
                # sleep for the length of the video
                self.timer.sleep(self.vid_length_of_vid)
                # stop the video recording
                self.camera.stop_encoder()
                # stopping camera so can reconfigure if resolution changes
                self.camera.stop()

            # choose the configuration and output type based on desired resoltuion and specified output type
            elif VID_RESOLUTION_INPUT == 9:
                # set video path 
                vid_path = os.path.join(desktop_path, (f'{self.user_name}_video_res_{vid_width}_{vid_height}_duration_{vid_duration}_fps_{vid_fps}_{current_time}.mjpeg'))
                # set the video configuration
                video_config = self.camera.create_video_configuration({"size": self.vid_resolution}, buffer_count=5, controls={"FrameDurationLimits": frame_duration})
                # the following line will select an optimim resolution that is closest to the desired resolution
                self.camera.configure(video_config)
                # select the appropriate encoder for the resolution and output 
                encoder = JpegEncoder()
                # select the appropriate output
                output = vid_path
                # start the camera capturing frames
                self.camera.start()
                # start the encoder recording video (this is, frames are thrown away. Now they are stored)
                self.camera.start_encoder(encoder, output)
                # sleep for the length of the video
                self.timer.sleep(self.vid_length_of_vid)
                # stop the video recording
                self.camera.stop_encoder()
                # stopping camera so can reconfigure if resolution changes
                self.camera.stop()

            # choose the configuration and output type based on desired resoltuion and specified output type
            elif VID_RESOLUTION_INPUT == 10:
                # set video path 
                vid_path = os.path.join(desktop_path, (f'{self.user_name}_video_res_{vid_width}_{vid_height}_duration_{vid_duration}_fps_{vid_fps}_{current_time}.mjpeg'))
                # set the video configuration
                video_config = self.camera.create_video_configuration({"size": self.vid_resolution}, buffer_count=3, controls={"FrameDurationLimits": frame_duration})
                # the following line will select an optimim resolution that is closest to the desired resolution
                self.camera.configure(video_config)
                # select the appropriate encoder for the resolution and output 
                encoder = JpegEncoder()
                # select the appropriate output
                output = vid_path
                # start the camera capturing frames
                self.camera.start()
                # start the encoder recording video (this is, frames are thrown away. Now they are stored)
                self.camera.start_encoder(encoder, output)
                # sleep for the length of the video
                self.timer.sleep(self.vid_length_of_vid)
                # stop the video recording
                self.camera.stop_encoder()
                # stopping camera so can reconfigure if resolution changes
                self.camera.stop()

            # choose the configuration and output type based on desired resoltuion and specified output type
            elif VID_RESOLUTION_INPUT == 11:
                # set video path 
                vid_path = os.path.join(desktop_path, (f'{self.user_name}_video_res_{vid_width}_{vid_height}_duration_{vid_duration}_fps_{vid_fps}_{current_time}.mjpeg'))
                # set the video configuration
                video_config = self.camera.create_video_configuration({"size": self.vid_resolution}, buffer_count=1, controls={"FrameDurationLimits": frame_duration})
                # the following line will select an optimim resolution that is closest to the desired resolution
                self.camera.configure(video_config)
                # select the appropriate encoder for the resolution and output 
                encoder = JpegEncoder()
                # select the appropriate output
                output = vid_path
                # start the camera capturing frames
                self.camera.start()
                # start the encoder recording video (this is, frames are thrown away. Now they are stored)
                self.camera.start_encoder(encoder, output)
                # sleep for the length of the video
                self.timer.sleep(self.vid_length_of_vid)
                # stop the video recording
                self.camera.stop_encoder()
                # stopping camera so can reconfigure if resolution changes
                self.camera.stop()

            else:
                e = "You did not select a valid resolution input for the video. Please put the device in maintenance mode and select a valid resolution for the video in the global variables in the camera.py file"
                self.timer.sleep(120)
                self.tele_bot_cam.send_telegram(function_name + e)

        except Exception as e:  
            function_name = 'Camera.capture_video:'
            e = str(e)
            self.timer.sleep(120)
            self.tele_bot_cam.send_telegram(function_name + e) 
        
    def update_vid_frame_rate(self, mode):
        '''takes in the frame rate and updates the frame rate that the videos are 
            taken at 
            Params: frame rate (frames per second)'''
        try:
            self.vid_frame_rate = int(mode)

        except Exception as e:  
            function_name = 'Camera.update_vid_frame_rate:'
            e = str(e)
            self.timer.sleep(120)
            self.tele_bot_cam.send_telegram(function_name + e) 

    def update_img_frame_rate(self, mode):
        '''takes in the frame rate and updates the frame rate that the pictures are 
            taken at 
            Params: frame rate (frames per second)'''
        try:
            self.img_num_per_burst = int(mode)

        except Exception as e:  
            function_name = 'Camera.update_img_frame_rate:'
            e = str(e)
            self.timer.sleep(120)
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

#camera = Camera('ljeantet')
#camera.output_folder = 'test'
#camera.capture_images()
#camera.capture_video()
