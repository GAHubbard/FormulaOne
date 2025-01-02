"""
I don't know, I guess some stuff goes here
"""


from threading import Thread            # Base
from f1_race import F1
import f1_race
import time

def display_latest_message() -> None:
    """
    Probably a stump function intended to show how we can have multiple threads accessing the same variable
    :return:
    """
    while True:
        msg = f1_race.get_latest_message()
        print(msg)
        time.sleep(.1)

def main():
    race = F1()
    race.output_to_file = True

    # Create the thread objects and NO SHIT THE ONLY DIFFERENCE IS race.session INSTEAD of race.session()
    data_handler_thread = Thread(target=race.session)
    message_display_thread = Thread(target=display_latest_message)

    message_display_thread.start()
    data_handler_thread.start()

    data_handler_thread.join()
    message_display_thread.join()


if __name__ == "__main__":
    main()