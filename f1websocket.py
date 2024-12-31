"""
This file contains the F1WebSocket class, which handles the negotiation, connection, sending and recieving of data for the websocket connnection to the F1 livetiming server.
Created by: Graham Hubbard
Date: 2024-12-28
"""


import websocket
from websocket import WebSocket
import requests
from requests import Response
import json
from utils import *


class F1WebSocket:

    def __init__(self):
        self.url = 'livetiming.formula1.com/signalr'
        self._cookie = None
        self._token = None
        self._message_count = 0
    
    @property
    def _headers(self):
        return {'User-Agent': 'BestHTTP', 'Accept-Encoding': 'gzip,identity', 'Cookie': self._cookie, 'Connection': 'keep-alive, Upgrade'}

    @property
    def _parameters(self):
        return {"clientProtocol": "1.5", "transport": "websockets", "connectionToken": self._token, "connectionData": [{"name":"Streaming"}]}

    @property
    def invoke_data(self):
        self._increase_message_count()
        return json.dumps({"H": "Streaming", "M": "Subscribe", "A": [["Heartbeat", "CarData.z", "Position.z",
                            "ExtrapolatedClock", "TopThree", "RcmSeries",
                            "TimingStats", "TimingAppData",
                            "WeatherData", "TrackStatus", "DriverList",
                            "RaceControlMessages", "SessionInfo",
                            "SessionData", "LapCount", "TimingData"]], "I": self._message_count})

    def _create_handshake(self) -> str:
        """
        Returns url for handshake
        """
        handshake_action = 'negotiate'
        handshake_connection_type = 'https'
        handshake_url = create_url(self.url, handshake_connection_type, handshake_action)
        return handshake_url

    def _initiate_handshake(self) -> Response:
        """
        Returns response from handshake 
        """
        handshake_url = self._create_handshake()
        response = requests.get(handshake_url)
        return response

    def _get_token_and_cookie(self):
        """
        Returns token from handshake response body and cookie from header
        """
        response = self._initiate_handshake()
        self._token = json.loads(response.content)['ConnectionToken']
        self._cookie = response.headers['Set-Cookie']

    def _create_websocket(self) -> str:
        """
        Returns url for websocket
        """
        websocket_action = 'connect'
        websocket_connection_type = 'wss'
        self._get_token_and_cookie()
        websocket_url = create_url(self.url, websocket_connection_type, websocket_action, self._parameters)
        return websocket_url

    def connection(self) -> WebSocket:
        """
        Returns a websocket connection to F1 livetiming
        """
        return  websocket.create_connection(self._create_websocket(), header=self._headers)

    def _increase_message_count(self):
        """
        Increases message count by 1
        """
        self._message_count += 1
        