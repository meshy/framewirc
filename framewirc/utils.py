from collections import deque

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


def to_unicode(bytestring):
    """Try to decode as UTF8, then fall back to cchardet."""
    try:
        return bytestring.decode()
    except AttributeError:
        if not isinstance(bytestring, str):
            raise
        return bytestring
    except UnicodeDecodeError:
        charset = cchardet.detect(bytestring)['encoding'] or 'utf-8'
        return bytestring.decode(charset, 'surrogateescape')


def to_bytes(string):
    try:
        return string.encode()
    except AttributeError:
        if not isinstance(string, bytes):
            raise
        return string


def _chunk_message(message, max_length):
    # Split the message on linebreaks, and loop over lines.
    lines = deque(message.splitlines())
    while lines:
        line = lines.popleft()
        line_bytes = to_bytes(line)
        # If the line fits, add it the the lines.
        if len(line_bytes) < max_length:
            yield line_bytes
            continue

        # Whole line doesn't fit, so see if it can be split on space.
        letterpoint = None  # Where we should break if there is no space
        spacepoint = None  # Where we should break if there is a space.
        line_length = 0  # The running total size of the line
        for i, str_char in enumerate(line):
            char_length = len(to_bytes(str_char))
            line_length += char_length
            if str_char == ' ':
                spacepoint = i
            if line_length > max_length:
                letterpoint = i
                break

        if spacepoint is not None:
            # Break on the last space that fits.
            start = line[:spacepoint]
            yield to_bytes(start)
            # ... and add what's left back into the line pool.
            end = line[(spacepoint + 1):]
            lines.appendleft(end)
            continue

        # Whole line does not contain spaces, so split within word.
        start = line[:letterpoint]
        yield to_bytes(start)
        end = line[letterpoint:]
        lines.appendleft(end)


def chunk_message(message, max_length):
    """
    Chunk a unicode message into lines with a max_length in bytes.

    Splits the message by linebreak chars, then words, and finally letters to
    keep the string chunks short enough.
    """
    return list(_chunk_message(message, max_length))
