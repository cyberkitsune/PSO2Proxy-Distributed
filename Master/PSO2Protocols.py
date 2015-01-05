from twisted.internet import protocol
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


class BlockSender(protocol.Protocol):
    def __init__(self):
        pass

    def connectionMade(self):
        # Get some IP
        ip = "127.0.0.1"
        # Do stuff


class BlockSenderFactory(protocol.Factory):
    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return BlockSender()