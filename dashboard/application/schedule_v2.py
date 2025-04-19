"""
Contains useful ways to get schedule information using F1's API
"""

import load_dotenv
import os
import requests
import datetime

# Load environment variables from .env file
load_dotenv.load_dotenv()

# Access the API key
api_key = os.environ.get('F1APIKEY')

# Set the headers to have the API Key
headers = {
    'apikey': api_key,
    'locale': 'en'
}

# API URL
meeting_api_url = "https://api.formula1.com/v1/editorial-eventlisting/events"

session_api_url_needs_meeting = "https://api.formula1.com/v1/event-tracker/meeting"


def season_api_is_showing() -> int:
    """
    Returns what year the F1 api is showing
    :return:
    """

    url = "https://api.formula1.com/v1/editorial-eventlisting/events"

    response = requests.get(meeting_api_url, headers=headers)

    return int(response.json()['year'])


def get_list_of_event_dictionaries() -> list[dict]:
    """
    Returns a list of events or meetings as dictionaries
    :return:
    """

    response = requests.get(meeting_api_url, headers=headers)

    return response.json()['events']


def get_next_or_current_meeting_info() -> dict or None:
    """
    Returns information about the next practice session as dictionary

    ** Will return the next meeting info the day after a race (all in utc) **

    ** Will return None if there is no next meeting because the season is over **

    ** this function is kinda overkill because the meetings are in order already by time in the dictionary **

    :return: dict for event or None if there are no next meetings
    """

    # get the current date in utc time
    current_date_in_utc = datetime.datetime.now(datetime.timezone.utc).date()

    event_list: list[dict] = get_list_of_event_dictionaries()

    event_dict_with_time_as_keys = {}
    for event in event_list:
        race_date_in_utc = get_end_time_of_event_or_meeting_in_utc(event).date()
        event_dict_with_time_as_keys[race_date_in_utc] = event

    sorted_event_list_with_time_as_keys = sorted(event_dict_with_time_as_keys.items(), key=lambda x: x[0])

    # the first event/meeting is the upcoming event
    if current_date_in_utc < sorted_event_list_with_time_as_keys[0][0]:
        return sorted_event_list_with_time_as_keys[0][1]
    elif current_date_in_utc > sorted_event_list_with_time_as_keys[-1][0]:
        return None
    else:
        for index, date_event_tuple in enumerate(sorted_event_list_with_time_as_keys):
            if date_event_tuple[0] < current_date_in_utc <= sorted_event_list_with_time_as_keys[index + 1][0]:
                return sorted_event_list_with_time_as_keys[index + 1][1]


def get_end_time_of_event_or_meeting_in_utc(event_or_meeting: dict) -> datetime.datetime:
    """
    Returns the scheduled end time of the race or in the acase of the practice meeting/event
    it will return the scheduled end time of the last session

    :param event_or_meeting: dictionary that returns from one element of get_list_of_event_dictionaries()
    :return: a datetime object for the scheduled end time
    """

    local_end_time = datetime.datetime.fromisoformat(event_or_meeting['meetingEndDate'])

    gmt_offset_as_string = event_or_meeting['gmtOffset']

    gmt_offset_as_timedelta = convert_f1_gmt_offset_string_to_time_delta(gmt_offset_as_string)

    end_time_utc = local_end_time - gmt_offset_as_timedelta

    return end_time_utc


def get_start_time_of_event_or_meeting_in_utc(event_or_meeting: dict) -> datetime.datetime:
    """
    Return the scheduled start time of session 1 or practice 1 of an event / meeting

    :param event_or_meeting: dictionary that returns from one element of get_list_of_event_dictionaries()
    :return: a datetime object for the scheduled start time
    """

    local_start_time = datetime.datetime.fromisoformat(event_or_meeting['meetingStartDate'])

    gmt_offset_as_string = event_or_meeting['gmtOffset']

    gmt_offset_as_timedelta = convert_f1_gmt_offset_string_to_time_delta(gmt_offset_as_string)

    start_time_utc = local_start_time - gmt_offset_as_timedelta

    return start_time_utc


def convert_f1_gmt_offset_string_to_time_delta(gmt_offset_string: str) -> datetime.timedelta:
    """
    Takes an f1 API gmt offset and converts it to a time delta

    ** currently only implemented for https://api.formula1.com/v1/editorial-eventlisting/events calls **

    :param gmt_offset_string: looks like "+03:00"
    :return: should return a positive 3 hour timedelta
    """

    if gmt_offset_string.startswith('+'):
        is_positive = True
    else:
        is_positive = False

    hours_delta = gmt_offset_string[1:3]

    if is_positive:
        return datetime.timedelta(hours=int(hours_delta))
    else:
        return datetime.timedelta(hours=-int(hours_delta))


