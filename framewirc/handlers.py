from . import commands, filters, parsers
from .messages import build_message


@filters.allow([commands.PRIVMSG, commands.NOTICE, commands.RPL_WHOISUSER])
def capture_mask_length(client, message):
    """Try to measure the mask the network will add to PRIVMSGs."""
    if client.mask_length is not None:
        # We already know, so this can be skipped.
        return

    if message.command in [commands.PRIVMSG, commands.NOTICE]:
        nick = parsers.nick(message.prefix)['nick']
        if nick == client.nick:
            client.mask_length = len(message.prefix)
    else:  # RPL_WHOISUSER
        nick = message.params[0]
        if nick == client.nick:
            client.mask_length = len(' '.join(message.params[:-1]))


@filters.allow(commands.PING)
def ping(client, message):
    """On recieving PING, repond with PONG."""
    payload = build_message('PONG', suffix=message.suffix)
    client.connection.send(payload)


@filters.allow(commands.ERR_NICKNAMEINUSE)
def nickname_in_use(client, message):
    """If nick is being used, append a caret."""
    client.set_nick(client.nick + '^')


basic_handlers = (capture_mask_length, ping, nickname_in_use)
