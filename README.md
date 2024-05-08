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

To change the password if you have forgetten your password you can use the command: `sudo passwd username`

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
This is an optional step. But at this stage you might find you are tired of switching between plugging you mouse in, then your keyboard or retyping commands rather than copy and pasting them. To solve this you can access the Pi terminal from your PC (provided the PC and Pi are on the same wifi connection). This must be done through the GUI for adjusting Pi configurations (it can also be done through adjust additional configuration files, that method can be found in the headless set up video tutorial).

1. Determine Raspberry Pi's IP Address:
   - Run the following command: `hostname -I`
   - Note down the IP address; you'll need it to connect via SSH.
2. Enable SSH (if not already):
   - If SSH is not enabled on your Raspberry Pi, you'll need to enable it with the configuration GUI which is accessed by running the following command: `sudo raspi-config`
   - In the GUI navigate to Interfacing Options > SSH and select "Yes" to enable SSH.
3. Connect via SSH:
   - On your PC (which should be on the same network as your Raspberry Pi), open a terminal or command prompt.
   - To connect via SSH, use the following command, replacing pi with your user_name (if you haven't changed it, it will be 'pi') and  your_pi_ip with the IP address you noted down earlier: `ssh pi@your_pi_ip`
   - You might be prompted with a message about the authenticity of the host; type "yes" to continue.
   - Enter the default password when prompted (the default password is 'raspberry' unless you've changed it) OR enter your pi password if you have set one (note that when entering your password, it will not show up on the screen)


### 7. Installing the necessary packages on the Pi ###
The Pi OS does not have all the packages we need to run the code in this repository, so we will need to install that
1. Install python3, pydrive, telepot, google-api-python-client and psutli packages by running the following commands in the terminal:
   - `sudo apt update`
   - `sudo apt install python3=3.9.2-3`
   - `pip install telepot==12.7`
   - `pip install google-api-python-client==2.125.0`
   - `pip install psutil==5.8.0`
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
3. Now you must test your Bot:
   1. Open the terminal on you Pi and enter the python interpreter with the following command: `python3`
   2. Enter the following commands:
      - `import telepot`
      - `bot = telepot.Bot('*copy your bot token from earlier*')`
      - `bot.getMe()`
   3. If this returns your bot account info, then it is working as expected
   4. You must now go on telegram on your smart phone and send the bot a message
   5. Now you will need to get the send address of you mobile device chat to send messages from your raspberry pi (this is a global variable that will need to be put into the code on your pi). Do so by entering the following commands:
     - `bot.getUpdates(limit=1, offset=-1)`
     - This retrieves the infomation of the last message sent to the bot
     - In the returned dictionary, you will see the following entries under 'chat' : { 'id' : 123456789 , …
     - copy that id and save it. That is your send address and will be input into the script as a global variable

### 9. Creating a API token to allow the device to upload automatically to a folder in you drive ###
This step is where you might run into the most problems due to various permission issues and firewalls. If you are using a company account, or an account that is linked to some institution where you are not in control of the permissions and firewalls, and you run into any issues, my first suggestions is to create a new person google account and attempt using that. Alternatively, talk to your IT department. 

The following documentation on Google API's will come in handy if you run into any troubles or you want further understanding (Specifically look under the heading 'Access to Google APIs: for TV & Device Apps' as this is the type of access that was used):

https://developers.google.com/identity/protocols/oauth2

We use the google-api-python-client to access the drive. The github respository for this package can be found here:

https://github.com/googleapis/google-api-python-client 

Now for the simple overview instructions:

1. You must first navigate to the Google Developer Console by following this link: https://console.developers.google.com/
2. Then you must select create new project (this should be a button in the top right corner)
3. Give you project a name and leave location as 'No organisation' and create project
4. select  '+ Enable APIs and services'
5. This will take you to the API library
6. Search for Google Drive in the search bar and select Google Drive API
7. Then select Enable
8. Now in the navigation panel on the left of the screen you can navigate to the OAuth consent screen
9. Select the Configure Consent Screen button 
10. Select the External option and create
11. Fill in only the required fields on the proceeding page (you can use any name and supply your own email address). Leave the rest blank.
12. You will then go to the Scopes section. Here you must only select the relevant scopes. For the 'Limited input device' authentification (which is what we will be using) all scopes must be non-sensitive. Select 'Add or remove scopes' and only select the Google Drive API: /auth/drive.file. It must be the .file scope. And you will see it under the non-sensitive scopes section. Save and continue.
13. For the test users, you must add the email address associated with the drives that you wish to access. Save and continue.
14. Select back to dashboard
15. Now in the navigation panel on the left of the screen you can navigate to the Credentials tab
16. Click create credentials and the OAuth client ID (these will be used to access your drive)
17. In the Application type drop down, select 'TVs and Limited Input devices' and Name the device whatever you see fit. (we use the TVs and Limited Input devices so you can use another device to verify your account, such as a cellphone or laptop. The Pi sometimes times out when trying to verification and can be very frustrating…
18. You will have a pop up with your client ID and client secret. You must save these as these are gobal variable that will need to be input into your code. You can view the ID and secret again by selecting the specified credential at a later stage

### 10. Set up VNC to remote into the device from anywhere ###
It is a good idea to have VNC viewer installed on your PC and VNC server installed on your pi. This will allow you to access the GUI of the pi, even when not on the same wifi connection. The following steps are for setting up VNC on your PC and on the pi. Note that the instructions for the PC are for a Linux operating system: 

1. install RealVNC Viewer on your laptop: https://linuxconfig.org/how-to-install-realvnc-viewer-on-linux
2. Install RealVNC Server on the Pi, check out the first few steps here:

https://help.realvnc.com/hc/en-us/articles/360002249917-VNC-Connect-and-Raspberry-Pi#setting-up-your-raspberry-pi-0-0

3. Then scroll down in that same article to the 'Establishing a cloud connection' section and follow those instructions. You should end up with email credentials and a password that you can use to connect to your device.

### 11. Set up a wifi configuration for the pi to automatically connect to a specific wifi ###
You may want to deploy your pi somewhere where there is a wifi connection but you do not have a monitor available to select the correct wifi connection. In this case you would like to set up the pi to connect to a specific wifi connection automatically. You can also set up multiple network connections and create a priority connection list (i.e. try connect to wifi1 first and if that's not available, then try connect to wifi2).

The instructions presented here are from the following post (scroll down to 'Set up your Wi-Fi on Raspberry Pi OS Lite' and navigate to the subheading 'Raspberry Pi OS Bullseye and previous versions'): 

https://raspberrytips.com/raspberry-pi-wifi-setup/ 

further information on the wpa_supplicant.conf

https://w1.fi/cgit/hostap/plain/wpa_supplicant/wpa_supplicant.conf 

We will be either creating or adjusting the wpa_supplicant.conf file. This contains info about the network connections.

1. navigate to the wpa_supplicant.conf file `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
2. By default the file will be almost empty (unless you have already connected to a wifi connection, then you will see the information for that connection in this file)
3. If there is not already a line in the file stating `country=some_country` then you must add a line stating `country=US`. I do not live in the US but that is what is added automatically when you connect to a wifi connection through the UI and it has worked for me. You can change this to your country if US does not work.
4. Then you will need to add the network you want to connect to automatically by adding the following code:

```
network={
 ssid="YOURSSID"
 psk="YOURPASSWORD"
}
```

5. If you would like to add a priority as mentioned above, you can the following line within the network {}: `priority=some_number` where the higher the number, the higher the priority (and the highest priority will connect first).

Note: When connecting to a phone hotspot the phone hotspot it must be set to 2.4Ghz and not 5G and the Security set to WPA2-Personal or give no password for the hotspot.

### 12. Copying the scripts to Desktop and inputting/adjusting the Global variables ###
I have designed the system so that everything is run from and saved to the desktop. For this to work you must first copy all the scripts from the repository that you cloned to the desktop in step 5 (these are the .py files inside the Desktop/masters-raspberry-pi-dev/files_on_pi/OOP directory) onto the desktop. 

Next you will need to update the global variables within these files to align with your own credentials.  
Update the Global variables in the main.py, drive.py and telegram.py (use `sudo nano script_name.py` )
1. main.py
   - USER_NAME = 'your-pi-user-name'
   - You can also change the sleep and upload times in this file
2. drive.py
   - CLIENT_ID = 'your-client-id'
   - CLIENT_SECRET = 'your-client-secret'
   - Client id and secret were found in the step 9
   - DESTINATION_FOLDER_ID = 'the-last-bit-of-the-url-for-the-drive-folder-you-want-to-upload-to'
   - destination folder id is the id of the folder in your google drive that you want to save the files to. To find the id of the your destination folder, first navigate to the desired folder in you google drive, then copy the part of the url after the last /. So if your url is: "https://drive.google.com/drive/u/1/folders/1TcHJojfyXrKM75Rjsns8US773gcALbt5j", then your folder id is: "1TcHJojfyXrKM75Rjsns8US773gcALbt5j"
3. telegram.py
   - TELE_TOKEN = 'your bot token'
   - TELE_SEND_ADDRESS = 'your send address'
   - For telegram token and send address see step 8
4. camera.py
   - VID_RESOLUTION_INPUT = 'chosen resolution category' #see script for details
   - VID_FRAME_RATE = 'chosen frame rate'
   - VID_SEC_LENGTH_OF_VIDEO = 'chosen length of each video
   - IMG_SEC_BURST_LENGTH = 'chosen length of image burst in seconds'
   - IMG_NUM_PER_BURST = 'number of pictures to take per burst'
   - IMG_RESOLUTION = VID_RESOLUTION_OPTIONS.get(VID_RESOLUTION_INPUT) #this will default to make the image resolution equal to that of the chosen video resolution. You can adjust this to a tuple with the desired resolution. maximum possible resolution is `(4608, 2592)` and is an example of how to input a tuple.
   - IMG_BUFFER_COUNT = 1 #leave this as 1 unless you need to take more than an image a second. See script for details.

Now the scripts have you credentials and are ready to be run. I would advise testing them at this point by using `sudo -E python3 main.py` from the desktop in the terminal. The sudo -E part of the command is because you need to have sudo priviledges in order to change or update system clock (which the script does on start up).

### 13. Set up the Pi to lauch the main.py script on start up ###
Once you have tested the script runs smoothly, you now need to set the pi up so that the script is run automatically when the pi starts up. To do this we use the @reboot command in the crontab (the crontab is a Linux command that allows you to schedule tasks to run at specific times):

1. in your terminal run the command `crontab -e` this opens the crontab for editting
2. scroll to the bottom and add the following three lines:
  - `@reboot v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0`
  - `@reboot sudo -E python3 /home/your_pi_username/Desktop/main.py`
  - `0 0 * * * sudo reboot`

*@reboot runs the proceeding command on start up
*The first command is to enable the HDR setting for the camera. This helps with contrast and making the picture quality better. Its not strictly necessary.
*The second command runs the python script that you are pointing to. The part after python3 is just the path to your python script you want to run on startup (in this case it will be the main.py)
*sudo runs the script with admin privileges. This is required in order to set the system clock to the current time. The -E preserves the current environment that the script is running in (so you don't need to install modules/dependencies globally in order to access them when running as an admin). 
*The third line reboots the pi at midnight everynight. This is incase the python script is killed for some reason and you are unable to reboot it remotely. If you would like it to happen weekly `0 0 * * 0` 
*For further information on crontab commands, check out this article: https://www.jcchouinard.com/python-automation-with-cron-on-mac/

Lekka! You are good to go! Good luck and happy recording!


