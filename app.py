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

        session.send_data(conn)     # Send message to SignalR endpoint to request specific data

        stale_data_count = 0            # Stale data count set to 0
        previous_heartbeat = None       # Previous Heartbeat timestamp
        data_handler_loop: bool = True  # Loop control boolean

        # data handler loop
        while data_handler_loop:

            data = json.loads(conn.recv())
            if 'R' in data:
                current_heartbeat = parser.parse(data['R']['Heartbeat']['Utc'])
                if previous_heartbeat is None or current_heartbeat > previous_heartbeat:
                    stale_data_count = 0
                    previous_heartbeat = current_heartbeat
                    output_file.write(str(data) + '\n')
                else:
                    stale_data_count += 1
                stale_data = True if stale_data_count >= 100 else session.send_data(conn)


def main():
    data_handler_thread = Thread(target=data_handler())
    data_handler_thread.start()


if __name__ == "__main__":
    main()