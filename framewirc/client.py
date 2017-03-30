import asyncio

from . import commands, utils
from .connection import Connection
from .messages import build_message, make_privmsgs


class Client(utils.RequiredAttributesMixin):
    """Handle events from Connection and offer methods for sending data."""
    connection_class = Connection
    required_attributes = ('handlers', 'real_name', 'nick')

    def connect_to(self, host, **kwargs):
        """Create a Connection. Handled in the event loop."""
        self.connection = self.connection_class(client=self, host=host, **kwargs)
        loop = asyncio.get_event_loop()
        return loop.create_task(self.connection.connect())

    def join(self, *channels):
        """Join a number of channels."""
        msg = build_message(commands.JOIN, ','.join(channels))
        self.connection.send(msg)

    def on_connect(self):
        """We're connected! Send our identity to the network!"""
        nick = self.nick
        msg = build_message(commands.USER, nick, '0 *', suffix=self.real_name)
        self.connection.send(msg)
        self.set_nick(nick)

    def on_message(self, message):
        """Get a message from IRC and send it to all handlers."""
        for handler in self.handlers:
            handler(self, message)

    def part(self, *channels, message=b''):
        """Part from a number of channels (message optional)."""
        msg = build_message(commands.PART, ','.join(channels), suffix=message)
        self.connection.send(msg)

    def privmsg(self, target, message, third_person=False):
        self.connection.send_batch(make_privmsgs(target, message, third_person))

    def set_nick(self, new_nick):
        """Set a nick on the network."""
        self.connection.send(build_message(commands.NICK, new_nick))
        self.nick = new_nick
