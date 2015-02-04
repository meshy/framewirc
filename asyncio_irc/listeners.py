class Listener:
    """Always invokes the handler."""
    def __init__(self, handler):
        self.handler = handler

    def handle(self, connection, message):
        self.handler(connection, message=message)


class CommandListener(Listener):
    """Only invokes the handler on one particular command."""
    def __init__(self, command, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = command

    def handle(self, connection, message):
        if message.command == self.command:
            super().handle(connection, message)


class WhitelistListener(Listener):
    """Invokes the handler for a whitelist of commands."""
    def __init__(self, whitelist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.whitelist = whitelist

    def handle(self, connection, message):
        if message.command in self.whitelist:
            super().handle(connection, message)


class BlacklistListener(Listener):
    """Invokes the handler for all but a blacklist of commands."""
    def __init__(self, blacklist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blacklist = blacklist

    def handle(self, connection, message):
        if message.command not in self.blacklist:
            super().handle(connection, message)
