
from ..Net import Net

class Timer:
    def __init__(self, time, start=True):
        self.duration = time
        self.elapsed = 0.0
        self.done = False
        self.running = False
        if start: self.start()

    def start(self):
        self.running = True
        self.done = False
        self.elapsed = 0.0

    def update(self):
        if not self.running: return 
        self.elapsed += Net.dt
        if self.elapsed >= self.duration:
            self.done = True
            self.running = False
            return True
