import asyncio

from . import commands, exceptions
from .message import build_message, MAX_LENGTH, ReceivedMessage
from .utils import LINEFEED


class Connection:
    """
    Communicates with an IRC network.

    Incoming data is sent to `handlers`.
    """
    bad_nick_addendum = b'^'
    bad_nick_triggers = (
        commands.ERR_NICKNAMEINUSE,
        commands.ERR_NICKCOLLISION,
    )

    def __init__(self, **kwargs):
        """
        Allow for attributes to be set on subclasses and with params.

        Throws MissingAttributes if a required attribute has not been set
        one way or another.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

        required = ('handlers', 'host', 'nick', 'port', 'real_name', 'ssl')
        missing_attrs = []

        for attr in required:
            if not hasattr(self, attr):
                missing_attrs.append(attr)

        if missing_attrs:
            raise exceptions.MissingAttributes(missing_attrs)

    @asyncio.coroutine
    def connect(self):
        """Connect to the server, and dispatch incoming messages."""
        connection = asyncio.open_connection(self.host, self.port, ssl=self.ssl)
        self.reader, self.writer = yield from connection

        self.on_connect()

        while self._connected:
            raw_message = yield from self.reader.readline()
            self.handle(raw_message)

    def disconnect(self):
        """Close the connection to the server."""
        self._connected = False
        self.writer.close()

    def handle(self, raw_message):
        """Dispatch the message to all handlers."""
        if not raw_message:
            self.disconnect()
            return

        message = ReceivedMessage(raw_message)

        if message.command in self.bad_nick_triggers:
            self.set_nick(self.nick + self.bad_nick_addendum)

        for handler in self.handlers:
            handler(self, message)

    def on_connect(self):
        """Upon connection to the network, send user's credentials."""
        nick = self.nick
        msg = build_message(commands.USER, nick, '0 *', suffix=self.real_name)
        self.send(msg)
        self.set_nick(nick)
        self._connected = True

    def send(self, message):
        """Dispatch a message to the IRC network."""
        # Must be bytes.
        if not isinstance(message, bytes):
            raise exceptions.MustBeBytes

        # Must not exceed 512 characters in length.
        if len(message) > MAX_LENGTH:
            raise exceptions.MessageTooLong

        # Must end in windows line feed (CR-LF).
        if message[-2:] != LINEFEED:
            raise exceptions.NoLineEnding

        # Must not contain other line feeds
        if message.count(LINEFEED) > 1:
            raise exceptions.StrayLineEnding

        # Send to network.
        self.writer.write(message)

    def send_batch(self, messages):
        for message in messages:
            self.send(message)

    def set_nick(self, new_nick):
        self.send(build_message(commands.NICK, new_nick))
        self.nick = new_nick
