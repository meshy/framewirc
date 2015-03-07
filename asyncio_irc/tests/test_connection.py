from unittest import mock, TestCase

from ..connection import Connection
from ..exceptions import (
    MessageTooLong,
    MissingAttributes,
    MustBeBytes,
    NoLineEnding,
    StrayLineEnding,
)


class ConnectionInitTest(TestCase):
    handlers = [mock.Mock()]
    host = 'test.example.com'
    port = 1337
    nick = 'meshy'
    ssl = mock.Mock()
    real_name = 'Charlie Denton'

    def get_init_params(self, remove=()):
        params = {
            'handlers': self.handlers,
            'host': self.host,
            'port': self.port,
            'nick': self.nick,
            'ssl': self.ssl,
            'real_name': self.real_name,
        }
        for to_remove in remove:
            params.pop(to_remove)
        return params

    def test_set_on_init(self):
        """Make sure that __init__ params override defaults."""
        connection = Connection(**self.get_init_params())

        self.assertEqual(connection.handlers, self.handlers)
        self.assertEqual(connection.host, self.host)
        self.assertEqual(connection.port, self.port)
        self.assertEqual(connection.ssl, self.ssl)
        self.assertEqual(connection.nick, self.nick)
        self.assertEqual(connection.real_name, self.real_name)

    def test_set_on_subclass(self):
        """Make sure that defaults are not overridden when params missing."""

        class MyConnection(Connection):
            handlers = self.handlers
            host = self.host
            port = self.port
            ssl = self.ssl
            real_name = self.real_name

        connection = MyConnection(nick=self.nick)

        self.assertEqual(connection.handlers, self.handlers)
        self.assertEqual(connection.host, self.host)
        self.assertEqual(connection.port, self.port)
        self.assertEqual(connection.ssl, self.ssl)
        self.assertEqual(connection.nick, self.nick)

    def test_handlers_not_set(self):
        """An error should be thrown when the handlers are undefined."""
        missing = 'handlers'
        params = self.get_init_params(remove=(missing,))

        with self.assertRaises(MissingAttributes) as cm:
            Connection(**params)

        self.assertIn(missing, str(cm.exception))

    def test_host_not_set(self):
        """An error should be thrown when the host is undefined."""
        missing = 'host'
        params = self.get_init_params(remove=(missing,))

        with self.assertRaises(MissingAttributes) as cm:
            Connection(**params)

        self.assertIn(missing, str(cm.exception))

    def test_port_not_set(self):
        """An error should be thrown when the port is undefined."""
        missing = 'port'
        params = self.get_init_params(remove=(missing,))

        with self.assertRaises(MissingAttributes) as cm:
            Connection(**params)

        self.assertIn(missing, str(cm.exception))

    def test_nick_not_set(self):
        """An error should be thrown when the nick undefined."""
        missing = 'nick'
        params = self.get_init_params(remove=(missing,))

        with self.assertRaises(MissingAttributes) as cm:
            Connection(**params)

        self.assertIn(missing, str(cm.exception))

    def test_ssl_not_set(self):
        """An error should be thrown when ssl is undefined."""
        missing = 'ssl'
        params = self.get_init_params(remove=(missing,))

        with self.assertRaises(MissingAttributes) as cm:
            Connection(**params)

        self.assertIn(missing, str(cm.exception))

    def test_real_name_not_set(self):
        """An error should be thrown when the real_name undefined."""
        missing = 'real_name'
        params = self.get_init_params(remove=(missing,))

        with self.assertRaises(MissingAttributes) as cm:
            Connection(**params)

        self.assertIn(missing, str(cm.exception))


class ConnectionTestCase(TestCase):
    def setUp(self):
        self.connection = Connection(
            handlers=[],
            host='example.com',
            port=6697,
            ssl=True,
            nick='unused',
            real_name='Charlie Denton',
        )
        self.connection.writer = mock.MagicMock()


class TestSend(ConnectionTestCase):
    def test_ideal_case(self):
        message = b'PRIVMSG meshy :Nice IRC lib you have there\r\n'
        self.connection.send(message)
        self.connection.writer.write.assert_called_with(message)

    def test_not_bytes(self):
        message = 'PRIVMSG meshy :Nice IRC lib you have there\r\n'
        with self.assertRaises(MustBeBytes):
            self.connection.send(message)
        self.assertFalse(self.connection.writer.write.called)

    def test_only_one_line_ending(self):
        message = b'PRIVMSG meshy :Nice \r\nCODE :injection you have there\r\n'
        with self.assertRaises(StrayLineEnding):
            self.connection.send(message)
        self.assertFalse(self.connection.writer.write.called)

    def test_line_ending_at_eol(self):
        message = b'PRIVMSG meshy :Nice line ending you have forgotten there'
        with self.assertRaises(NoLineEnding):
            self.connection.send(message)
        self.assertFalse(self.connection.writer.write.called)

    def test_message_too_long(self):
        message = b'FIFTEEN chars :' + 496 * b'a' + b'\r\n'  # 513 chars
        with self.assertRaises(MessageTooLong):
            self.connection.send(message)
        self.assertFalse(self.connection.writer.write.called)

    def test_message_just_right(self):
        message = b'FIFTEEN chars :' + 495 * b'a' + b'\r\n'  # 512 chars
        self.connection.send(message)
        self.connection.writer.write.assert_called_with(message)


class TestSendBatch(ConnectionTestCase):
    def test_send_batch(self):
        messages = [
            b'PRVMSG meshy :Getting there\r\n',
            b'PRVMSG meshy :It is almost usable!\r\n',
        ]
        self.connection.send_batch(messages)
        calls = self.connection.writer.write.mock_calls
        self.assertEqual(calls, list(map(mock.call, messages)))


class TestSetNick(ConnectionTestCase):
    def test_command_sent(self):
        new_nick = 'meshy'
        self.connection.set_nick(new_nick)
        self.connection.writer.write.assert_called_with(b'NICK meshy\r\n')

    def test_new_nick_kept(self):
        new_nick = 'meshy'
        self.connection.set_nick(new_nick)
        self.assertEqual(self.connection.nick, new_nick)
