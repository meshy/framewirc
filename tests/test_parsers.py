from unittest import TestCase

from framewirc.parsers import nick


class TestNick(TestCase):
    """The nick parser can deal with several nick formats."""
    def test_nick_with_ident(self):
        raw_nick = 'nickname!ident@hostname'

        result = nick(raw_nick)

        expected = {
            'nick': 'nickname',
            'ident': 'ident',
            'host': 'hostname',
        }
        self.assertEqual(result, expected)

    def test_nick_without_ident(self):
        raw_nick = '~nickname@hostname'

        result = nick(raw_nick)

        expected = {
            'nick': 'nickname',
            'ident': None,
            'host': 'hostname',
        }
        self.assertEqual(result, expected)
