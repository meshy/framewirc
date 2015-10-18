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
