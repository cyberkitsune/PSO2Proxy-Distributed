import redis
import json
import struct
import socket
import io
from ProxyServer import ProxyServers
from PSO2Protocols import shipdata
from ServerCommands import CommandHandlers
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