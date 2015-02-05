from .utils import to_bytes


class Message:
    """A message recieved from the IRC network."""

    def __init__(self, raw_message):
        self.raw = raw_message
        self.prefix, self.command, self.params, self.suffix = self._elements()

    def _elements(self):
        """
        Split the raw message into it's component parts.

        Adapted from http://stackoverflow.com/a/930706/400691
        """
        message = self.raw.strip()

        prefix = b''
        # Odd slicing required for bytes to avoid getting int instead of char
        # http://stackoverflow.com/q/28249597/400691
        if message[0:1] == b':':
            prefix, message = message[1:].split(b' ', 1)

        suffix = b''
        if b' :' in message:
            message, suffix = message.split(b' :', 1)

        command, *params = message.split()
        params = list(filter(None, params))

        return prefix, command, params, suffix


def message_bytes(command, prefix=b'', params=None, suffix=b''):
    command = to_bytes(command)
    prefix = to_bytes(prefix)
    params = list(map(to_bytes, params or []))
    suffix = to_bytes(suffix)

    message = command
    if prefix:
        message = b':' + prefix + b' ' + message
    if params:
        params = b' '.join(params)
        message = message + b' ' + params
    if suffix:
        message = message + b' :' + suffix
    return message
