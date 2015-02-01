class Listener:
    def __init__(self, handler):
        self.handler = handler

    def handle(self, connection, message):
        self.handler(connection, message=message)


class CommandListener(Listener):
    def __init__(self, command, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = command

    def handle(self, connection, message):
        if message.command == self.command:
            super().handle(connection, message)

# class RegexListener(Listener):
#     def __init__(self, regex, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.regex = regex
