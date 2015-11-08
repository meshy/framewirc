from unittest import TestCase

from framewirc.parsers import is_channel, nick


class TestIsChannel(TestCase):
    """Tests for the boolean function is_channel."""
    def test_starts_with_ampersand(self):
        """True when starts with an & ("ampersand")."""
        self.assertTrue(is_channel('&channel'))

    def test_starts_with_exclamtion_mark(self):
        """True when starts with an ! ("exclamation mark" AKA "bang")."""
        self.assertTrue(is_channel('!channel'))

    def test_starts_with_hash(self):
        """True when starts with a # ("hash", AKA "pound")."""
        self.assertTrue(is_channel('#channel'))

    def test_starts_with_plus(self):
        """True when starts with a + ("plus" AKA "add")."""
        self.assertTrue(is_channel('+channel'))

    def test_starts_with_alpha_char(self):
        self.assertFalse(is_channel('channel'))

    def test_50_chars(self):
        """True when up to 50 chars."""
        channel = '#' + 49 * 'a'
        self.assertTrue(is_channel(channel))

    def test_51_chars(self):
        """False when 51 chars or more."""
        channel = '#' + 50 * 'a'
        self.assertFalse(is_channel(channel))

    def test_contains_space(self):
        """False when contains space."""
        self.assertFalse(is_channel('#contains space'))

    def test_contains_comma(self):
        """False when contains comma."""
        self.assertFalse(is_channel('#contains,comma'))

    def test_contains_bel(self):
        """False when contains ASCII BEL control char."""
        # "\7" is one way python can escape the ASCII BEL char.
        self.assertFalse(is_channel('#contains\7BEL'))


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
