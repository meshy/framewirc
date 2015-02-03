import asyncio

from asyncio_irc.connection import Connection
from asyncio_irc.listeners import CommandListener, Listener
from asyncio_irc.commands import Command


def on_ping(connection, message):
    payload = Command.PONG.value
    if message.trailing:
        payload += b' :' + message.trailing
    connection.send(payload)


def console_output(connection, message):
    print(message.prefix, message.command, message.params, message.trailing)


listeners = (
    Listener(handler=console_output),
    CommandListener(command=Command.PING, handler=on_ping),
)


if __name__ == '__main__':
    c = Connection(
        listeners=listeners,
        host='leguin.freenode.net',
        port=6697,
    )
    asyncio.Task(c.connect())
    loop = asyncio.get_event_loop()
    loop.run_forever()
