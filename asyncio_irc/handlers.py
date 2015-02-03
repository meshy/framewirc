from .commands import Command


def ping(connection, message):
    """On recieving PING, repond with PONG."""
    payload = Command.PONG.value
    if message.trailing:
        payload += b' :' + message.trailing
    connection.send(payload)
