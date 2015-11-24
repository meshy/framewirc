from framewirc import exceptions


class MissingAttributesTest:
    def test_message(self):
        attrs = ['some', 'attrs']
        expected = 'Required attribute(s) missing: {}'.format(attrs)

        exception = exceptions.MissingAttributes(attrs)

        assert str(exception) == expected
