from collections import deque

from . import commands, exceptions
from .strings import to_bytes, to_unicode
from .utils import LINEFEED


ACTION_START = b'\1ACTION '
ACTION_END = b'\1'
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
        message = self.rstrip()

        prefix = b''
        # Odd slicing required for bytes to avoid getting int instead of char
        # http://stackoverflow.com/q/28249597/400691
        if message[0:1] == b':':
            prefix, message = message[1:].split(b' ', 1)

        suffix = b''
        if b' :' in message:
            message, suffix = message.split(b' :', 1)

        command, *params = message.split()
        params = tuple(to_unicode(p) for p in params if p)

        # Suffix not yet turned to unicode to allow more complex encoding logic
        return to_unicode(prefix), to_unicode(command), params, suffix


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
    if len(message) > MAX_LENGTH:
        raise exceptions.MessageTooLong

    return message


def _chunk_message(message, max_length):
    # Split the message on linebreaks, and loop over lines.
    lines = deque(message.splitlines())
    while lines:
        line = lines.popleft()
        line_bytes = line.encode()
        # If the line fits, add it the the lines.
        if len(line_bytes) < max_length:
            yield line_bytes
            continue

        # See if there is a space below the max length.
        spacepoint = line_bytes.rfind(b' ', 0, max_length+1)
        if spacepoint != -1:
            # Break on the last space that fits.
            start = line_bytes[:spacepoint]
            yield start
            # ... and add what's left back into the line pool.
            end = line_bytes[(spacepoint + 1):].decode()
            lines.appendleft(end)
            # And move onto the next line.
            continue

        # Whole line does not contain spaces, so split within word.
        line_length = 0  # The running total size of the line
        for i, str_char in enumerate(line):
            char_length = len(str_char.encode())
            line_length += char_length
            if line_length > max_length:
                letterpoint = i
                break

        start = line[:letterpoint]
        yield start.encode()
        end = line[letterpoint:]
        lines.appendleft(end)


def chunk_message(message, max_length):
    """
    Chunk a unicode message into lines with a max_length in bytes.

    Splits the message by linebreak chars, then words, and finally letters to
    keep the string chunks short enough.
    """
    return list(_chunk_message(message, max_length))


def make_privmsgs(target, message, third_person=False):
    """Turn a string into a number of PRIVMSG commands."""
    overhead = 5  # Two spaces, a colon, and the \r\n line ending.
    if third_person:
        overhead += len(ACTION_START) + len(ACTION_END)

    max_length = MAX_LENGTH - (len(commands.PRIVMSG) + len(target) + overhead)
    messages = []
    for line in chunk_message(message, max_length=max_length):
        if third_person:
            line = ACTION_START + line + ACTION_END
        messages.append(build_message(commands.PRIVMSG, target, suffix=line))
    return messages
