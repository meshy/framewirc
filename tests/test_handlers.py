from unittest import mock

from framewirc import handlers
from framewirc.messages import ReceivedMessage

from .utils import BlankClient


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


class TestCaptureMaskLength:
    def test_length_known(self):
        """If the mask_length is already known, skip."""
        client = BlankClient(mask_length=42, nick='user')
        mask = b'user!~mask@should.never.change'  # Except when nick does.
        raw_message = b':%s PRIVMSG #channel :Message ignored'
        message = ReceivedMessage(raw_message % mask)

        handlers.capture_mask_length(client, message)

        # We shouldn't have started the calculation at all, let alone changed
        # the value of client.mask_length.
        assert client.mask_length != len(mask)

    def test_privmsg(self):
        """Determine mask length from PRIVMSGs sent by ourself."""
        client = BlankClient(mask_length=None, nick='nick')
        mask = b'nick!~user@host.example.com'
        raw_message = b':%s PRIVMSG #channel :Message ignored'
        message = ReceivedMessage(raw_message % mask)

        handlers.capture_mask_length(client, message)

        assert client.mask_length == len(mask)

    def test_notice(self):
        """Determine mask length from NOTICEs sent by ourself."""
        client = BlankClient(mask_length=None, nick='nick')
        mask = b'nick!~user@host.example.com'
        raw_message = b':%s NOTICE #channel :Message ignored'
        message = ReceivedMessage(raw_message % mask)

        handlers.capture_mask_length(client, message)

        assert client.mask_length == len(mask)

    def test_rpl_whoisuser(self):
        """If we WHOIS ourself, we can get the mask length from that."""
        client = BlankClient(mask_length=None, nick='nick')

        # Mask has spaces in RPL_WHOISUSER. We need the the params (excluding
        # the `*`). ie:             |<----------------------->| == 27 chars
        raw_message = b':server 311 nick ~user host.example.com * :Real name'
        message = ReceivedMessage(raw_message)

        handlers.capture_mask_length(client, message)

        assert client.mask_length == 27  # (See comment on raw_message.)

    def test_other(self):
        """Do not respond to other commands."""
        client = BlankClient(mask_length=None, nick='nick')
        mask = b'nick!~user@host.example.com'
        raw_message = b':%s OTHER #channel :Message ignored'
        message = ReceivedMessage(raw_message % mask)

        handlers.capture_mask_length(client, message)

        assert client.mask_length is None
