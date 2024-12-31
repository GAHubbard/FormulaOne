"""
I don't know, I guess some stuff goes here
"""

from f1websocket import F1WebSocket     # Custom F1 WebSocket Package
from datetime import datetime           # Base
from threading import Thread            # Base
from contextlib import closing          # Base
from dateutil import parser             # pip install python-dateutil
import json                             # Base

def data_handler():
    """
    Gets data from F1's Live Timing API endpoint and saves it to a file.
    :return:
    """

    # output file saved in YYYY-MM-DD HH-MM-SS.txt in append mode
    output_file = open(f'output-{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.txt', 'a', encoding='utf-8')

    session = F1WebSocket()  # create custom web socket

    # Ensure websocket closes in case of errors
    with closing(session.connection()) as conn:

        conn.send(session.invoke_data)     # Send message to SignalR endpoint to request specific data

        stale_data_count = 0            # Stale data count set to 0
        previous_heartbeat = None       # Previous Heartbeat timestamp
        data_handler_loop: bool = True  # Loop control boolean

        # data handler loop
        while data_handler_loop:

            data = json.loads(conn.recv())  # receive data back from the server and convert to a dictionary

            if 'R' in data:  # If the message received from the server actually has race data in  it

                current_heartbeat = parser.parse(data['R']['Heartbeat']['Utc'])  # Convert heartbeat to datetime obj

                # if previous heartbeat datetime has not been set or earlier in time to the current heart beat
                if previous_heartbeat is None or current_heartbeat > previous_heartbeat:
                    stale_data_count = 0                    # reset the stale data counter to 0
                    previous_heartbeat = current_heartbeat  # update the previous heartbeat datetime
                    output_file.write(str(data) + '\n')     # output the new data (not stale) to the file
                else:
                    stale_data_count += 1                   # add the stale data counter up

                # set the loop boolean to False if the stale data counter gets to 100 or ask the server for more data
                data_handler_loop = False if stale_data_count >= 100 else conn.send(session.invoke_data)


def main():
    data_handler_thread = Thread(target=data_handler())
    data_handler_thread.start()
    data_handler_thread.join()


if __name__ == "__main__":
    main()