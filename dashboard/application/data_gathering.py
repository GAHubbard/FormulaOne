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


def session(feeds: list[str], output_to_file: bool = False):
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

    websocket = F1WebSocket(feeds)  # create custom web socket

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
                    global_variables.TOP_THREE = data['R']['TopThree'] # UPDATE THE GLOBAL VARIABLE WITH THE TOP 3 DATA
                    if output_to_file:
                        output_file.write(str(data) + '\n')     # output the new data (not stale) to the file
                else:
                    stale_data_count += 1                   # add the stale data counter up
                # set the loop boolean to False if the stale data counter gets to 100 or ask the server for more data
                if stale_data_count >= 100:
                    pass
                    #break
                else:
                    conn.send(websocket.invoke_data)
            elif 'M' in data and len(data['M']) > 0:
                if output_to_file:
                    output_file.write(str(data) + '\n')
                for feed in data['M']:
                     feed_name = feed['A'][0]
                     feed_data = feed['A'][1]
                     feed_timestamp = feed['A'][2]
                     pass_data_to_global_variable(feed_name, feed_data, feed_timestamp)
                     if feed_name == 'SessionStatus' and feed_data['Status'] == 'Finalised' or 'Ends':
                         break

def pass_data_to_global_variable(feed: str, data: str, timestamp: str):
    pass