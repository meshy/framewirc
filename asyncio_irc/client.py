from . import utils


class Client(utils.RequiredAttributesMixin):
    required_attributes = ['handlers']

    def handle(self, message):
        """Dispatch the message to all handlers."""
        for handler in self.handlers:
            handler(self, message)
