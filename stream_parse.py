import json
import requests


response = requests.get('https://livetiming.formula1.com/static/2025/2025-03-16_Australian_Grand_Prix/2025-03-16_Race/Index.json')
stream_data = json.loads(response.content)

for feed in stream_data['Feeds']:
    output_file = open(f'jsonstreams_output_files/{feed}_jsonstream.txt', 'w')
    feed_response = requests.get(f'https://livetiming.formula1.com/static/2025/2025-03-16_Australian_Grand_Prix/2025-03-16_Race/{stream_data['Feeds'][feed]['StreamPath']}')
    output_file.write(feed_response.content.decode('utf-8-sig'))
