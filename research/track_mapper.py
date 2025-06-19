"""
File is used to research how F1 live timing actually creates coordinates for their telemetry data
"""

import json
from pandas import DataFrame
import time
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import pandas as pd

FILE_PATH_TO_TELEMETRY = r"C:\Users\Matth\PycharmProjects\F1\FormulaOne\dashboard\application\position_map_44_2025-06-15-1444.txt"


def convert_telemetry_file_to_dataframe(telemetry_file_path: str) -> DataFrame:

    with open(telemetry_file_path, 'r') as f:
        file_content = f.read()

        list_of_telemetry_data = []  # we will load each line of the file into this


        # go through each line in the file
        for line in file_content.splitlines():

            # convert each line to a dictionary via eval because they are strings just like dictionaries
            line_as_dict = eval(line)

            list_of_telemetry_data.append(line_as_dict)

    # convert the list to a dataframe
    telemetry_dataframe = DataFrame(list_of_telemetry_data)
    telemetry_dataframe['Timestamp'] = pd.to_datetime(telemetry_dataframe['Timestamp'], utc=True)

    return telemetry_dataframe


def get_min_max_x(telemetry_data: DataFrame) -> (DataFrame, DataFrame):
    return telemetry_data['X'].min(), telemetry_data['X'].max()

def get_min_max_y(telemetry_data: DataFrame) -> (DataFrame, DataFrame):
    return telemetry_data['Y'].min(), telemetry_data['Y'].max()

def get_min_max_z(telemetry_data: DataFrame) -> (DataFrame, DataFrame):
    return telemetry_data['Z'].min(), telemetry_data['Z'].max()

def get_min_max_time(telemetry_data: DataFrame) -> (DataFrame, DataFrame):
    return telemetry_data['Timestamp'].min(), telemetry_data['Timestamp'].max()

def map_telemetry_data(telemetry_data: DataFrame) -> None:

    min_x, max_x = get_min_max_x(telemetry_data)
    min_y, max_y = get_min_max_y(telemetry_data)
    min_z, max_z = get_min_max_z(telemetry_data)
    min_time, max_time = get_min_max_time(telemetry_data)

    print(f"X range: {min_x} - {max_x}")
    print(f"Y range: {min_y} - {max_y}")
    print(f"Z range: {min_z} - {max_z}")
    print(f"Time range: {min_time} - {max_time}")

    plt.figure(figsize=(12, 8))

    x_range = max_x - min_x
    y_range = max_y - min_y
    z_range = max_z - min_z

    plt.ion()

    plt.xlim(min_x - round(x_range * .1), max_x + round(x_range * .1))
    plt.ylim(min_y - round(y_range * .1), max_y + round(y_range * .1))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.autoscale(False)

    plt.grid(True)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Telemetry Grid")


    map_x_y = plt.scatter([],[])
    plt.show()
    x_so_far = []
    y_so_far = []
    time_now = datetime.now(timezone.utc)

    # plot per record per 1 second
    """
    for record in telemetry_data.itertuples():
        x_so_far.append(record.X)
        y_so_far.append(record.Y)
        map_x_y.set_offsets(list(zip(x_so_far, y_so_far)))
        plt.draw()
        plt.pause(1)
    """

    # loop while preserving real time passing
    time_offset = time_now - telemetry_data.iloc[0].Timestamp
    record_index = 0
    while True:
        race_time = datetime.now(timezone.utc) - time_offset
        if telemetry_data.iloc[record_index].Timestamp < race_time:
            x_so_far.append(telemetry_data.iloc[record_index].X)
            y_so_far.append(telemetry_data.iloc[record_index].Y)
            map_x_y.set_offsets(list(zip(x_so_far, y_so_far)))
            plt.draw()
            plt.pause(.001)
            record_index = record_index + 1
        if record_index >= len(telemetry_data):
            break

if __name__ == "__main__":
    telemetry_df = convert_telemetry_file_to_dataframe(FILE_PATH_TO_TELEMETRY)

    map_telemetry_data(telemetry_df)



