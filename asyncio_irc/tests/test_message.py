from itertools import product
from unittest import mock, TestCase

from .. import exceptions
from ..message import build_message, make_privmsgs, ReceivedMessage


class TestReceivedMessage(TestCase):
    """Test the ReceivedMessage class."""
    def build_message(self, prefix, params, suffix):
        raw_message = b'COMMAND'
        if prefix:
            raw_message = b':prefixed-data ' + raw_message
        if params:
            raw_message += b' param1 param2'
        if suffix:
            raw_message += b' :suffix message'

        return raw_message

    def test_permutations(self):
        """
        Make sure that Message attributes are set correctly.

        Checks every combination of a prefix, params, and suffix data.
        """
        on_off = True, False
        for prefix, params, suffix in product(on_off, on_off, on_off):
            with self.subTest(prefix=prefix, params=params, suffix=suffix):
                raw_message = self.build_message(prefix, params, suffix)

                message = ReceivedMessage(raw_message)

                expected_prefix = 'prefixed-data' if prefix else ''
                expected_params = ('param1', 'param2') if params else ()
                expected_suffix = 'suffix message' if suffix else ''

                self.assertEqual(message.command, 'COMMAND')
                self.assertEqual(message.prefix, expected_prefix)
                self.assertEqual(message.params, expected_params)
                self.assertEqual(message.suffix, expected_suffix)


class TestBuildMessage(TestCase):
    """Make sure that build_message correctly builds bytes objects."""
    def test_basic(self):
        """Simple command only."""
        message = build_message(b'COMMAND')
        self.assertEqual(message, b'COMMAND\r\n')

    def test_prefix(self):
        """Command with prefix."""
        message = build_message(b'COMMAND', prefix=b'something')
        self.assertEqual(message, b':something COMMAND\r\n')

    def test_params(self):
        """Command with params."""
        message = build_message(b'COMMAND', b'param1', b'param2')
        self.assertEqual(message, b'COMMAND param1 param2\r\n')

    def test_suffix(self):
        """Command with suffix."""
        message = build_message(b'COMMAND', suffix=b'suffix ftw!')
        self.assertEqual(message, b'COMMAND :suffix ftw!\r\n')

    def test_all(self):
        """Command with prefix, params, and suffix."""
        message = build_message(
            b'COMMAND',
            b'param1',
            b'param2',
            prefix=b'something',
            suffix=b'suffix ftw!',
        )
        expected = b':something COMMAND param1 param2 :suffix ftw!\r\n'
        self.assertEqual(message, expected)

    def test_unicode(self):
        """
        Make sure build_message works when passed strings.

        No valid commands contain unicode chars, so not bothering with ♬ in it.
        """
        message = build_message(
            'COMMAND',
            'tést',
            'test',
            prefix='mμ',
            suffix='ftẃ!',
        )
        expected = b':m\xce\xbc COMMAND t\xc3\xa9st test :ft\xe1\xba\x83!\r\n'
        self.assertEqual(message, expected)


class TestBuildMessageExceptions(TestCase):
    def test_linefeed_in_suffix(self):
        """Make sure that the suffix cannot contain a linefeed (\r\n)."""
        with self.assertRaises(exceptions.StrayLineEnding):
            build_message('COMMAND', suffix='\r\n')

    def test_linefeed_in_params(self):
        """Make sure that the params cannot contain a linefeed (\r\n)."""
        with self.assertRaises(exceptions.StrayLineEnding):
            build_message('COMMAND', '\r\n')

    def test_linefeed_in_prefix(self):
        """Make sure that the prefix cannot contain a linefeed (\r\n)."""
        with self.assertRaises(exceptions.StrayLineEnding):
            build_message('COMMAND', prefix='\r\n')

    def test_linefeed_in_command(self):
        """Make sure that the suffix cannot contain a linefeed (\r\n)."""
        with self.assertRaises(exceptions.StrayLineEnding):
            build_message('COMMAND\r\n')

    def test_message_too_long(self):
        """Make sure that the the message cannot be longer than 512 bytes."""
        with self.assertRaises(exceptions.MessageTooLong):
            build_message('A' * 511)  # 513 chars when \r\n added.


class TestMakePrivMsgs(TestCase):
    """Ensure make_privmsgs correctly constructs PRIVMSG command lists."""
    def test_simple(self):
        expected = [
            b'PRIVMSG meshy :Just a simple message\r\n',
        ]
        messages = make_privmsgs('meshy', 'Just a simple message')
        self.assertEqual(messages, expected)

    def test_linebreaks(self):
        expected = [
            b'PRIVMSG meshy :A message\r\n',
            b'PRIVMSG meshy :split onto lines\r\n',
            b'PRIVMSG meshy :with varying linebreaks\r\n',
        ]
        messages = make_privmsgs(
            'meshy',
            'A message\rsplit onto lines\nwith varying linebreaks',
        )
        self.assertEqual(messages, expected)

    def test_long_line(self):
        too_long = (
            "We're no strangers to love, You know the rules and so do I. " +
            "A full commitment's what I'm thinking of, You wouldnt get " +
            "this from any other guy. I just wanna tell you how I'm " +
            "feeling, Gotta make you understand… Never gonna give you up, " +
            "Never gonna let you down, Never gonna run around and desert " +
            "you. Never gonna make you cry, Never gonna say goodbye, Never " +
            "gonna tell a lie and hurt you. We've known each other for so " +
            "long your heart's been aching but you're too shy to say it. " +
            "Inside we both know what's been going on, We know the game " +
            "and we're gonna play it."
        )
        expected = [
            (
                b"PRIVMSG meshy :We're no strangers to love, You know the " +
                b"rules and so do I. A full commitment's what I'm thinking " +
                b"of, You wouldnt get this from any other guy. I just wanna " +
                b"tell you how I'm feeling, Gotta make you " +
                b"understand\xe2\x80\xa6 Never gonna give you up, Never " +
                b"gonna let you down, Never gonna run around and desert " +
                b"you. Never gonna make you cry, Never gonna say goodbye, " +
                b"Never gonna tell a lie and hurt you. We've known each " +
                b"other for so long your heart's been aching but you're too " +
                b"shy to say it. Inside we both\r\n"
            ),
            (
                b"PRIVMSG meshy :know what's been going on, We know the " +
                b"game and we're gonna play it.\r\n"
            ),
        ]

        messages = make_privmsgs('meshy', too_long)
        self.assertEqual(messages, expected)

    def test_max_length(self):
        """Is the correct max_length calculated?"""
        msg = 'A test message'
        with mock.patch('asyncio_irc.message.chunk_message') as chunk_message:
            make_privmsgs('meshy', msg)

        expected_max = 495  # 512 - len(r'PRIVMSG meshy :' + '\r\n')
        chunk_message.assert_called_with(msg, max_length=expected_max)
