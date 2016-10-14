from . import exceptions


LINEFEED = b'\r\n'


class RequiredAttributesMixin:
    """
    Mixin that requires instances to have certain attributes.

    The required attributes must be listed in `required_attributes`. Throws
    `MissingAttributes` if a required attribute has not been set.

    Attributes can be set directly on the class...:

        class MyClass(RequiresAttributesMixin):
            required_attributes = ['spam']
            spam = 'eggs'

    ...or passed through as kwargs:

        class MyClass(RequiresAttributesMixin):
            required_attributes = ['spam']

        MyClass(spam='eggs')

    All kwargs passed will be set onto the class (even those that are not in
    `required_attributes`), and will override existing attributes of the same
    name.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        missing_attrs = []
        for attr in self.required_attributes:
            if not hasattr(self, attr):
                missing_attrs.append(attr)

        if missing_attrs:
            raise exceptions.MissingAttributes(missing_attrs)
