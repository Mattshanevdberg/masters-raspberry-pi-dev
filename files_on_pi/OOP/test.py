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
from picamera2.encoders import H264Encoder, JpegEncoder, MJPEGEncoder
from picamera2.outputs import FfmpegOutput
from pprint import *
import time
from picamera2.outputs import FileOutput
import os
import math



#initiate camera
cam = picamera2.Picamera2()

#check the available sensors and resolutions, this is only if you need to do not know what resolutions are available
pprint(cam.sensor_modes)

def mjpeg_encoder(resolution, frame_rate):
    print(f'current resolution is: {resolution}')
    print(f'current frame rate is attempting is: {frame_rate}')

    frame_duration = math.ceil(1000000/frame_rate)
    print(frame_duration)
    frame_dur2 = (frame_duration, frame_duration)
    print(frame_dur2)

    video_config = cam.create_video_configuration(main={"size": resolution, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})

    cam.configure(video_config)
    
    pprint(cam.video_configuration)
    
    # the frame durations are between: 8324, 77249844
    a, b, c = cam.camera_controls["FrameDurationLimits"]
    print(a, b, c)

    frame_duration = math.ceil(1000000/frame_rate)
    print(frame_duration)
    frame_dur2 = (frame_duration, frame_duration)
    print(frame_dur2)
    cam.video_configuration.controls.FrameDurationLimits = frame_dur2


    time_stamp = time.strftime("%y_%m_%d_%H_%M")
    output_name = f'{time_stamp}_test.mp4'

    encoder = H264Encoder()
    output = FfmpegOutput(output_name)

    cam.start_recording(encoder, output)
    time.sleep(10)
    cam.stop_recording()



# first resolution and frame rate
resolution1 = (1280, 720) #720p HD quality
frame_rate1 = 15.0
mjpeg_encoder(resolution1, frame_rate1)

resolution1 = (1280, 1440) #720p HD quality
frame_rate2 = 50.0
mjpeg_encoder(resolution1, frame_rate2)

resolution2 = (2560, 1000) #720p HD quality
frame_rate3 = 12.0
mjpeg_encoder(resolution2, frame_rate1)



