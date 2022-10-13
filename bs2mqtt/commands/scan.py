from pysecur3.MCP import MCPDiscover

from ..abc import ICommmand


class ScanCommand(ICommmand):
    def execute(self, args):
        disc = MCPDiscover(args.listen_ip, args.broadcast_ip)
        disc.run()

        if len(disc.devices) > 0:
            for ip in disc.devices:
                print('Found device on address: %s, device attributes: %s ' % (ip, disc.devices[ip]))
        else:
            print('No found any device!')
