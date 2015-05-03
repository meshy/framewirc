import asyncio

from . import commands
from . import utils
from .connection import Connection
from .message import build_message, make_privmsgs


class Client(utils.RequiredAttributesMixin):
    """Handle events from Connection and offer methods for sending data."""
    connection_class = Connection
    required_attributes = ('handlers', 'real_name', 'nick')

    def connect_to(self, host, **kwargs):
        """Create a Connection. Handled in the event loop."""
        self.connection = self.connection_class(client=self, host=host, **kwargs)
        return asyncio.Task(self.connection.connect())

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

    def privmsg(self, target, message):
        self.connection.send_batch(make_privmsgs(target, message))

    def set_nick(self, new_nick):
        """Set a nick on the network."""
        self.connection.send(build_message(commands.NICK, new_nick))
        self.nick = new_nick
