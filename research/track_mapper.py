"""
File is used to research how F1 live timing actually creates coordinates for their telemetry data
"""

import json
from pandas import DataFrame

FILE_PATH_TO_TELEMETRY = r"C:\Users\Matth\PycharmProjects\F1\FormulaOne\dashboard\application\position_map_44_2025-06-15-1444.txt"


def convert_telemetry_file_to_dataframe(telemetry_file_path: str) -> pandas.DataFrame:

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

    return telemetry_dataframe


def get_min_max_x(telemetry_data: DataFrame) -> (DataFrame, DataFrame):
    return telemetry_data['X'].min(), telemetry_data['X'].max()

def get_min_max_y(telemetry_data: DataFrame) -> (DataFrame, DataFrame):
    return telemetry_data['Y'].min(), telemetry_data['Y'].max()


def map_telemetry_data(telemetry_data: pandas.DataFrame) -> None:

    min_x, max_x = get_min_max_x(telemetry_data)
    min_y, max_y = get_min_max_y(telemetry_data)



    print(f""

    pass

if __name__ == "__main__":
    telemetry_df = convert_telemetry_file_to_dataframe(FILE_PATH_TO_TELEMETRY)

    map_telemetry_data(telemetry_df)

