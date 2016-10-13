import cchardet


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