def test_resolution_and_frame_rate():

    #cam = picamera2.Picamera2()
    # input resolution to test
    # resolution 1
    resolution1 = (1280,720) #720p HD quality
    resolution2 = (2560, 1440) # 2 x res1
    resolution3 = (3200, 1800) # 2.5 x res1
    resolution4 = (3840, 2160) # 3 x res1
    resolution5 = (4608, 2592) # theoretical max resolution

    resolution = resolution1

    print(f'current resolution is: {resolution}')

    # for a specific resolution, up the frame rate iteratively taking 10sec videos
    for frame_rate in range(50, 200, 10):

        # print the frame rate 
        print(f'current frame rate is attempting is: {frame_rate}')

        # configure camera
        video_config = cam.create_video_configuration(main={"size": resolution, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
        cam.configure(video_config)

        # set the encoder and start camera
        encoder = JpegEncoder(q=80)
        cam.start() 

        #set the output file name
        encoder.output = FileOutput(f"{resolution}_{frame_rate}.mjpeg")

        #start recording
        cam.start_encoder(encoder)

        # record a 10 second video
        time.sleep(10)

        #end recorder
        cam.stop_encoder()

        #stop the camera so that you can reconfigure it with a different resolution
        cam.stop()

def capture_mjpeg_v4I2():
    #cam2 = picamera2.Picamera2()

    # first resolution and frame rate
    resolution1 = (1280,720) #720p HD quality
    frame_rate = 15
    video_config = cam.create_video_configuration(main={"size": resolution1, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
    cam.configure(video_config)

    encoder = MJPEGEncoder(10000000)

    name = f'{resolution1}_{frame_rate}.mjpeg'
    cam.start_recording(encoder, name)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()

    # second resolution and frame rate
    resolution1 = (1280,720) #720p HD quality
    frame_rate = 50
    video_config = cam.create_video_configuration(main={"size": resolution1, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
    cam.configure(video_config)

    encoder = MJPEGEncoder(10000000)

    name = f'{resolution1}_{frame_rate}.mjpeg'
    cam.start_recording(encoder, name)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()

    # third resolution and frame rate
    resolution1 = (1280,720) #720p HD quality
    frame_rate = 100
    video_config = cam.create_video_configuration(main={"size": resolution1, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
    cam.configure(video_config)

    encoder = MJPEGEncoder(10000000)

    name = f'{resolution1}_{frame_rate}.mjpeg'
    cam.start_recording(encoder, name)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()
#cam = picamera2.Picamera2()
    # forth resolution and frame rate
    resolution2 = (2560, 1440) # 2 x res1
    frame_rate = 15
    video_config = cam.create_video_configuration(main={"size": resolution2, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
    cam.configure(video_config)

    encoder = MJPEGEncoder(10000000)

    name = f'{resolution2}_{frame_rate}.mjpeg'
    cam.start_recording(encoder, name)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()

def mp4_with_res_adjust():

    # first resolution and frame rate
    resolution1 = (1280,720) #720p HD quality
    frame_rate = 15
    video_config = cam.create_video_configuration(main={"size": resolution1, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
    cam.configure(video_config)

    # Initialize the encoder with a bitrate, adjust as needed
    encoder = H264Encoder(10000000)  # Example bitrate

    # Specify the output file name and format
    name = f'{resolution1}_{frame_rate}.mp4'
    output = FfmpegOutput(name)
    # Start recording
    cam.start_recording(encoder, output)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()

    # first resolution and frame rate
    resolution1 = (1280,720) #720p HD quality
    frame_rate = 50
    video_config = cam.create_video_configuration(main={"size": resolution1, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
    cam.configure(video_config)

    # Initialize the encoder with a bitrate, adjust as needed
    encoder = H264Encoder(10000000)  # Example bitrate

    # Specify the output file name and format
    name = f'{resolution1}_{frame_rate}.mp4'
    output = FfmpegOutput(name)
    # Start recording
    cam.start_recording(encoder, output)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()

    # first resolution and frame rate
    resolution1 = (1280,720) #720p HD quality
    frame_rate = 100
    video_config = cam.create_video_configuration(main={"size": resolution1, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
    cam.configure(video_config)

    # Initialize the encoder with a bitrate, adjust as needed
    encoder = H264Encoder(10000000)  # Example bitrate

    # Specify the output file name and format
    name = f'{resolution1}_{frame_rate}.mp4'
    output = FfmpegOutput(name)
    # Start recording
    cam.start_recording(encoder, output)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()

    # first resolution and frame rate
    resolution1 = (2560, 1440) #720p HD quality
    frame_rate = 15
    video_config = cam.create_video_configuration(main={"size": resolution1, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
    cam.configure(video_config)

    # Initialize the encoder with a bitrate, adjust as needed
    encoder = H264Encoder(10000000)  # Example bitrate

    # Specify the output file name and format
    name = f'{resolution1}_{frame_rate}.mp4'
    output = FfmpegOutput(name)
    # Start recording
    cam.start_recording(encoder, output)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()

    # first resolution and frame rate
    resolution1 = (3200, 1800) #720p HD quality
    frame_rate = 15
    video_config = cam.create_video_configuration(main={"size": resolution1, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
    cam.configure(video_config)

    # Initialize the encoder with a bitrate, adjust as needed
    encoder = H264Encoder(10000000)  # Example bitrate

    # Specify the output file name and format
    name = f'{resolution1}_{frame_rate}.mp4'
    output = FfmpegOutput(name)
    # Start recording
    cam.start_recording(encoder, output)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()

    # first resolution and frame rate
    resolution1 = (3200, 1800) #720p HD quality
    frame_rate = 22
    video_config = cam.create_video_configuration(main={"size": resolution1, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
    cam.configure(video_config)

    # Initialize the encoder with a bitrate, adjust as needed
    encoder = H264Encoder(10000000)  # Example bitrate

    # Specify the output file name and format
    name = f'{resolution1}_{frame_rate}.mp4'
    output = FfmpegOutput(name)
    # Start recording
    cam.start_recording(encoder, output)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()


def config_direct_into_object_new(resolution, frame_rate):
    #cam = picamera2.Picamera2()
    #set the inputs
    encoder = '.h264'
    extension = '.mp4'
    hour = int(time.strftime('%H'))
    now = time.strftime("%y_%m_%d_%H_%M")
    resolutionstr = str(resolution).replace('(', '-').replace(')', '-').replace(' ', '-')
    frame_ratestr = str(frame_rate).replace('.', '-')
    h264_output = resolutionstr+frame_ratestr+now+encoder
    mp4_output = 'test'+resolutionstr+frame_ratestr+now+extension
    frame_duration = math.ceil(1000000/frame_rate)
    print(frame_duration)
    frame_dur2 = (frame_duration, frame_duration)
    print(frame_dur2)
    cam.video_configuration.controls.FrameDurationLimits = frame_dur2
    cam.video_configuration.size = resolution
    print(cam.video_configuration.controls)
    print(cam.video_configuration)

    # Initialize the encoder with a bitrate, adjust as needed
    encoder = H264Encoder(bitrate=17000000)  # Example bitrate

    # Start recording
    cam.start_recording(encoder, h264_output)
    print('camera started recording')
    time.sleep(10)
    print('sleep done')
    cam.stop_recording()
    print('recording done')
    cam.stop()
    print('camera stopped')

    #convert h264 to mp4, and delete h264 file
    strframe_rate = str(frame_rate)
    os.system("ffmpeg -r "+strframe_rate+" -i "+h264_output+" -c copy "+mp4_output)
    #os.remove(h264_output)

# first resolution and frame rate
#resolution1 = (1280, 720) #720p HD quality
#frame_rate1 = 15.0
#config_direct_into_object(resolution1, frame_rate1)
#cam = picamera2.Picamera2()
#resolution1 = (1280, 720) #720p HD quality
#frame_rate2 = 50.0
#config_direct_into_object(resolution1, frame_rate2)

#resolution2 = (3200, 1800) #720p HD quality
#frame_rate3 = 12.0
#config_direct_into_object(resolution2, frame_rate3)

def config_direct_into_object(resolution, frame_rate):
    #set the inputs
    encoder = '.h264'
    extension = '.mp4'
    resolutionstr = str(resolution).replace('(', '-').replace(')', '-')
    frame_ratestr = str(frame_rate)
    h264_output = resolutionstr+frame_ratestr+encoder
    mp4_output = resolutionstr+frame_ratestr+extension
    cam.video_configuration.controls.FrameRate = frame_rate
    cam.video_configuration.size = resolution
    

    # Initialize the encoder with a bitrate, adjust as needed
    encoder = H264Encoder(bitrate=17000000)  # Example bitrate

    # Start recording
    cam.start_recording(encoder, h264_output)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()

    #convert h264 to mp4, and delete h264 file
    os.system("ffmpeg -r "+frame_ratestr+" -i "+h264_output+" -c copy "+mp4_output)
    os.remove(h264_output)

# first resolution and frame rate
#resolution1 = (1280, 720) #720p HD quality
#frame_rate1 = 15.0
#config_direct_into_object(resolution1, frame_rate1)

#resolution1 = (1280, 720) #720p HD quality
#frame_rate2 = 50.0
#config_direct_into_object(resolution1, frame_rate2)

#resolution2 = (3200, 1800) #720p HD quality
#frame_rate3 = 12.0
#config_direct_into_object(resolution1, frame_rate1)

'''

# Now we need to check that the correct resolution and fps were captured
import cv2 
import glob
import os

def get_video_properties(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}.")
        return None
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count2 = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps if fps else 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    cap.release()
    
    resolution = (width, height)
    return frame_count, frame_count2, fps, duration, resolution

def process_videos_with_extension(path_to_directory, extension):
    # Use glob to find all files with the specified extension in the current directory
    path_pattern = os.path.join(path_to_directory, f'*.{extension}')
    # 
    for video_path in glob.glob(path_pattern):
        properties = get_video_properties(video_path)
        if properties:
            frame_count, frame_count2, fps, duration, resolution = properties
            print(f"Video Path: {video_path}")
            print(f"Total number of frames: {frame_count}, framecount2 {frame_count2}")
            print(f"Frames per second (FPS): {fps}")
            print(f"Duration (in seconds): {duration}")
            print(f"Resolution: {resolution[0]}x{resolution[1]}\n")

# Example usage - process all .mjpeg files in the current directory
process_videos_with_extension('/home/matthew/Desktop/Desktop','mp4')
'''

