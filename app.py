"""
I don't know, I guess some stuff goes here
"""


from threading import Thread            # Base
from f1_race import F1


def main():
    race = F1()
    race.output_to_file = True
    data_handler_thread = Thread(target=race.session())
    data_handler_thread.start()
    data_handler_thread.join()


if __name__ == "__main__":
    main()