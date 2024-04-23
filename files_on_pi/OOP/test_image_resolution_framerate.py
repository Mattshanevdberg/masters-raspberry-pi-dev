import picamera2
from picamera2.encoders import H264Encoder, JpegEncoder, MJPEGEncoder, Encoder
from picamera2.outputs import FfmpegOutput
from pprint import *
import time
from picamera2.outputs import FileOutput
import os
import math
import io


picam2 = picamera2.Picamera2()

#print out the available sensors
#pprint(picam2.sensor_modes)

# add an if statement to select the correct sensor configuration based on the d>
# 0 = 'size': (1536, 864),'fps': 120.13
# 1 = 'size': (2304, 1296), 'fps': 56.03
# 2 = 'size': (4608, 2592), 'fps': 14.35
mode = picam2.sensor_modes[1]
#pprint(mode)

# set frame rate to automatically be something that can be handled by all resol>
config = picam2.create_still_configuration({"size": (2752, 1550)}, buffer_count=5, controls={"FrameDurationLimits": (25000, 25000)})

#config = picam2.create_video_configuration(raw={'format': mode['format'], 'siz>
#pprint(config)
# the following line will select an optimim resolution that is closest to the d>
picam2.align_configuration(config)

#print out the video configuration before the frame duration change
#pprint(config)

# here I think it would help to create set frame rates
# 5 = 200000
# 10 = 100000
# 12 = 83332
# 15 = 66666
# 20 = 50000
# 25 = 40000


picam2.configure(config)

pprint(picam2.camera_configuration())



# trying the h264Encoder
#encoder = H264Encoder()
#output = "h264mjpeg10sec38fpsL1920x1080.mp4"
#configuration is high and frame rate is at max for the specified resolution
# start recording and stop recording will start the camera and the encoder at t>
# only the lowest sensor resolution appears to work for the H264 encoder...
#picam2.start_recording(encoder, output)
# trying to start the camera and encoder seperately
picam2.start()
# set the frame rate to a different frame rate (the one that the video says it >
#picam2.set_controls({"FrameDurationLimits": (40000, 40005)})
#time.sleep(3)
start_time = time.time()
while (time.time() - start_time) < 10:
    cur_time = time.time()
    file_name = str(cur_time)+".jpg"
    picam2.capture_file(file_name)

#metadata = picam2.capture_metadata()
#controls = {c: metadata[c] for c in ["FrameDuration"]}
#print(controls)
#picam2.start_encoder(encoder, output)
#time.sleep(10)
#print(metadata["FrameDuration"])
# setting the rate through the set controls command
#time.sleep(5)
#picam2.set_controls({"FrameDurationLimits": (50000, 50005)})
#time.sleep(2)
#picam2.start()
#metadata2 = picam2.capture_metadata()
#controls2 = {c: metadata2[c] for c in ["FrameDuration"]}
#print(controls2)
#time.sleep(2)
#picam2.stop_recording()
#stop camera and encoder seperately
#picam2.stop_encoder()

#testin different frame reates
#picam2.set_controls({"FrameDurationLimits": (25641, 25642)})
#output = "h264mjpeg10sec39fpsL1920x1080.mp4"
#time.sleep(2)
#metadata = picam2.capture_metadata()
#controls = {c: metadata[c] for c in ["FrameDuration"]}
#print(controls)
#picam2.start_encoder(encoder, output)
#time.sleep(10)
#picam2.stop_encoder()
