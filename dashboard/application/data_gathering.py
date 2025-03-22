"""
Needs a better file name. Don't know what this does yet
Created by: Graham Hubbard
Date: 2024-12-30
"""


from datetime import datetime           # base python
from f1websocket import F1WebSocket     # custom file
from contextlib import closing          # base python
from dateutil import parser             # pip install python-dateutil
import json                             # base python
import global_variables                 # custom file
import time


def session(feeds: list[str] | None, output_to_file: bool = False):
    """
    Gets data from F1's Live Timing API endpoint and saves it to a file.
    and updates a global variable. A lot of what is going on here right now is for testing but this will
    be getting the data in the final product.
    :param feeds: list of feeds names to get data from these are the arguments we pass to the server function named
    Subscribe.  This function then returns us messages giving us data for every argument we pass.
    Logically these are the list of feeds we want data on.
    :param output_to_file: If true, save the data to file, if false, then don't.
    :return:
    """
    # output file saved in YYYY-MM-DD HH-MM-SS.txt in append mode
    if output_to_file:
        output_file = open(f'output-{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.txt', 'a', encoding='utf-8')
        raw_output_file = open(f'raw_output-{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.txt', 'a', encoding='utf-8')
    
    websocket = F1WebSocket(feeds)  # create custom web socket

    # Ensure websocket closes in case of errors
    start_time = time.time()
    with closing(websocket.connection()) as conn:

        conn.send(websocket.invoke_data)     # Send message to SignalR endpoint to request specific data

        previous_heartbeat = None       # Previous Heartbeat timestamp
        session_status = True
        
        # data handler loop
        while session_status:
            data = json.loads(conn.recv())  # receive data back from the server and convert to a dictionary
            time_split = time.time() - start_time
            raw_output_file.write(str({time_split: data}) + '\n')
            if 'M' in data and len(data['M']) > 0:
                if output_to_file:
                    output_file.write(str(data) + '\n')
                for feed in data['M']:
                    feed_name = feed['A'][0]
                    feed_data = feed['A'][1]
                    feed_timestamp = feed['A'][2]
                    pass_data_to_global_variable(feed_name, feed_data, feed_timestamp)
                    session_status = is_end_of_session(feed_name, feed_data)

def pass_data_to_global_variable(feed: str, data: str, timestamp: str):
    pass

def is_end_of_session(feed: str, data: str) -> bool:
    return False if (feed == 'SessionStatus' )and ('Status' in data) and (data['Status'] == 'Finalised' or 'Ends') else True
    