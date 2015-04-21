def command_blacklist(blacklist):
    """
    Decorates a handler to filter out a blacklist of commands.

    The decorated handler will not be called if message.command is in the
    blacklist:

        @command_blacklist(['A', 'B'])
        def handle_everything_except_a_and_b(connection, message):
            pass

    Single-item blacklists may be passed as a string:

        @command_blacklist('THIS')
        def handle_everything_except_this(connection, message):
            pass
    """
    blacklist = [blacklist] if isinstance(blacklist, str) else blacklist

    def inner_decorator(handler):
        def wrapped(connection, message):
            if message.command not in blacklist:
                handler(connection=connection, message=message)
        return wrapped
    return inner_decorator


def command_whitelist(whitelist):
    """
    Decorates a handler to filter all except a whitelist of commands

    The decorated handler will only be called if message.command is in the
    whitelist:

        @command_whitelist(['A', 'B'])
        def handle_only_a_and_b(connection, message):
            pass

    Single-item whitelists may be passed as a string:

        @command_whitelist('THIS')
        def handle_only_this(connection, message):
            pass
    """
    whitelist = [whitelist] if isinstance(whitelist, str) else whitelist

    def inner_decorator(handler):
        def wrapped(connection, message):
            if message.command in whitelist:
                handler(connection=connection, message=message)
        return wrapped
    return inner_decorator
