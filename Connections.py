"""
Description
"""

import websockets
import requests
from requests import Response
from urllib.parse import urlencode
import json

class Utilities:


    def create_url(url: str, connection_type: str, action: str, parameters = {}) -> str:
        """
        Returns encoded url with given url connection type, action and parameters
        """
        parameters_encoded = urlencode(parameters) 
        encoded_url = f'{connection_type}://{url}/{action}{"?" if parameters_encoded else ""}{parameters_encoded}'
        return encoded_url


class WebSocket:


    def __init__(self) -> None:
        self.url = 'livetiming.formula1.com/signalr'
        self._cookie = None
        self._token = None
        self._headers = {'User-Agent': 'BestHTTP', 'Accept-Encoding': 'gzip,identity', 'Cookie': self._cookie}
        self._parameters = {"clientProtocol": "1.5", "transport": "websockets", "connectionToken": self._token, "connectionData": [{"name":"Streaming"}]}
        pass


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
        return response
    

    def _get_token(self) -> str:
        """
        Returns token from handshake response body
        """
        self._token = json.loads(self._initiate_handshake)['ConnectionToken']


    def _get_cookie(self) -> str:
        """
        Returns cookie from handshake response headers
        """ 
        self._cookie = self._initiate_handshake.headers['Set-Cookie']
    

    def _create_websocket(self):
        """
        
        """
        websocket_action = 'connect'
        websocket_connection_type = 'wss'
        websocket_url = Utilities.create_url(self.url,  websocket_connection_type, websocket_action)
        return websocket_url

    async def session(self):
        with websockets.connect(self._create_websocket(), additional_headers=self._headers) as session:
            self._send_data(session)
            while True:
                response = await self._receive_data(session)


    def _send_data(self, ws):
        topics = json.dumps({"H": "Streaming", "M": "Subscribe", "A": [["Heartbeat", "CarData.z", "Position.z",
                            "ExtrapolatedClock", "TopThree", "RcmSeries",
                            "TimingStats", "TimingAppData",
                            "WeatherData", "TrackStatus", "DriverList",
                            "RaceControlMessages", "SessionInfo",
                            "SessionData", "LapCount", "TimingData"]], "I": 1})
        ws.send(topics)


    def _receive_data(self, ws):
        data = ws.recv()
        return data
        