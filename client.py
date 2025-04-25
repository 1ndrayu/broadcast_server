import asyncio
import websockets

async def connect_to_server():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        print("Connected to server. Type messages to send:")
        asyncio.create_task(receive_messages(websocket))
        while True:
            msg = input()
            await websocket.send(msg)

async def receive_messages(websocket):
    async for message in websocket:
        print(f"\n[Broadcast] {message}")
