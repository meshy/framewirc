import asyncio

from .message import Message


class Connection:
    """
    Communicates with an IRC network.

    Incoming data is transformed into Message objects, and sent to `listeners`.
    """

    def __init__(self, *, listeners, host, port, ssl=True):
        self.listeners = listeners
        self.host = host
        self.port = port
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
        """Dispatch the message to all listeners."""
        if not raw_message:
            self.disconnect()
            return

        message = Message(raw_message)
        for listener in self.listeners:
            listener.handle(self, message)

    def on_connect(self):
        """Upon connection to the network, send user's credentials."""
        self.send('USER meshybot 0 * :MeshyBot7')
        self.send('NICK meshybot')

    def send(self, message):
        """Dispatch a message to the IRC network."""
        # Cast to bytes
        try:
            message = message.encode()
        except AttributeError:
            pass

        # Add line ending.
        message = message + b'\r\n'
        print('write', message)
        self.writer.write(message)
