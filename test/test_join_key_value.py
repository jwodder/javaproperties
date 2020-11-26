import pytest
from   javaproperties import join_key_value

@pytest.mark.parametrize('key,value,s', [
    ('', '', '='),
    ('key', 'value', 'key=value'),
    ('two words', 'value', 'two\\ words=value'),
    ('key', 'two words', 'key=two words'),
    (' key', 'value', '\\ key=value'),
    ('key', ' value', 'key=\\ value'),
    ('key ', 'value', 'key\\ =value'),
    ('key', 'value ', 'key=value '),
    ('   ', 'value', '\\ \\ \\ =value'),
    ('key', '   ', 'key=\\   '),
    ('US', '\x1F', 'US=\\u001f'),
    ('tilde', '~', 'tilde=~'),
    ('delete', '\x7F', 'delete=\\u007f'),
    ('padding', '\x80', 'padding=\\u0080'),
    ('nbsp', '\xA0', 'nbsp=\\u00a0'),
    ('edh', '\xF0', 'edh=\\u00f0'),
    ('snowman', '\u2603', 'snowman=\\u2603'),
    ('goat', '\U0001F410', 'goat=\\ud83d\\udc10'),
    ('taog', '\uDC10\uD83D', 'taog=\\udc10\\ud83d'),
    ('newline', '\n', 'newline=\\n'),
    ('carriage-return', '\r', 'carriage-return=\\r'),
    ('tab', '\t', 'tab=\\t'),
    ('form-feed', '\f', 'form-feed=\\f'),
    ('bell', '\a', 'bell=\\u0007'),
    ('escape', '\x1B', 'escape=\\u001b'),
    ('vertical-tab', '\v', 'vertical-tab=\\u000b'),
    ('backslash', '\\', 'backslash=\\\\'),
    ('equals', '=', 'equals=\\='),
    ('colon', ':', 'colon=\\:'),
    ('hash', '#', 'hash=\\#'),
    ('exclamation', '!', 'exclamation=\\!'),
    ('null', '\0', 'null=\\u0000'),
    ('backspace', '\b', 'backspace=\\u0008'),
])
def test_join_key_value(key, value, s):
    assert join_key_value(key, value) == s

@pytest.mark.parametrize('key,value,sep,s', [
    ('key', 'value', ' = ', 'key = value'),
    ('key', 'value', ':', 'key:value'),
    ('key', 'value', ' ', 'key value'),
    ('key', 'value', '\t', 'key\tvalue'),
    (' key ', ' value ', ' : ', '\\ key\\  : \\ value '),
])
def test_join_key_value_separator(key, value, sep, s):
    assert join_key_value(key, value, separator=sep) == s

@pytest.mark.parametrize('key,value,s', [
    ('', '', '='),
    ('key', 'value', 'key=value'),
    ('two words', 'value', 'two\\ words=value'),
    ('key', 'two words', 'key=two words'),
    (' key', 'value', '\\ key=value'),
    ('key', ' value', 'key=\\ value'),
    ('key ', 'value', 'key\\ =value'),
    ('key', 'value ', 'key=value '),
    ('   ', 'value', '\\ \\ \\ =value'),
    ('key', '   ', 'key=\\   '),
    ('US', '\x1F', 'US=\\u001f'),
    ('tilde', '~', 'tilde=~'),
    ('delete', '\x7F', 'delete=\\u007f'),
    ('padding', '\x80', 'padding=\x80'),
    ('nbsp', '\xA0', 'nbsp=\xA0'),
    ('edh', '\xF0', 'edh=\xF0'),
    ('snowman', '\u2603', 'snowman=\u2603'),
    ('goat', '\U0001F410', 'goat=\U0001F410'),
    ('taog', '\uDC10\uD83D', 'taog=\udc10\ud83d'),
    ('newline', '\n', 'newline=\\n'),
    ('carriage-return', '\r', 'carriage-return=\\r'),
    ('tab', '\t', 'tab=\\t'),
    ('form-feed', '\f', 'form-feed=\\f'),
    ('bell', '\a', 'bell=\\u0007'),
    ('escape', '\x1B', 'escape=\\u001b'),
    ('vertical-tab', '\v', 'vertical-tab=\\u000b'),
    ('backslash', '\\', 'backslash=\\\\'),
    ('equals', '=', 'equals=\\='),
    ('colon', ':', 'colon=\\:'),
    ('hash', '#', 'hash=\\#'),
    ('exclamation', '!', 'exclamation=\\!'),
    ('null', '\0', 'null=\\u0000'),
    ('backspace', '\b', 'backspace=\\u0008'),
])
def test_join_key_value_no_ensure_ascii(key, value, s):
    assert join_key_value(key, value, ensure_ascii=False) == s
