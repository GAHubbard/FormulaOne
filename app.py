"""
I don't know, I guess some stuff goes here
"""

from f1websocket import F1WebSocket
from datetime import datetime
import json
from threading import Thread
from contextlib import closing
from dateutil import parser

def data_handler():
    output_file = open(f'output-{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.txt', 'a')
    session = F1WebSocket()
    with closing(session.connection()) as conn:
        session.send_data(conn)
        stale_data_count = 0
        previous_heartbeat = None
        stale_data = False
        while not (stale_data == True):
            data = session.receive_data(conn)
            if 'R' in data:
                current_heartbeat = parser.parse(data['R']['Heartbeat']['Utc'])
                if previous_heartbeat == None or current_heartbeat > previous_heartbeat:
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