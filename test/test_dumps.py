from   __future__     import unicode_literals
from   collections    import OrderedDict
from   datetime       import datetime
from   dateutil.tz    import tzoffset
import pytest
from   javaproperties import dumps

@pytest.mark.parametrize('d,s', [
    ({}, ''),
    ({"key": "value"}, 'key=value\n'),
    ([("key", "value"), ("zebra", "apple")], 'key=value\nzebra=apple\n'),
    ([("zebra", "apple"), ("key", "value")], 'zebra=apple\nkey=value\n'),
    (
        OrderedDict([("key", "value"), ("zebra", "apple")]),
        'key=value\nzebra=apple\n',
    ),
    (
        OrderedDict([("zebra", "apple"), ("key", "value")]),
        'zebra=apple\nkey=value\n',
    ),
    ({"two words": "value"}, 'two\\ words=value\n'),
    ({"key": "two words"}, 'key=two words\n'),
    ({" key": "value"}, '\\ key=value\n'),
    ({"key": " value"}, 'key=\\ value\n'),
    ({"key ": "value"}, 'key\\ =value\n'),
    ({"key": "value "}, 'key=value \n'),
    ({"   ": "value"}, '\\ \\ \\ =value\n'),
    ({"key": "   "}, 'key=\\   \n'),
    ({"US": "\x1F"}, 'US=\\u001f\n'),
    ({"tilde": "~"}, 'tilde=~\n'),
    ({"delete": "\x7F"}, 'delete=\\u007f\n'),
    ({"edh": "\xF0"}, 'edh=\\u00f0\n'),
    ({"snowman": "\u2603"}, 'snowman=\\u2603\n'),
    ({"goat": "\U0001F410"}, 'goat=\\ud83d\\udc10\n'),
    ({"taog": "\uDC10\uD83D"}, 'taog=\\udc10\\ud83d\n'),
    ({"newline": "\n"}, 'newline=\\n\n'),
    ({"carriage-return": "\r"}, 'carriage-return=\\r\n'),
    ({"tab": "\t"}, 'tab=\\t\n'),
    ({"form-feed": "\f"}, 'form-feed=\\f\n'),
    ({"bell": "\a"}, 'bell=\\u0007\n'),
    ({"escape": "\x1B"}, 'escape=\\u001b\n'),
    ({"vertical-tab": "\v"}, 'vertical-tab=\\u000b\n'),
    ({"backslash": "\\"}, 'backslash=\\\\\n'),
    ({"equals": "="}, 'equals=\\=\n'),
    ({"colon": ":"}, 'colon=\\:\n'),
    ({"hash": "#"}, 'hash=\\#\n'),
    ({"exclamation": "!"}, 'exclamation=\\!\n'),
    ({"null": "\0"}, 'null=\\u0000\n'),
    ({"backspace": "\b"}, 'backspace=\\u0008\n'),
])
def test_dumps(d,s):
    assert dumps(d, timestamp=False) == s

@pytest.mark.parametrize('d,s', [
    ({"key": "value", "zebra": "apple"}, 'key=value\nzebra=apple\n'),
    ([("key", "value"), ("zebra", "apple")], 'key=value\nzebra=apple\n'),
    ([("zebra", "apple"), ("key", "value")], 'key=value\nzebra=apple\n'),
    (
        OrderedDict([("key", "value"), ("zebra", "apple")]),
        'key=value\nzebra=apple\n',
    ),
    (
        OrderedDict([("zebra", "apple"), ("key", "value")]),
        'key=value\nzebra=apple\n',
    ),
])
def test_dumps_sorted(d,s):
    assert dumps(d, timestamp=False, sort_keys=True) == s

@pytest.mark.parametrize('ts,s', [
    (None, 'key=value\n'),
    (1473703254, '#Mon Sep 12 14:00:54 EDT 2016\nkey=value\n'),
    (
        datetime.fromtimestamp(1473703254),
        '#Mon Sep 12 14:00:54 EDT 2016\nkey=value\n',
    ),
    (
        datetime.fromtimestamp(1473703254, tzoffset('PDT', -25200)),
        '#Mon Sep 12 11:00:54 PDT 2016\nkey=value\n',
    ),
])
def test_dump_timestamp(ts, s):
    assert dumps({"key": "value"}, timestamp=ts) == s

@pytest.mark.parametrize('d,s', [
    ({"US": "\x1F"}, 'US=\\u001f\n'),
    ({"delete": "\x7F"}, 'delete=\\u007f\n'),
    ({"padding": "\x80"}, 'padding=\x80\n'),
    ({"nbsp": "\xA0"}, 'nbsp=\xA0\n'),
    ({"edh": "\xF0"}, 'edh=\xF0\n'),
    ({"snowman": "\u2603"}, 'snowman=\u2603\n'),
    ({"goat": "\U0001F410"}, 'goat=\U0001F410\n'),
    ({"taog": "\uDC10\uD83D"}, 'taog=\uDC10\uD83D\n'),
    ({"newline": "\n"}, 'newline=\\n\n'),
    ({"carriage-return": "\r"}, 'carriage-return=\\r\n'),
    ({"tab": "\t"}, 'tab=\\t\n'),
    ({"form-feed": "\f"}, 'form-feed=\\f\n'),
    ({"bell": "\a"}, 'bell=\\u0007\n'),
    ({"escape": "\x1B"}, 'escape=\\u001b\n'),
    ({"vertical-tab": "\v"}, 'vertical-tab=\\u000b\n'),
    ({"backslash": "\\"}, 'backslash=\\\\\n'),
    ({"equals": "="}, 'equals=\\=\n'),
    ({"colon": ":"}, 'colon=\\:\n'),
    ({"hash": "#"}, 'hash=\\#\n'),
    ({"exclamation": "!"}, 'exclamation=\\!\n'),
    ({"null": "\0"}, 'null=\\u0000\n'),
    ({"backspace": "\b"}, 'backspace=\\u0008\n'),
])
def test_dumps_no_ensure_ascii(d,s):
    assert dumps(d, timestamp=False, ensure_ascii=False) == s

def test_dumps_comment():
    assert dumps(
        {"key": "value"},
        comments='This is a comment.',
        timestamp=False,
    ) == '#This is a comment.\nkey=value\n'

def test_dumps_tab_separator():
    assert dumps({"key": "value"}, separator='\t', timestamp=False) \
        == 'key\tvalue\n'

def test_dumps_timestamp_and_comment():
    assert dumps(
        {"key": "value"},
        comments='This is a comment.',
        timestamp=1473703254,
    ) == '#This is a comment.\n#Mon Sep 12 14:00:54 EDT 2016\nkey=value\n'
