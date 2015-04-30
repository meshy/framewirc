from . import commands, filters
from .message import build_message


@filters.command_whitelist(commands.PING)
def ping(client, message):
    """On recieving PING, repond with PONG."""
    payload = build_message('PONG', suffix=message.suffix)
    client.connection.send(payload)


@filters.command_whitelist(commands.ERR_NICKNAMEINUSE)
def nickname_in_use(client, message):
    """If nick is being used, append a caret."""
    client.set_nick(client.nick + '^')


basic_handlers = (ping, nickname_in_use)
