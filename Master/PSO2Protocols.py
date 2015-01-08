from twisted.internet import protocol
from ProxyServer import ProxyServers

import struct
import io

shipdata = io.BytesIO()


class ShipInfo(protocol.Protocol):
    def __init__(self):
        pass

    def connectionMade(self):
        self.transport.write(shipdata.getvalue())
        self.transport.loseConnection()


class ShipInfoFactory(protocol.Factory):
    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return ShipInfo()


def get_users(server):
    return server.users


class BlockSender(protocol.Protocol):
    def __init__(self):
        pass

    def connectionMade(self):
        if len(ProxyServers) < 1:
            self.transport.loseConnection()
            return
        servers = sorted(ProxyServers.values(), key=get_users)
        server = None
        for pserver in servers:
            if pserver.enabled:
                server = pserver
                break
        if server is None:
            self.transport.loseConnection()
            return
        o1, o2, o3, o4 = server.address.split(".")
        buf = bytearray()
        buf += struct.pack('i', 0x90)
        buf += struct.pack('BBBB', 0x11, 0x2C, 0x0, 0x0)
        buf += struct.pack('92x')  # lol SEGA
        buf += struct.pack('BBBB', int(o1), int(o2), int(o3), int(o4))
        buf += struct.pack('H', self.transport.getHost().port)
        buf += struct.pack('38x')

        print("[BlockSend] Sending client to server %s currently with %i users." % (server.name, server.users))
        server.users += 1
        self.transport.write(str(buf))
        self.transport.loseConnection()


class BlockSenderFactory(protocol.Factory):
    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return BlockSender()