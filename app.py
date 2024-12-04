"""
I don't know, I guess some stuff goes here
"""

from connections import WebSocket
import asyncio
import time
from datetime import datetime
import json


async def main():
    output_file = open(f'output-{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.txt', 'a')
    session = WebSocket()
    async with session.connection() as conn:
        await session.send_data(conn)
        previous_heartbeat = None
        while True:
            data = await session.receive_data(conn)
            data_decoded = json.loads(data)
            if 'R' in data_decoded:
                output_file.write(data + '\n')
                current_heartbeat = data_decoded['R']['ExtrapolatedClock']['Utc']
                if current_heartbeat != previous_heartbeat:
                    count = 0
                    previous_heartbeat = current_heartbeat
                else:
                    count =+ 1
                exit() if count >= 100 else await session.send_data(conn)


if __name__ == "__main__":
    asyncio.run(main())