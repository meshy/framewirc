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
        # If the line fits, add it to the accepted lines.
        if len(line_bytes) <= max_length:
            yield line_bytes
            continue

        # See if there is a space below the max length.
        spacepoint = line_bytes.rfind(b' ', 0, max_length+1)
        if spacepoint != -1:
            # Break on the last space that fits.
            start = line_bytes[:(spacepoint + 1)]
            yield start
            # ... and add what's left back into the line pool.
            end = line_bytes[(spacepoint + 1):].decode()
            lines.appendleft(end)
            # And move onto the next line.
            continue

        # Split by byte length, and work backwards to char boundary.
        chunk_bytes = line_bytes[:max_length]
        b1, b2, b3, b4 = chunk_bytes[:max_length][-4:]

        # Last character doesn't cross the boundary.
        if (
            b4 >> 7 == 0b0 or  # 1-byte char.
            b3 >> 5 == 0b110 or  # 2-byte char.
            b2 >> 4 == 0b1110 or  # 3-byte char.
            b1 >> 3 == 0b11110  # 4-byte char.
        ):
            offset = 0

        # b4 begins a char crossing the boundary.
        elif b4 >> 6 == 0b11:  # 2-, 3-, or 4-byte char.
            offset = 1

        # b3 begins a char crossing the boundary.
        elif b3 >> 5 == 0b111:  # 3- or 4-byte char.
            offset = 2

        # b2 must begin a 4-byte char crossing the boundary.
        else:  # ie: b2 >> 4 == 0b11110
            offset = 3

        yield chunk_bytes[:max_length-offset]
        lines.appendleft(line_bytes[max_length-offset:].decode())


def chunk_message(message, max_length):
    """
    Chunk a unicode message into lines with a max_length in bytes.

    Splits the message by linebreak chars, then words, and finally letters to
    keep the string chunks short enough.
    """
    return list(_chunk_message(message, max_length))


def make_privmsgs(target, message, third_person=False, mask_length=None):
    """
    Turns `message` into a list of `PRIVMSG` commands (to `target`).

    The `third_person` flag can be used to send `/me` commands.

    If the message is too long, we span it across multiple commands.

    We don't send a mask prefix, but the network will add it. This lets clients
    know who the sender of the message is, and impacts the maximum length of
    the transmitted command.

    When the `mask_length` is `None`, we allow a default of 100 chars.
    """
    # If we don't know exactly how long the mask will be, make a guess.
    # I can't find a maximum length in the spec; 100 chars seems safe.
    if mask_length is None:
        mask_length = 100

    # Three spaces, two colons, \r, and \n makes 7:
    #     :mask PRIVMSG target :message\r\n
    #     ^    ^       ^      ^^        ^ ^
    overhead = mask_length + len(commands.PRIVMSG) + len(target) + 7

    # Third person messages (ie: /me) have a few extra chars.
    if third_person:
        overhead += len(ACTION_START) + len(ACTION_END)

    max_length = MAX_LENGTH - overhead
    messages = []
    for line in chunk_message(message, max_length=max_length):
        if third_person:
            line = ACTION_START + line + ACTION_END
        messages.append(build_message(commands.PRIVMSG, target, suffix=line))
    return messages
