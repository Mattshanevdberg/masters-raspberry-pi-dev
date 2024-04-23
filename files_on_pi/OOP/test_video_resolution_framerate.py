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

# add an if statement to select the correct sensor configuration based on the desired resolution
# 0 = 'size': (1536, 864),'fps': 120.13
# 1 = 'size': (2304, 1296), 'fps': 56.03
# 2 = 'size': (4608, 2592), 'fps': 14.35
mode = picam2.sensor_modes[1]
#pprint(mode)

# set frame rate to automatically be something that can be handled by all resolutions
config = picam2.create_video_configuration({"size": (3792, 2133)}, buffer_count=3, controls={"FrameDurationLimits": (500000, 500000)})
#config = picam2.create_video_configuration(raw={'format': mode['format'], 'size': mode['size']})
#pprint(config)
# the following line will select an optimim resolution that is closest to the desired resolution
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
# 30 = 33333
# 40 = 25000
# 50 = 20000
# 60 = 16667
# 80 = 12500
# 100 = 10000
# 110 = 9090
# 120 = 8332
 
#config = picam2.create_video_configuration(controls={"FrameDurationLimits": (999995, 100005)})

picam2.configure(config)

pprint(picam2.camera_configuration())
# here we will potentially have to check if raw is smaller and adjust raw accordingly

# checking the camera controls - this just gives you the options available for camera controls. You must capture the metadata for each frame to see if the controls worked
#pprint(picam2.camera_controls)
# so here I am going to start the camera and run for 2 seconds, then change the frame rate and run for a further 2 seconds, checking the metadata of the frames captured
# all the code below is commented out to test the camera function
#picam2.start()
#time.sleep(1)
#metadata = picam2.capture_metadata()
#controls = {c: metadata[c] for c in ["FrameDuration"]}
#print(controls)
##print(metadata["FrameDuration"])
## setting the rate through the set controls command
##time.sleep(2)
#picam2.set_controls({"FrameDurationLimits": (50000, 50005)})
#time.sleep(2)
##picam2.start()
#metadata2 = picam2.capture_metadata()
#controls2 = {c: metadata2[c] for c in ["FrameDuration"]}
#print(controls2)
#time.sleep(2)
##print(metadata["FrameDuration"])
##picam2.stop()
# so this sets the frame rate and it works!

# the configuration will remain the same so the below line is pointless. Once the camera is started you cannot update the config
#pprint(picam2.camera_configuration())

# trying a simple way to capture an image with the same input as the video config
#data = io.BytesIO()
#picam2.capture_file(data, format='jpeg')
#print("finished")
# that did not work

# Try to capture a video using the encoder
#first we must choose the encoder and the output
#encoder = H264Encoder(bitrate=10000000)
#output = "test.h264"
#trying the null encoder with the .m2v output
#encoder = Encoder()
#output = "testnullmp4.mjpeg"
#trying the JpegEncoder encoder with the .mjpeg output
encoder = JpegEncoder()
#output = "MJPEGmjpeg10sec38fpsL1920x1080.mjpeg"
#trying the JpegEncoder encoder with the .mjpeg output
#encoder = MJPEGEncoder()
#output = "testMJPEGmjpeg.mjpeg"
# trying the h264Encoder
#encoder = H264Encoder()
output = "Jpegmjpeg10sec2fpsL3792x2133.mjpeg"
#configuration is high and frame rate is at max for the specified resolution
# start recording and stop recording will start the camera and the encoder at the same time
# only the lowest sensor resolution appears to work for the H264 encoder...
#picam2.start_recording(encoder, output)
# trying to start the camera and encoder seperately
picam2.start()
# set the frame rate to a different frame rate (the one that the video says it is at)
#picam2.set_controls({"FrameDurationLimits": (40000, 40005)})
#time.sleep(3)
metadata = picam2.capture_metadata()
controls = {c: metadata[c] for c in ["FrameDuration"]}
print(controls)
picam2.start_encoder(encoder, output)
time.sleep(10)
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
picam2.stop_encoder()
#testin different frame reates
picam2.set_controls({"FrameDurationLimits": (333333, 333334)})
output = "Jpegmjpeg10sec3fpsL3792x2133.mjpeg"
time.sleep(4)
metadata = picam2.capture_metadata()
controls = {c: metadata[c] for c in ["FrameDuration"]}
print(controls)
picam2.start_encoder(encoder, output)
time.sleep(10)
picam2.stop_encoder()

picam2.set_controls({"FrameDurationLimits": (250000, 250000)})
output = "Jpegmjpeg10sec4fpsL3792x2133.mjpeg"
time.sleep(2)
metadata = picam2.capture_metadata()
controls = {c: metadata[c] for c in ["FrameDuration"]}
print(controls)
picam2.start_encoder(encoder, output)
time.sleep(10)
picam2.stop_encoder()

picam2.set_controls({"FrameDurationLimits": (200000, 200000)})
output = "Jpegmjpeg10sec5fpsL3792x2133.mjpeg"
time.sleep(2)
metadata = picam2.capture_metadata()
controls = {c: metadata[c] for c in ["FrameDuration"]}
print(controls)
picam2.start_encoder(encoder, output)
time.sleep(10)
picam2.stop_encoder()


picam2.stop()
