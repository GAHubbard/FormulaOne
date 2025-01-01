"""
Needs a better file name. Don't know what this does yet
Created by: Graham Hubbard
Date: 2024-12-30
"""


from datetime import datetime
import utils
import requests
from requests import Response
from f1websocket import F1WebSocket
from contextlib import closing          # Base
from dateutil import parser             # pip install python-dateutil
import json                             # Base


class F1:

    def __init__(self):
        self.year = datetime.now().strftime('%Y')
        self.month = datetime.now().strftime('%m')
        self.day = datetime.now().strftime('%d')
        self.hour = datetime.now().strftime('%H')
        self.minute = datetime.now().strftime('%M')
        self.seconds = datetime.now().strftime('%S')
        self.netloc = 'livetiming.formula1.com'
        self.output_to_file = False
        pass

    def get_schedule(self) -> Response:
        schedule_scheme = 'https'
        schedule_netloc = self.netloc
        schedule_path = f'/static/{self.year}/Index.json'
        schedule_url = utils.create_url(scheme=schedule_scheme, netloc=schedule_netloc, path=schedule_path)
        response = requests.get(schedule_url)
        return response

    def session(self):
        """
        Gets data from F1's Live Timing API endpoint and saves it to a file.
        :return:
        """

        # output file saved in YYYY-MM-DD HH-MM-SS.txt in append mode
        if self.output_to_file:
            output_file = open(f'output-{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.txt', 'a', encoding='utf-8')

        websocket = F1WebSocket()  # create custom web socket

        # Ensure websocket closes in case of errors
        with closing(websocket.connection()) as conn:

            conn.send(websocket.invoke_data)     # Send message to SignalR endpoint to request specific data

            stale_data_count = 0            # Stale data count set to 0
            previous_heartbeat = None       # Previous Heartbeat timestamp

            # data handler loop
            while True:

                data = json.loads(conn.recv())  # receive data back from the server and convert to a dictionary

                if 'R' in data:  # If the message received from the server actually has race data in  it

                    current_heartbeat = parser.parse(data['R']['Heartbeat']['Utc'])  # Convert heartbeat to datetime obj

                    # if previous heartbeat datetime has not been set or earlier in time to the current heart beat
                    if previous_heartbeat is None or current_heartbeat > previous_heartbeat:
                        stale_data_count = 0                    # reset the stale data counter to 0
                        previous_heartbeat = current_heartbeat  # update the previous heartbeat datetime
                        if self.output_to_file:
                            output_file.write(str(data) + '\n')     # output the new data (not stale) to the file
                    else:
                        stale_data_count += 1                   # add the stale data counter up

                    # set the loop boolean to False if the stale data counter gets to 100 or ask the server for more data
                    if stale_data_count >= 100:
                        break
                    else:
                        conn.send(websocket.invoke_data)

    def get_car_telemetry_data(self):
        pass

    def get_car_position_data(self):
        pass