import datetime
import blessed
import time

import json_explore

import global_variables

control_row: str = "Press q to quit, p to pause (30), d to dive into Position.z"  # row gives user options on what to do
time_row: str = ""     # row gives the latest time

test_time = datetime.datetime.now()
status_row: list = ["UNKNOWN", test_time]   # row gives the status of the track

r_status_row = ""

driver_list: list[str] = [] # driver list data

other_data: list[str] = []

data_gathering_status_line: str = "" # data gathering status line

last_r_data_set_line: str = ""

last_44_position_data: str = ""

term = blessed.Terminal()  # return a blessed terminal object

def display_rows():
    """
    Displays to Terminal based on rows
    :return:
    """
    while global_variables.session_status:
        run_json_explore = False

        with term.fullscreen(), term.cbreak(), term.hidden_cursor():

            while True:

                print(term.clear + term.move_xy(0,0), end='')

                print(f"{control_row}")

                print(f"{time_row}")

                print(f"{r_status_row}")

                print(f"Status: {status_row[0]} as of {status_row[1].strftime('%H:%M:%S')}")

                driver_list_copy = driver_list.copy()

                for index, value in enumerate(driver_list_copy):
                    print(f"{index + 1}: {value}")

                print()

                other_data_copy = other_data.copy()
                for index, value in enumerate(other_data_copy):
                    print(f"{value}")

                print(f"{data_gathering_status_line}")

                print()

                print(f"{last_r_data_set_line}")

                print(term.move_xy(0,25), end='')

                print(f"{last_44_position_data}")

                key = term.inkey(timeout=1)

                if key == "q":
                    time.sleep(5)
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
                    filename = f"position_map_44_{timestamp}.txt"
                    try:
                        with open(filename, 'w') as f:
                            for position_entry in global_variables.position_map_44:
                                f.write(f"{position_entry}\n")
                        print(f"Saved position map to {filename}")
                    except Exception as e:
                        print(f"Failed to save position map to {filename}")
                    global_variables.session_status = False
                    break
                if key == "p":
                    time.sleep(30)

                if key == "d":
                    run_json_explore = True
                    break


        if run_json_explore:
            json_explore.json_explore_json(last_r_data_set_line)
            input("Press anything to return to dashboard...")

        if not global_variables.session_status:
            break


def debug_or_normal_mode() -> bool:
    """
    Prompts the user to enter debug or normal mode
    :return: Returns True if normal mode, False if debug mode
    """

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():

        # set default behavior is normal mode not debug
        normal_mode_true_debug_false_flag = True
        quit_flag = False

        # way out of loop is to press Q or q or enter key
        while True:
            print(term.home + term.clear, end='')  # clear terminal and go to top
            print(term.move_xy(0,0) + term.bold + f"Press q to quit, left / right arrows, and enter" + term.normal, end='')
            print(term.move_xy(0,1) + term.yellow +  f"Do you want to enter " + term.normal,end='')

            if normal_mode_true_debug_false_flag:  # normal mode is selected
                print(term.bold + term.underline + f"Normal Mode" + term.normal, end='')
                print(f" | Debug Mode", end='')
                print(term.cyan + " ?" + term.normal)
            else:  # debug mode is selected
                print(f"Normal Mode | ", end='')
                print(term.bold + term.underline + f"Debug Mode" + term.normal, end='')
                print(term.cyan + " ?" + term.normal)

            key = term.inkey()  # get key input from user

            # this exits the program if the user
            if key.lower() == 'q':
                quit_flag = True
                break
            elif key.name == 'KEY_LEFT':
                normal_mode_true_debug_false_flag = True
            elif key.name == 'KEY_RIGHT':
                normal_mode_true_debug_false_flag = False
            elif key.name == 'KEY_ENTER':
                break

        # now check to see if they wanted to quit
        if quit_flag:
            exit()
        else:
            if normal_mode_true_debug_false_flag:
                return True
            else:
                return False
