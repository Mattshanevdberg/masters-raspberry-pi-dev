# Raspberry Pi Based Remote Video Monitoring Device
The following is a step by step guide to setting up a remote video monitoring device. 
This github contains the software code that is run on the device
Please see paper: 'OPEN Monitor: An Open Source Wildlife Monitoring Systems for Africa' for further information on application

## Functionality Overview: ##
- Automatic remote video and image monitoring system
- Automatic video recording on start up
- Uploading captured data to a google drive over predetermined time periods over a wifi connection
- Basic functionality and remote control over Telegram (allows control of multiple cameras over a single channel)
### Simple overview of the basic functionality of the camera system: ###
![picture_software_overview_4_github](https://github.com/Mattshanevdberg/masters-raspberry-pi-dev/assets/110899554/22655c25-6320-4824-8360-2ad0ed95a18c)

The following is a list of telegram commands that can be sent via Telegram for device remote control:
| Command | Functionality |
| --- | --- |
| all: OR device_name: | When sending commands over the telegram channel, you can send a command directly to a specific device or have that command applied to all devices on the channel. Each message sent must have 'all:' or 'device name:' before the desired command |
| video | Continuously captures videos and saves them to the device |
| image | Continuously captures images and saves them to the device |
| sleep | Puts the device to sleep. Checks for new messages every 60 seconds. Used for conserving power |
| maintenance | Similar to sleep mode. Puts the code on hold so that changes, upgrades or bug fixes can be implemented |
| upload | Systematically uploads all recordings that have been saved to the device to a Google drive and deletes the files from the device once upload is complete. Uploads are done in batches of 20 |
| ping | Pings the device to check connectivity. Device responds with 'PING' every 5 seconds |
| reboot | Reboots device |
| refresh_token | A refresh token for the Google drive API is saved on the device. If this is deleted for any reason. This command will retrieve a new token |
| video_frame_rate | Sets the frame rate that videos are taken at |
| image_frame_rate | sets the rate images are taken at |

An example image of Telegram communication:
![Example_of_Telegram_comms](https://github.com/Mattshanevdberg/masters-raspberry-pi-dev/assets/110899554/e4a38684-bc52-4aa8-92b4-2f09395bbb6e)

## Hardware Requirements ##
- 

