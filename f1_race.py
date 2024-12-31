"""
Needs a better file name. Don't know what this does yet
Created by: Graham Hubbard
Date: 2024-12-30
"""


from datetime import datetime
import utils
import requests
from requests import Response


class F1:

    def __init__(self):
        self.year = datetime.now().strftime('%Y')
        self.month = datetime.now().strftime('%m')
        self.day = datetime.now().strftime('%d')
        self.hour = datetime.now().strftime('%H')
        self.minute = datetime.now().strftime('%M')
        self.seconds = datetime.now().strftime('%S')
        self.netloc = 'livetiming.formula1.com'
        pass

    def get_schedule(self) -> Response:
        schedule_scheme = 'https'
        schedule_netloc = self.netloc
        schedule_path = f'/static/{self.year}/Index.json'
        schedule_url = utils.create_url(scheme=schedule_scheme, netloc=schedule_netloc, path=schedule_path)
        response = requests.get(schedule_url)
        return response

    def session(self):
        #do what data handler does?
        pass

    def get_car_telemetry_data(self):
        pass

    def get_car_position_data(self):
        pass

    def output_to_file(self):
        pass