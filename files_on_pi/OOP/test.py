'''
from owntime import Timer
import time

inte = 25

output = 1/inte

time_ = Timer()

print (output)
print(time.time())
time_.sleep(output)
print(time.tiem())
'''
'''
import drive
from owntime import Timer
access_token_timer = Timer('matthew')

drive_auth = drive.DriveAuth('matthew', access_token_timer)

drive_upload = drive.DriveUpload('matthew', drive_auth, access_token_timer)
#print(drive_auth.retrieve_refresh_token)
#drive_upload.collect_folder_paths_to_upload()
#drive_upload.delete_folders()
#drive_upload.upload_folders_to_drive()
#drive.request_device_authorization()
print(drive_upload.check_for_low_memory())
'''
import picamera2
from picamera2.encoders import H264Encoder, JpegEncoder
from picamera2.outputs import FfmpegOutput
from pprint import *
import time
from picamera2.outputs import FileOutput 


#initiate camera
cam = picamera2.Picamera2()

#check the available sensors and resolutions, this is only if you need to do not know what resolutions are available
#pprint(cam.sensor_modes)

# input resolution to test
# resolution 1
resolution1 = (1280,720) #720p HD quality
resolution2 = (2560, 1440) # 2 x res1
resolution3 = (3200, 1800) # 2.5 x res1
resolution4 = (3840, 2160) # 3 x res1
resolution5 = (4608, 2592) # theoretical max resolution

resoltion = resolution1

print(f'current resolution is: {resoltion}')

# for a specific resolution, up the frame rate iteratively taking 10sec videos
for frame_rate in range(50, 200, 10):

    # print the frame rate 
    print(f'current frame rate is attempting is: {frame_rate}')

    # configure camera
    video_config = cam.create_video_configuration(main={"size": resolution1, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
    cam.configure(video_config)

    # set the encoder and start camera
    encoder = JpegEncoder(q=80)
    cam.start() 

    #set the output file name
    encoder.output = FileOutput(f"{resoltion}_{frame_rate}.mjpeg")

    #start recording
    cam.start_encoder(encoder)

    # record a 10 second video
    time.sleep(10)

    #end recorder
    cam.stop_encoder()
