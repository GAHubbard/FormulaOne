"""
I don't know, I guess some stuff goes here
"""


from threading import Thread
from data_gathering import session
import global_variables             # Custom package for dealing with global variables
import time
import utils
import requests
import json

def global_print():
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
    race_path = '2024/2024-11-23_Las_Vegas_Grand_Prix/2024-11-23_Race/'
    main(race_path)