def get_first_session_start_of_upcoming_or_current_meeting_in_utc() -> datetime.datetime:
    """
    Returns the first session start datetime of the upcoming or current meeting as a datetime object

    ** RETURNS IN UTC **
    :return: a datetime for the utc start time in utc
    """

    current_or_upcoming_meeting = get_next_or_current_meeting_info()

    return get_start_time_of_event_or_meeting_in_utc(current_or_upcoming_meeting)


def get_name_of_event_or_meeting(meeting: dict) -> str:
    """
    Returns the name of the event or meeting based on

    https://api.formula1.com/v1/editorial-eventlisting/events call

    respoonse.json() -> events -> some element -> meeeting param for this function

    response.json()[events][0-n]

    :param meeting: a return from api call above then events key then some element
    :return: a string for the name for the event
    """

    return meeting['meetingName']


def get_session_json_from_a_meeting_key(meeting_key: str) -> dict:
    """
    Returns a dictionary for a specific session based on a meeting key found in the events url api
    :param meeting_key: example is 1258 for Saudi Arabia 2025
    :return:
    """

    response = requests.get(f"{session_api_url_needs_meeting}/{meeting_key}", headers=headers)

    return response.json()


def get_the_upcoming_or_current_sessions_for_a_meeting() -> dict:
    """
    Returns a dictionary for the sessions for the upcoming or current meeting
    :return:
    """

    meeting_key: str = get_next_or_current_meeting_info()['meetingKey']

    return get_session_json_from_a_meeting_key(meeting_key)


def get_session_list(session_dict: dict) -> list[dict]:
    """
    Returns sessions for a meeting when given the session_dictionary return from the session api

    :param session_dict: is a session return using a meetingKey or the upcoming current sessions
    :return:
    """

    return session_dict['seasonContext']['timetables']


def get_upcoming_or_ongoing_session() -> dict:
    """
    Returns a dictionary with information on the upcoming session

    ** if the session is still scheduled to be ongoing then it will return the current session **

    ** because session list is in order for a given session dictionary this doesn't need to sort by time **

    ** UNSURE WHAT HAPPENS AT END OF MEEETING OR END OF SESSION **

    :return:
    """

    # get the sessions dictionary for the current or upcoming meeting
    sessions_info = get_the_upcoming_or_current_sessions_for_a_meeting()

    # get the session list for that meeting
    session_list = get_session_list(sessions_info)

    # get the current time in utc
    current_time_in_utc: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)

    if current_time_in_utc < get_session_start_time_in_utc_from_timetables_list_in_session_dictionary(session_list[0]):
        return session_list[0]
    else:
        for index, session in enumerate(session_list):
            if get_session_start_time_in_utc_from_timetables_list_in_session_dictionary(session) < current_time_in_utc <= get_session_start_time_in_utc_from_timetables_list_in_session_dictionary(session_list[index + 1]):

                # check to see if the session is still going on
                end_time_utc = get_session_end_time_in_utc_from_timetables_list_in_session_dictionary(session)
                if current_time_in_utc <= end_time_utc:
                    return session  # session is still ongoing to return current session
                else:
                    return session_list[index + 1]  # session has ended so return the next session


def get_session_start_time_in_utc_from_timetables_list_in_session_dictionary(specific_session_in_timetables_list: dict) -> datetime.datetime:
    """
    Returns a datetime object for the session start time in utc from a timetables list

    argument for this function: using the session api return -> seasonContext -> timetables -> any element

    :param specific_session_in_timetables_list: session_dictionary_from_session_api['seasonContext']['timetables'][0-n]
    :return: a utc datetime object for the session start time in utc
    """

    # get the local start time
    start_time_local_time = datetime.datetime.strptime(specific_session_in_timetables_list['startTime'], '%Y-%m-%dT%H:%M:%S')

    # get the gmt offset as a string
    gmt_offset_as_string = specific_session_in_timetables_list['gmtOffset']

    # convert that to a time delta
    gmt_offset_as_time_delta = convert_f1_gmt_offset_string_to_time_delta(gmt_offset_as_string)

    # apply the timedelta to the local time
    start_time_utc = start_time_local_time - gmt_offset_as_time_delta

    # FORCE START_TIME_UTC TO BE TIMEZONE AWARE OR A BUG HAPPENS IN COMPARISON OF DATETIMES
    start_time_utc = start_time_utc.replace(tzinfo=datetime.timezone.utc)

    return start_time_utc


