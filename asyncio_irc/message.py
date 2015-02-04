class Message:
    """A message recieved from the IRC network."""

    def __init__(self, raw_message):
        self.raw = raw_message
        self.prefix, self.command, self.params, self.suffix = self.elements()

    def elements(self):
        """
        Split the raw message into it's component parts.

        Adapted from http://stackoverflow.com/a/930706/400691
        """
        message = self.raw.strip()

        prefix = b''
        if message[0:1] == b':':  # Odd slicing required for bytes
            prefix, message = message[1:].split(b' ', 1)

        suffix = b''
        if b' :' in message:
            message, suffix = message.split(b' :', 1)

        command, *params = message.split()
        params = list(filter(None, params))

        return prefix, command, params, suffix
