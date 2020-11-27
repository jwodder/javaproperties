import pytest
from   javaproperties import Comment, KeyValue, Whitespace, parse

@pytest.mark.parametrize('s,objects', [
    ('', []),
    ('\n', [Whitespace('\n')]),
    (' \n\t\n', [Whitespace(' \n'), Whitespace('\t\n')]),
    ('key=value\n', [KeyValue('key', 'value', 'key=value\n')]),
    ('\xF0=\u2603\n', [KeyValue('\xF0', '\u2603', '\xF0=\u2603\n')]),
    ('\\u00F0=\\u2603\n', [KeyValue('\xF0', '\u2603', '\\u00F0=\\u2603\n')]),
    (' key :\t value \n', [KeyValue('key', 'value ', ' key :\t value \n')]),
    (
        '#This is a comment.\n'
        '# So is this.\n'
        'comment: no\n'
        ' ! Also a comment\n',
        [
            Comment('#This is a comment.\n'),
            Comment('# So is this.\n'),
            KeyValue('comment', 'no', 'comment: no\n'),
            Comment(' ! Also a comment\n'),
        ],
    ),
    (
        '#Before blank\n'
        '\n'
        '#After blank\n'
        '\n'
        'before=blank\n'
        '\n'
        'after=blank\n',
        [
            Comment('#Before blank\n'),
            Whitespace('\n',),
            Comment('#After blank\n'),
            Whitespace('\n'),
            KeyValue('before', 'blank', 'before=blank\n'),
            Whitespace('\n'),
            KeyValue('after', 'blank', 'after=blank\n'),
        ],
    ),
    ('key va\\\n lue\n', [KeyValue('key', 'value', 'key va\\\n lue\n')]),
    ('key va\\\n', [KeyValue('key', 'va', 'key va\\\n')]),
    ('key va\\', [KeyValue('key', 'va', 'key va\\')]),
    (' \\\n\t\\\r\n\f\\\r \n', [Whitespace(' \\\n\t\\\r\n\f\\\r \n')]),
    (
        'key = v\\\n\ta\\\r\n\fl\\\r u\\\ne\n',
        [KeyValue('key', 'value', 'key = v\\\n\ta\\\r\n\fl\\\r u\\\ne\n')],
    ),
])
def test_parse(s, objects):
    assert list(parse(s)) == objects

def test_keyvalue_attributes():
    kv = KeyValue('a', 'b', 'c')
    assert kv.key == 'a'
    assert kv.value == 'b'
    assert kv.source == 'c'

def test_comment_attributes():
    c = Comment('a')
    assert c.source == 'a'

def test_whitespace_attributes():
    ws = Whitespace('a')
    assert ws.source == 'a'

