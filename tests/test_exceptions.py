from framewirc import exceptions


def test_message():
    attrs = ['some', 'attrs']
    expected = 'Required attribute(s) missing: {}'.format(attrs)

    exception = exceptions.MissingAttributes(attrs)

    assert str(exception) == expected
