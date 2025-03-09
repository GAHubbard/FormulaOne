import utils
import requests
import datetime
import json
from FormulaOne.assets.application import app
import time
        
def get_schedule() -> dict:
    year = datetime.date.today().year
    schedule_scheme = 'https'
    schedule_netloc = 'livetiming.formula1.com'
    schedule_path = f'/static/{year}/Index.json'
    schedule_url = utils.create_url(scheme=schedule_scheme, netloc=schedule_netloc, path=schedule_path)
    response = requests.get(schedule_url)
    schedule = json.loads(response.content)
    return schedule

def detect_race():
    schedule = get_schedule()
    meetings = schedule['Meetings']
    while True:
        current_time = datetime.datetime.now(datetime.timezone.utc)
        for meeting in meetings:
            sessions = meeting['Sessions']
            for session in sessions:
                start_time = datetime.datetime.fromisoformat(session['StartDate']).replace(tzinfo=datetime.timezone.utc)
                time_diff = start_time-current_time
                if 0 < time_diff.total_seconds() < 900:
                    race_path = session['Path']
                    app.main(race_path)
        time.sleep(600)


if __name__ == "__main__":
    detect_race()