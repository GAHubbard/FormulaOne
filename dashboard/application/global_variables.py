"""
Global Variables File
Contains global variables along with functions related to them
"""

# global R data sent at the beginning and every now and then
signal_r_romeo_message_object = {}

# these init variables serve as flags that ensure the R runs once
driver_tracker_bool_initalized = False
track_status_bool_initalized = False

# these variables hold the values of the JsonStreams
driver_tracker: list = []
track_status: list = []

# Below lines may not be recent

SESSION_INFO = None
ARCHIVE_STATUS = None
TRACKING_STATUS = None
SESSION_DATA = None
CONTENT_STREAMS = None
AUDIO_STREAMS = None
EXTRAPOLATED_CLOCK = None
CHAMPIONSHIP_PREDICTION = None
CAR_DATA = None
POSITION = None
DRIVER_LIST = None
TIMING_DATE_F1 = None
LAP_SERIES = None
TIMING_DATA = None
TOP_THREE = None
TIMING_APP_DATA = None
TIMING_STATS = None
DRIVER_RACE_INFO = None
LAP_COUNT = None
TYRE_STINT_SERIES = None
SESSION_STATUS = None
HEART_BEAT = None
WEATHER_DATA = None
WEATHER_DATA_SERIES = None
TLARCM = None
RACE_CONTROL_MESSAGES = None
TEAM_RADIO = None
CURRENT_TYRES = None
OVERTAKE_SERIES = None
PIT_LANE_TIME_COLLECTION = None
PIT_STOP_SERIES = None