import json
import requests


response = requests.get('https://livetiming.formula1.com/static/2024/2024-11-23_Las_Vegas_Grand_Prix/2024-11-22_Practice_3/Index.json')
stream_data = json.loads(response.content)

for feed in stream_data['Feeds']:
    output_file = open(f'output\{feed}_jsonstream.txt', 'w')
    feed_response = requests.get(f'https://livetiming.formula1.com/static/2024/2024-11-23_Las_Vegas_Grand_Prix/2024-11-22_Practice_3/{stream_data['Feeds'][feed]['StreamPath']}')
    output_file.write(feed_response.content.decode('utf-8-sig'))
