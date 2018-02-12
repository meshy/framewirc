from itertools import product
from unittest import mock

import pytest
from hypothesis import given, strategies

from framewirc import exceptions
from framewirc.messages import (
    build_message,
    chunk_message,
    make_privmsgs,
    ReceivedMessage,
)
from framewirc.strings import to_bytes


on_off = True, False


@pytest.mark.parametrize('prefix,params,suffix', product(on_off, on_off, on_off))
def test_received_message(prefix, params, suffix):
    """
    Test the ReceivedMessage class.

    Make sure that Message attributes are set correctly. Checks every
    combination of a prefix, params, and suffix data.
    """
    raw_message = b'COMMAND'
    if prefix:
        raw_message = b':prefixed-data ' + raw_message
    if params:
        raw_message += b' param1 param2'
    if suffix:
        raw_message += b' :suffix message'
    raw_message += b'\r\n'

    message = ReceivedMessage(raw_message)

    expected_prefix = 'prefixed-data' if prefix else ''
    expected_params = ('param1', 'param2') if params else ()
    expected_suffix = b'suffix message' if suffix else b''

    assert message.command == 'COMMAND'
    assert message.prefix == expected_prefix
    assert message.params == expected_params
    assert message.suffix == expected_suffix


class TestBuildMessage:
    """Make sure that build_message correctly builds bytes objects."""
    def test_basic(self):
        """Simple command only."""
        message = build_message(b'COMMAND')
        assert message == b'COMMAND\r\n'

    def test_prefix(self):
        """Command with prefix."""
        message = build_message(b'COMMAND', prefix=b'something')
        assert message == b':something COMMAND\r\n'

    def test_params(self):
        """Command with params."""
        message = build_message(b'COMMAND', b'param1', b'param2')
        assert message == b'COMMAND param1 param2\r\n'

    def test_suffix(self):
        """Command with suffix."""
        message = build_message(b'COMMAND', suffix=b'suffix ftw!')
        assert message == b'COMMAND :suffix ftw!\r\n'

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
        assert message == expected

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
        assert message == expected


class TestBuildMessageExceptions:
    def test_linefeed_in_suffix(self):
        """Make sure that the suffix cannot contain a linefeed (\r\n)."""
        with pytest.raises(exceptions.StrayLineEnding):
            build_message('COMMAND', suffix='\r\n')

    def test_linefeed_in_params(self):
        """Make sure that the params cannot contain a linefeed (\r\n)."""
        with pytest.raises(exceptions.StrayLineEnding):
            build_message('COMMAND', '\r\n')

    def test_linefeed_in_prefix(self):
        """Make sure that the prefix cannot contain a linefeed (\r\n)."""
        with pytest.raises(exceptions.StrayLineEnding):
            build_message('COMMAND', prefix='\r\n')

    def test_linefeed_in_command(self):
        """Make sure that the suffix cannot contain a linefeed (\r\n)."""
        with pytest.raises(exceptions.StrayLineEnding):
            build_message('COMMAND\r\n')

    def test_message_too_long(self):
        """Make sure that the the message cannot be longer than 512 bytes."""
        with pytest.raises(exceptions.MessageTooLong):
            build_message('A' * 511)  # 513 chars when \r\n added.


class TestChunkMessage:
    """Test the behaviour of the chunk_message function."""
    def test_return_type(self):
        """Does it return a list of bytes objects?"""
        messages = chunk_message('Just a simple message', max_length=100)
        assert messages == [b'Just a simple message']

    def test_split_linefeeds(self):
        """Does it split on newline chars?"""
        msg = 'A message\rsplit over\nmany lines\r\nwith odd linebreaks.'
        expected = [
            b'A message',
            b'split over',
            b'many lines',
            b'with odd linebreaks.',
        ]
        assert chunk_message(msg, max_length=100) == expected

    def test_split_long_line(self):
        """Does it split long lines?"""
        msg = 'Message to be split into chunks of twenty characters or less.'
        expected = [
            b'Message to be split',
            b'into chunks of',
            b'twenty characters or',
            b'less.',
        ]
        assert chunk_message(msg, max_length=20) == expected

    def test_split_long_word(self):
        """Does it split long words?"""
        msg = 'Sup Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch?'
        expected = [
            b'Sup',
            b'Llanfairpwllgwyngyll',
            b'gogerychwyrndrobwlll',
            b'lantysiliogogogoch?',
        ]
        assert chunk_message(msg, max_length=20) == expected

    def test_split_long_unicode(self):
        """Are words with multi-byte chars split correctly?"""
        # Repeated failures lead to success.
        msg = '失敗を繰り返すことで、成功に至る。'
        expected = [
            to_bytes('失敗を繰り返'),
            to_bytes('すことで、成'),
            to_bytes('功に至る。'),
        ]
        assert chunk_message(msg, max_length=20) == expected

    _multibyte_strings = (
        'øøøøøøøøøø',  # 2-byte
        '。。。。。。。。。。',  # 3-byte
        '💩💩💩💩💩💩💩💩💩💩',  # 4-byte
    )
    _variations = product([4, 5, 6, 7], _multibyte_strings)

    @pytest.mark.parametrize('max_length,message', _variations)
    def test_split_mid_char(self, max_length, message):
        """Check obvious permutations of mid-char breaks."""
        # The string chunks up without error.
        result = chunk_message(message, max_length=max_length)
        # When rejoined, the original string is restored.
        assert ''.join(map(bytes.decode, result)) == message

    @given(strategies.integers(min_value=4, max_value=255), strategies.text())
    def test_split_garbage(self, max_length, message):
        """Check mid-char breaks in garbage unicode."""
        # The string chunks up without error.
        result = chunk_message(message, max_length=max_length)
        # No chunks exceed the max length.
        for line in result:
            assert len(line) <= max_length
        # We strip newlines out of the message to avoid confusion.
        message = ''.join(message.splitlines())
        # When rejoined, the original string is restored.
        assert ''.join(map(bytes.decode, result)) == message


class TestMakePrivMsgs:
    """Ensure make_privmsgs correctly constructs PRIVMSG command lists."""
    def test_simple(self):
        expected = [
            b'PRIVMSG meshy :Just a simple message\r\n',
        ]
        messages = make_privmsgs('meshy', 'Just a simple message')
        assert messages == expected

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
        assert messages == expected

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
        assert messages == expected

    def test_max_length(self):
        """Is the correct max_length calculated?"""
        msg = 'A test message'
        with mock.patch('framewirc.messages.chunk_message') as chunk_message:
            make_privmsgs('meshy', msg)

        expected_max = 495  # 512 - len(b'PRIVMSG meshy :' + b'\r\n')
        chunk_message.assert_called_with(msg, max_length=expected_max)

    def test_third_person(self):
        """Are third person messages marked?"""
        expected = [b'PRIVMSG meshy :\1ACTION is in 3rd person\1\r\n']
        messages = make_privmsgs('meshy', 'is in 3rd person', third_person=True)
        assert messages == expected

    def test_third_person_max_length(self):
        """Are third person messages wrapped correctly?"""
        msg = 'A test message'
        with mock.patch('framewirc.messages.chunk_message') as chunk_message:
            make_privmsgs('meshy', msg, third_person=True)

        expected_max = 486  # 512 - len(b'PRIVMSG meshy :\1ACTION ' + b'\1\r\n')
        chunk_message.assert_called_with(msg, max_length=expected_max)
