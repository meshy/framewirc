import pytest

from framewirc import exceptions
from framewirc.utils import RequiredAttributesMixin


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
