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



#initiate camera
cam = picamera2.Picamera2()

#check the available sensors and resolutions, this is only if you need to do not know what resolutions are available
#pprint(cam.sensor_modes)
def test_resolution_and_frame_rate():
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
        encoder.output = FileOutput(f"{resoltion}_{frame_rate}.mjpeg")

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

    name = f'"{resolution1}_{frame_rate}.mjpeg"'
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

    name = f'"{resolution1}_{frame_rate}.mjpeg"'
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

    name = f'"{resolution1}_{frame_rate}.mjpeg"'
    cam.start_recording(encoder, name)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()

    # forth resolution and frame rate
    resolution2 = (2560, 1440) # 2 x res1
    frame_rate = 15
    video_config = cam.create_video_configuration(main={"size": resolution2, "format": "RGB888"}, buffer_count=2, controls={"FrameRate": frame_rate})
    cam.configure(video_config)

    encoder = MJPEGEncoder(10000000)

    name = f'"{resolution1}_{frame_rate}.mjpeg"'
    cam.start_recording(encoder, name)
    time.sleep(10)
    cam.stop_recording()
    cam.stop()



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
process_videos_with_extension('/home/matthew/Desktop/Desktop','mjpeg')

'''