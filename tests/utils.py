from framewirc.client import Client


class BlankClient(Client):
    """A pre-configured Client for tests that reduces setup."""
    handlers = []
    nick = 'test_nick'
    real_name = 'Test User'