@pytest.mark.parametrize('c,is_t', [
    ('#\n', False),
    ('#Mon Sep 26 14:57:44 EDT 2016', True),
    ('#Mon Sep 26 14:57:44 EDT 2016\n', True),
    (' # Mon Sep 26 14:57:44 EDT 2016\n', True),
    ('#Wed Dec 31 19:00:00 EST 1969\n', True),
    ('#Fri Jan 01 00:00:00 EST 2016\n', True),
    ('#Tue Feb 02 02:02:02 EST 2016\n', True),
    ('#Thu Mar 03 03:03:03 EST 2016\n', True),
    ('#Mon Apr 04 04:04:04 EDT 2016\n', True),
    ('#Thu May 05 05:05:05 EDT 2016\n', True),
    ('#Mon Jun 06 06:06:06 EDT 2016\n', True),
    ('#Thu Jul 07 07:07:07 EDT 2016\n', True),
    ('#Mon Aug 08 08:08:08 EDT 2016\n', True),
    ('#Fri Sep 09 09:09:09 EDT 2016\n', True),
    ('#Mon Oct 10 10:10:10 EDT 2016\n', True),
    ('#Fri Nov 11 11:11:11 EST 2016\n', True),
    ('#Mon Dec 12 12:12:12 EST 2016\n', True),
    ('#Sun Jan 03 06:00:00 EST 2016\n', True),
    ('#Mon Jan 04 00:00:00 EST 2016\n', True),
    ('#Tue Jan 05 01:00:00 EST 2016\n', True),
    ('#Wed Jan 06 02:00:00 EST 2016\n', True),
    ('#Thu Jan 07 03:00:00 EST 2016\n', True),
    ('#Fri Jan 08 04:00:00 EST 2016\n', True),
    ('#Sat Jan 09 05:00:00 EST 2016\n', True),
    ('#Mon Feb 29 03:14:15 EST 2016\n', True),
    ('#Fri May 13 13:13:13 EDT 2016\n', True),
    ('#Mon Sep 26 14:57:44  2016\n', True),
    ('#Sat Jan 09 05:00:60 EST 2016\n', True),
    ('#Sat Jan 09 05:00:61 EST 2016\n', True),
    ('#Mon Feb 32 03:14:15 EST 2016\n', False),
    ('#Sun Jan  3 06:00:00 EST 2016\n', False),
    ('#Sun Jan 03  6:00:00 EST 2016\n', False),
    ('#Sat Jan 09 05:00:62 EST 2016\n', False),
    ('#Sat Jan 09 24:00:00 EST 2016\n', False),
    ('#Sat Jan 09 05:60:00 EST 2016\n', False),
    ('#Mo  Mär 02 13:59:03 EST 2020\n', False),
])
def test_comment_is_timestamp(c, is_t):
    assert Comment(c).is_timestamp() == is_t

@pytest.mark.parametrize('s,ss', [
    ('key=value', 'key=value'),
    ('key=value\n', 'key=value'),
    ('key=value\r\n', 'key=value'),
    ('key=value\r', 'key=value'),
    ('key va\\\n', 'key va'),
    ('key va\\\\\n', 'key va\\\\'),
    ('key va\\\\\\\n', 'key va\\\\'),
    ('key va\\', 'key va'),
    ('key va\\\n \\', 'key va\\\n '),
    ('key va\\\n \\\n', 'key va\\\n '),
    ('key va\\\n\\', 'key va\\\n'),
    ('key va\\\n\\\n', 'key va\\\n'),
])
def test_keyvalue_source_stripped(s, ss):
    assert KeyValue(None, None, s).source_stripped == ss

@pytest.mark.parametrize('s,ss', [
    ('#comment', '#comment'),
    ('#comment\n', '#comment'),
    ('#comment\r\n', '#comment'),
    ('#comment\r', '#comment'),
    ('#comment\\\n', '#comment\\'),
])
def test_comment_source_stripped(s, ss):
    assert Comment(s).source_stripped == ss

@pytest.mark.parametrize('s,ss', [
    (' ', ' '),
    ('\n', ''),
    ('\r\n', ''),
    ('\r', ''),
    ('\\', ''),
    ('\\\n', ''),
    ('\\\\\n', '\\\\'),
    ('\\\\\\\n', '\\\\'),
    ('\\\n \\', '\\\n '),
    ('\\\n \\\n', '\\\n '),
    ('\\\n\\', '\\\n'),
    ('\\\n\\\n', '\\\n'),
])
def test_whitespace_source_stripped(s, ss):
    assert Whitespace(s).source_stripped == ss

@pytest.mark.parametrize('s,v', [
    ('#comment', 'comment'),
    ('#comment\n', 'comment'),
    ('!comment\n', 'comment'),
    (' #comment\n', 'comment'),
    ('# comment\n', ' comment'),
    (' # comment\n', ' comment'),
    ('\t#comment\n', 'comment'),
    ('#\tcomment\n', '\tcomment'),
    ('\t#\tcomment\n', '\tcomment'),
    ('#comment value \n', 'comment value '),
    ('  weird edge # case', 'weird edge # case'),
])
def test_comment_value(s,v):
    assert Comment(s).value == v
