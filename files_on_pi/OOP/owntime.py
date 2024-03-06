import time
import datetime
import requests
import subprocess
from telegram import TelegramBot

class Timer:
    def __init__(self, user_name):
        self.start_time = None
        self.elapsed_time = None
        self.telegram_bot = TelegramBot(self.user_name)
        self.user_name = user_name

    def set_system_clock_from_web(self):
        '''Sets the system clock for the raspberry pi to the current date and time in GMT+2'''
        try:
            # Make a request to the worldtimeapi to get the current time in GMT+2
            response = requests.get('http://worldtimeapi.org/api/timezone/Africa/Johannesburg')
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            
            # Parse the response JSON and extract the datetime string
            datetime_str = response.json()['datetime']
            
            # Convert the datetime string to a datetime object
            datetime_obj = datetime.datetime.fromisoformat(datetime_str)
            
            # Format the datetime object for setting the system clock
            # The format for the 'date' command should be 'YYYY-MM-DD HH:MM:SS'
            formatted_datetime_for_command = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

            # Command to set the system date and time
            set_time_command = f'date -s "{formatted_datetime_for_command}"'
            
            # Execute the command
            subprocess.run(set_time_command, shell=True, check=True)
            
            return True
        
        except requests.exceptions.RequestException as e:
            # Handle any errors that occur during the request
            e = str(e)
            self.sleep(120)    
            function_name = 'Timer.set_system_clock_from_web (web error)'
            self.telegram_bot.send_telegram(function_name + e)
            print(e)
            return False
        
        except subprocess.CalledProcessError as e:
            # Handle any errors that occur during the subprocess
            e = str(e)
            self.sleep(120)    
            function_name = 'Timer.set_system_clock_from_web (system clock error)'
            self.telegram_bot.send_telegram(function_name + e)
            print(e)
            return False        

    def start_timer(self):
        #TESTED: 06-10-2023
        self.start_time = time.time()
        #print(time.time())

    def check_elapsed_time(self):
        #TESTED: 06-10-2023
        '''checks the elapsed time since the start timer function was called
            returns: elapsed time'''
        self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time    

    def sleep(self, interval):
        #TESTED: 06-10-2023
        time.sleep(interval)
    
    def get_date_time(self):
        return time.strftime('%Y-%m-%d_%H-%M')
    
    def is_current_time_in_window(self, start_time_int, end_time_int):
        #TESTED: 06-10-2023
        '''returns true if the current time is in window and false if not'''
        try:
            # Convert the integers to time objects
            start_hour, start_minute = divmod(start_time_int, 100)
            end_hour, end_minute = divmod(end_time_int, 100)
            start_time = datetime.time(start_hour, start_minute)
            end_time = datetime.time(end_hour, end_minute)

            # Get the current time
            current_time = datetime.datetime.now().time()

            # Check if the current time is within the time window
            return start_time <= current_time <= end_time
        
        except Exception as e:  
            e = str(e)
            self.sleep(120)    
            function_name = 'Timer.is_current_time_in_window'
            self.telegram_bot.send_telegram(function_name + e)
            return False
        
    def get_current_datetime_from_web(self):
        '''This function is currently not in use'''
        try:
            # Make a request to the worldtimeapi to get the current time in GMT+2
            response = requests.get('http://worldtimeapi.org/api/timezone/Africa/Johannesburg')
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            
            # Parse the response JSON and extract the datetime string
            datetime_str = response.json()['datetime']
            
            # Convert the datetime string to a datetime object
            datetime_obj = datetime.datetime.fromisoformat(datetime_str)
            
            # Format the datetime object as a string in the specified format
            formatted_datetime = datetime_obj.strftime('%Y-%m-%d_%H-%M')
            
            return formatted_datetime
        except requests.exceptions.RequestException as e:
            # Handle any errors that occur during the request
            
            e = str(e)
            self.sleep(120)    
            function_name = 'Timer.get_current_datetime_from_web'
            self.telegram_bot.send_telegram(function_name + e)
            print(e)
            return False
        
# Test 
#timer_ = Timer()
#print(timer_.set_system_clock_from_web())
#print(timer_.is_current_time_in_window(500,600))