import asyncio
from unittest import mock, TestCase

from .utils import BlankClient
from .. import exceptions
from ..client import Client
from ..connection import Connection
from ..message import ReceivedMessage


class TestConnectTo(TestCase):
    def test_connection_stored(self):
        """Has "connection" been stored on the client?"""
        client = BlankClient()
        with mock.patch('asyncio.Task', spec=asyncio.Task):
            client.connect_to('irc.example.com')
        self.assertIsInstance(client.connection, Connection)

    def test_task_returned(self):
        """Is the correct "Task" created and returned?"""
        client = BlankClient()
        with mock.patch('asyncio.Task', spec=asyncio.Task) as Task:
            result = client.connect_to('irc.example.com')
        self.assertEqual(result, Task(client.connection.connect()))


class TestRequiredFields(TestCase):
    """Test to show that RequiredAttribuesMixin is properly configured."""

    def test_fields(self):
        """Are the correct fields being checked?"""
        required = ['handlers', 'real_name', 'nick']
        self.assertCountEqual(Client.required_attributes, required)

    def test_uses_required_attributes_mixin(self):
        """Is RequiredAttributesMixin.__init__ actually getting called?"""
        with self.assertRaises(exceptions.MissingAttributes) as cm:
            Client()

        expectied = "Required attribute(s) missing: ['handlers', 'real_name', 'nick']"
        self.assertEqual(str(cm.exception), expectied)


class TestOnMessage(TestCase):
    def test_handlers_called(self):
        """When a message comes in, it should be passed to the handlers."""
        handler = mock.MagicMock()
        client = BlankClient(handlers=[handler])
        message = ReceivedMessage(b'TEST message\r\n')

        client.on_message(message)

        handler.assert_called_with(client, message)


class TestOnConnect(TestCase):
    def setUp(self):
        """Can't make an IRC connection in tests, so a mock will have to do."""
        self.client = Client(
            handlers=[],
            nick='anick',
            real_name='Real Name',
        )
        self.client.connection = mock.MagicMock()

    def test_user_command_sent(self):
        self.client.on_connect()
        expected = b'USER anick 0 * :Real Name\r\n'
        self.client.connection.send.assert_any_call(expected)

    def test_set_nick_called(self):
        self.client.on_connect()
        expected = b'NICK anick\r\n'
        self.client.connection.send.assert_called_with(expected)


class TestSetNick(TestCase):
    """Test the Client.set_nick() method."""
    def setUp(self):
        """Can't make an IRC connection in tests, so a mock will have to do."""
        self.client = BlankClient()
        self.client.connection = mock.MagicMock()

    def test_command_sent(self):
        """Should send a message to the network."""
        new_nick = 'meshy'
        self.client.set_nick(new_nick)
        self.client.connection.send.assert_called_with(b'NICK meshy\r\n')

    def test_new_nick_kept(self):
        """Should store the new nick on the Client."""
        new_nick = 'meshy'
        self.client.set_nick(new_nick)
        self.assertEqual(self.client.nick, new_nick)
