import socket
# own imports
from telegram import TelegramBot
from owntime import Timer

### GLOBALS ###
#dont actually need the IP address..
class Maintenance:
    def __init__(self, device_name):

        self.device_name = device_name
        self.timer = Timer()
        self.tele_bot_cam = TelegramBot(self.device_name)
    
    def get_ip_address(self):
        '''returns the current IP address'''
        try: 
            # Create a socket and connect to Google's DNS server
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)  # Timeout in seconds
            sock.connect(("8.8.8.8", 80))

            # Get the local IP address from the socket
            ip_address = sock.getsockname()[0]
            return ip_address
        except Exception as e:
        # print error to file
            e = str(e)
            function_name = 'DriveAuth.retrieve_refresh_token:'
            self.telegram_bot.send_telegram(f"{function_name}: {e}")          
            return 'issue with function could not get the ip address'  

maintenance = Maintenance('USER_NAME')
ip_address = maintenance.get_ip_address()
print(ip_address)