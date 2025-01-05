"""
Global Variables File
Contains global variables along with functions related to them
"""
CURRENT_RACE_DATA = None
CURRENT_CAR_TELEMETRY = None
CURRENT_CAR_POSITION = None
TIMING_DATA = None
WEATHER_DATA = None
CURRENT_RACE_HEARTBEAT = None
CURRENT_TELEMETRY_HEARTBEAT = None

def reset_global_variables() -> None:
    """
    Resets the global variables to None
    :return:
    """
    global CURRENT_RACE_DATA
    global CURRENT_CAR_TELEMETRY
    global CURRENT_CAR_POSITION
    global TIMING_DATA
    global WEATHER_DATA
    global CURRENT_RACE_HEARTBEAT
    global CURRENT_TELEMETRY_HEARTBEAT

    CURRENT_RACE_DATA = None
    CURRENT_CAR_TELEMETRY = None
    CURRENT_CAR_POSITION = None
    TIMING_DATA = None
    WEATHER_DATA = None
    CURRENT_RACE_HEARTBEAT = None
    CURRENT_TELEMETRY_HEARTBEAT = None
