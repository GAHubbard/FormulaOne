"""
I don't know, I guess some stuff goes here
"""


from threading import Thread
from f1_race import F1            # Base
import global_variables
import time


def global_print():
    while True:
        print(global_variables.CURRENT_RACE_DATA)
        time.sleep(1)

def main():
    race = F1()
    race.output_to_file = False
    threads = []
    thread_targets = [{'target': race.session, 'args': []},
                      {'target': global_print, 'args': []}]
    
    for thread_target in thread_targets:
        thread = Thread(target=thread_target['target'], args=thread_target['args'])
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    global_variables.initialize()
    main()