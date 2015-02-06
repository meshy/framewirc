import asyncio

from asyncio_irc import commands, handlers
from asyncio_irc.connection import Connection
from asyncio_irc.filters import (
    command_blacklist,
    command_only,
    command_whitelist,
)
from asyncio_irc.utils import to_unicode


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


@command_blacklist(raw_commands + (commands.PING, commands.PRIVMSG))
def console_output(connection, message):
    print(message.prefix, message.command, message.params, message.suffix)


@command_whitelist(raw_commands)
def main_channel(connection, message):
    print(to_unicode(message.suffix))


handlers = (
    handlers.ping,
    main_channel,
    console_output,
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
