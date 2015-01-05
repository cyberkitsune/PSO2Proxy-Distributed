CommandHandlers = {}


class CommandHandler(object):
    def __init__(self, command):
        self.command = command

    def __call__(self, f):
        CommandHandlers[self.command] = f
