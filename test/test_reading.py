from javaproperties import loads

def test_loads_simple():
    assert loads('foo=bar') == {"foo": "bar"}

def test_loads_key_only():
    assert loads("foo") == {"foo": ""}

def test_loads_space_equals():
    assert loads("foo =bar") == {"foo": "bar"}

def test_loads_equals_space():
    assert loads("foo= bar") == {"foo": "bar"}

def test_loads_padded_equals():
    assert loads("foo = bar") == {"foo": "bar"}

def test_loads_nokey():
    assert loads("=bar") == {"": "bar"}

def test_loads_spacekey():
    assert loads(" =bar") == {"": "bar"}

def test_loads_trailing_space():
    assert loads("foo=bar ") == {"foo": "bar "}

def test_loads_leading_space():
    assert loads(" foo=bar") == {"foo": "bar"}

def test_loads_space_equals_space():
    assert loads(' = ') == {"": ""}

def test_loads_equals_only():
    assert loads('=') == {"": ""}

def test_loads_nothing():
    assert loads('') == {}

def test_loads_space():
    assert loads(' ') == {}

def test_loads_linefeed():
    assert loads('\n') == {}

def test_loads_crlf():
    assert loads('\r\n') == {}

def test_loads_cr():
    assert loads('\r') == {}


def test_loads_comment():
    assert loads('#This is a comment.') == {}

def test_loads_comment_key_value():
    assert loads('#This is a comment.\nkey = value') == {"key": "value"}

def test_loads_key_value_comment():
    assert loads('key = value\n#This is a comment.') == {"key": "value"}


def test_loads_bang_comment():
    assert loads('!This is a comment.') == {}

def test_loads_bang_comment_key_value():
    assert loads('!This is a comment.\nkey = value') == {"key": "value"}

def test_loads_key_value_bang_comment():
    assert loads('key = value\n!This is a comment.') == {"key": "value"}


def test_loads_continued_value():
    assert loads('key = val\\\nue') == {"key": "value"}

def test_loads_continued_value_spaced():
    assert loads('key = val\\\n    ue') == {"key": "value"}

def test_loads_continued_key():
    assert loads('ke\\\ny = value') == {"key": "value"}

def test_loads_continued_key_spaced():
    assert loads('ke\\\n    y = value') == {"key": "value"}

def test_loads_three_words():
    assert loads('one two three') == {"one": "two three"}

def test_loads_simple_linefeed():
    assert loads('foo=bar\n') == {"foo": "bar"}

def test_loads_simple_crlf():
    assert loads('foo=bar\r\n') == {"foo": "bar"}

def test_loads_simple_cr():
    assert loads('foo=bar\r') == {"foo": "bar"}

def test_loads_key_colon_value():
    assert loads('key:value') == {"key": "value"}

def test_loads_key_space_value():
    assert loads('key value') == {"key": "value"}

def test_loads_surrogate_pair():
    assert loads('goat = \\uD83D\\uDC10') == {"goat": u"\U0001F410"}

def test_loads_bad_surrogate():
    assert loads('taog = \\uDC10\\uD83D') == {"taog": u"\uDC10\uD83D"}

def test_loads_continue_comment():
    assert loads('foo = bar\\\n    # comment') == {"foo": "bar# comment"}


# multiline line continuations
# \uXXXX escape sequences
# \n, \r, etc. escape sequences
# comment character in middle of line
# escaped space/=/: in key
# escaped non-special character
# blank line after line continuation
# blank lines
# multiple key-value entries
# multiple key-value entries with the same key
# series of all-whitespace lines joined with line continuations
# EOF after line continuation
# CRLF
# multiple backslashes (even & odd numbers) in a row
# "continuation" in a comment
