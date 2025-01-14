import logging

from datetime import datetime

class Timer:
    def __init__(self):
        self.startTime = 0
        self.endTime = 0
        pass

    def start(self, message = ""):
        """Start the timer. Can also log messages"""
        if message != "":
            logging.info(message)
        self.startTime = datetime.now()
    
    def stop(self, message = ""):
        """End the timer. Can also log messages"""
        if message != "":
            logging.info(message)
        self.endTime = datetime.now()

    def get_elapsed_time(self, message = ""):
        """Return elapsed time in seconds. Log messages and the time will replace %m"""
        if message != "":
            logging.info(message.replace("%m", str((self.endTime - self.startTime).seconds)))
        return (self.endTime - self.startTime).seconds