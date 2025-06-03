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
import display                          # custom file


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
        session_status = True
        
        # data handler loop
        while session_status:
            data = json.loads(conn.recv())  # receive data back from the server and convert to a dictionary
            if 'M' in data:
                for feed in data['M']:
                    feed_name = feed['A'][0]
                    feed_data = feed['A'][1]
                    feed_timestamp = feed['A'][2]
                    pass_data_to_global_variable(feed_name, feed_data, feed_timestamp)
                    session_status = False if (feed == 'SessionStatus') and ('Status' in data) and (data['Status'] in ['Finalised', 'Ends']) else True
                if output_to_file:
                        output_file.write(str(data) + '\n')
            time_split = time.time() - start_time
            raw_output_file.write(str({time_split: data}) + '\n')  # returns as much as possible

            if 'R' in data:
                if not global_variables.driver_tracker_bool_initalized:
                    global_variables.driver_tracker_bool_initalized = True
                    initial_time_stamp_str: str = data['R']['ExtrapolatedClock']['Utc']
                    initial_time_stamp = datetime.fromisoformat(initial_time_stamp_str.replace('Z', '+00:00'))
                    global_variables.driver_tracker.append(data['R']['DriverTracker'])
                    global_variables.driver_tracker.append(initial_time_stamp)
                if not global_variables.track_status_bool_initalized:
                    global_variables.track_status_bool_initalized = True
                    initial_time_stamp_str: str = data['R']['ExtrapolatedClock']['Utc']
                    initial_time_stamp = datetime.fromisoformat(initial_time_stamp_str.replace('Z', '+00:00'))
                    global_variables.track_status.append(data['R']['TrackStatus']['Message'])
                    global_variables.track_status.append(initial_time_stamp)

            if 'M' in data:
                # see whats in M and update accoringly
                # data['M'} will be a list of elements
                for update in data['M']:
                    update_info = update['A'] # this is silly but whatever
                    # now we check for different feeds here
                    feed_name: str = update_info[0]
                    feed_data: dict = update_info[1]
                    feed_timestamp = update_info[2]
                    feed_timestamp_dt: datetime = datetime.fromisoformat(feed_timestamp.replace('Z', '+00:00'))

                    # update just the DriverTracker Output
                    if feed_name == 'DriverTracker':
                        # timestamp update
                        global_variables.driver_tracker[1] = feed_timestamp_dt

                        # make a local copy of R DriverTracker
                        local_copy_driver_tracker: dict = global_variables.driver_tracker[0]
                        # get the keys in M message / feed_data
                        for key, value in feed_data.items():
                            if isinstance(value, dict):
                                for key_1, value_1 in feed_data[key].items():
                                    for key_2, value_2 in feed_data[key][key_1].items():
                                        local_copy_driver_tracker[key][int(key_1)][key_2] = value_2
                            else:
                                local_copy_driver_tracker[key] = value
                    if feed_name == 'TrackStatus':
                        global_variables.track_status[1]: datetime = feed_timestamp_dt
                        global_variables.track_status[0] = feed_data['Message']

def session_new():
    # create custom web socket
    # it will still create the correct websocket with None as an argument
    websocket = F1WebSocket(None)

    # ensure proper closing of websocket
    with closing(websocket.connection()) as conn:
        # Send message to SignalR endpoint to request specific data
        conn.send(websocket.invoke_data)

        # data gathering loop runs when global session_status is True
        while global_variables.session_status:

            # recieve data
            data = json.loads(conn.recv())

            # C messages (i have no idea what they do)
            if 'C' in data:
                handle_c_message(data)
            # R messages contain entire data set
            elif 'R' in data:
                handle_r_message(data)
            # M messages contain updates to portions
            elif 'M' in data:
                handle_m_message(data)


# r status flags
first_r = False
last_r_time: datetime = None
def handle_r_message(data):

    global last_r_time
    global first_r

    # first R on run behavior
    if not first_r:
        last_r_time = datetime.now()
        display.data_gathering_status_line = f"Downloaded Initial Dataset...R: {last_r_time.strftime('%Y-%m-%d %H-%M-%S')}"
        firt_r = True

    # other R during runs
    else:
        last_r_time = datetime.now()
        display.data_gathering_status_line = f"New R Message...R: {last_r_time.strftime('%Y-%m-%d %H-%M-%S')}"


def handle_m_message(data):

    display.data_gathering_status_line = f"New M Message...M: {data}"

def handle_c_message(data):

    display.data_gathering_status_line = f"New C Message...C: {data}"

def pass_data_to_global_variable(feed: str, data: str, timestamp: str):
    
    pass