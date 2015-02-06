def command_blacklist(blacklist):
    """Decorates a handler to filter out a blacklist of commands."""
    def inner_decorator(handler):
        def wrapped(connection, message):
            if message.command not in blacklist:
                handler(connection=connection, message=message)
        return wrapped
    return inner_decorator


def command_only(command):
    """Decorates a handler to filter all but one particular command."""
    def inner_decorator(handler):
        def wrapped(connection, message):
            if message.command == command:
                handler(connection=connection, message=message)
        return wrapped
    return inner_decorator


def command_whitelist(whitelist):
    """Decorates a handler to filter all except a whitelist of commands."""
    def inner_decorator(handler):
        def wrapped(connection, message):
            if message.command in whitelist:
                handler(connection=connection, message=message)
        return wrapped
    return inner_decorator
