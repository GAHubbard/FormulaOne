import blessed
import time

time_row: str = ""
status_row: str = ""

driver_list: list[str] = []

other_data: list[str] = []

term = blessed.Terminal()

def display_rows():
    """
    Displays to Terminal based on rows
    :return:
    """
    time.sleep(45)
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





