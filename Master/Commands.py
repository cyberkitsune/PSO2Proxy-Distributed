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

    for server in ProxyServers:
        r.publish("proxy-server-%s" % server.name, json.dumps({'command': 'exec', 'input': line}))
        print("[PSO2PD] Sent command \"%s\" to %s" % (line, server.name))


@CommandHandler("list")
def list(line):
    from ProxyServer import ProxyServers
    for server in ProxyServers:
        print("[List] Server \"%s\" - Usercount %i" % (server.name, server.users))
    print("[List] %i proxy servers connected in total." % len(ProxyServers))