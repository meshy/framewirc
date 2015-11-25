def deny(blacklist):
    """
    Decorates a handler to filter out a blacklist of commands.

    The decorated handler will not be called if message.command is in the
    blacklist:

        @deny(['A', 'B'])
        def handle_everything_except_a_and_b(client, message):
            pass

    Single-item blacklists may be passed as a string:

        @deny('THIS')
        def handle_everything_except_this(client, message):
            pass
    """
    blacklist = [blacklist] if isinstance(blacklist, str) else blacklist

    def inner_decorator(handler):
        def wrapped(client, message):
            if message.command not in blacklist:
                handler(client=client, message=message)
        return wrapped
    return inner_decorator


def allow(whitelist):
    """
    Decorates a handler to filter all except a whitelist of commands

    The decorated handler will only be called if message.command is in the
    whitelist:

        @allow(['A', 'B'])
        def handle_only_a_and_b(client, message):
            pass

    Single-item whitelists may be passed as a string:

        @allow('THIS')
        def handle_only_this(client, message):
            pass
    """
    whitelist = [whitelist] if isinstance(whitelist, str) else whitelist

    def inner_decorator(handler):
        def wrapped(client, message):
            if message.command in whitelist:
                handler(client=client, message=message)
        return wrapped
    return inner_decorator
