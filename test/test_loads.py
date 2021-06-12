from collections import OrderedDict
import pytest
from javaproperties import InvalidUEscapeError, loads


@pytest.mark.parametrize(
    "s,d",
    [
        ("key=value", {"key": "value"}),
        ("key", {"key": ""}),
        ("key ", {"key": ""}),
        ("key =value", {"key": "value"}),
        ("key= value", {"key": "value"}),
        ("key = value", {"key": "value"}),
        ("=value", {"": "value"}),
        (" =value", {"": "value"}),
        ("key=value ", {"key": "value "}),
        (" key=value", {"key": "value"}),
        (" = ", {"": ""}),
        ("=", {"": ""}),
        ("", {}),
        (" ", {}),
        ("\n", {}),
        ("\r\n", {}),
        ("\r", {}),
        ("#This is a comment.", {}),
        ("#This is a comment.\nkey = value", {"key": "value"}),
        ("key = value\n#This is a comment.", {"key": "value"}),
        ("!This is a comment.", {}),
        ("!This is a comment.\nkey = value", {"key": "value"}),
        ("key = value\n!This is a comment.", {"key": "value"}),
        ("key = val\\\nue", {"key": "value"}),
        ("key = val\\\n    ue", {"key": "value"}),
        ("key = val \\\nue", {"key": "val ue"}),
        ("key = val \\\n  ue", {"key": "val ue"}),
        ("ke\\\ny = value", {"key": "value"}),
        ("ke\\\n    y = value", {"key": "value"}),
        ("one two three", {"one": "two three"}),
        ("key=value\n", {"key": "value"}),
        ("key=value\r\n", {"key": "value"}),
        ("key=value\r", {"key": "value"}),
        ("key:value", {"key": "value"}),
        ("key value", {"key": "value"}),
        ("\\ key\\  = \\ value ", {" key ": " value "}),
        ("\\ key\\  : \\ value ", {" key ": " value "}),
        ("\\ key\\  \t \\ value ", {" key ": " value "}),
        ("\\ key\\    \\ value ", {" key ": " value "}),
        ("\\ key\\ =\\ value ", {" key ": " value "}),
        ("\\ key\\ :\\ value ", {" key ": " value "}),
        ("\\ key\\  \\ value ", {" key ": " value "}),
        ("\\ key\\ \t\\ value ", {" key ": " value "}),
        ("goat = \\uD83D\\uDC10", {"goat": "\U0001F410"}),
        ("taog = \\uDC10\\uD83D", {"taog": "\uDC10\uD83D"}),
        ("goat = \uD83D\uDC10", {"goat": "\U0001F410"}),
        ("goat = \uD83D\\uDC10", {"goat": "\U0001F410"}),
        ("goat = \\uD83D\uDC10", {"goat": "\U0001F410"}),
        ("taog = \uDC10\uD83D", {"taog": "\uDC10\uD83D"}),
        ("goat = \\uD83D\\\n    \\uDC10", {"goat": "\U0001F410"}),
        ("\\\n# comment", {"#": "comment"}),
        ("   \\\n# comment", {"#": "comment"}),
        ("key = value\\\n    # comment", {"key": "value# comment"}),
        ("key = value\\\n", {"key": "value"}),
        ("key = value\\", {"key": "value"}),
        ("key = value\\\n    ", {"key": "value"}),
        ("# comment\\\nkey = value", {"key": "value"}),
        ("\\\n", {}),
        ("\\\nkey = value", {"key": "value"}),
        (" \\\nkey = value", {"key": "value"}),
        ("key = value\nfoo = bar", {"key": "value", "foo": "bar"}),
        ("key = value\r\nfoo = bar", {"key": "value", "foo": "bar"}),
        ("key = value\rfoo = bar", {"key": "value", "foo": "bar"}),
        ("key = value1\nkey = value2", {"key": "value2"}),
        ("snowman = \\u2603", {"snowman": "\u2603"}),
        ("pokmon = \\u00E9", {"pokmon": "\u00E9"}),
        ("newline = \\u000a", {"newline": "\n"}),
        ("key = value\\\n\\\nend", {"key": "valueend"}),
        ("key = value\\\n    \\\nend", {"key": "valueend"}),
        ("key = value\\\\\nend", {"key": "value\\", "end": ""}),
        ("c#sharp = sucks", {"c#sharp": "sucks"}),
        ("fifth = #5", {"fifth": "#5"}),
        ("edh = \xF0", {"edh": "\xF0"}),
        ("snowman = \u2603", {"snowman": "\u2603"}),
        ("goat = \U0001F410", {"goat": "\U0001F410"}),
        ("newline = \\n", {"newline": "\n"}),
        ("tab = \\t", {"tab": "\t"}),
        ("form.feed = \\f", {"form.feed": "\f"}),
        ("two\\ words = one key", {"two words": "one key"}),
        ("hour\\:minute = 1440", {"hour:minute": "1440"}),
        ("E\\=mc^2 = Einstein", {"E=mc^2": "Einstein"}),
        ("two\\\\ words = not a key", {"two\\": "words = not a key"}),
        ("two\\\\\\ words = one key", {"two\\ words": "one key"}),
        ("invalid-escape = \\0", {"invalid-escape": "0"}),
        ("invalid-escape = \\q", {"invalid-escape": "q"}),
        ("invalid-escape = \\?", {"invalid-escape": "?"}),
        ("invalid-escape = \\x40", {"invalid-escape": "x40"}),
        (" \\ key = value", {" key": "value"}),
        (" \\u0020key = value", {" key": "value"}),
        (" \\  key = value", {" ": "key = value"}),
        ("key = \\  value", {"key": "  value"}),
        ("\nkey = value", {"key": "value"}),
        (" \nkey = value", {"key": "value"}),
        ("key = value\n", {"key": "value"}),
        ("key = value\n ", {"key": "value"}),
        ("key = value\n\nfoo = bar", {"key": "value", "foo": "bar"}),
        ("key = value\n \nfoo = bar", {"key": "value", "foo": "bar"}),
        (b"key=value\nedh=\xF0", {"key": "value", "edh": "\xF0"}),
        (
            b"key=value\n"
            b"edh=\xC3\xB0\n"
            b"snowman=\xE2\x98\x83\n"
            b"goat=\xF0\x9F\x90\x90",
            {
                "key": "value",
                "edh": "\xC3\xB0",
                "snowman": "\xE2\x98\x83",
                "goat": "\xF0\x9F\x90\x90",
            },
        ),
        ("key\tvalue=pair", {"key": "value=pair"}),
        ("key\\\tvalue=pair", {"key\tvalue": "pair"}),
        ("key\fvalue=pair", {"key": "value=pair"}),
        ("key\\\fvalue=pair", {"key\fvalue": "pair"}),
        ("key\0value", {"key\0value": ""}),
        ("key\\\0value", {"key\0value": ""}),
        ("the = \\u00f0e", {"the": "\xF0e"}),
        ("\\u00f0e = the", {"\xF0e": "the"}),
        ("goat = \\U0001F410", {"goat": "U0001F410"}),
        ("key\\u003Dvalue", {"key=value": ""}),
        ("key\\u003Avalue", {"key:value": ""}),
        ("key\\u0020value", {"key value": ""}),
        ("key=\\\\u2603", {"key": "\\u2603"}),
        ("key=\\\\u260x", {"key": "\\u260x"}),
    ],
)
def test_loads(s, d):
    assert loads(s) == d


