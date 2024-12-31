"""
Needs a better file name. Don't know what this does yet
Created by: Graham Hubbard
Date: 2024-12-30
"""

from datetime import datetime
from utils import *

class F1:

    def __init__(self):
        self.year = datetime.now().strftime('%Y')
        self.month = datetime.now().strftime('%m')
        self.day = datetime.now().strftime('%d')
        self.hour = datetime.now().strftime('%H')
        self.minute = datetime.now().strftime('%M')
        self.seconds = datetime.now().strftime('%S')
        pass

    def get_schedule(self):
        #make httpos reques to get shcdule and find which reace is currently running
        pass

    def session(self):
        #do what data handler does?
        pass

    def get_car_telemetry_data(self):
        pass

    def get_car_position_data(self):
        pass

    def output_to_file(self):
        pass