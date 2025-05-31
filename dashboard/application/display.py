import blessed
import time

from reflex_chakra import breadcrumb_separator

control_row: str = ""  # row gives user options on what to do
time_row: str = ""     # row gives the latest time
status_row: str = ""   # row gives the status of the track

driver_list: list[str] = [] # driver list data

other_data: list[str] = []

term = blessed.Terminal()

def display_rows():
    """
    Displays to Terminal based on rows
    :return:
    """
    time.sleep(45)

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():

        while True:
            time.sleep(2)

            print(term.clear + term.move_xy(0,0), end='')

            print(f"{time_row}")

            print(f"Status: {status_row[0]} as of {status_row[1].strftime('%H:%M:%S')}")

            driver_list_copy = driver_list.copy()

            for index, value in enumerate(driver_list_copy):
                print(f"{index + 1}: {value}")

            print()

            other_data_copy = other_data.copy()
            for index, value in enumerate(other_data_copy):
                print(f"{value}")

def debug_or_normal_mode() -> None:
    """
    Prompts the user to enter debug or normal mode
    :return:
    """

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():

        # set default behavior is normal mode not debug
        normal_mode_true_debug_false_flag = True
        quit_flag = False

        # way out of loop is to press Q or q or enter key
        while True:
            print(term.home + term.clear, end='')  # clear terminal and go to top
            print(term.move_xy(0,0) + term.bold, f"Press q to quit, left / right arrows, and enter", end='')
            print(term.move_xy(0,1) + term.yellow +  f"Do you want to enter " ,end='')

            if normal_mode_true_debug_false_flag:  # normal mode is selected
                print(term.bold, term.underline, f"Normal Mode", end='')
                print(f"| Debug Mode")
            else:  # debug mode is selected
                print(f"Normal Mode | ", end='')
                print(term.bold, term.underline, f"Debug Mode")

            key = term.inkey()  # get key input from user

            # this exits the program if the user
            if key.lower() == 'q' or key.upper() == 'Q':
                quit_flag = True
                break

            if key.name == 'KEY_LEFT':
                normal_mode_true_debug_false_flag = True
            if key.name == 'KEY_RIGHT':
                normal_mode_true_debug_false_flag = False
            if key.name == 'KEY_ENTER':
                break

        # now check to see if they wanted to quit
        if quit_flag:
            exit()
        else:
            if normal_mode_true_debug_false_flag:
                # normal_mode()
                pass
            else:
                # debug_mode()
                pass
