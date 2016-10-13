import pytest

from framewirc import exceptions
from framewirc.utils import RequiredAttributesMixin, to_bytes, to_unicode


class TestToUnicode:
    def test_already_unicode(self):
        text = 'тнιѕ ιѕ αℓяєα∂у υηι¢σ∂є'
        assert to_unicode(text) == text

    def test_ascii(self):
        assert to_unicode(b'Just plain ASCII') == 'Just plain ASCII'

    def test_latin_1(self):
        assert to_unicode(b'Ume\xe5') == 'Umeå'

    def test_utf8(self):
        assert to_unicode(b'Hyl\xc3\xb4') == 'Hylô'

    def test_windows_1250(self):
        assert to_unicode(b'Miko\xb3aj Kopernik') == 'Mikołaj Kopernik'

    def test_not_bytes_or_string(self):
        with pytest.raises(TypeError):
            to_unicode(None)

    def test_expected_decoding_first(self):
        """
        An undecoded bytestring will try "expected" before utf8.

        This is because some non-UTF8 strings can be "valid" utf8.
        """
        # UTF8 would make this '\x1b$BEl5~ET\x1b(B'
        assert to_unicode(b'\x1b$BEl5~ET\x1b(B', ['iso-2022-jp']) == '東京都'

    def test_expected_decoding_quietly_wrong(self):
        """
        An expected decoding can be wrong, and not throw errors.

        Perhaps not ideal, but I don't know if it's possible to catch this.
        """
        # Decoding incorrectly throws no error in this case
        assert to_unicode(b'Ume\xe5', ['windows_1250']) == 'Umeĺ'

    def test_expected_decoding_loudly_wrong(self):
        """An expected decoding can fall back to another encoding."""
        text = b'\xff\xfe\xb5\x03\xbb\x03\xbb\x03\xb7\x03\xbd\x03\xb9\x03\xba\x03\xac\x03'
        # `text` is encoded in utf16
        assert to_unicode(text, ['iso-2022-jp', 'utf16']) == 'ελληνικά'


class TestToBytes:
    def test_unicode(self):
        assert to_bytes('ಠ_ಠ') == b'\xe0\xb2\xa0_\xe0\xb2\xa0'

    def test_already_bytes(self):
        text = b'bytes!'
        assert to_bytes(text) == text

    def test_not_bytes_or_string(self):
        with pytest.raises(TypeError):
            to_bytes(None)


class TestRequiredAttributesMixin:
    """Tests for RequiredAttributesMixin"""
    def test_kwarg(self):
        """Attributes can be passed through as kwargs."""
        class RequiresFoo(RequiredAttributesMixin):
            required_attributes = ['foo']

        result = RequiresFoo(foo='bar')
        assert result.foo == 'bar'

    def test_attribute(self):
        """Attributes can be set directly on the class."""
        class RequiresFoo(RequiredAttributesMixin):
            foo = 'bar'
            required_attributes = ['foo']

        result = RequiresFoo()
        assert result.foo == 'bar'

    def test_kwargs_overrides_attribute(self):
        """Attributes set on the class should be overridden by kwargs."""
        class RequiresFoo(RequiredAttributesMixin):
            foo = 'bar'
            required_attributes = ['foo']

        result = RequiresFoo(foo='baz')
        assert result.foo == 'baz'

    def test_attibute_not_set(self):
        """Failing to set the attribute should raise an error."""
        class RequiresFoo(RequiredAttributesMixin):
            required_attributes = ['foo']

        with pytest.raises(exceptions.MissingAttributes):
            RequiresFoo()

    def test_error_description(self):
        """The error raised should have a good description."""
        class RequiresFoo(RequiredAttributesMixin):
            required_attributes = ['foo']

        with pytest.raises(exceptions.MissingAttributes) as exception:
            RequiresFoo()

        assert "Required attribute(s) missing: ['foo']" in str(exception)
