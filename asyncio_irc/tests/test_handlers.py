from unittest import mock, TestCase

from .. import handlers
from ..message import ReceivedMessage


class TestPing(TestCase):
    def test_ping(self):
        """Respond to PING with PONG."""
        connection = mock.MagicMock()
        message = ReceivedMessage(b'PING :hostname.example.com')

        handlers.ping(connection, message)

        connection.send.assert_called_with(b'PONG :hostname.example.com')
