from   __future__     import unicode_literals
from   six            import unichr
from   javaproperties import to_comment

def test_to_comment_single_line():
    assert to_comment('This is a comment.') == '#This is a comment.'

def test_to_comment_commented():
    assert to_comment('#This is a double comment.') == \
        '##This is a double comment.'

def test_to_comment_trailing_linefeed():
    assert to_comment('This comment has a trailing newline.\n') == \
        '#This comment has a trailing newline.\n#'

def test_to_comment_trailing_crlf():
    assert to_comment('This comment has a trailing CRLF.\r\n') == \
        '#This comment has a trailing CRLF.\n#'

def test_to_comment_trailing_cr():
    assert to_comment('This comment has a trailing carriage return.\r') == \
        '#This comment has a trailing carriage return.\n#'

def test_to_comment_multiline():
    assert to_comment('This is a comment.\nThis is also a comment.') == \
        '#This is a comment.\n#This is also a comment.'

def test_to_comment_inner_hash():
    assert to_comment('This is a comment.\n#This is also a comment.') == \
        '#This is a comment.\n#This is also a comment.'

def test_to_comment_inner_bang():
    assert to_comment('This is a comment.\n!This is also a comment.') == \
        '#This is a comment.\n!This is also a comment.'

def test_to_comment_latin_1():
    assert to_comment('edh=\xF0') == '#edh=\xF0'

def test_to_comment_xFF():
    assert to_comment('\xFF is the highest Latin-1 character.') == \
        '#\xFF is the highest Latin-1 character.'

def test_to_comment_x100():
    assert to_comment('\u0100 is the lowest non-Latin-1 character.') == \
        '#\\u0100 is the lowest non-Latin-1 character.'

def test_to_comment_non_latin_1():
    assert to_comment('snowman=\u2603') == '#snowman=\\u2603'

def test_to_comment_astral_plane():
    assert to_comment('goat=\U0001F410') == '#goat=\\ud83d\\udc10'

def test_to_comment_controls():
    # All C0 and C1 control characters other than \n and \r
    s = ''.join(unichr(i) for i in list(range(0x20)) + list(range(0x7F, 0xA0))
                          if i not in (10, 13))
    assert to_comment(s) == '#' + s
