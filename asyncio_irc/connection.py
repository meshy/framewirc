import asyncio

from . import exceptions
from . import utils
from .message import MAX_LENGTH, ReceivedMessage


class Connection(utils.RequiredAttributesMixin):
    """
    Communicates with an IRC network.

    Incoming data is sent to `client.on_message`.
    """
    required_attributes = ('client', 'host')
    port = 6697
    ssl = True

    @asyncio.coroutine
    def connect(self):
        """Connect to the server, and dispatch incoming messages."""
        connection = asyncio.open_connection(self.host, self.port, ssl=self.ssl)
        self.reader, self.writer = yield from connection

        self._connected = True
        self.client.on_connect()

        while self._connected:
            raw_message = yield from self.reader.readline()
            self.handle(raw_message)

    def disconnect(self):
        """Close the connection to the server."""
        self._connected = False
        self.writer.close()

    def handle(self, raw_message):
        """Dispatch the message to the client."""
        if not raw_message:
            # A blank message means that the connection has closed.
            self.disconnect()
            return

        self.client.on_message(ReceivedMessage(raw_message))

    def send(self, message):
        """Dispatch a message to the IRC network."""
        # Must be bytes.
        if not isinstance(message, bytes):
            raise exceptions.MustBeBytes

        # Must not exceed 512 characters in length.
        if len(message) > MAX_LENGTH:
            raise exceptions.MessageTooLong

        # Must end in windows line feed (CR-LF).
        if message[-2:] != utils.LINEFEED:
            raise exceptions.NoLineEnding

        # Must not contain other line feeds
        if message.count(utils.LINEFEED) > 1:
            raise exceptions.StrayLineEnding

        # Send to network.
        self.writer.write(message)

    def send_batch(self, messages):
        for message in messages:
            self.send(message)
