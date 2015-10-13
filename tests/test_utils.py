from unittest import TestCase

from hypothesis import example, given
from hypothesis.strategies import binary

from framewirc import exceptions
from framewirc.utils import chunk_message, RequiredAttributesMixin, to_bytes, to_unicode


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

    @given(binary())
    @example(b'\xc5\xa1\xc4\xa1\xc5\xc3\xc4\xa1\xc4\xa1')  # Gets recognised as EUC-TW
    def test_for_exceptions(self, bytestring):
        """Use hypothesis to try to make it break!"""
        to_unicode(bytestring)


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

    def test_split_long_unicode(self):
        """Are words with multi-byte chars split correctly?"""
        # Repeated failures lead to success.
        msg = '失敗を繰り返すことで、成功に至る。'
        expected = [
            to_bytes('失敗を繰り返'),
            to_bytes('すことで、成'),
            to_bytes('功に至る。'),
        ]
        messages = chunk_message(msg, max_length=20)
        self.assertEqual(messages, expected)


class TestRequiredAttributesMixin(TestCase):
    """Tests for RequiredAttributesMixin"""
    def test_kwarg(self):
        """Attributes can be passed through as kwargs."""
        class RequiresFoo(RequiredAttributesMixin):
            required_attributes = ['foo']

        result = RequiresFoo(foo='bar')
        self.assertEqual(result.foo, 'bar')

    def test_attribute(self):
        """Attributes can be set directly on the class."""
        class RequiresFoo(RequiredAttributesMixin):
            foo = 'bar'
            required_attributes = ['foo']

        result = RequiresFoo()
        self.assertEqual(result.foo, 'bar')

    def test_kwargs_overrides_attribute(self):
        """Attributes set on the class should be overridden by kwargs."""
        class RequiresFoo(RequiredAttributesMixin):
            foo = 'bar'
            required_attributes = ['foo']

        result = RequiresFoo(foo='baz')
        self.assertEqual(result.foo, 'baz')

    def test_attibute_not_set(self):
        """Failing to set the attribute should raise an error."""
        class RequiresFoo(RequiredAttributesMixin):
            required_attributes = ['foo']

        with self.assertRaises(exceptions.MissingAttributes):
            RequiresFoo()

    def test_error_description(self):
        """The error raised should have a good description."""
        class RequiresFoo(RequiredAttributesMixin):
            required_attributes = ['foo']

        with self.assertRaises(exceptions.MissingAttributes) as cm:
            RequiresFoo()

        expectied = "Required attribute(s) missing: ['foo']"
        self.assertEqual(str(cm.exception), expectied)
