from asyncio import StreamWriter
from unittest import mock, TestCase

from framewirc.client import Client
from framewirc.connection import Connection
from framewirc.exceptions import (
    MessageTooLong,
    MustBeBytes,
    NoLineEnding,
    StrayLineEnding,
)
from framewirc.message import ReceivedMessage

from .utils import BlankClient


class TestRequiredFields(TestCase):
    """Test to show that RequiredAttribuesMixin is properly configured."""
    def test_fields(self):
        """Are the correct fields being checked?"""
        required = ('client', 'host')
        self.assertCountEqual(Connection.required_attributes, required)

    def test_uses_required_attributes_mixin(self):
        """Is RequiredAttributesMixin.__init__ actually getting called?"""
        kwargs = {'host': 'example.com'}
        path = 'framewirc.utils.RequiredAttributesMixin.__init__'
        with mock.patch(path, return_value=None) as mixin_init:
            Connection(**kwargs)

        mixin_init.assert_called_with(**kwargs)


class ConnectionTestCase(TestCase):
    """Base TestCase for tests that want an instance of Connection."""
    def setUp(self):
        self.connection = Connection(
            client=BlankClient(),
            host='example.com',
            nick='unused',
            real_name='Charlie Denton',
        )
        self.connection.writer = mock.MagicMock(spec=StreamWriter)


class TestHandle(ConnectionTestCase):
    def test_normal_message(self):
        """Messages should be passed through to client.on_message()."""
        raw_message = b'PRIVMSG meshy :You should really see this!\r\n'
        self.connection.client = mock.MagicMock(spec=Client)
        self.connection.handle(raw_message)

        expected = ReceivedMessage(raw_message)
        self.connection.client.on_message.assert_called_with(expected)

    def test_empty_message_does_not_call_on_message(self):
        """Do not pass empty messages through to client.on_message()."""
        self.connection.client = mock.MagicMock(spec=Client)
        self.connection.handle(b'')

        self.assertFalse(self.connection.client.on_message.called)

    def test_empty_message(self):
        """
        Call Connection.disconnect when we empty message received.

        (Empty messages indicate the connection has closed.)
        """
        self.connection.disconnect = mock.MagicMock()
        self.connection.handle(b'')

        self.connection.disconnect.assert_called_with()


class TestSend(ConnectionTestCase):
    def test_ideal_case(self):
        message = b'PRIVMSG meshy :Nice IRC lib you have there\r\n'
        self.connection.send(message)
        self.connection.writer.write.assert_called_with(message)

    def test_not_bytes(self):
        message = 'PRIVMSG meshy :What µŋhandłed µŋicode yoµ ħave!\r\n'
        with self.assertRaises(MustBeBytes):
            self.connection.send(message)
        self.assertFalse(self.connection.writer.write.called)

    def test_only_one_line_ending(self):
        message = b'PRIVMSG meshy :Nice \r\nCODE :injection you have there\r\n'
        with self.assertRaises(StrayLineEnding):
            self.connection.send(message)
        self.assertFalse(self.connection.writer.write.called)

    def test_line_ending_at_eol(self):
        message = b'PRIVMSG meshy :Nice line ending you have forgotten there'
        with self.assertRaises(NoLineEnding):
            self.connection.send(message)
        self.assertFalse(self.connection.writer.write.called)

    def test_message_too_long(self):
        message = b'FIFTEEN chars :' + 496 * b'a' + b'\r\n'  # 513 chars
        with self.assertRaises(MessageTooLong):
            self.connection.send(message)
        self.assertFalse(self.connection.writer.write.called)

    def test_message_just_right(self):
        message = b'FIFTEEN chars :' + 495 * b'a' + b'\r\n'  # 512 chars
        self.connection.send(message)
        self.connection.writer.write.assert_called_with(message)


class TestSendBatch(ConnectionTestCase):
    def test_send_batch(self):
        messages = [
            b'PRIVMSG meshy :Getting there\r\n',
            b'PRIVMSG meshy :It is almost usable!\r\n',
        ]
        self.connection.send_batch(messages)
        calls = self.connection.writer.write.mock_calls
        self.assertEqual(calls, list(map(mock.call, messages)))
