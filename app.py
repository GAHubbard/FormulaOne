"""
I don't know, I guess some stuff goes here
"""

from connections import WebSocket
import asyncio


async def main():
    session = WebSocket()
    await session.connection()
    """    async with session.connection() as conn:
        await session.send_data(conn)
        data = await session.receive_data(conn)
        print(data)"""
    


if __name__ == "__main__":
    asyncio.run(main())


