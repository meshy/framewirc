import asyncio

from .message import Message


class Connection:
    """
    Communicates with an IRC network.

    Incoming data is transformed into Message objects, and sent to `listeners`.
    """

    def __init__(self, listeners, host, port, ssl=True):
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
            message = yield from self.reader.readline()
            self.handle(message)

    def disconnect(self):
        """Close the connection to the server."""
        self._connected = False
        self.writer.close()
        self.on_disconnect()

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
        self.send(b'USER meshybot 0 * :MeshyBot7')
        self.send(b'NICK meshybot')

    def on_disconnect(self):
        print('Connection closed')

    def send(self, message):
        message = message + b'\r\n'
        print('write', message)
        self.writer.write(message)
