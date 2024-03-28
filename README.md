# Raspberry Pi Based Remote Video Monitoring Device
The following is a step by step guide to setting up a remote video monitoring device. 

This github contains the software code that is run on the device.

Please see paper: 'OPEN Monitor: An Open Source Wildlife Monitoring Systems for Africa' for further information on application

## Functionality overview: ##
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

## Minimum hardware requirements ##
- Raspberry Pi Zero 2 W
- Raspberry Pi Camera Module 3 (earlier camera modules will not work with the code provided)
- Pi5 cam csi cable 200mm
- MicroSD card
- Micro USB Power Supply
- Casing for Raspberry Pi

Suggested additional hardware:
- Micro USB to USB adapter
- Micro HDMI to HDMI adapter
- External keyboard and mouse
- Additional display monitor and HDMI connector

## Set up instructions ##
The following is a step by step set up instructions of the camera system.

*Note: these instructions assume you already have the Raspberry Pi OS on your SD card and have access to a display, external mouse and keypad that you can use; as well as some working knowledge of microelectronics and coding. If your SD does not have the OS on it already then please see this video to set that up (only the first four and a half minutes are required, unless you wish to do a headless set up. That is for advanced users though and is not supported in this documentation): 
https://www.youtube.com/watch?v=yn59qX-Td3E 

### 1. Hardware set up ###
Please see the following Youtube Video for setting up the camera module with the Raspberry Pi: 

https://www.youtube.com/watch?v=oo0A_yRrIxQ 

*Note: The Pi must not be powered up when connecting the camera to the device. This could cause permanent damage to the camera module.

### 2. Connecting the Pi for the first time ###
Make sure the display is connected and the Micro USB to USB adapter is connected before powering up the Pi.

*Note: if you are not working with a display, the set up could be tricky but is still possible. Please see the Youtube tutorial under Set up instructions for how to do a headless set up. This will cover SSH into your pi and connecting to wifi sections.

### 3. Changing the Pi user name and password ###
This step is not strictly neccessary but is probably a good idea.

By default your Raspberry Pi comes with an account 'pi' with the password 'raspberry'. You may want to change these to unique strings. The following article will explain how to do this: 

https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-change-the-default-account-username-and-password

### 4. Connecting the Pi to the internet ###
Once you have the Pi on and you can see the UI on your display you can connect to wifi through the wifi icon in the top right hand corner of the display screen. 

### 5. Cloning the Github repository onto the Pi ###
It is time to get this repository onto the Pi.

Please clone the repository onto the Desktop as this will make the proceeding steps easier. This is done through the terminal.

### 6. Update the Pi configurations for this project ###
It is possible to update the Pi configurations through the GUI. This is done by opening the command prompt and running the command `sudo raspi-config`. This will open a GUI for adjusting the Pi configurations.

However, for ease of set up I have provided a config.txt file in the reposistory that can be used. 

Copy the text from the config.txt file and run the following command `sudo nano /boot/config.txt`, then replace the text in that file with your copied text and save it. Alternatively you can remove the original config.txt file from the boot directory and replace it with the config.txt file in this repository.

### 7. SSH into your Pi ###
This is an optional step. But at this stage you might find you are tired of switching between plugging you mouse in, then your keyboard or retyping commands rather than copy and pasting them. To solve this you can access the Pi terminal from your PC (provided the PC and Pi are on the same wifi connection). 

### 7. Installing the necessary packages on the Pi ###
The Pi OS does not have all the packages we need to run the code in this repository, so we will need to install that
1. Install python3, pydrive, telepot, google-api-python-client and psutli packages by running the following commands in the terminal:
   - `sudo apt update`
   - `sudo apt install python3`
   - `pip install pydrive`
   - `pip install telepot`
   - `pip install google-api-python-client`
   - `pip install psutil`
2. Reboot your device by running the following command (for the installed packages and updates to take place):
   - `sudo reboot`
   
### 8. Setting up your Telegram bot for communicating with your Pi remotely ###
The instructions here are based off of the following tutorial, so please refer to this link if further explanation is required: 

https://www.instructables.com/Set-up-Telegram-Bot-on-Raspberry-Pi/

1. Install Telegram on your mobile smart phonen (done through the relevant app store)
2. Create a bot account for your Pi to use
   1. Search for a user called 'BotFather'
   2. text him '\newbot' and answer the questions. You can name the bot whatever you please, perhaps 'Pi_camera' or something fun... (I called mine 'Penguin_pi' because I was using the device to remotely monitor penguins)
   3. At the end of the process, you will be given a token, something like: 123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ. Save this, it is the token that your Pi will use when sending messages.
3. Now you must test your 

