"""
Main App that starts all the threads and variables needed for live analysis of F1 sessions
By Graham H. and Matthew R.
"""


from threading import Thread        # Base Python for threading
import json                         # Base Python for working with json objects
import time                         # Base Python used to slow down threads
from data_gathering import session  # Custom package for getting data from F1's Livetiming API
import global_variables             # Custom package for dealing with global variables
import utils                        # Custom package
import requests                     # pip install requests

def global_print():
    """
    prints global variables in its own thread.  Mostly used for testing purposes.
    :return:
    """
    while True:
        print(global_variables.CURRENT_RACE_DATA)
        time.sleep(1)


def main(race_path):
    global_variables.reset_global_variables()
    feeds = get_jsonstreams(race_path)
    threads: list[Thread] = []
    thread_targets = [{'target': session, 'args': (feeds, True,)}]#,{'target': global_print, 'args': ()}

    for thread_target in thread_targets:
        thread = Thread(target=thread_target['target'], args=thread_target['args'])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def get_jsonstreams(race_path):
    feeds = []
    race_scheme = 'https'
    race_netloc = 'livetiming.formula1.com'
    race_path = f'static/{race_path}Index.json'
    race_url = utils.create_url(race_scheme, race_netloc, race_path)
    response = requests.get(race_url)
    stream_data = json.loads(response.content)
    for feed in stream_data['Feeds']:
        feeds.append(feed)
    return feeds


if __name__ == "__main__":
    """
    This section is intended to be run whenever the session finder finds a session.
    It then figures out the API endpoint paths for the session and starts the application with that path.
    [This could probabaly be explained better in the future]
    """
    race_path = '2024/2024-11-23_Las_Vegas_Grand_Prix/2024-11-23_Race/'     # race path for testing purposes
    main(race_path)