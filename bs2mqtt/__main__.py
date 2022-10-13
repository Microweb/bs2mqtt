import argparse

from .commands import ScanCommand, ServeCommand, InitCommand


COMMANDS = {
    "scan": ScanCommand(),
    "init": InitCommand(),
    "serve": ServeCommand(),
}

def main():
    root = argparse.ArgumentParser(prog='PROG')

    sub = root.add_subparsers(dest='command')
    scan_parser = sub.add_parser('scan')
    scan_parser.add_argument('-i', '--listen-ip', default='', help='IP to listen incoming packets on. Default: all available ips')
    scan_parser.add_argument('-b', '--broadcast-ip', default='255.255.255.255', help='Broadcast address. Default: 255.255.255.255')

    init_parser = sub.add_parser('init')
    init_parser.add_argument('-c', '--config', default='', help='IP to listen incoming packets on. Default: all available ips')

    serve_parser = sub.add_parser('serve')
    serve_parser.add_argument('-c', '--config', default='', help='IP to listen incoming packets on. Default: all available ips')

    args = root.parse_args()
    COMMANDS[args.command].execute(args)




if __name__ == '__main__':
    main()