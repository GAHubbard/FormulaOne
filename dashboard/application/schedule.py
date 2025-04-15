"""
File contains functions related to the schedule


"""
import datetime

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


def has_f1_posted_the_upcoming_schedule_info() -> (bool, str):
    """
    Returns whether or not f1 has posting the upcoming schedule

    ** ALL TIMES ARE IN ZULU **

    Truth Table

    Once...

    :return:
    """
    pass


if __name__ == "__main__":
    """
    Test code for this module
    """

    print(f"Current or Upcoming Race: {get_upcoming_or_current_meeting_slash_race_as_dict()}")

    print(f"All Races So Far Including Current: {get_all_meetings_slash_races()}")

    print(f"Next Race: {get_next_or_upcoming_location()}")

    print(f"Is the current week or upcoming week a sprint weekend?: {'Yes' if is_current_or_upcoming_week_sprint() else 'No'}")

