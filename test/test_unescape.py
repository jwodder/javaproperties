import pytest
from   javaproperties import InvalidUEscapeError, unescape

@pytest.mark.parametrize('sin,sout', [
    ('', ''),
    ('foobar', 'foobar'),
    (' space around ', ' space around '),
    ('\\ space\\ around\\ ', ' space around '),
    ('\\ \\ \\ ', '   '),
    ('\\u0000', '\0'),
    ('\\0', '0'),
    ('\\a', 'a'),
    ('\\b', 'b'),
    ('\\t', '\t'),
    ('\\n', '\n'),
    ('\\v', 'v'),
    ('\\f', '\f'),
    ('\\r', '\r'),
    ('\\e', 'e'),
    ('\\u001F', '\x1F'),
    ('\\q', 'q'),
    ('\\xF0', 'xF0'),
    ('\\!', '!'),
    ('\\#', '#'),
    ('\\:', ':'),
    ('\\=', '='),
    ('\\\\', '\\'),
    ('\\\\u2603', '\\u2603'),
    ('\\u007f', '\x7F'),
    ('\\u00f0', '\xF0'),
    ('\\u2603', '\u2603'),
    ('\\u012345678', '\u012345678'),
    ('\\uabcd', '\uABCD'),
    ('\\uABCD', '\uABCD'),
    ('\\ud83d\\udc10', '\U0001F410'),
    ('\\U0001f410', 'U0001f410'),
    ('\\udc10\\ud83d', '\uDC10\uD83D'),
    ('\0', '\0'),
    ('\t', '\t'),
    ('\n', '\n'),
    ('\x7F', '\x7F'),
    ('\xF0', '\xF0'),
    ('\u2603', '\u2603'),
    ('\U0001F410', '\U0001F410'),
])
def test_unescape(sin, sout):
    assert unescape(sin) == sout

@pytest.mark.parametrize('s,esc', [
    ('\\u', '\\u'),
    ('\\u ', '\\u '),
    ('\\ux', '\\ux'),
    ('\\uab', '\\uab'),
    ('\\uab\\cd', '\\uab\\c'),
    ('\\uab\\u0063d', '\\uab\\u'),
    ('\\uabc', '\\uabc'),
    ('\\uabc ', '\\uabc '),
    ('\\uabcx', '\\uabcx'),
    ('\\uxabc', '\\uxabc'),
    ('\\u abcx', '\\u abc'),
])
def test_unescape_invalid_u_escape(s, esc):
    with pytest.raises(InvalidUEscapeError) as excinfo:
        unescape(s)
    assert excinfo.value.escape == esc
    assert str(excinfo.value) == 'Invalid \\u escape sequence: ' + esc
