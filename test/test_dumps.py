from __future__     import unicode_literals
from javaproperties import dumps

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

def test_dumps_astral_plane():
    assert dumps({"goat": "\U0001F410"}, timestamp=False) == \
        'goat=\\ud83d\\udc10\n'

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

def test_dumps_non_latin_1():
    assert dumps({"snowman": "\u2603"}, timestamp=False) == 'snowman=\\u2603\n'

def test_dumps_latin_1():
    assert dumps({"edh": "\xF0"}, timestamp=False) == 'edh=\\u00f0\n'

def test_dumps_delete():
    assert dumps({"delete": "\x7F"}, timestamp=False) == 'delete=\\u007f\n'

def test_dumps_newline():
    assert dumps({"newline": "\n"}, timestamp=False) == 'newline=\\n\n'

def test_dumps_backslash():
    assert dumps({"backslash": "\\"}, timestamp=False) == 'backslash=\\\\\n'


# characters outside the [\x20-\x7E] range
# =, :, #, and !
# \n, \r, etc.
# timestamps with & without a timezone
# comments
# non-Latin-1 characters in comments
# multiline comments
# `str`s in Python 2 (Separate test file?)
# custom separator?
# OrderedDict
# sorting keys
