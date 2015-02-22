from unittest import TestCase

from ..utils import chunk_message, to_bytes, to_unicode


class TestToUnicode(TestCase):
    def test_already_unicode(self):
        text = 'тнιѕ ιѕ αℓяєα∂у υηι¢σ∂є'
        result = to_unicode(text)
        self.assertEqual(result, text)

    def test_ascii(self):
        text = b'This is just plain ASCII'
        expected = 'This is just plain ASCII'
        result = to_unicode(text)
        self.assertEqual(result, expected)

    def test_latin_1(self):
        text = b'Ume\xe5'
        expected = 'Umeå'
        result = to_unicode(text)
        self.assertEqual(result, expected)

    def test_windows_1250(self):
        text = b'Miko\xb3aj Kopernik'
        expected = 'Mikołaj Kopernik'
        result = to_unicode(text)
        self.assertEqual(result, expected)

    def test_not_bytes_or_string(self):
        with self.assertRaises(AttributeError):
            to_unicode(None)


class TestToBytes(TestCase):
    def test_unicode(self):
        text = 'ಠ_ಠ'
        expected = b'\xe0\xb2\xa0_\xe0\xb2\xa0'
        result = to_bytes(text)
        self.assertEqual(result, expected)

    def test_already_bytes(self):
        text = b'bytes!'
        result = to_bytes(text)
        self.assertEqual(result, text)

    def test_not_bytes_or_string(self):
        with self.assertRaises(AttributeError):
            to_bytes(None)


class TestChunkMessage(TestCase):
    """Test the behaviour of the chunk_message function."""
    def test_return_type(self):
        """Does it return a list of bytes objects?"""
        expected = [b'Just a simple message']
        messages = chunk_message('Just a simple message', max_length=100)
        self.assertEqual(messages, expected)

    def test_split_linefeeds(self):
        """Does it split on newline chars?"""
        msg = 'A message\rsplit over\nmany lines\r\nwith odd linebreaks.'
        expected = [
            b'A message',
            b'split over',
            b'many lines',
            b'with odd linebreaks.',
        ]
        messages = chunk_message(msg, max_length=100)
        self.assertEqual(messages, expected)

    def test_split_long_line(self):
        """Does it split long lines?"""
        msg = 'Message to be split into chunks of twenty characters or less.'
        expected = [
            b'Message to be split',
            b'into chunks of',
            b'twenty characters or',
            b'less.',
        ]
        messages = chunk_message(msg, max_length=20)
        self.assertEqual(messages, expected)

    def test_split_long_word(self):
        """Does it split long words?"""
        msg = 'Sup Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch?'
        expected = [
            b'Sup',
            b'Llanfairpwllgwyngyll',
            b'gogerychwyrndrobwlll',
            b'lantysiliogogogoch?',
        ]
        messages = chunk_message(msg, max_length=20)
        self.assertEqual(messages, expected)
