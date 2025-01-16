import zlib
import base64


def get_car_telemetry_data(data):
    if ['R'] in data:
        heartbeat = data['R']['Heartbeat']['Utc']
        zipped_data = data['R']['CarData.z']
        unzipped_data = zlib.decompress(base64.b64decode(zipped_data), -zlib.MAX_WBITS)
        unzipped_data.decode('utf-8-sig')

def get_car_position_data(data):
    pass