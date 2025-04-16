"""
Contains useful ways to get schedule information using F1's API
"""

import load_dotenv
import os
import requests

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


def get_next_or_current_practice_session_info() -> dict:
    """
    Returns information about the next practice session as dictionary

    ** Will return the current practice session info until the day after the final race all converted to UTC **

    :return:
    """

    pass


if __name__ == "__main__":
    print(season_api_is_showing())

    print(get_list_of_event_dictionaries())
