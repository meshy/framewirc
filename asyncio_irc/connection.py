import asyncio

from . import commands
from .message import build_message, ReceivedMessage
from .utils import to_bytes


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

    def __init__(self, handlers, host, port, nick, real_name=None, ssl=True):
        self.handlers = handlers
        self.host = host
        self.port = port
        self._proposed_nick = nick
        self.real_name = real_name or nick
        self.ssl = ssl

    @asyncio.coroutine
    def connect(self):
        """Connect to the server, and dispatch incoming messages."""
        connection = asyncio.open_connection(self.host, self.port, ssl=self.ssl)
        self.reader, self.writer = yield from connection

        self.on_connect()

        self._connected = True
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
        nick = self._proposed_nick
        self.send(build_message('USER', nick, '0 *', suffix=self.real_name))
        self.set_nick(nick)

    def send(self, message):
        """Dispatch a message to the IRC network."""
        # Must be bytes.
        assert isinstance(message, bytes)
        # Must end in windows line feed (CR-LF).
        assert message[-2:] == b'\r\n'
        # Must not exceed 512 characters in length.
        assert len(message) <= 512

        # Send to network.
        self.writer.write(message)

    def set_nick(self, new_nick):
        self.send(build_message('NICK', new_nick))
        self.nick = new_nick
