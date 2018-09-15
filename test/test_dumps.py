from   __future__     import unicode_literals
from   collections    import OrderedDict
from   datetime       import datetime
from   dateutil.tz    import tzoffset
from   javaproperties import dumps

def test_dumps_nothing():
    assert dumps({}, timestamp=False) == ''

def test_dumps_simple():
    assert dumps({"key": "value"}, timestamp=False) == 'key=value\n'

def test_dumps_two_simple():
    assert dumps([("key", "value"), ("zebra", "apple")], timestamp=False) == \
        'key=value\nzebra=apple\n'

def test_dumps_two_simple_rev():
    assert dumps([("zebra", "apple"), ("key", "value")], timestamp=False) == \
        'zebra=apple\nkey=value\n'

def test_dumps_two_simple_sorted():
    assert dumps(
        [("key", "value"), ("zebra", "apple")],
        timestamp=False,
        sort_keys=True,
    ) == 'key=value\nzebra=apple\n'

def test_dumps_two_simple_rev_sorted():
    assert dumps(
        [("zebra", "apple"), ("key", "value")],
        timestamp=False,
        sort_keys=True,
    ) == 'key=value\nzebra=apple\n'

def test_dumps_ordereddict():
    assert dumps(
        OrderedDict([("key", "value"), ("zebra", "apple")]),
        timestamp=False,
    ) == 'key=value\nzebra=apple\n'

def test_dumps_ordereddict_rev():
    assert dumps(
        OrderedDict([("zebra", "apple"), ("key", "value")]),
        timestamp=False,
    ) == 'zebra=apple\nkey=value\n'

def test_dumps_ordereddict_sorted():
    assert dumps(
        OrderedDict([("key", "value"), ("zebra", "apple")]),
        timestamp=False,
        sort_keys=True,
    ) == 'key=value\nzebra=apple\n'

def test_dumps_ordereddict_rev_sorted():
    assert dumps(
        OrderedDict([("zebra", "apple"), ("key", "value")]),
        timestamp=False,
        sort_keys=True,
    ) == 'key=value\nzebra=apple\n'

def test_dumps_space_in_key():
    assert dumps({"two words": "value"}, timestamp=False) == \
        'two\\ words=value\n'

def test_dumps_space_in_value():
    assert dumps({"key": "two words"}, timestamp=False) == 'key=two words\n'

def test_dumps_leading_space_in_value():
    assert dumps({"key": " value"}, timestamp=False) == 'key=\\ value\n'

def test_dumps_trailing_space_in_value():
    assert dumps({"key": "value "}, timestamp=False) == 'key=value \n'

def test_dumps_three_space_value():
    assert dumps({"key": "   "}, timestamp=False) == 'key=\\ \\ \\ \n'

def test_dumps_x1F():
    assert dumps({"US": "\x1F"}, timestamp=False) == 'US=\\u001f\n'

def test_dumps_tilde():
    assert dumps({"tilde": "~"}, timestamp=False) == 'tilde=~\n'

def test_dumps_delete():
    assert dumps({"delete": "\x7F"}, timestamp=False) == 'delete=\\u007f\n'

def test_dumps_latin_1():
    assert dumps({"edh": "\xF0"}, timestamp=False) == 'edh=\\u00f0\n'

def test_dumps_non_latin_1():
    assert dumps({"snowman": "\u2603"}, timestamp=False) == 'snowman=\\u2603\n'

def test_dumps_astral_plane():
    assert dumps({"goat": "\U0001F410"}, timestamp=False) == \
        'goat=\\ud83d\\udc10\n'

def test_dumps_bad_surrogate():
    assert dumps({"taog": "\uDC10\uD83D"}, timestamp=False) == \
        'taog=\\udc10\\ud83d\n'

def test_dumps_newline():
    assert dumps({"newline": "\n"}, timestamp=False) == 'newline=\\n\n'

def test_dumps_carriage_return():
    assert dumps({"carriage-return": "\r"}, timestamp=False) == \
        'carriage-return=\\r\n'

def test_dumps_tab():
    assert dumps({"tab": "\t"}, timestamp=False) == 'tab=\\t\n'

def test_dumps_form_feed():
    assert dumps({"form-feed": "\f"}, timestamp=False) == 'form-feed=\\f\n'

def test_dumps_bell():
    assert dumps({"bell": "\a"}, timestamp=False) == 'bell=\\u0007\n'

def test_dumps_escape():
    assert dumps({"escape": "\x1B"}, timestamp=False) == 'escape=\\u001b\n'

def test_dumps_vertical_tab():
    assert dumps({"vertical-tab": "\v"}, timestamp=False) == \
        'vertical-tab=\\u000b\n'

def test_dumps_backslash():
    assert dumps({"backslash": "\\"}, timestamp=False) == 'backslash=\\\\\n'

def test_dumps_comment():
    assert dumps({"key": "value"}, comments='This is a comment.', timestamp=False) == '#This is a comment.\nkey=value\n'

def test_dumps_tab_separator():
    assert dumps({"key": "value"}, separator='\t', timestamp=False) == 'key\tvalue\n'

def test_dumps_none_timestamp():
    assert dumps({"key": "value"}, timestamp=None) == 'key=value\n'

def test_dumps_epoch_timestamp():
    assert dumps({"key": "value"}, timestamp=1473703254) == \
        '#Mon Sep 12 14:00:54 EDT 2016\nkey=value\n'

def test_dumps_naive_datetime():
    assert dumps(
        {"key": "value"},
        timestamp=datetime.fromtimestamp(1473703254)
    ) == '#Mon Sep 12 14:00:54 EDT 2016\nkey=value\n'

def test_dumps_aware_datetime():
    assert dumps(
        {"key": "value"},
        timestamp=datetime.fromtimestamp(1473703254, tzoffset('PDT', -25200))
    ) == '#Mon Sep 12 11:00:54 PDT 2016\nkey=value\n'

def test_dumps_timestamp_and_comment():
    assert dumps(
        {"key": "value"},
        comments='This is a comment.',
        timestamp=1473703254
    ) == '#This is a comment.\n#Mon Sep 12 14:00:54 EDT 2016\nkey=value\n'

def test_dumps_equals():
    assert dumps({"equals": "="}, timestamp=False) == 'equals=\\=\n'

def test_dumps_colon():
    assert dumps({"colon": ":"}, timestamp=False) == 'colon=\\:\n'

def test_dumps_hash():
    assert dumps({"hash": "#"}, timestamp=False) == 'hash=\\#\n'

def test_dumps_exclamation():
    assert dumps({"exclamation": "!"}, timestamp=False) == 'exclamation=\\!\n'

def test_dumps_null():
    assert dumps({"null": "\0"}, timestamp=False) == 'null=\\u0000\n'

def test_dumps_backspace():
    assert dumps({"backspace": "\b"}, timestamp=False) == 'backspace=\\u0008\n'
