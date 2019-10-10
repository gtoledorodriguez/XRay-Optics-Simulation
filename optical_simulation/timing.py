from time import strftime
from time import time


class Timing():
    timings = []
    initial_time = 0;
    def __init__(self):
        self.timings = []
        self.initial_time = self.get_current_time()

    def get_current_time(self): # in ms
        return int(round(time() * 1000))

    def start_time(self):
        self.initial_time = self.get_current_time()

    def reset_time(self):
        self.timings = []
        self.start_time()

    def add_time(self, function_name):
        x = self.get_current_time()
        self.timings.append([function_name, strftime("%Y/%m/%d %H:%M:%S"), x])

    def get_timings(self):
        last_time = self.initial_time
        for i in range(len(self.timings)):
            temp = self.timings[i][2]
            self.timings[i][2] -= last_time
            last_time = temp
        return self.timings
