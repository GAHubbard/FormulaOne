"""
Description
"""

import websockets
from websockets.asyncio.client import ClientConnection
import requests
from requests import Response
import json
from ._utilities import Utilities
import asyncio


class WebSocket:


    def __init__(self):
        self.url = 'livetiming.formula1.com/signalr'
        self._cookie = None
        self._token = None
        self._headers = {'User-Agent': 'BestHTTP', 'Accept-Encoding': 'gzip,identity', 'Cookie': self._cookie}
        self._parameters = {"clientProtocol": "1.5", "transport": "websockets", "connectionToken": self._token, "connectionData": [{"name":"Streaming"}]}
        self._topics = json.dumps({"H": "Streaming", "M": "Subscribe", "A": [["Heartbeat", "CarData.z", "Position.z",
                            "ExtrapolatedClock", "TopThree", "RcmSeries",
                            "TimingStats", "TimingAppData",
                            "WeatherData", "TrackStatus", "DriverList",
                            "RaceControlMessages", "SessionInfo",
                            "SessionData", "LapCount", "TimingData"]], "I": 1})


    def _create_handshake(self) -> str:
        """
        Returns url for handshake
        """
        handshake_action = 'negotiate'
        handshake_connection_type = 'https'
        handshake_url = Utilities.create_url(self.url, handshake_connection_type, handshake_action)
        return handshake_url
    

    def _initiate_handshake(self) -> Response:
        """
        Returns response from handshake 
        """
        handshake_url = self._create_handshake()
        response = requests.get(handshake_url)
        print
        return response
    

    def _get_token(self) -> str:
        """
        Returns token from handshake response body
        """
        self._token = json.loads( self._initiate_handshake().content)['ConnectionToken']
        return self._token


    def _get_cookie(self) -> str:
        """
        Returns cookie from handshake response headers
        """ 
        self._cookie = self._initiate_handshake().headers['Set-Cookie']
        return self._cookie
    

    def _create_websocket(self) -> str:
        """
        
        """
        websocket_action = 'connect'
        websocket_connection_type = 'wss'
        self._get_token()
        websocket_url = Utilities.create_url(self.url,  websocket_connection_type, websocket_action, self._parameters)
        return websocket_url

    async def connection(self) -> ClientConnection:
        self._get_cookie()
        async with websockets.connect(self._create_websocket(), additional_headers=self._headers) as conn:
            await self.send_data(conn)
            data = await self.receive_data(conn)
            return data


    def send_data(self, ws: ClientConnection):
        ws.send(self._topics)


    def receive_data(self, ws: ClientConnection):
        data = ws.recv()
        return data
        