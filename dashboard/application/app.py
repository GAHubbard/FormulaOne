"""
Main App that starts all the threads and variables needed for live analysis of F1 sessions
By Graham H. and Matthew R.
"""


from threading import Thread        # Base Python for threading
import json                         # Base Python for working with json objects
import time                         # Base Python used to slow down threads
import data_gathering  # Custom package for getting data from F1's Livetiming API
import global_variables             # Custom package for dealing with global variables
import utils                        # Custom package
import requests                     # pip install requests
import data_processing
import display

def global_print():
    """
    prints global variables in its own thread.  Mostly used for testing purposes.
    :return:
    """
    while True:
        print(global_variables.TOP_THREE)
        if global_variables.TOP_THREE is not None and 'Lines' in global_variables.TOP_THREE:
            order = 1
            while order < 4:
                print(global_variables.TOP_THREE['Lines'][order-1]['BroadcastName'])

                time.sleep(10)
                order += 1


        time.sleep(1)


def main(session_path: str) -> None:
    """
    App begins running once a F1 session starts (really its about 15 minutes prior)
    This sets up some things and starts the apps threads
    :param session_path: API endpoint for session
    :return:
    """

    # grab various JSON streams for session
    feeds: list[str] | None = get_jsonstreams(session_path)

    # initialize the various Threads for each feed
    threads: list[Thread] = []

    # create the threads definitions (target and args)
    # each key in this dictionary is a function meant to be a thread and its value is the arguments as a tuple
    # the key also needs to be the object that represents the function not a string
    thread_targets_and_args = {data_gathering.session: (feeds, True,),
                               data_processing.print_driver_list: (),
                               display.display_rows: ()}

    # loop through and start each thread
    for key, value in thread_targets_and_args.items():
        thread = Thread(target=key, args=value)
        thread.start()
        threads.append(thread)

    # join each thread back to the main thread when they finish
    for thread in threads:
        thread.join()


def get_jsonstreams(session_path: str) -> list[str] | None:
    """
    Returns list of streams based on the session path.
    :param session_path: API endpoint for the session
    :return: List of streams for the current session
    """

    feeds: list[str] = []  # streams to return

    # url for streams
    # it's kind of weird because we just use a recent session path instead of the live or upcoming because
    # the upcoming path isn't available
    race_feed_url = f"https://livetiming.formula1.com/static/{session_path}Index.json"

    # Get response that returns JSON API end points
    response = requests.get(race_feed_url)
    if response.status_code == 200:
        stream_data: dict = json.loads(response.content)

        # Loop through the streaming data feeds and find the .json paths
        for feed in stream_data['Feeds']:
            feeds.append(feed)
    else:
        feeds = None

    return feeds  # return the list of .json paths such as []

def new_main(cli_flag = True) -> None:
    """
    New main function that does old main but a little better now that we have learned how to get data from F1 better
    :return:
    """

    # initialize the various Threads
    threads: list[Thread] = []

    # if in CLI mode
    if cli_flag:

        # ask user if they want to download raw data (debug mode) or just enter normal mode
        normal_true_or_debug_false: bool = display.debug_or_normal_mode()

        # normal mode
        if normal_true_or_debug_false:
            # create the threads definitions (target and args)
            # each key in this dictionary is a function meant to be a thread and its value is the arguments as a tuple
            # the key also needs to be the object that represents the function not a string
            thread_targets_and_args = {data_gathering.session_new: (),
                                       display.display_rows: ()}

            # loop through and start each thread
            for key, value in thread_targets_and_args.items():
                thread = Thread(target=key, args=value)
                thread.start()
                threads.append(thread)

            # join each thread back to the main thread when they finish
            for thread in threads:
                thread.join()

        else:  # debug mode
            pass
    else:
        # non CLI mode
        # prior behavior and probably website stuff
        pass


if __name__ == "__main__":
    """
    This section is intended to be run whenever the session finder finds a session.
    It then figures out the API endpoint paths for the session and starts the application with that path.
    [This could probably be explained better in the future]
    [Or maybe we implement this differently]
    """
    # testing out new main function that fixes a lot of the stuff we did wrong before
    new_main()  # You can put cli_flag = False as an arugment and you will get the non CLI behavior
    # end of test
    #session_path_test = '2025/2025-04-20_Saudi_Arabian_Grand_Prix/2025-04-19_Practice_3/'     # race path for testing purposes
    #main(session_path_test)