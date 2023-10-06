import time
import datetime

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = None

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
        # Convert the integers to time objects
        start_hour, start_minute = divmod(start_time_int, 100)
        end_hour, end_minute = divmod(end_time_int, 100)
        start_time = datetime.time(start_hour, start_minute)
        end_time = datetime.time(end_hour, end_minute)

        # Get the current time
        current_time = datetime.datetime.now().time()

        # Check if the current time is within the time window
        return start_time <= current_time <= end_time