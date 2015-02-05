from .message import build_message


def ping(connection, message):
    """On recieving PING, repond with PONG."""
    payload = build_message('PONG', suffix=message.suffix)
    connection.send(payload)
