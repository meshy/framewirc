from unittest import mock, TestCase

from .. import handlers
from ..message import ReceivedMessage


class TestPing(TestCase):
    def test_ping(self):
        """Respond to PING with PONG."""
        client = mock.MagicMock()
        message = ReceivedMessage(b'PING :hostname.example.com')

        handlers.ping(client, message)

        client.connection.send.assert_called_with(b'PONG :hostname.example.com\r\n')

    def test_other(self):
        """Do not respond to other commands."""
        client = mock.MagicMock()
        message = ReceivedMessage(b'DERP :hostname.example.com')

        handlers.ping(client, message)

        self.assertFalse(client.connection.send.called)
