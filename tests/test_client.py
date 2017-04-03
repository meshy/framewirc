import asyncio
from unittest import mock

import pytest

from framewirc import exceptions
from framewirc.client import Client
from framewirc.connection import Connection
from framewirc.messages import ReceivedMessage

from .utils import BlankClient


class TestConnectTo:
    def test_connection_stored(self):
        """Has "connection" been stored on the client?"""
        client = BlankClient()
        mock_path = 'asyncio.BaseEventLoop.create_task'
        with mock.patch(mock_path, spec=asyncio.Task):
            client.connect_to('irc.example.com')
        assert isinstance(client.connection, Connection)

    def test_task_returned(self):
        """Is the correct "Task" created and returned?"""
        client = BlankClient()
        mock_path = 'asyncio.BaseEventLoop.create_task'
        with mock.patch(mock_path, spec=asyncio.Task) as Task:
            result = client.connect_to('irc.example.com')
        assert result == Task(client.connection.connect())


class TestJoin:
    """Test the Client.join() method."""
    def setup_method(self, method):
        """Can't make an IRC connection in tests, so a mock will have to do."""
        self.client = BlankClient()
        self.client.connection = mock.MagicMock(spec=Connection)

    def test_singular(self):
        """Can join a channel on a network."""
        self.client.join('#framewirc')
        self.client.connection.send.assert_called_with(b'JOIN #framewirc\r\n')

    def test_multiple(self):
        """Can join multiple channels simultaneously."""
        self.client.join('#framewirc', '#meshy')
        self.client.connection.send.assert_called_with(b'JOIN #framewirc,#meshy\r\n')


class TestOnMessage:
    def test_handlers_called(self):
        """When a message comes in, it should be passed to the handlers."""
        handler = mock.MagicMock()
        client = BlankClient(handlers=[handler])
        message = ReceivedMessage(b'TEST message\r\n')

        client.on_message(message)

        handler.assert_called_with(client, message)


class TestOnConnect:
    def setup_method(self, method):
        """Can't make an IRC connection in tests, so a mock will have to do."""
        self.client = Client(
            handlers=[],
            nick='anick',
            real_name='Real Name',
        )
        self.client.connection = mock.MagicMock(spec=Connection)

    def test_user_command_sent(self):
        self.client.on_connect()
        expected = b'USER anick 0 * :Real Name\r\n'
        self.client.connection.send.assert_any_call(expected)

    def test_set_nick_called(self):
        self.client.on_connect()
        self.client.connection.send.assert_called_with(b'NICK anick\r\n')


class TestPart:
    """Test the Client.part() method."""
    def setup_method(self, method):
        """Can't make an IRC connection in tests, so a mock will have to do."""
        self.client = BlankClient()
        self.client.connection = mock.MagicMock(spec=Connection)

    def test_singular(self):
        """It's possible to leave a channel."""
        self.client.part('#framewirc')
        self.client.connection.send.assert_called_with(b'PART #framewirc\r\n')

    def test_message(self):
        """If provided with a parting message, pass it on."""
        self.client.part('#framewirc', message='Leeroy Jenkins!')
        expected = b'PART #framewirc :Leeroy Jenkins!\r\n'
        self.client.connection.send.assert_called_with(expected)

    def test_multiple(self):
        """When passed multiple channels, leave them all."""
        self.client.part('#framewirc', '#meshy')
        expected = b'PART #framewirc,#meshy\r\n'
        self.client.connection.send.assert_called_with(expected)


class TestPrivmsg:
    def test_simple_message(self):
        client = BlankClient()
        client.connection = mock.MagicMock(spec=Connection)
        client.privmsg('#channel', 'Morning, everyone.')

        expected = [b'PRIVMSG #channel :Morning, everyone.\r\n']
        client.connection.send_batch.assert_called_once_with(expected)

    def test_multiline_message(self):
        client = BlankClient()
        client.connection = mock.MagicMock(spec=Connection)
        client.privmsg('#channel', 'Multi\r\nline\r\nmessage.')

        expected = [
            b'PRIVMSG #channel :Multi\r\n',
            b'PRIVMSG #channel :line\r\n',
            b'PRIVMSG #channel :message.\r\n',
        ]
        client.connection.send_batch.assert_called_once_with(expected)

    def test_third_person_message(self):
        client = BlankClient()
        client.connection = mock.MagicMock(spec=Connection)
        client.privmsg('#channel', 'is speaking in 3rd person!', third_person=True)

        expected = [b'PRIVMSG #channel :\1ACTION is speaking in 3rd person!\1\r\n']
        client.connection.send_batch.assert_called_once_with(expected)

    def test_mask_length(self):
        mask_length = mock.Mock()
        client = BlankClient(mask_length=mask_length)
        client.connection = mock.MagicMock(spec=Connection)
        message = 'We know the size of the mask!'
        with mock.patch('framewirc.client.make_privmsgs') as make_privmsgs:
            client.privmsg('#channel', message)

        make_privmsgs.assert_called_once_with(
            '#channel',
            message,
            third_person=False,
            mask_length=mask_length,
        )


class TestRequiredFields:
    """Test to show that RequiredAttribuesMixin is properly configured."""

    def test_fields(self):
        """Are the correct fields being checked?"""
        assert Client.required_attributes == ('handlers', 'real_name', 'nick')

    def test_uses_required_attributes_mixin(self):
        """Is RequiredAttributesMixin.__init__ actually getting called?"""
        with pytest.raises(exceptions.MissingAttributes) as exception:
            Client()

        expected = "Required attribute(s) missing: ['handlers', 'real_name', 'nick']"
        assert expected in str(exception)


class TestSetNick:
    """Test the Client.set_nick() method."""
    def setup_method(self, method):
        """Can't make an IRC connection in tests, so a mock will have to do."""
        self.client = BlankClient(mask_length=42)
        self.client.connection = mock.MagicMock(spec=Connection)

    def test_command_sent(self):
        """Should send a message to the network."""
        self.client.set_nick('meshy')
        self.client.connection.send.assert_called_with(b'NICK meshy\r\n')

    def test_new_nick_kept(self):
        """Should store the new nick on the Client."""
        new_nick = 'meshy'
        self.client.set_nick(new_nick)
        assert self.client.nick == new_nick

    def test_mask_length_reset(self):
        """When the nick changes, reset the mask_length."""
        self.client.set_nick('meshy')
        assert self.client.mask_length is None
