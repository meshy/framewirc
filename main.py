import asyncio

from asyncio_irc.connection import Connection
from asyncio_irc.listeners import CommandListener, Listener


def on_ping(connection, message):
    payload = b'PONG'
    if message.params:
        payload += b' ' + b' '.join(message.params)
    connection.send(payload)


def console_output(connection, message):
    print(message.prefix, message.command, message.params, message.trailing)


listeners = [
    Listener(handler=console_output),
    CommandListener(command=b'PING', handler=on_ping),
]


c = Connection(listeners, 'leguin.freenode.net', 6697)
asyncio.Task(c.connect())
loop = asyncio.get_event_loop()
loop.run_forever()
