from unittest import TestCase

from framewirc.parsers import nick


class TestNick(TestCase):
    """The nick parser can deal with several nick formats."""
    def test_nick_with_ident(self):
        result = nick('nickname!ident@hostname')

        expected = {
            'nick': 'nickname',
            'ident': 'ident',
            'host': 'hostname',
        }
        self.assertEqual(result, expected)

    def test_nick_without_ident(self):
        result = nick('~nickname@hostname')

        expected = {
            'nick': 'nickname',
            'ident': None,
            'host': 'hostname',
        }
        self.assertEqual(result, expected)
