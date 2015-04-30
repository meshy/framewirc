import asyncio

from asyncio_irc import commands, handlers
from asyncio_irc.client import Client
from asyncio_irc.filters import command_blacklist, command_whitelist
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
def console_output(client, message):
    print(message.prefix, message.command, message.params, message.suffix)


@command_whitelist(raw_commands)
def main_channel(client, message):
    print(to_unicode(message.suffix))


handlers = (
    handlers.ping,
    main_channel,
    console_output,
)


class MyClient(Client):
    handlers = handlers
    nick = 'meshybot'
    real_name = 'MeshyBot7'

if __name__ == '__main__':
    MyClient().connect_to('leguin.freenode.net')
    asyncio.get_event_loop().run_forever()
