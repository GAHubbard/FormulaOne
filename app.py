"""
I don't know, I guess some stuff goes here
"""

from connections import WebSockets
from datetime import datetime
import json
from threading import Thread
from contextlib import closing


def data_handler():
    output_file = open(f'output-{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.txt', 'a')
    session = WebSockets()
    with closing(session.connection()) as conn:
        session.send_data(conn)
        previous_heartbeat = None
        new_data = True
        while new_data:
            data = session.receive_data(conn)
            data_decoded = json.loads(data)
            if 'R' in data_decoded:
                current_heartbeat = data_decoded['R']['Heartbeat']['Utc']
                if current_heartbeat != previous_heartbeat:
                    count = 0
                    previous_heartbeat = current_heartbeat
                    output_file.write(data + '\n')
                else:
                    count += 1
                new_data = False if count >= 100 else session.send_data(conn)


def main():
    data_handler_thread = Thread(target=data_handler())
    data_handler_thread.start()


if __name__ == "__main__":
    main()