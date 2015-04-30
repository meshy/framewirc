from . import commands, filters
from .message import build_message


@filters.command_whitelist(commands.PING)
def ping(client, message):
    """On recieving PING, repond with PONG."""
    payload = build_message('PONG', suffix=message.suffix)
    client.connection.send(payload)
