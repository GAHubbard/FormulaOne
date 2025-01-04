import utils
import requests
from requests import Response
import datetime
import json
        
def get_schedule() -> dict:
    year = '2024' #datetime.date.today().year
    schedule_scheme = 'https'
    schedule_netloc = 'livetiming.formula1.com'
    schedule_path = f'/static/{year}/Index.json'
    schedule_url = utils.create_url(scheme=schedule_scheme, netloc=schedule_netloc, path=schedule_path)
    response = requests.get(schedule_url)
    schedule = json.loads(response.content)
    return schedule

def detect_race():
    schedule = get_schedule()
    current_date = '2024-06-30' #datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    meetings = schedule['Meetings']
    for meeting in meetings:
        sessions = meeting['Sessions']
        for session in sessions:
            if current_date in session['StartDate']:
                print(session['Path'])



#detect_race()
start_time = datetime.datetime.fromisoformat('2024-06-30T15:00:00')
current_time = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
print(start_time, current_time)