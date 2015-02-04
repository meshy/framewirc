from itertools import product
from unittest import TestCase

from ..message import Message


class TestMessage(TestCase):
    """Test the Message class."""
    def build_message(self, prefix, params, suffix):
        raw_message = b'COMMAND'
        if prefix:
            raw_message = b':prefixed-data ' + raw_message
        if params:
            raw_message += b' param1 param2'
        if suffix:
            raw_message += b' :suffix message'

        return raw_message

    def test_possibilities(self):
        """
        Make sure that Messages can be created.

        Checks every combination of a prefix, params, and suffix data.
        """
        on_off = True, False
        for prefix, params, suffix in product(on_off, on_off, on_off):
            with self.subTest(prefix=prefix, params=params, suffix=suffix):
                raw_message = self.build_message(prefix, params, suffix)

                message = Message(raw_message)

                expected_prefix = b'prefixed-data' if prefix else b''
                expected_params = [b'param1', b'param2'] if params else []
                expected_suffix = b'suffix message' if suffix else b''

                self.assertEqual(message.command, b'COMMAND')
                self.assertEqual(message.prefix, expected_prefix)
                self.assertEqual(message.params, expected_params)
                self.assertEqual(message.suffix, expected_suffix)
