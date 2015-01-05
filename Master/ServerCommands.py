from ProxyServer import ProxyServers, ProxyServer

CommandHandlers = {}


class CommandHandler(object):
    def __init__(self, command):
        self.command = command

    def __call__(self, f):
        CommandHandlers[self.command] = f


@CommandHandler("newserver")
def new_server(messageobj):
    s = ProxyServer(messageobj['ip'], messageobj['name'])
    if s.name not in ProxyServers:
        ProxyServers[s.name] = s