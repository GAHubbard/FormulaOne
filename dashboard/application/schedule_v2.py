"""
Contains useful ways to get schedule information using F1's API
"""

import load_dotenv
import os
import requests
import datetime

"""
!! TODO !! try out /en/racing/2025/bahrain
!! TODO !! countryKey is 36
!! TODO !! meetingKey is 1257

"""

# Load environment variables from .env file
load_dotenv.load_dotenv()

# Access the API key
api_key = os.environ.get('F1APIKEY')

# Set the headers to have the API Key
headers = {
    'apikey': api_key
}

# API URL
api_url = "https://api.formula1.com/v1/editorial-eventlisting/events"


def season_api_is_showing() -> int:
    """
    Returns what year the F1 api is showing
    :return:
    """

    url = "https://api.formula1.com/v1/editorial-eventlisting/events"

    response = requests.get(api_url, headers=headers)

    return int(response.json()['year'])


def get_list_of_event_dictionaries() -> list[dict]:
    """
    Returns a list of events or meetings as dictionaries
    :return:
    """

    response = requests.get(api_url, headers=headers)

    return response.json()['events']


def get_next_or_current_meeting_info() -> dict or None:
    """
    Returns information about the next practice session as dictionary

    ** Will return the next meeting info the day after a race (all in utc) **

    ** Will return None if there is no next meeting because the season is over **

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



if __name__ == "__main__":
    print(season_api_is_showing())

    print(get_list_of_event_dictionaries())

    print(get_next_or_current_meeting_info())

    print(get_first_session_start_of_upcoming_or_current_meeting_in_utc())
