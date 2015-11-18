def is_channel(name):
    """
    Determine if a string is a valid channel name.

    The exact text from RFC2812 §1.3 is as follows:

    Channels names are strings (beginning with a '&', '#', '+' or '!'
    character) of length up to fifty (50) characters.  Apart from the
    requirement that the first character is either '&', '#', '+' or '!',
    the only restriction on a channel name is that it SHALL NOT contain
    any spaces (' '), a control G (^G or ASCII 7), a comma (',').  Space
    is used as parameter separator and command is used as a list item
    separator by the protocol).  A colon (':') can also be used as a
    delimiter for the channel mask.  Channel names are case insensitive.
    """
    if len(name) > 50:
        return False
    if set(name).intersection(',\7 '):  # Note the space
        return False
    if name[0] not in '&#+!':
        return False
    return True


def nick(raw_nick):
    """
    Split nick into constituent parts.

    Nicks with an ident are in the following format:

        nick!ident@hostname

    When they don't have an ident, they have a leading tilde instead:

        ~nick@hostname
    """
    if '!' in raw_nick:
        nick, _rest = raw_nick.split('!')
        ident, host = _rest.split('@')
    else:
        nick, host = raw_nick.split('@')
        nick = nick.lstrip('~')
        ident = None
    return {
        'nick': nick,
        'ident': ident,
        'host': host,
    }


def privmsg(message):
    """
    Split received PRIVMSG command into a dictionary of parts.

    When the message target is a channel, 'channel' is set to that. Otherwise,
    'channel' is defined as the sender's nick.
    """
    target = message.params[0]
    raw_sender = message.prefix
    sender_nick = nick(raw_sender)['nick']

    if is_channel(target):
        channel = target
    else:
        channel = sender_nick

    raw_body = message.suffix
    third_person = False
    if raw_body.startswith(b'\1ACTION ') and raw_body.endswith(b'\1'):  # /me
        third_person = True
        raw_body = raw_body.lstrip(b'\1ACTION ').rstrip(b'\1')

    return {
        'channel': channel,
        'raw_body': raw_body,
        'raw_sender': raw_sender,
        'sender_nick': sender_nick,
        'target': target,
        'third_person': third_person,
    }


def apply_kwargs_parser(parser):
    """
    Decorator that passes the result of a kwargs parser to a handler as kwargs.

    The parser needs to accept any number of kwargs.

    Keys returned by the parser will overwrite those that the handler would
    otherwise have received.
    """
    def inner_decorator(handler):
        def wrapped(**kwargs):
            parser_result = parser(**kwargs)
            kwargs.update(parser_result)
            handler(**kwargs)
        return wrapped
    return inner_decorator


def apply_message_parser(parser):
    """
    Decorator that passes the result of a message parser to a handler as kwargs.

    The parser will only be passed a `message` kwarg.
    """
    def inner_decorator(handler):
        def wrapped(client, message):
            parser_result = parser(message=message)
            handler(client=client, message=message, **parser_result)
        return wrapped
    return inner_decorator