def test_loads_multiple_ordereddict():
    assert loads(
        "key = value\nfoo = bar", object_pairs_hook=OrderedDict
    ) == OrderedDict([("key", "value"), ("foo", "bar")])


def test_loads_multiple_ordereddict_rev():
    assert loads(
        "foo = bar\nkey = value", object_pairs_hook=OrderedDict
    ) == OrderedDict([("foo", "bar"), ("key", "value")])


@pytest.mark.parametrize(
    "s,esc",
    [
        ("\\u = bad", "\\u"),
        ("\\u abcx = bad", "\\u"),
        ("\\u", "\\u"),
        ("\\uab bad", "\\uab"),
        ("\\uab:bad", "\\uab"),
        ("\\uab=bad", "\\uab"),
        ("\\uabc = bad", "\\uabc"),
        ("\\uabcx = bad", "\\uabcx"),
        ("\\ux = bad", "\\ux"),
        ("\\uxabc = bad", "\\uxabc"),
        ("bad = \\u ", "\\u "),
        ("bad = \\u abcx", "\\u abc"),
        ("bad = \\u", "\\u"),
        ("bad = \\uab\\cd", "\\uab\\c"),
        ("bad = \\uab\\u0063d", "\\uab\\u"),
        ("bad = \\uabc ", "\\uabc "),
        ("bad = \\uabc", "\\uabc"),
        ("bad = \\uabcx", "\\uabcx"),
        ("bad = \\ux", "\\ux"),
        ("bad = \\uxabc", "\\uxabc"),
    ],
)
def test_loads_invalid_u_escape(s, esc):
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads(s)
    assert excinfo.value.escape == esc
    assert str(excinfo.value) == "Invalid \\u escape sequence: " + esc
