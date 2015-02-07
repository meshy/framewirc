from unittest import mock, TestCase

from .. import filters
from ..message import ReceivedMessage


class TestCommandBlacklist(TestCase):
    def setUp(self):
        self.connection = object()
        self.handler = mock.Mock()

    def test_correct(self):
        message = ReceivedMessage(b'COMMAND\r\n')
        wrapped = filters.command_blacklist(['WRONG_COMMAND'])(self.handler)

        wrapped(self.connection, message)

        self.handler.assert_called_once_with(
            connection=self.connection,
            message=message,
        )

    def test_incorrect(self):
        message = ReceivedMessage(b'WRONG_COMMAND\r\n')
        wrapped = filters.command_blacklist(['WRONG_COMMAND'])(self.handler)

        wrapped(self.connection, message)

        self.assertFalse(self.handler.called)


class TestCommandOnly(TestCase):
    def setUp(self):
        self.connection = object()
        self.handler = mock.Mock()

    def test_correct(self):
        message = ReceivedMessage(b'COMMAND\r\n')
        wrapped = filters.command_only('COMMAND')(self.handler)

        wrapped(self.connection, message)

        self.handler.assert_called_once_with(
            connection=self.connection,
            message=message,
        )

    def test_incorrect(self):
        message = ReceivedMessage(b'WRONG_COMMAND\r\n')
        wrapped = filters.command_only('COMMAND')(self.handler)

        wrapped(self.connection, message)

        self.assertFalse(self.handler.called)


class TestCommandWhitelist(TestCase):
    def setUp(self):
        self.connection = object()
        self.handler = mock.Mock()

    def test_correct(self):
        message = ReceivedMessage(b'COMMAND\r\n')
        wrapped = filters.command_whitelist(['COMMAND'])(self.handler)

        wrapped(self.connection, message)

        self.handler.assert_called_once_with(
            connection=self.connection,
            message=message,
        )

    def test_incorrect(self):
        message = ReceivedMessage(b'WRONG_COMMAND\r\n')
        wrapped = filters.command_whitelist(['COMMAND'])(self.handler)

        wrapped(self.connection, message)

        self.assertFalse(self.handler.called)
