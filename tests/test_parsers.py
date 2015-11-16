from unittest import mock, TestCase

from framewirc.message import build_message, ReceivedMessage
from framewirc.parsers import (
    is_channel,
    message_to_kwargs,
    nick,
    privmsg,
)


class TestIsChannel(TestCase):
    """Tests for the boolean function is_channel."""
    def test_starts_with_ampersand(self):
        """True when starts with an & ("ampersand")."""
        self.assertTrue(is_channel('&channel'))

    def test_starts_with_exclamtion_mark(self):
        """True when starts with an ! ("exclamation mark" AKA "bang")."""
        self.assertTrue(is_channel('!channel'))

    def test_starts_with_hash(self):
        """True when starts with a # ("hash" AKA "pound")."""
        self.assertTrue(is_channel('#channel'))

    def test_starts_with_plus(self):
        """True when starts with a + ("plus" AKA "add")."""
        self.assertTrue(is_channel('+channel'))

    def test_starts_with_alpha_char(self):
        """False when starts with a normal char."""
        self.assertFalse(is_channel('channel'))

    def test_50_chars(self):
        """True when up to 50 chars."""
        channel = '#' + 49 * 'a'
        self.assertTrue(is_channel(channel))

    def test_51_chars(self):
        """False when 51 chars or more."""
        channel = '#' + 50 * 'a'
        self.assertFalse(is_channel(channel))

    def test_contains_space(self):
        """False when contains space."""
        self.assertFalse(is_channel('#contains space'))

    def test_contains_comma(self):
        """False when contains comma."""
        self.assertFalse(is_channel('#contains,comma'))

    def test_contains_bel(self):
        """False when contains ASCII BEL control char."""
        # "\7" is one way python can escape the ASCII BEL char.
        self.assertFalse(is_channel('#contains\7BEL'))


class TestNick(TestCase):
    """The nick parser can deal with several nick formats."""
    def test_nick_with_ident(self):
        result = nick('nickname!ident@hostname')

        expected = {
            'nick': 'nickname',
            'ident': 'ident',
            'host': 'hostname',
        }
        self.assertEqual(result, expected)

    def test_nick_without_ident(self):
        result = nick('~nickname@hostname')

        expected = {
            'nick': 'nickname',
            'ident': None,
            'host': 'hostname',
        }
        self.assertEqual(result, expected)


class TestPrivmsg(TestCase):
    def processed_message(
            self,
            target=b'#target',
            sender=b'nick!ident@host',
            body='message body'):
        """Build a PRIVMSG, and process it with parsers.privmsg."""
        message = build_message('PRIVMSG', target, prefix=sender, suffix=body)
        return privmsg(ReceivedMessage(message))

    def test_text(self):
        """The message suffix is the 'raw_body'."""
        result = self.processed_message()

        self.assertEqual(result['raw_body'], b'message body')

    def test_raw_sender(self):
        """The 'raw_sender' key is populated by the message prefix."""
        result = self.processed_message()

        self.assertEqual(result['raw_sender'], 'nick!ident@host')

    def test_sender_nick(self):
        """The `sender_nick` key is the sender's nick."""
        result = self.processed_message()

        self.assertEqual(result['sender_nick'], 'nick')

    def test_target(self):
        """The 'target' key is populated by the message params."""
        result = self.processed_message()

        self.assertEqual(result['target'], '#target')

    def test_channel_when_channel(self):
        """When sent to a channel, the 'channel' should reflect that."""
        target = '#channel'
        result = self.processed_message(target=target)

        self.assertEqual(result['channel'], target)

    def test_channel_when_direct(self):
        """When sent directly to a user, the 'channel' is the sender."""
        target = 'targetUser'
        sender_nick = 'senderUser'
        sender = sender_nick + '!ident@hostname'
        result = self.processed_message(target=target, sender=sender)

        self.assertEqual(result['channel'], sender_nick)

    def test_not_third_person(self):
        """Normal messages should not be marked as `third_person`."""
        result = self.processed_message()

        self.assertFalse(result['third_person'])

    def test_third_person(self):
        """
        Set `third_person` when the message is sent as a "CTCP ACTION".

        This is generally the result of a user typing a "/me" command into
        their client.
        """
        result = self.processed_message(body='\1ACTION is third person!\1')

        self.assertEqual(result['raw_body'], b'is third person!')
        self.assertTrue(result['third_person'])


def parser_taking_message(message):
    return {'key': 'value'}


class TestMessageToKwargs(TestCase):
    def setUp(self):
        self.client = object()
        self.handler = mock.Mock()
        self.message = object()

    def test_result_passed(self):
        """Dictionary returned from parser passed as kwargs."""
        wrapped = message_to_kwargs(parser_taking_message)(self.handler)

        wrapped(client=self.client, message=self.message)

        self.handler.assert_called_once_with(
            client=self.client,
            message=self.message,
            key='value',
        )

    def test_parser_called_with_kwarg(self):
        """
        The parser is called with `message=message`.

        It's not really a big deal, but it's slightly more flexible if the
        parser is called with kwargs.
        """
        parser = mock.Mock(return_value={})
        wrapped = message_to_kwargs(parser)(self.handler)
        wrapped(client=self.client, message=self.message)
        parser.assert_called_once_with(message=self.message)
