import cchardet


def to_unicode(bytestring):
    """Try to decode as UTF8, then fall back to cchatdet."""
    try:
        return bytestring.decode()
    except AttributeError:
        if not isinstance(bytestring, str):
            raise
        return bytestring
    except UnicodeDecodeError:
        charset = cchardet.detect(bytestring)['encoding']
        return bytestring.decode(charset)


def to_bytes(string):
    try:
        return string.encode()
    except AttributeError:
        if not isinstance(string, bytes):
            raise
        return string
