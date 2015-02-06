from . import commands, filters
from .message import build_message


@filters.command_only(commands.PING)
def ping(connection, message):
    """On recieving PING, repond with PONG."""
    payload = build_message('PONG', suffix=message.suffix)
    connection.send(payload)
