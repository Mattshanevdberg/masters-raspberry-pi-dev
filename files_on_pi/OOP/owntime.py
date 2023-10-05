import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = None

    def start_timer(self):
        self.start_time = time.time()
        print(time.time())

    def check_elapsed_time(self):
        '''checks the elapsed time since the start timer function was called
            returns: elapsed time'''
        self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time    

    def sleep(self, interval):
        time.sleep(interval)
    
    def get_date_time(self):
        return time.strftime('%Y-%m-%d_%H-%M')