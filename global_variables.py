"""
Global Variables File
Contains global variables along with functions related to them
"""

# I (Matt) could not get the code to run without having these variables in the global scope of the package
# We could also just not have the reset global variables function.  I didn't know if you (graham) intended on it
# being called during the execution of the app to potentially reset the variables because a new racing session was
# about to start
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

    # set these variables to global to ensure they refer to the global scoped variables
    global CURRENT_RACE_DATA
    global CURRENT_CAR_TELEMETRY
    global CURRENT_CAR_POSITION
    global TIMING_DATA
    global WEATHER_DATA
    global CURRENT_RACE_HEARTBEAT
    global CURRENT_TELEMETRY_HEARTBEAT

    # Reset the variables to empty
    CURRENT_RACE_DATA = None
    CURRENT_CAR_TELEMETRY = None
    CURRENT_CAR_POSITION = None
    TIMING_DATA = None
    WEATHER_DATA = None
    CURRENT_RACE_HEARTBEAT = None
    CURRENT_TELEMETRY_HEARTBEAT = None
