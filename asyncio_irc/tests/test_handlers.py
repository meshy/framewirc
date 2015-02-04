from unittest import mock, TestCase

from .. import handlers
from ..message import Message


class TestPing(TestCase):
    def test_ping(self):
        """Respond to PING with PONG."""
        connection = mock.MagicMock()
        message = Message(b'PING :hostname.example.com')

        handlers.ping(connection, message)

        connection.send.assert_called_with(b'PONG :hostname.example.com')
