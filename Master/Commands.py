import json

Commands = {}


class CommandHandler():
    def __init__(self, command):
        self.command = command

    def __call__(self, f):
        Commands[self.command] = f


@CommandHandler("allexec")
def allexec(line):
    from ProxyRedis import r
    from ProxyServer import ProxyServers

    for server in ProxyServers.values():
        r.publish("proxy-server-%s" % server.name, json.dumps({'command': 'exec', 'input': line}))
        print("[PSO2PD] Sent command \"%s\" to %s" % (line, server.name))


@CommandHandler("list")
def list(line):
    from ProxyServer import ProxyServers
    for server in ProxyServers.values():
        print("[List] Server \"%s\" - Usercount %i - Enabled %s" % (server.name, server.users, server.enabled))
    print("[List] %i proxy servers connected in total." % len(ProxyServers))


@CommandHandler("disable")
def disable(line):
    from ProxyServer import ProxyServers
    if line in ProxyServers:
        ProxyServers[line].enabled = not ProxyServers[line].enabled
        print("Toggled %s enable state." % ProxyServers[line].name)
    else:
        print("Not a proxy server")