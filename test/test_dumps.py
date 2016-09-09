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

def test_dumps_delete():
    assert dumps({"delete": "\x7F"}, timestamp=False) == 'delete=\\u007f\n'

def test_dumps_latin_1():
    assert dumps({"edh": "\xF0"}, timestamp=False) == 'edh=\\u00f0\n'

def test_dumps_non_latin_1():
    assert dumps({"snowman": "\u2603"}, timestamp=False) == 'snowman=\\u2603\n'

def test_dumps_astral_plane():
    assert dumps({"goat": "\U0001F410"}, timestamp=False) == \
        'goat=\\ud83d\\udc10\n'

def test_dumps_newline():
    assert dumps({"newline": "\n"}, timestamp=False) == 'newline=\\n\n'

def test_dumps_backslash():
    assert dumps({"backslash": "\\"}, timestamp=False) == 'backslash=\\\\\n'

def test_dumps_comment():
    assert dumps({"key": "value"}, comments='This is a comment.', timestamp=False) == '#This is a comment.\nkey=value\n'

def test_dumps_hash_comment():
    assert dumps({"key": "value"}, comments='#This is a double comment.', timestamp=False) == '##This is a double comment.\nkey=value\n'

def test_dumps_comment_linefeed():
    assert dumps({"key": "value"}, comments='This comment has a trailing newline.\n', timestamp=False) == '#This comment has a trailing newline.\n#\nkey=value\n'

def test_dumps_multiline_comment():
    assert dumps({"key": "value"}, comments='This is a comment.\nThis is also a comment.', timestamp=False) == '#This is a comment.\n#This is also a comment.\nkey=value\n'

def test_dumps_commented_comment():
    assert dumps({"key": "value"}, comments='This is a comment.\n#This is also a comment.', timestamp=False) == '#This is a comment.\n#This is also a comment.\nkey=value\n'

def test_dumps_latin_1_comment():
    assert dumps({"key": "value"}, comments='edh=\xF0', timestamp=False) == '#edh=\xF0\nkey=value\n'

def test_dumps_non_latin_1_comment():
    assert dumps({"key": "value"}, comments='snowman=\u2603', timestamp=False) == '#snowman=\\u2603\nkey=value\n'

def test_dumps_astral_plane_comment():
    assert dumps({"key": "value"}, comments='goat=\U0001F410', timestamp=False) == '#goat=\\ud83d\\udc10\nkey=value\n'

def test_dumps_tab_separator():
    assert dumps({"key": "value"}, separator='\t', timestamp=False) == 'key\tvalue\n'


# =, :, #, and !
# \n, \r, etc.
# timestamps with & without a timezone
# comment and timestamp
# custom separator
# OrderedDict
# sorting keys
