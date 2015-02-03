from bs4 import UnicodeDammit


def decode_bytes(bytestring):
    """Try to decode as UTF8, then fall back to UnicodeDammit."""
    try:
        return bytestring.decode()
    except UnicodeDecodeError:
        guesses = ['latin-1', 'iso-8859-1']
        return UnicodeDammit(bytestring, guesses).markup
