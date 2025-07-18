import zlib
import base64
import global_variables
import time
import datetime
import blessed
import display


def get_car_telemetry_data(data):
    if ['R'] in data:
        heartbeat = data['R']['Heartbeat']['Utc']
        zipped_data = data['R']['CarData.z']
        unzipped_data = zlib.decompress(base64.b64decode(zipped_data), -zlib.MAX_WBITS)
        unzipped_data.decode('utf-8-sig')


def print_driver_list():
    time.sleep(30)
    if global_variables.driver_tracker_bool_initalized:
        while True:
            time.sleep(1)
            local_copy_driver_tracker: list = global_variables.driver_tracker.copy()
            local_time_stamp: datetime.datetime = local_copy_driver_tracker[1]

            #print(f"Last Update: {local_time_stamp.strftime('%Y-%m-%d %H:%M:%S')}")

            display.time_row = f"Last Update: {local_time_stamp.strftime('%Y-%m-%d %H:%M:%S')}"

            local_lines: list = local_copy_driver_tracker[0]['Lines']

            if len(display.driver_list) == 0:
                for index, value in enumerate(local_lines):
                    display.driver_list.append(f"{value['RacingNumber']}")
            else:
                for index, value in enumerate(local_lines):
                    display.driver_list[index] = f"{value['RacingNumber']}"

            display.status_row = global_variables.track_status


def get_car_position_data(data):
    pass