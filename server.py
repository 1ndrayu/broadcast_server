import asyncio
import websockets
from datetime import datetime

connected_clients = {}

async def handler(websocket, path):
    try:
        username = await websocket.recv()
        connected_clients[websocket] = username
        await broadcast(f"{username} has joined the chat.")

        async for message in websocket:
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_msg = f"[{timestamp}] @{username}: {message}"
            await broadcast(formatted_msg)

    except websockets.ConnectionClosed:
        pass
    finally:
        username = connected_clients.get(websocket, "Unknown")
        connected_clients.pop(websocket, None)
        await broadcast(f"{username} has left the chat.")

async def broadcast(message):
    if connected_clients:
        await asyncio.wait([client.send(message) for client in connected_clients])

def start_server():
    print("Starting broadcast server on ws://localhost:6789")
    server = websockets.serve(handler, "localhost", 6789)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
