import utils
import requests
import datetime
import json
import app
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
                gmt_offset = session['GmtOffset'].split(':')
                start_time_local = datetime.datetime.fromisoformat(session['StartDate'])
                start_time_utc = start_time_local-datetime.timedelta(hours=int(gmt_offset[0]), minutes=int(gmt_offset[1]), seconds=int(gmt_offset[2]))
                start_time_utc = start_time_utc.replace(tzinfo=datetime.timezone.utc)
                time_diff = current_time-start_time_utc
                print(time_diff)
                if 0 < time_diff.total_seconds() < 900:
                    race_path = session['Path']
                    app.main(race_path)
        time.sleep(600)


if __name__ == "__main__":
    detect_race()