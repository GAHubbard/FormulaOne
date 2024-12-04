import sys
import requests
from requests import Response
import json
import websocket
import urllib      
import time
from datetime import datetime
import threading
import asyncio
import aioconsole  # package used for awaiting io inputs from user

running: bool = True

def create_url(type: str, action: str, parameters: dict) -> str:
    """
    Returns url based given on connection type, action and parameters
    """
    url = 'livetiming.formula1.com/signalr'
    connection_type = 'wss' if type == 'websocket' else 'https'
    parameters_encoded = urllib.parse.urlencode(parameters) 
    url_unparsed = f'{connection_type}://{url}/{action}{"?" if parameters_encoded else ""}{parameters_encoded}'
    return url_unparsed


def get_handshake() -> Response:
    """
    Creates handshake connection and returns token and cookie
    """
    get_parameters = {"connectionData": [{"name":"Streaming"}], "clientProtocol": "1.5"}
    get_action = 'negotiate'
    get_connection_type = 'rest'
    get_url = create_url(get_connection_type, get_action, get_parameters)
    response = requests.get(get_url)
    return response


def create_websocket_connection(token: str, cookie: str):
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
    wss_url = create_url(wss_connection_type, wss_action, wss_parameters)
    return wss_url, wss_headers, wss_data


def data_retriever(url: str, headers: dict, data: json):
    output_file = open(f'output-{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.txt', 'a')
    heartbeat = None
    global running
    ws = websocket.create_connection(url, additional_headers=headers)
    while running:
        print("\nin the retrieve data loop")
        ws.send(data)
        response = ws.recv()
        response_dict = json.loads(response)
        if 'R' in response_dict:
            current_heartbeat = response_dict['R']['Heartbeat']['Utc']
            #print(heartbeat, current_heartbeat)
            if heartbeat is None:
                heartbeat = current_heartbeat
                output_file.write(response + '\n')
            elif current_heartbeat != heartbeat:
                heartbeat = current_heartbeat
            # response_dict = json.loads(response)
            # cardata_z = response_dict['R']['CarData.z'] + 'CarData.z.jsonStream'
            # await get_car_data(cardata_z, headers=headers)
                output_file.write(response + '\n')
        time.sleep(5)


"""
async def get_car_data(data_path, headers):
    connection = 'rest'
    car_data_url = create_url(connection, data_path, {})
    response = requests.post(car_data_url, headers)
    print(response)
"""


def user_input_cli():
    """
    User input loop
    :return:
    """
    global running

    while running:
        i: str = input("Press Q to quit:")
        if i == 'Q':
            running = False


def main():
    # headers_encoded = json.dumps(headers) if headers is not None else ''
    get_response = get_handshake()
    # Retrieve connection token from response body
    token = json.loads(get_response.content)['ConnectionToken']
    # Retrieve cookie from response header
    cookie = get_response.headers['Set-Cookie']
    websocket = create_websocket_connection(token, cookie)

    user_input_thread = threading.Thread(target=user_input_cli)
    data_retrieval_thread = threading.Thread(target=data_retriever, args=(websocket[0],websocket[1],websocket[2]))

    data_retrieval_thread.start()
    user_input_thread.start()
    data_retrieval_thread.join()
    data_retrieval_thread.join()

if __name__ == "__main__":
    main()