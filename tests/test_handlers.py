from unittest import mock

from framewirc import handlers
from framewirc.message import ReceivedMessage


class TestPing:
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

        assert client.connection.send.called is False


class TestBadNick:
    def test_nicknameinuse(self):
        """Should call client.set_nick when there's a name clash."""
        client = mock.MagicMock(nick='taken')
        message = ReceivedMessage(b'433')  # ERR_NICKNAMEINUSE

        handlers.nickname_in_use(client, message)

        client.set_nick.assert_called_with('taken^')

    def test_other(self):
        """Do not respond to other commands."""
        client = mock.MagicMock()
        message = ReceivedMessage(b'OTHER')

        handlers.nickname_in_use(client, message)

        assert client.set_nick.called is False
