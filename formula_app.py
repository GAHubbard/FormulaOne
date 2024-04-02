import requests
import json
import asyncio
import websockets
import urllib      
import time                      


def create_url(type: str, url: str, action: str, parameters: dict) -> str:
    connection_type = 'wss' if type == 'websocket' else 'https'
    parameters_encoded = urllib.parse.urlencode(parameters)
    url_unparsed = f'{connection_type}://{url}/{action}?{parameters_encoded}'
    return url_unparsed


def get_handshake() -> requests.Response:
    raw_url = 'livetiming.formula1.com/signalr'
    get_parameters = {"connectionData": [{"name":"Streaming"}], "clientProtocol": "1.5"}
    get_action = 'negotiate'
    get_connection_type = 'rest'
    get_url = create_url(get_connection_type, raw_url, get_action, get_parameters)
    response = requests.get(get_url)
    return response


async def handler(url: str, headers: dict, data: json):
    output_file = open('output.txt', 'a')
    i = 0
    async with websockets.connect(url, extra_headers=headers) as ws:
        while i < 100:
            start_time = time.time()
            await ws.send(data)
            response = await ws.recv()
            time_split = time.time()-start_time
            if 'R' in json.loads(response):
                output_file.write(str(time_split) + ' ' + response + '\n')
            i += 1


async def establish_websocket_session(token: str, cookie: str):
    raw_url = 'livetiming.formula1.com/signalr'
    # Create websocket headers with cookie
    wss_data = json.dumps({"H": "Streaming", "M": "Subscribe", "A": [["Heartbeat", "CarData.z", "Position.z",
                            "ExtrapolatedClock", "TopThree", "RcmSeries",
                            "TimingStats", "TimingAppData",
                            "WeatherData", "TrackStatus", "DriverList",
                            "RaceControlMessages", "SessionInfo",
                            "SessionData", "LapCount", "TimingData"]], "I": 1})
    wss_headers = {'User-Agent': 'BestHTTP', 'Accept-Encoding': 'gzip,identity', 'Cookie': cookie}
    wss_parameters = {"clientProtocol": "1.5", "transport": "websockets", "connectionToken": token, "connectionData": [{"name":"Streaming"}]}
    wss_action = 'connect'
    wss_connection_type = 'websocket'
    # Create websocket connection url with conneciton token
    wss_url = create_url(wss_connection_type, raw_url, wss_action, wss_parameters)
    await handler(wss_url, wss_headers, wss_data)


async def connection():
    # headers_encoded = json.dumps(headers) if headers is not None else ''
    get_response = get_handshake()
    # Retreve connection token from response body
    token = json.loads(get_response.content)['ConnectionToken']
    # Retrieve cookie from response header
    cookie = get_response.headers['Set-Cookie']
    await establish_websocket_session(token, cookie)


if __name__ == "__main__":
    asyncio.run(connection())