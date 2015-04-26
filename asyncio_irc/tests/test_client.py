from unittest import mock, TestCase

from ..client import Client
from ..message import ReceivedMessage


class TestRequiredFields(TestCase):
    """Test to show that RequiredAttribuesMixin is properly configured."""
    def test_fields(self):
        """Are the correct fields being checked?"""
        required = ['handlers']
        self.assertCountEqual(Client.required_attributes, required)

    def test_uses_required_attributes_mixin(self):
        """Is RequiredAttributesMixin.__init__ actually getting called?"""
        kwargs = {'handlers': []}
        path = 'asyncio_irc.utils.RequiredAttributesMixin.__init__'
        with mock.patch(path, return_value=None) as mixin_init:
            Client(**kwargs)

        mixin_init.assert_called_with(**kwargs)


class TestClientHandle(TestCase):
    def test_handlers_called(self):
        """When a message comes in, it should be passed to the handlers."""
        handler = mock.MagicMock()
        client = Client(handlers=[handler])
        message = ReceivedMessage(b'TEST message\r\n')

        client.handle(message)

        handler.assert_called_with(client, message)
