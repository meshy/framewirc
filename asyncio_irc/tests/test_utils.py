from unittest import TestCase

from ..utils import to_bytes, to_unicode


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
