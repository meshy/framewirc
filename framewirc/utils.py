import cchardet

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


def to_unicode(bytestring, encodings=('utf8',)):
    """Try to convert a string of bytes into a unicode string."""
    # If we already have a unicode string, just return it.
    if isinstance(bytestring, str):
        return bytestring

    # Try each of the encodings until no error is thrown.
    for encoding in encodings:
        try:
            return bytestring.decode(encoding)
        except AttributeError:
            msg = '`bytestring` should be `ReceivedMessage` or `bytes`.'
            raise TypeError(msg)
        except UnicodeDecodeError:
            continue

    # Try to guess the encoding. If that doesn't work use utf8.
    encoding = cchardet.detect(bytestring)['encoding'] or 'utf8'

    # As everything else failed, be more lenient with errors.
    return bytestring.decode(encoding, errors='surrogateescape')


def to_bytes(string):
    try:
        return string.encode()
    except AttributeError:
        if not isinstance(string, bytes):
            msg = '`string` should be `unicode` or `bytes`.'
            raise TypeError(msg)
        return string
