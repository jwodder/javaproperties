import pytest
from javaproperties import to_comment

# All C0 and C1 control characters other than \n and \r:
s = "".join(
    chr(i) for i in list(range(0x20)) + list(range(0x7F, 0xA0)) if i not in (10, 13)
)


@pytest.mark.parametrize(
    "cin,cout",
    [
        ("", "#"),
        ("foobar", "#foobar"),
        (" leading", "# leading"),
        ("trailing ", "#trailing "),
        ("   ", "#   "),
        ("This is a comment.", "#This is a comment."),
        ("#This is a double comment.", "##This is a double comment."),
        ("trailing newline\n", "#trailing newline\n#"),
        ("trailing CRLF\r\n", "#trailing CRLF\n#"),
        ("trailing carriage return\r", "#trailing carriage return\n#"),
        ("line one\nline two", "#line one\n#line two"),
        ("line one\n#line two", "#line one\n#line two"),
        ("line one\n!line two", "#line one\n!line two"),
        ("\0", "#\0"),
        ("\a", "#\a"),
        ("\b", "#\b"),
        ("\t", "#\t"),
        ("\n", "#\n#"),
        ("\v", "#\v"),
        ("\f", "#\f"),
        ("\r", "#\n#"),
        ("\x1B", "#\x1B"),
        ("\x1F", "#\x1F"),
        ("!", "#!"),
        ("#", "##"),
        (":", "#:"),
        ("=", "#="),
        ("\\", "#\\"),
        ("\\u2603", "#\\u2603"),
        ("~", "#~"),
        ("\x7F", "#\x7F"),
        ("\x80", "#\x80"),
        ("\xA0", "#\xA0"),
        ("\xF0", "#\xF0"),
        ("\xFF", "#\xFF"),
        ("\u0100", "#\\u0100"),
        ("\u2603", "#\\u2603"),
        ("\U0001F410", "#\\ud83d\\udc10"),
        ("\uDC10\uD83D", "#\\udc10\\ud83d"),
        (s, "#" + s),
    ],
)
def test_to_comment(cin, cout):
    assert to_comment(cin) == cout
    assert to_comment(cin, ensure_ascii=None) == cout


@pytest.mark.parametrize(
    "cin,cout",
    [
        ("", "#"),
        ("foobar", "#foobar"),
        (" leading", "# leading"),
        ("trailing ", "#trailing "),
        ("   ", "#   "),
        ("This is a comment.", "#This is a comment."),
        ("#This is a double comment.", "##This is a double comment."),
        ("trailing newline\n", "#trailing newline\n#"),
        ("trailing CRLF\r\n", "#trailing CRLF\n#"),
        ("trailing carriage return\r", "#trailing carriage return\n#"),
        ("line one\nline two", "#line one\n#line two"),
        ("line one\n#line two", "#line one\n#line two"),
        ("line one\n!line two", "#line one\n!line two"),
        ("\0", "#\0"),
        ("\a", "#\a"),
        ("\b", "#\b"),
        ("\t", "#\t"),
        ("\n", "#\n#"),
        ("\v", "#\v"),
        ("\f", "#\f"),
        ("\r", "#\n#"),
        ("\x1B", "#\x1B"),
        ("\x1F", "#\x1F"),
        ("!", "#!"),
        ("#", "##"),
        (":", "#:"),
        ("=", "#="),
        ("\\", "#\\"),
        ("\\u2603", "#\\u2603"),
        ("~", "#~"),
        ("\x7F", "#\x7F"),
        ("\x80", "#\x80"),
        ("\xA0", "#\xA0"),
        ("\xF0", "#\xF0"),
        ("\xFF", "#\xFF"),
        ("\u0100", "#\u0100"),
        ("\u2603", "#\u2603"),
        ("\U0001F410", "#\U0001F410"),
        ("\uDC10\uD83D", "#\uDC10\uD83D"),
        (s, "#" + s),
    ],
)
def test_to_comment_no_ensure_ascii(cin, cout):
    assert to_comment(cin, ensure_ascii=False) == cout


@pytest.mark.parametrize(
    "cin,cout",
    [
        ("", "#"),
        ("foobar", "#foobar"),
        (" leading", "# leading"),
        ("trailing ", "#trailing "),
        ("   ", "#   "),
        ("This is a comment.", "#This is a comment."),
        ("#This is a double comment.", "##This is a double comment."),
        ("trailing newline\n", "#trailing newline\n#"),
        ("trailing CRLF\r\n", "#trailing CRLF\n#"),
        ("trailing carriage return\r", "#trailing carriage return\n#"),
        ("line one\nline two", "#line one\n#line two"),
        ("line one\n#line two", "#line one\n#line two"),
        ("line one\n!line two", "#line one\n!line two"),
        ("\0", "#\0"),
        ("\a", "#\a"),
        ("\b", "#\b"),
        ("\t", "#\t"),
        ("\n", "#\n#"),
        ("\v", "#\v"),
        ("\f", "#\f"),
        ("\r", "#\n#"),
        ("\x1B", "#\x1B"),
        ("\x1F", "#\x1F"),
        ("!", "#!"),
        ("#", "##"),
        (":", "#:"),
        ("=", "#="),
        ("\\", "#\\"),
        ("\\u2603", "#\\u2603"),
        ("~", "#~"),
        ("\x7F", "#\x7F"),
        ("\x80", "#\\u0080"),
        ("\xA0", "#\\u00a0"),
        ("\xF0", "#\\u00f0"),
        ("\xFF", "#\\u00ff"),
        ("\u0100", "#\\u0100"),
        ("\u2603", "#\\u2603"),
        ("\U0001F410", "#\\ud83d\\udc10"),
        ("\uDC10\uD83D", "#\\udc10\\ud83d"),
        (
            s,
            "#"
            + "".join(chr(i) for i in list(range(0x20)) + [0x7F] if i not in (10, 13))
            + "".join(f"\\u{i:04x}" for i in range(0x80, 0xA0)),
        ),
    ],
)
def test_to_comment_ensure_ascii(cin, cout):
    assert to_comment(cin, ensure_ascii=True) == cout
