from .commands import Command


def ping(connection, message):
    """On recieving PING, repond with PONG."""
    payload = Command.PONG + b' :' + message.suffix
    connection.send(payload)
