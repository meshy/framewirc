from itertools import product
from unittest import TestCase

from ..message import Message


class TestMessage(TestCase):
    """Test the Message class."""
    def test_possibilities(self):
        """
        Make sure that Messages can be created.

        Checks every combination of a prefix, params, and trailing data.
        """
        choices = True, False
        for prefix, params, trailing in product(choices, choices, choices):
            with self.subTest(prefix=prefix, params=params, trailing=trailing):
                raw_message = b'COMMAND'
                if prefix:
                    raw_message = b':prefixed-data ' + raw_message
                if params:
                    raw_message += b' param1 param2'
                if trailing:
                    raw_message += b' :trailing message'

                message = Message(raw_message)

                expected_prefix = b'prefixed-data' if prefix else b''
                expected_params = [b'param1', b'param2'] if params else []
                expected_trailing = b'trailing message' if trailing else b''

                self.assertEqual(message.command, b'COMMAND')
                self.assertEqual(message.prefix, expected_prefix)
                self.assertEqual(message.params, expected_params)
                self.assertEqual(message.trailing, expected_trailing)
