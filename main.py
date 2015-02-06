import asyncio

from asyncio_irc import commands, handlers
from asyncio_irc.connection import Connection
from asyncio_irc.listeners import (
    BlacklistListener,
    CommandListener,
    WhitelistListener,
)
from asyncio_irc.utils import to_unicode


def console_output(connection, message):
    print(message.prefix, message.command, message.params, message.suffix)


def main_channel(connection, message):
    print(to_unicode(message.suffix))


raw_commands = (
    commands.NOTICE,
    commands.RPL_WELCOME,
    commands.RPL_YOURHOST,
    commands.RPL_CREATED,
    commands.RPL_MYINFO,
    commands.RPL_MOTDSTART,
    commands.RPL_MOTD,
    commands.RPL_ENDOFMOTD,
)

blacklist = raw_commands + (commands.PING,)


handlers = (
    CommandListener(command=commands.PING, handler=handlers.ping),
    WhitelistListener(whitelist=simple_commands, handler=main_channel),
    BlacklistListener(blacklist=blacklist, handler=console_output),
)


if __name__ == '__main__':
    c = Connection(
        handlers=handlers,
        host='leguin.freenode.net',
        port=6697,
        nick='meshybot',
        real_name='MeshyBot7',
    )
    asyncio.Task(c.connect())
    loop = asyncio.get_event_loop()
    loop.run_forever()
