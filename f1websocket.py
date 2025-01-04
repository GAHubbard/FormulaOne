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
import utils


class F1WebSocket:

    def __init__(self, feeds):
        self.netloc = 'livetiming.formula1.com/signalr'
        self._cookie = None
        self._token = None
        self._message_count = 0
        self.feeds = feeds
    
    @property
    def _headers(self):
        return {'User-Agent': 'BestHTTP', 'Accept-Encoding': 'gzip,identity', 'Cookie': self._cookie, 'Connection': 'keep-alive, Upgrade'}

    @property
    def _parameters(self):
        return {"clientProtocol": "1.5", "transport": "websockets", "connectionToken": self._token, "connectionData": [{"name":"Streaming"}]}

    @property
    def invoke_data(self):
        self._increase_message_count()
        return json.dumps({"H": "Streaming", "M": "Subscribe", "A": [self.feeds], "I": self._message_count})

    def _create_handshake(self) -> str:
        """
        Returns url for handshake
        """
        handshake_path = '/negotiate'
        handshake_scheme = 'https'
        handshake_url = utils.create_url(scheme = handshake_scheme, netloc = self.netloc,  path = handshake_path)
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
        websocket_path = '/connect'
        websocket_scheme = 'wss'
        self._get_token_and_cookie()
        websocket_url = utils.create_url(scheme = websocket_scheme, netloc = self.netloc, path = websocket_path, query_parameters = self._parameters)
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
        