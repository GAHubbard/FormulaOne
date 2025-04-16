"""
File contains functions related to the schedule


"""
import datetime
import urllib.parse

import json_explore
import requests
import json

def get_upcoming_or_current_meeting_slash_race_as_dict() -> dict:
    """
    Returns the dictionary corresponding to the !! current or upcoming race. !!

    ** NOTE F1 DOESN'T UPDATE THIS UNTIL THE {NOT THE MONDAY BEFORE THE NEXT RACE} **

    :return: dictionary contains info like

    Sessions: list                      # contains info for each practice session, qualifying, or race
	Key: 1257: <class 'int'>            # idk
	Code: F1202504: <class 'str'>       # idk
	Number: 4: <class 'int'>            # Meeting Number - 1 cause they start at 0
	Location: Sakhir: <class 'str'>     # City
	OfficialName: FORMULA 1 GULF AIR BAHRAIN GRAND PRIX 2025: <class 'str'>     # long name
	Name: Bahrain Grand Prix: <class 'str'>                                     # medium name
	Country: dict                       # contains country info like Name of Country and Trigraph for Country
	Circuit: dict                       # contains circuit like the shortname for the circuit (usually city name)

    """

    # get all meetings via the f1 url and the current year
    all_meetings_so_far_including_current: list[dict] = get_all_meetings_slash_races()

    return all_meetings_so_far_including_current[-1]  # gets the last Meeting/Race


def get_all_meetings_slash_races() -> list[dict]:
    """
    Returns a list of dictionaries corresponding to a meeting / race

    :return: dictionary contains info like

    Sessions: list                      # contains info for each practice session, qualifying, or race
	Key: 1257: <class 'int'>            # idk
	Code: F1202504: <class 'str'>       # idk
	Number: 4: <class 'int'>            # Meeting Number - 1 cause they start at 0
	Location: Sakhir: <class 'str'>     # City
	OfficialName: FORMULA 1 GULF AIR BAHRAIN GRAND PRIX 2025: <class 'str'>     # long name
	Name: Bahrain Grand Prix: <class 'str'>                                     # medium name
	Country: dict                       # contains country info like Name of Country and Trigraph for Country
	Circuit: dict                       # contains circuit like the shortname for the circuit (usually city name)

    """

    # get current year
    current_year = datetime.datetime.now().year

    # create schedule url
    url = f"https://livetiming.formula1.com/static/{current_year}/Index.json"

    # get response from f1 url
    response: requests.Response = requests.get(url)

    #convert to dictionary
    response_dict: dict = json.loads(response.content.decode(response.apparent_encoding))

    return response_dict['Meetings']


def get_next_or_upcoming_location() -> (str, str):
    """
    Returns the next or upcoming racing location as a tuple of (city, country)

    ** F1 WILL NOT UPDATE THIS {AT LEAST THE MONDAY BEFORE THE NEXT RACE} **

    :return: Returns a tuple with the upcoming location (city, country) as strings
    """
    # default situation
    city: str = ""
    country: str = ""

    # get current meeting
    current_or_upcoming_meeting: dict = get_upcoming_or_current_meeting_slash_race_as_dict()

    # get city and country
    city = current_or_upcoming_meeting['Location']
    country = current_or_upcoming_meeting['Country']['Name']

    return city, country


def is_current_or_upcoming_week_sprint() -> bool:
    """
    Returns True if the current week is sprint weekend

    ** F1 WILL NOT UPDATE THIS {AT LEAST THE MONDAY BEFORE THE NEXT RACE} **

    :return: True if sprint weekend and False if not
    """

    # get the current or upcoming meeting
    current_or_upcoming_meeting = get_upcoming_or_current_meeting_slash_race_as_dict()

    # get session 2 (session 1 will always be practice 1)
    session_2: dict = current_or_upcoming_meeting['Sessions'][1]

    session_2_name: str = session_2['Name']

    # if sprint is in the name for session 2 which will always be a sprint qualifying on sprint weekends
    if 'sprint' in session_2_name.lower():
        return True
    else:
        return False


