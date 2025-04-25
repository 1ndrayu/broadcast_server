import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            await broadcast(message)
    except websockets.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)

async def broadcast(message):
    if connected_clients:
        await asyncio.wait([client.send(message) for client in connected_clients])

def start_server():
    print("Starting broadcast server on ws://localhost:6789")
    server = websockets.serve(handler, "localhost", 6789)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
