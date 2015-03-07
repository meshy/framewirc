from unittest import TestCase

from .. import exceptions


class MissingAttributesTest(TestCase):
    def test_message(self):
        attrs = ['some', 'attrs']
        expected = 'Required attribute(s) missing: {}'.format(attrs)

        exception = exceptions.MissingAttributes(attrs)

        self.assertEqual(str(exception), expected)
