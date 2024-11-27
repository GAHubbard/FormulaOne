"""
Description
"""


import json


class SignalR:


    def __init__(self):
        self._hub = 'Streaming'
        self._method = 'Subscribe'
        self._id = 1
        self._arguments = [["Heartbeat", "CarData.z", "Position.z",
                            "ExtrapolatedClock", "TopThree", "RcmSeries",
                            "TimingStats", "TimingAppData",
                            "WeatherData", "TrackStatus", "DriverList",
                            "RaceControlMessages", "SessionInfo",
                            "SessionData", "LapCount", "TimingData"]]


    def invoke(self):
        data = {'H':self._hub,
                'M': self._method,
                'A': self._arguments,
                'I': self._id}
        return json.dumps(data)