import asyncio

from asyncio_irc.connection import Connection
from asyncio_irc.commands import Command
from asyncio_irc import handlers
from asyncio_irc.listeners import (
    BlacklistListener,
    CommandListener,
    Listener,
    WhitelistListener,
)


def console_output(connection, message):
    print(message.prefix, message.command, message.params, message.trailing)


def main_channel(connection, message):
    print(message.trailing)


simple_commands = (
    Command.NOTICE,
    Command.RPL_WELCOME,
    Command.RPL_YOURHOST,
    Command.RPL_CREATED,
    Command.RPL_MYINFO,
    Command.RPL_MOTDSTART,
    Command.RPL_MOTD,
    Command.RPL_ENDOFMOTD,
)

blacklist = simple_commands + (Command.PING,)


listeners = (
    CommandListener(command=Command.PING, handler=handlers.ping),
    WhitelistListener(whitelist=simple_commands, handler=main_channel),
    BlacklistListener(blacklist=blacklist, handler=console_output),
)


if __name__ == '__main__':
    c = Connection(
        listeners=listeners,
        host='leguin.freenode.net',
        port=6697,
        nick='meshybot',
        real_name='MeshyBot7',
    )
    asyncio.Task(c.connect())
    loop = asyncio.get_event_loop()
    loop.run_forever()
