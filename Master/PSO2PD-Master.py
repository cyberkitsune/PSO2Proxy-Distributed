import json
import os
import struct
import socket
from twisted.internet import stdio

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.protocols import basic

from WebAPI import setup_web

from PSO2Protocols import shipdata, ShipInfoFactory, BlockSenderFactory
from Commands import Commands
from ProxyRedis import p, r, redis_config


class ServerConsole(basic.LineReceiver):
    def __init__(self):
        self.delimiter = os.linesep

    def connectionMade(self):
        self.transport.write('>>> ')

    def lineReceived(self, line):
        """

        :type line: str
        """
        command = line.split(' ')[0]
        if command in Commands:
            if len(line.split(' ')) > 1:
                Commands[command](line.split(' ', 1)[1])
            else:
                Commands[command](line)
        else:
            print("[PSO2PD] Command not found.")
        self.transport.write('>>> ')

print("=== PSO2Proxy-Distributed master server starting...")

rthread = p.run_in_thread(sleep_time=0.001)

print("[Redis] Messaging thread running.")

print("[PSO2PD] Getting ship statuses...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(("210.189.208.1", 12199))  # Un-hardcode this!
    shipdata.write(s.recv(4))
    size = struct.unpack_from("i", shipdata.getvalue())[0]
    shipdata.write(s.recv(size - 4))

except:
    print("[PSO2PD] I got an error :(")

print("[PSO2PD] Cached ship query.")

print("[PSO2PD] Starting reactors...")

for x in xrange(0, 10):
    endpoint = TCP4ServerEndpoint(reactor, 12000 + (100 * x), interface=redis_config['bindip'])
    endpoint.listen(BlockSenderFactory())

for x in xrange(0, 10):
    endpoint = TCP4ServerEndpoint(reactor, 12099 + (100 * x), interface=redis_config['bindip'])
    endpoint.listen(ShipInfoFactory())

stdio.StandardIO(ServerConsole())

print("[PSO2PD] Reactor started.")

print("[PSO2PD] Announcing presence...")
r.publish("proxy-global", json.dumps({'command': "register"}))

setup_web()

reactor.run()

rthread.stop()