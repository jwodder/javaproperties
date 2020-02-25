from   __future__     import unicode_literals
import pytest
from   javaproperties import escape

@pytest.mark.parametrize('sin,sout', [
    ('', ''),
    ('foobar', 'foobar'),
    ('inner space', 'inner\\ space'),
    (' leading', '\\ leading'),
    ('trailing ', 'trailing\\ '),
    ('   ', '\\ \\ \\ '),
    ('\0', '\\u0000'),
    ('\a', '\\u0007'),
    ('\b', '\\u0008'),
    ('\t', '\\t'),
    ('\n', '\\n'),
    ('\v', '\\u000b'),
    ('\f', '\\f'),
    ('\r', '\\r'),
    ('\x1B', '\\u001b'),
    ('\x1F', '\\u001f'),
    ('!', '\\!'),
    ('#', '\\#'),
    (':', '\\:'),
    ('=', '\\='),
    ('\\', '\\\\'),
    ('\\u2603', '\\\\u2603'),
    ('~', '~'),
    ('\x7F', '\\u007f'),
    ('\xF0', '\\u00f0'),
    ('\u2603', '\\u2603'),
    ('\U0001F410', '\\ud83d\\udc10'),
    ('\uDC10\uD83D', '\\udc10\\ud83d'),
])
def test_escape(sin, sout):
    assert escape(sin) == sout