def get_session_end_time_in_utc_from_timetables_list_in_session_dictionary(specific_session_in_timetables_list: dict) -> datetime.datetime:
    """
    Returns a datetime object for the session end time in utc from a timetables list

    argument for this function: using the session api return -> seasonContext -> timetables -> any element

    :param specific_session_in_timetables_list: session_dictionary_from_session_api['seasonContext']['timetables'][0-n]
    :return: a utc datetime object for the session end time in utc
    """

    # get the local end time
    end_time_local_time = datetime.datetime.strptime(specific_session_in_timetables_list['endTime'], '%Y-%m-%dT%H:%M:%S')

    # get the gmt offset as a string
    gmt_offset_as_string = specific_session_in_timetables_list['gmtOffset']

    # convert that to a time delta
    gmt_offset_as_time_delta = convert_f1_gmt_offset_string_to_time_delta(gmt_offset_as_string)

    # apply the timedelta to the local time
    end_time_utc = end_time_local_time - gmt_offset_as_time_delta

    # FORCE START_TIME_UTC TO BE TIMEZONE AWARE OR A BUG HAPPENS IN COMPARISON OF DATETIMES
    end_time_utc = end_time_utc.replace(tzinfo=datetime.timezone.utc)

    return end_time_utc

def next_session_info_print(user_time: bool = False) -> None:
    """
    Prints out the next session info

    :param user_time: if False then utc time, if True then user time
    :return:
    """

    upcoming_or_current_meeting = get_next_or_current_meeting_info()
    name_of_meeting = get_name_of_event_or_meeting(upcoming_or_current_meeting)

    upcoming_session_timetable = get_upcoming_or_ongoing_session()

    upcoming_session_start_time = get_session_start_time_in_utc_from_timetables_list_in_session_dictionary(upcoming_session_timetable)

    name_of_upcoming_session = get_name_of_session_from_timetable(upcoming_session_timetable)

    print(f"Current or Upcoming Race: {name_of_meeting}")
    print(f"Upcoming Session: {name_of_upcoming_session}")

    time_zone_as_string = "(UTC)"

    if user_time:
        user_gmt_offset = datetime.datetime.now().astimezone().utcoffset().total_seconds() / 3600
        user_gmt_offset_time_delta = datetime.timedelta(hours=user_gmt_offset)
        upcoming_session_start_time = upcoming_session_start_time + user_gmt_offset_time_delta
        time_zone_as_string = "(Local)"

    print(f"Upcoming Session Start Time {time_zone_as_string}: {upcoming_session_start_time.strftime('%H:%M %A %d %B %Y')}")


def get_name_of_session_from_timetable(session_info: dict) -> str:
    """
    Returns the name of the session from a timetable dictionary returned from the session api
    :param session_info: session api -> seasonContext -> timetables -> any element
    :return:
    """

    return session_info['description']


def scheduled_session_status() -> None:
    """
    checks the time and prints information regarding the current scheduled or upcoming session
    :return:
    """

    current_or_upcoming_session = get_upcoming_or_ongoing_session()

    current_utc_datetime = datetime.datetime.now(datetime.timezone.utc)

    if current_utc_datetime < get_session_start_time_in_utc_from_timetables_list_in_session_dictionary(current_or_upcoming_session):
        print(f"Session is upcoming")
        next_session_info_print(user_time=True)

    # this conditional might be redundnat because the get_upcoming_or_ongoing_session will just return the current session if it hasn't ended yet
    # it might just need to be else by itself
    elif current_utc_datetime > get_session_start_time_in_utc_from_timetables_list_in_session_dictionary(current_or_upcoming_session):
        print(f"Session is in progress")
        next_session_info_print(user_time=True)

if __name__ == "__main__":
    print(season_api_is_showing())

    print(get_list_of_event_dictionaries())

    print(get_next_or_current_meeting_info())

    print(get_first_session_start_of_upcoming_or_current_meeting_in_utc())

    print(get_name_of_event_or_meeting(get_next_or_current_meeting_info()))

    print(get_session_json_from_a_meeting_key('1258'))

    print(get_the_upcoming_or_current_sessions_for_a_meeting())

    print(get_session_list(get_the_upcoming_or_current_sessions_for_a_meeting()))

    print(f"upcoming session dictionary: {get_upcoming_or_ongoing_session()}")

    print()

    print(get_session_start_time_in_utc_from_timetables_list_in_session_dictionary(get_upcoming_or_ongoing_session()))

    next_session_info_print()

    next_session_info_print(user_time=True)

    print()

    scheduled_session_status()