def has_f1_posted_the_upcoming_schedule_info() -> bool:
    """
    Returns whether or not f1 has posting the upcoming schedule
    Returns true during race weekend even if the next week hasn't been posted yet

    Also for timing in this function we assume GMT and UTC are the same.
    F1 uses GMT time at least in name, but I have a suspicious feeling they really mean UTC but just say GMT
    Either way they are different by less than a second so it shouldn't matter

    ** ALL TIMES ARE IN UTC Time **

    !! TODO !! WE NEED TO CHECK IF F1 IS PLANNING RACES AROUND THE LOCAL TIME RATHER THAN UTC
    !! TODO !! AS IN DOES F1 HAVE FRI SAT SUN RACES PURELY ON LOCAL TIME AND USING UTC MESSES UP THAT PATTERN


    Truth Table Example
    Example Race Weekend:
    F1 Activity -> Day of the week          -> is 3 FEB race posted -> function returns
    Nothing     -> Monday (All GMT/UTC Time)-> no                   -> False
    Nothing     -> Tuesday                  -> no                   -> False
    Nothing     -> Wednesday                -> yes                  -> True
    Nothing     -> Thursday                 -> yes                  -> True
    P1 and P2   -> Friday    1 FEB          -> yes                  -> True
    P3 and Qual -> Saturday  2 FEB          -> yes                  -> True
    Race        -> Sunday    3 FEB          -> yes                  -> True

    ** THIS FUNCTION ASSUMES THAT F1 WILL ALWAYS POST AT LEAST BY THURSDAY THE RACE SCHEDULE **

    Once...

    :return:
    """

    # get the utc time
    utc_time = datetime.datetime.now(datetime.timezone.utc)

    # get the current date in utc time
    utc_current_date = utc_time.date()

    pass


def get_beginning_utc_date_of_weekend() -> datetime.date:
    """
    Returns the beginning date of the weekend of the current week
    based on the time of the first session it returns the utc date

    Doesn't care if the f1 data is showing the upcoming current or past weekend.

    ** THIS JUST RETURNS THE LATEST MEETING DATA **

    ** F1 POSTS THE LOCAL SESSION START TIMES AND LOCAL SESSION END TIMES **
    ** THEY GIVE THE GMT OFFSET SO YOU KNOW THE TIMEZONE **

    - Postive GMT offsets look like GmtOffset: 03:00:00

    !! TODO !! how does f1 post times with negative gmt offsets

    :return: utc date of first session of the last meeting data from the API
    """

    # get latest posted meeting dict
    latest_posted_meeting: dict = get_upcoming_or_current_meeting_slash_race_as_dict()

    # get the first session
    first_session: dict = latest_posted_meeting['Sessions'][0]

    # get the start time and gmt offset
    start_time_first_session_str: str = first_session['StartDate']
    gmt_offset_str: str = first_session['GmtOffset']

    # convert the gmt offset to a timedelta
    time_delta_from_gmt_offset: datetime.timedelta = convert_gmt_offset_str_to_time_delta(gmt_offset_str)

    # convert the session time to a datetime
    start_time_first_session = datetime.datetime.strptime(start_time_first_session_str, "%Y-%m-%dT%H:%M:%S")

    # convert to utc time by subtracting the gmt offset
    utc_start_time_first_session = start_time_first_session - time_delta_from_gmt_offset

    # convert utc time to utc date
    return utc_start_time_first_session.date()


def convert_gmt_offset_str_to_time_delta(gmt_offset_str: str) -> datetime.timedelta:
    """
    Takes an F1 GMT offset string and converts it to a time delta
    :param gmt_offset_str: returned from F1 API

    Example:
    GmtOffset: 03:00:00 ->

    :return: A timedelta object representing the time delta of a gmt offset string
    """

    offset_int = int(gmt_offset_str[:2])

    offset_timedelta = datetime.timedelta(hours=offset_int)

    return offset_timedelta


def new_way_to_get_schedule_data():

    headers = {
        'locale': 'en',
        'apikey': 't3DrvCuXvjDX8nIvPpcSNTbB9kae1DPs'
    }

    url = "https://api.formula1.com/v1/editorial-eventlisting/events"

    response = requests.get(url, headers=headers)

    json_explore.json_explore_json(response.json())

    with open('schedule_return_real.json', 'w') as outfile:
        json_ob = json.dumps(response.json())
        outfile.write(json_ob)


if __name__ == "__main__":
    """
    Test code for this module
    """

    print(f"Current or Upcoming Race: {get_upcoming_or_current_meeting_slash_race_as_dict()}")

    print(f"All Races So Far Including Current: {get_all_meetings_slash_races()}")

    print(f"Next Race: {get_next_or_upcoming_location()}")

    print(f"Is the current week or upcoming week a sprint weekend?: {'Yes' if is_current_or_upcoming_week_sprint() else 'No'}")

    print(f"Start Date in UTC of first session: {get_beginning_utc_date_of_weekend()}")

    print(f"testing new schedule end point: {new_way_to_get_schedule_data()}")

