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


def main(session_path: str) -> None:
    """
    App begins running once a F1 session starts (really its about 15 minutes prior)
    :param session_path: API endpoint for session
    :return:
    """

    # grab various JSON streams for session
    feeds = get_jsonstreams(session_path)

    threads: list[Thread] = []

    thread_targets = [{'target': session, 'args': (feeds, True,)}] #,{'target': global_print, 'args': ()}

    for thread_target in thread_targets:
        thread = Thread(target=thread_target['target'], args=thread_target['args'])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def get_jsonstreams(session_path: str) -> list[str]:
    """
    Returns list of JSON streams based on the session path.
    :param session_path: API endpoint for the session
    :return: List of JSON streams for the current session
    """

    feeds = []  # JSON streams to return
    race_scheme = 'https'
    race_netloc = 'livetiming.formula1.com'
    full_path = f'static/{session_path}Index.json'  # insert session_path into url

    race_url = utils.create_url(race_scheme, race_netloc, full_path)
    response = requests.get(race_url)

    stream_data = json.loads(response.content)

    for feed in stream_data['Feeds']:
        feeds.append(feed)
    return feeds


if __name__ == "__main__":
    """
    This section is intended to be run whenever the session finder finds a session.
    It then figures out the API endpoint paths for the session and starts the application with that path.
    [This could probably be explained better in the future]
    """
    session_path_test = '2024/2024-11-23_Las_Vegas_Grand_Prix/2024-11-23_Race/'     # race path for testing purposes
    main(session_path_test)