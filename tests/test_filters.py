from unittest import mock, TestCase

from framewirc import filters
from framewirc.message import ReceivedMessage


class TestDeny(TestCase):
    def setUp(self):
        self.client = object()
        self.handler = mock.Mock()

    def test_correct_list(self):
        """Un-blacklisted commands should be allowed."""
        message = ReceivedMessage(b'COMMAND\r\n')
        wrapped = filters.deny(['WRONG_COMMAND'])(self.handler)

        wrapped(self.client, message)

        self.handler.assert_called_once_with(
            client=self.client,
            message=message,
        )

    def test_incorrect_list(self):
        """Blacklisted commands should not be allowed."""
        message = ReceivedMessage(b'WRONG_COMMAND\r\n')
        wrapped = filters.deny(['WRONG_COMMAND'])(self.handler)

        wrapped(self.client, message)

        self.assertFalse(self.handler.called)

    def test_correct_item(self):
        """Un-blacklisted commands should be allowed (string blacklist)."""
        message = ReceivedMessage(b'COMMAND\r\n')
        wrapped = filters.deny('WRONG_COMMAND')(self.handler)

        wrapped(self.client, message)

        self.handler.assert_called_once_with(
            client=self.client,
            message=message,
        )

    def test_incorrect_item(self):
        """Blacklisted commands should not be allowed (string blacklist)."""
        message = ReceivedMessage(b'WRONG_COMMAND\r\n')
        wrapped = filters.deny('WRONG_COMMAND')(self.handler)

        wrapped(self.client, message)

        self.assertFalse(self.handler.called)


class TestAllow(TestCase):
    def setUp(self):
        self.client = object()
        self.handler = mock.Mock()

    def test_correct_list(self):
        """Whitelisted commands should be allowed."""
        message = ReceivedMessage(b'COMMAND\r\n')
        wrapped = filters.allow(['COMMAND'])(self.handler)

        wrapped(self.client, message)

        self.handler.assert_called_once_with(
            client=self.client,
            message=message,
        )

    def test_incorrect_list(self):
        """Unlisted commands should not be allowed."""
        message = ReceivedMessage(b'WRONG_COMMAND\r\n')
        wrapped = filters.allow(['COMMAND'])(self.handler)

        wrapped(self.client, message)

        self.assertFalse(self.handler.called)

    def test_correct_item(self):
        """Whitelisted commands should be allowed (string whitelist)."""
        message = ReceivedMessage(b'COMMAND\r\n')
        wrapped = filters.allow('COMMAND')(self.handler)

        wrapped(self.client, message)

        self.handler.assert_called_once_with(
            client=self.client,
            message=message,
        )

    def test_incorrect_item(self):
        """Unlisted commands should not be allowed (string whitelist)."""
        message = ReceivedMessage(b'WRONG_COMMAND\r\n')
        wrapped = filters.allow('COMMAND')(self.handler)

        wrapped(self.client, message)

        self.assertFalse(self.handler.called)

    def test_incorrect_subitem(self):
        """Partial commands should not be allowed (string whitelist)."""
        message = ReceivedMessage(b'COMMA\r\n')
        wrapped = filters.allow('COMMAND')(self.handler)

        wrapped(self.client, message)

        self.assertFalse(self.handler.called)
