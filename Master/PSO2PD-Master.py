import struct
import socket

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

from PSO2Protocols import shipdata, ShipInfoFactory, BlockSenderFactory
from ProxyRedis import p


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
    endpoint = TCP4ServerEndpoint(reactor, 12000 + (100 * x))
    endpoint.listen(BlockSenderFactory())

for x in xrange(0, 10):
    endpoint = TCP4ServerEndpoint(reactor, 12099 + (100 * x))
    endpoint.listen(ShipInfoFactory())

print("[PSO2PD] Reactor started.")

reactor.run()