import asyncio
import websockets
import threading
from colorama import Fore, Style, init

init(autoreset=True)

async def connect_to_server():
    uri = "ws://localhost:6789"
    username = input("Enter your username: ")

    async with websockets.connect(uri) as websocket:
        await websocket.send(username)
        print(Fore.YELLOW + f"Connected to the server as @{username}\n")

        receive_task = asyncio.create_task(receive_messages(websocket, username))
        input_task = asyncio.create_task(send_messages(websocket, username))

        await asyncio.gather(receive_task, input_task)

async def receive_messages(websocket, username):
    try:
        async for message in websocket:
            if f"@{username}:" in message:
                print(Fore.GREEN + message)  # Your own message
            elif "joined the chat" in message or "left the chat" in message:
                print(Fore.LIGHTBLACK_EX + message)  # System message
            else:
                print(Fore.CYAN + message)  # Others' messages
    except websockets.ConnectionClosed:
        print(Fore.RED + "Disconnected from server.")

async def send_messages(websocket, username):
    while True:
        msg = input()
        if msg.strip() != "":
            await websocket.send(msg)
