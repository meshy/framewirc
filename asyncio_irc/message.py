from . import commands, exceptions
from .utils import chunk_message, LINEFEED, to_bytes, to_unicode


MAX_LENGTH = 512  # The largest legal size of an IRC command.


class ReceivedMessage(bytes):
    """A message recieved from the IRC network."""

    def __init__(self, raw_message_bytes_ignored):
        super().__init__()
        self.prefix, self.command, self.params, self.suffix = self._elements()

    def _elements(self):
        """
        Split the raw message into it's component parts.

        Adapted from http://stackoverflow.com/a/930706/400691
        """
        message = to_unicode(self.strip())

        prefix = ''
        # Odd slicing required for bytes to avoid getting int instead of char
        # http://stackoverflow.com/q/28249597/400691
        if message[0:1] == ':':
            prefix, message = message[1:].split(' ', 1)

        suffix = ''
        if ' :' in message:
            message, suffix = message.split(' :', 1)

        command, *params = message.split()
        params = tuple(filter(None, params))

        return prefix, command, params, suffix


def build_message(command, *args, prefix=b'', suffix=b''):
    """Construct a message that can be sent to the IRC network."""

    # Make sure everything is bytes.
    command = to_bytes(command)
    prefix = to_bytes(prefix)
    params = tuple(map(to_bytes, args))
    suffix = to_bytes(suffix)

    # Must not contain line feeds.
    to_check = (prefix, command, params, suffix) + params
    if any(filter(lambda s: LINEFEED in s, to_check)):
        raise exceptions.StrayLineEnding

    # Join the message together.
    message = command
    if prefix:
        message = b':' + prefix + b' ' + message
    if params:
        params = b' '.join(params)
        message = message + b' ' + params
    if suffix:
        message = message + b' :' + suffix
    message = message + LINEFEED

    # Must not exceed 512 characters in length.
    if len(message) > 512:
        raise exceptions.MessageTooLong

    return message


def make_privmsgs(target, message):
    """Turn a string into a number of PRIVMSG commands."""
    max_length = MAX_LENGTH - (len(commands.PRIVMSG) + len(target) + 5)
    messages = []
    for line in chunk_message(message, max_length=max_length):
        messages.append(build_message(commands.PRIVMSG, target, suffix=line))
    return messages
