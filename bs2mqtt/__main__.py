import asyncio
import argparse
from email.policy import default
import inspect
import os
import pathlib

from .commands import ScanCommand, ServeCommand, InitCommand


COMMANDS = {
    "scan": ScanCommand(),
    "init": InitCommand(),
    "serve": ServeCommand(),
}

def main():
    cwd = pathlib.Path.cwd()
    default_file = str(cwd / "configuration.json")

    root = argparse.ArgumentParser(prog="PROG")

    sub = root.add_subparsers(dest="command")
    scan_parser = sub.add_parser("scan")
    scan_parser.add_argument("-i", "--listen-ip", default="", help="IP to listen incoming packets on. Default: all available ips")
    scan_parser.add_argument("-b", "--broadcast-ip", default="255.255.255.255", help="Broadcast address. Default: 255.255.255.255")

    init_parser = sub.add_parser("init")
    init_parser.add_argument("--config", default=default_file, help="Path to configuration file")

    serve_parser = sub.add_parser("serve")
    serve_parser.add_argument("--config", default=default_file, help="Path to configuration file")

    args = root.parse_args()
    try:
        command = COMMANDS[args.command]
    except KeyError:
        print(f"Unknown command. (expected: {list(COMMANDS.keys())})")
    else:
        try:
            result = command.execute(args)
            if inspect.iscoroutine(result):
                asyncio.run(result)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()