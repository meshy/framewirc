"""Convert me into a quickstart or turn me into docs!"""
import asyncio

from framewirc import commands, handlers
from framewirc.client import Client
from framewirc.filters import command_blacklist, command_whitelist
from framewirc.utils import to_unicode


raw_commands = (
    commands.NOTICE,
    commands.RPL_CREATED,
    commands.RPL_ENDOFMOTD,
    commands.RPL_MOTD,
    commands.RPL_MOTDSTART,
    commands.RPL_MYINFO,
    commands.RPL_WELCOME,
    commands.RPL_YOURHOST,
)


@command_blacklist(raw_commands + (commands.PING, commands.PRIVMSG))
def console_output(client, message):
    print(message.prefix, message.command, message.params, message.suffix)


@command_whitelist(raw_commands)
def main_channel(client, message):
    print(to_unicode(message.suffix))


my_handlers = handlers.basic_handlers + (
    main_channel,
    console_output,
)


class MyClient(Client):
    handlers = my_handlers
    nick = 'meshybot'
    real_name = 'MeshyBot7'


if __name__ == '__main__':
    MyClient().connect_to('leguin.freenode.net')
    asyncio.get_event_loop().run_forever()
