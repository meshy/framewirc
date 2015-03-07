class MessageTooLong(Exception):
    pass


class MissingAttributes(Exception):
    def __init__(self, attrs):
        msg = 'Required attribute(s) missing: {}'.format(attrs)
        super().__init__(msg)


class NoLineEnding(Exception):
    pass


class StrayLineEnding(Exception):
    pass
