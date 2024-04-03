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
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from pprint import *
import time
from picamera2.outputs import FileOutput 

#initiate camera
cam = picamera2.Picamera2()

#check the available sensors and resolutions
pprint(cam.sensor_modes)

#video_config = cam.create_video_configuration(main={"size": (4608, 2592), "format": "RGB888"}, buffer_count=2, controls={"FrameRate": 12})
#video_config = cam.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"}, buffer_count=2, controls={"FrameRate": 12})
#video_config = cam.create_video_configuration(main={"size": (3840, 2160), "format": "RGB888"}, buffer_count=2, controls={"FrameRate": 12})
video_config = cam.create_video_configuration(main={"size": (2560, 1440), "format": "RGB888"}, buffer_count=2, controls={"FrameRate": 12})

cam.configure(video_config)

#encoder = H264Encoder()
encoder = JpegEncoder(q=80)

#output = FfmpegOutput('test.mp4')

cam.start() # potentially check that the camera started (a trouble shooting option)

#encoder.output = FileOutput('test.mp4')

encoder.output = FileOutput(f"{int(time.time())}.mjpeg")

cam.start_encoder(encoder)

time.sleep(2)

cam.stop_encoder()
