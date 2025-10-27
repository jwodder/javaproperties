import pytest
from javaproperties import escape


@pytest.mark.parametrize(
    "sin,sout",
    [
        ("", ""),
        ("foobar", "foobar"),
        ("inner space", "inner\\ space"),
        (" leading", "\\ leading"),
        ("trailing ", "trailing\\ "),
        ("   ", "\\ \\ \\ "),
        ("\0", "\\u0000"),
        ("\a", "\\u0007"),
        ("\b", "\\u0008"),
        ("\t", "\\t"),
        ("\n", "\\n"),
        ("\v", "\\u000b"),
        ("\f", "\\f"),
        ("\r", "\\r"),
        ("\x1b", "\\u001b"),
        ("\x1f", "\\u001f"),
        ("!", "\\!"),
        ("#", "\\#"),
        (":", "\\:"),
        ("=", "\\="),
        ("\\", "\\\\"),
        ("\\u2603", "\\\\u2603"),
        ("~", "~"),
        ("\x7f", "\\u007f"),
        ("\xf0", "\\u00f0"),
        ("\u2603", "\\u2603"),
        ("\U0001f410", "\\ud83d\\udc10"),
        ("\udc10\ud83d", "\\udc10\\ud83d"),
    ],
)
def test_escape(sin, sout):
    assert escape(sin) == sout


@pytest.mark.parametrize(
    "sin,sout",
    [
        ("", ""),
        ("foobar", "foobar"),
        ("inner space", "inner\\ space"),
        (" leading", "\\ leading"),
        ("trailing ", "trailing\\ "),
        ("   ", "\\ \\ \\ "),
        ("\0", "\\u0000"),
        ("\a", "\\u0007"),
        ("\b", "\\u0008"),
        ("\t", "\\t"),
        ("\n", "\\n"),
        ("\v", "\\u000b"),
        ("\f", "\\f"),
        ("\r", "\\r"),
        ("\x1b", "\\u001b"),
        ("\x1f", "\\u001f"),
        ("!", "\\!"),
        ("#", "\\#"),
        (":", "\\:"),
        ("=", "\\="),
        ("\\", "\\\\"),
        ("\\u2603", "\\\\u2603"),
        ("~", "~"),
        ("\x7f", "\\u007f"),
        ("\x80", "\x80"),
        ("\xa0", "\xa0"),
        ("\xf0", "\xf0"),
        ("\u2603", "\u2603"),
        ("\U0001f410", "\U0001f410"),
        ("\udc10\ud83d", "\udc10\ud83d"),
    ],
)
def test_escape_no_ensure_ascii(sin, sout):
    assert escape(sin, ensure_ascii=False) == sout
