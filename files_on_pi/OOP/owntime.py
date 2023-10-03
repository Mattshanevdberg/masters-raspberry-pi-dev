import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = None

    def start_timer(self):
        self.start_time = time.time()
        print(time.time())
        return self.start_time

    def check_elapsed_time(self):
        self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time    

    def sleep(self, interval):
        time.sleep(interval)