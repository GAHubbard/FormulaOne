"""
Description
"""


class SignalR:


    def __init__(self):
        self._hub = 'Streaming'
        self._method = 'Subscribe'
        self._iterator = None
        self._topics = [["Heartbeat", "CarData.z", "Position.z",
                            "ExtrapolatedClock", "TopThree", "RcmSeries",
                            "TimingStats", "TimingAppData",
                            "WeatherData", "TrackStatus", "DriverList",
                            "RaceControlMessages", "SessionInfo",
                            "SessionData", "LapCount", "TimingData"]]
        self._session = None


    