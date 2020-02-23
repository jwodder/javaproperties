from   __future__     import unicode_literals
import pytest
from   six            import unichr
from   javaproperties import to_comment

# All C0 and C1 control characters other than \n and \r:
s = ''.join(unichr(i) for i in list(range(0x20)) + list(range(0x7F, 0xA0))
                      if i not in (10, 13))

@pytest.mark.parametrize('cin,cout', [
    ('This is a comment.', '#This is a comment.'),
    ('#This is a double comment.', '##This is a double comment.'),
    (
        'This comment has a trailing newline.\n',
        '#This comment has a trailing newline.\n#',
    ),
    (
        'This comment has a trailing CRLF.\r\n',
        '#This comment has a trailing CRLF.\n#',
    ),
    (
        'This comment has a trailing carriage return.\r',
        '#This comment has a trailing carriage return.\n#',
    ),
    (
        'This is a comment.\nThis is also a comment.',
        '#This is a comment.\n#This is also a comment.',
    ),
    (
        'This is a comment.\n#This is also a comment.',
        '#This is a comment.\n#This is also a comment.',
    ),
    (
        'This is a comment.\n!This is also a comment.',
        '#This is a comment.\n!This is also a comment.',
    ),
    ('edh=\xF0', '#edh=\xF0'),
    (
        '\xFF is the highest Latin-1 character.',
        '#\xFF is the highest Latin-1 character.',
    ),
    (
        '\u0100 is the lowest non-Latin-1 character.',
        '#\\u0100 is the lowest non-Latin-1 character.',
    ),
    ('snowman=\u2603', '#snowman=\\u2603'),
    ('goat=\U0001F410', '#goat=\\ud83d\\udc10'),
    (s, '#' + s),
])
def test_to_comment(cin, cout):
    assert to_comment(cin) == cout
