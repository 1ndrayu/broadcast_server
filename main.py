import argparse
from server import start_server
from client import connect_to_server
import asyncio

def main():
    parser = argparse.ArgumentParser(description="Broadcast Server CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("start", help="Start the broadcast server")
    subparsers.add_parser("connect", help="Connect to the broadcast server as a client")

    args = parser.parse_args()

    if args.command == "start":
        start_server()
    elif args.command == "connect":
        asyncio.run(connect_to_server())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
