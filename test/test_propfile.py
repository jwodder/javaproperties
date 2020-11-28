from   collections    import OrderedDict
from   datetime       import datetime
from   dateutil.tz    import tzstr
import pytest
from   javaproperties import PropertiesFile, dumps

INPUT = '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
foo: first definition
bar=only definition

# Comment between values

key = value

zebra \\
    apple
foo : second definition

# Comment at end of file
'''

def test_propfile_empty():
    pf = PropertiesFile()
    pf._check()
    assert len(pf) == 0
    assert not bool(pf)
    assert dict(pf) == {}
    assert list(pf) == []
    assert list(reversed(pf)) == []
    assert pf.dumps() == ''

@pytest.mark.parametrize('src', [INPUT, INPUT.encode('iso-8859-1')])
def test_propfile_loads(src):
    pf = PropertiesFile.loads(src)
    pf._check()
    assert len(pf) == 4
    assert bool(pf)
    assert dict(pf) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }
    assert list(pf) == ["foo", "bar", "key", "zebra"]
    assert list(reversed(pf)) == ["zebra", "key", "bar", "foo"]

def test_propfile_dumps():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    assert pf.dumps() == INPUT

def test_propfile_getitem():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    assert pf["key"] == "value"
    assert pf["foo"] == "second definition"
    with pytest.raises(KeyError):
        pf["missing"]
    pf._check()

def test_propfile_setitem():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    pf["key"] = "lock"
    pf._check()
    assert dict(pf) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "lock",
        "zebra": "apple",
    }
    assert list(pf) == ["foo", "bar", "key", "zebra"]
    assert list(reversed(pf)) == ["zebra", "key", "bar", "foo"]
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
foo: first definition
bar=only definition

# Comment between values

key=lock

zebra \\
    apple
foo : second definition

# Comment at end of file
'''

def test_propfile_additem():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    pf["new"] = "old"
    pf._check()
    assert dict(pf) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
        "new": "old",
    }
    assert list(pf) == ["foo", "bar", "key", "zebra", "new"]
    assert list(reversed(pf)) == ["new", "zebra", "key", "bar", "foo"]
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
foo: first definition
bar=only definition

# Comment between values

key = value

zebra \\
    apple
foo : second definition

# Comment at end of file
new=old
'''

def test_propfile_delitem():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    del pf["key"]
    pf._check()
    assert dict(pf) == {
        "foo": "second definition",
        "bar": "only definition",
        "zebra": "apple",
    }
    assert list(pf) == ["foo", "bar", "zebra"]
    assert list(reversed(pf)) == ["zebra", "bar", "foo"]
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
foo: first definition
bar=only definition

# Comment between values


zebra \\
    apple
foo : second definition

# Comment at end of file
'''

def test_propfile_delitem_missing():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    with pytest.raises(KeyError):
        del pf["missing"]
    pf._check()
    assert len(pf) == 4
    assert bool(pf)
    assert dict(pf) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }
    assert list(pf) == ["foo", "bar", "key", "zebra"]
    assert list(reversed(pf)) == ["zebra", "key", "bar", "foo"]
    assert pf.dumps() == INPUT

def test_propfile_move_item():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    del pf["key"]
    pf._check()
    pf["key"] = "recreated"
    pf._check()
    assert dict(pf) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "recreated",
        "zebra": "apple",
    }
    assert list(pf) == ["foo", "bar", "zebra", "key"]
    assert list(reversed(pf)) == ["key", "zebra", "bar", "foo"]
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
foo: first definition
bar=only definition

# Comment between values


zebra \\
    apple
foo : second definition

# Comment at end of file
key=recreated
'''

def test_propfile_set_nochange():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    assert pf["key"] == "value"
    pf["key"] = "value"
    pf._check()
    assert dict(pf) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }
    assert list(pf) == ["foo", "bar", "key", "zebra"]
    assert list(reversed(pf)) == ["zebra", "key", "bar", "foo"]
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
foo: first definition
bar=only definition

# Comment between values

key=value

zebra \\
    apple
foo : second definition

# Comment at end of file
'''

def test_propfile_dumps_function():
    assert dumps(PropertiesFile.loads(INPUT), timestamp=False) == '''\
foo=second definition
bar=only definition
key=value
zebra=apple
'''

def test_propfile_set_repeated_key():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    pf["foo"] = "redefinition"
    pf._check()
    assert dict(pf) == {
        "foo": "redefinition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }
    assert list(pf) == ["foo", "bar", "key", "zebra"]
    assert list(reversed(pf)) == ["zebra", "key", "bar", "foo"]
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
foo=redefinition
bar=only definition

# Comment between values

key = value

zebra \\
    apple

# Comment at end of file
'''

def test_propfile_delete_repeated_key():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    del pf["foo"]
    pf._check()
    assert dict(pf) == {
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }
    assert list(pf) == ["bar", "key", "zebra"]
    assert list(reversed(pf)) == ["zebra", "key", "bar"]
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
bar=only definition

# Comment between values

key = value

zebra \\
    apple

# Comment at end of file
'''

def test_propfile_from_ordereddict():
    pf = PropertiesFile(OrderedDict([('key', 'value'), ('apple', 'zebra')]))
    pf._check()
    assert len(pf) == 2
    assert bool(pf)
    assert dict(pf) == {"apple": "zebra", "key": "value"}
    assert list(pf) == ["key", "apple"]
    assert list(reversed(pf)) == ["apple", "key"]
    assert pf.dumps() == 'key=value\napple=zebra\n'

def test_propfile_from_kwarg():
    pf = PropertiesFile(key='value')
    pf._check()
    assert len(pf) == 1
    assert bool(pf)
    assert dict(pf) == {"key": "value"}
    assert list(pf) == ["key"]
    assert list(reversed(pf)) == ["key"]
    assert pf.dumps() == 'key=value\n'

def test_propfile_from_pairs_list():
    pf = PropertiesFile([('key', 'value'), ('apple', 'zebra')])
    pf._check()
    assert len(pf) == 2
    assert bool(pf)
    assert dict(pf) == {"apple": "zebra", "key": "value"}
    assert list(pf) == ["key", "apple"]
    assert list(reversed(pf)) == ["apple", "key"]
    assert pf.dumps() == 'key=value\napple=zebra\n'

def test_propfile_from_ordereddict_and_kwarg():
    pf = PropertiesFile(OrderedDict([('key', 'value'), ('apple', 'zebra')]),
                        key='lock')
    pf._check()
    assert len(pf) == 2
    assert bool(pf)
    assert dict(pf) == {"apple": "zebra", "key": "lock"}
    assert list(pf) == ["key", "apple"]
    assert list(reversed(pf)) == ["apple", "key"]
    assert pf.dumps() == 'key=lock\napple=zebra\n'

def test_propfile_dumps_separator():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    assert pf.dumps(separator='\t') == INPUT

def test_propfile_set_dumps_separator():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    pf["key"] = "lock"
    pf._check()
    assert pf.dumps(separator='\t') == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
foo: first definition
bar=only definition

# Comment between values

key\tlock

zebra \\
    apple
foo : second definition

# Comment at end of file
'''

@pytest.mark.parametrize('ensure_ascii', [False, True])
def test_propfile_dumps_ensure_ascii(ensure_ascii):
    txt = INPUT + 'ð=edh\n'
    pf = PropertiesFile.loads(txt)
    pf._check()
    assert pf.dumps(ensure_ascii=ensure_ascii) == txt

def test_propfile_set_dumps_ensure_ascii():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    pf["ð"] = "edh"
    pf._check()
    assert pf.dumps(ensure_ascii=True) == INPUT + '\\u00f0=edh\n'

def test_propfile_set_dumps_no_ensure_ascii():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    pf["ð"] = "edh"
    pf._check()
    assert pf.dumps(ensure_ascii=False) == INPUT + 'ð=edh\n'

def test_propfile_copy():
    pf = PropertiesFile({"Foo": "bar"})
    pf2 = pf.copy()
    pf._check()
    pf2._check()
    assert pf is not pf2
    assert isinstance(pf2, PropertiesFile)
    assert pf == pf2
    assert dict(pf) == dict(pf2) == {"Foo": "bar"}
    pf2["Foo"] = "gnusto"
    pf._check()
    pf2._check()
    assert dict(pf) == {"Foo": "bar"}
    assert dict(pf2) == {"Foo": "gnusto"}
    assert pf != pf2
    pf2["fOO"] = "quux"
    pf._check()
    pf2._check()
    assert dict(pf) == {"Foo": "bar"}
    assert dict(pf2) == {"Foo": "gnusto", "fOO": "quux"}
    assert pf != pf2

def test_propfile_copy_more():
    pf = PropertiesFile.loads(INPUT)
    pf2 = pf.copy()
    pf._check()
    pf2._check()
    assert pf is not pf2
    assert isinstance(pf2, PropertiesFile)
    assert pf == pf2
    assert dict(pf) == dict(pf2) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }
    pf2["foo"] = "third definition"
    del pf2["bar"]
    pf2["key"] = "value"
    pf2["zebra"] = "horse"
    pf2["new"] = "old"
    pf._check()
    pf2._check()
    assert pf != pf2
    assert dict(pf) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }
    assert dict(pf2) == {
        "foo": "third definition",
        "key": "value",
        "zebra": "horse",
        "new": "old",
    }
    assert pf.dumps() == INPUT
    assert pf2.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
foo=third definition

# Comment between values

key=value

zebra=horse

# Comment at end of file
new=old
'''

def test_propfile_eq_empty():
    pf = PropertiesFile()
    pf2 = PropertiesFile()
    assert pf is not pf2
    assert pf == pf2

def test_propfile_eq_nonempty():
    pf = PropertiesFile({"Foo": "bar"})
    pf2 = PropertiesFile({"Foo": "bar"})
    assert pf is not pf2
    assert pf == pf2

def test_propfile_eq_self():
    pf = PropertiesFile.loads(INPUT)
    assert pf == pf

def test_propfile_neq():
    assert PropertiesFile({"Foo": "bar"}) != PropertiesFile({"Foo": "BAR"})

def test_propfile_eq_dict():
    pf = PropertiesFile({"Foo": "BAR"})
    assert pf == {"Foo": "BAR"}
    assert {"Foo": "BAR"} == pf
    assert pf != {"Foo": "bar"}
    assert {"Foo": "bar"} != pf

def test_propfile_eq_set_nochange():
    pf = PropertiesFile.loads(INPUT)
    pf2 = PropertiesFile.loads(INPUT)
    assert pf == pf2
    assert pf["key"] == pf2["key"] == "value"
    pf2["key"] = "value"
    assert pf == pf2
    assert dict(pf) == dict(pf2)
    assert pf.dumps() == INPUT
    assert pf.dumps() != pf2.dumps()

def test_propfile_neq_one_comment():
    pf = PropertiesFile.loads('#This is a comment.\nkey=value\n')
    pf2 = PropertiesFile.loads('key=value\n')
    assert pf != pf2
    assert dict(pf) == dict(pf2)

def test_propfile_neq_different_comments():
    pf = PropertiesFile.loads('#This is a comment.\nkey=value\n')
    pf2 = PropertiesFile.loads('#This is also a comment.\nkey=value\n')
    assert pf != pf2
    assert dict(pf) == dict(pf2)

def test_propfile_eq_one_repeated_key():
    pf = PropertiesFile.loads('key = value\nkey: other value\n')
    pf2 = PropertiesFile.loads('key other value')
    assert pf == pf2
    assert dict(pf) == dict(pf2) == {"key": "other value"}

def test_propfile_eq_repeated_keys():
    pf = PropertiesFile.loads('key = value\nkey: other value\n')
    pf2 = PropertiesFile.loads('key: whatever\nkey other value')
    assert pf == pf2
    assert dict(pf) == dict(pf2) == {"key": "other value"}

def test_propfile_neq_string():
    pf = PropertiesFile.loads('key = value\nkey: other value\n')
    assert pf != 'key = value\nkey: other value\n'
    assert 'key = value\nkey: other value\n' != pf

def test_propfile_preserve_trailing_escape():
    pf = PropertiesFile.loads('key = value\\')
    pf._check()
    assert dict(pf) == {"key": "value"}
    assert pf.dumps() == 'key = value\\'

def test_propfile_add_after_trailing_escape():
    pf = PropertiesFile.loads('key = value\\')
    pf._check()
    pf["new"] = "old"
    pf._check()
    assert dict(pf) == {"key": "value", "new": "old"}
    assert pf.dumps() == 'key = value\nnew=old\n'

def test_propfile_preserve_trailing_comment_escape():
    pf = PropertiesFile.loads('#key = value\\')
    pf._check()
    assert dict(pf) == {}
    assert pf.dumps() == '#key = value\\'

def test_propfile_add_after_trailing_comment_escape():
    pf = PropertiesFile.loads('#key = value\\')
    pf._check()
    pf["new"] = "old"
    pf._check()
    assert dict(pf) == {"new": "old"}
    assert pf.dumps() == '#key = value\\\nnew=old\n'

def test_propfile_preserve_no_trailing_newline():
    pf = PropertiesFile.loads('key = value')
    pf._check()
    assert dict(pf) == {"key": "value"}
    assert pf.dumps() == 'key = value'

def test_propfile_add_after_no_trailing_newline():
    pf = PropertiesFile.loads('key = value\\')
    pf._check()
    pf["new"] = "old"
    pf._check()
    assert dict(pf) == {"key": "value", "new": "old"}
    assert pf.dumps() == 'key = value\nnew=old\n'

def test_propfile_preserve_comment_no_trailing_newline():
    pf = PropertiesFile.loads('#key = value')
    pf._check()
    assert dict(pf) == {}
    assert pf.dumps() == '#key = value'

def test_propfile_add_after_comment_no_trailing_newline():
    pf = PropertiesFile.loads('#key = value')
    pf._check()
    pf["new"] = "old"
    pf._check()
    assert dict(pf) == {"new": "old"}
    assert pf.dumps() == '#key = value\nnew=old\n'

def test_propfile_preserve_trailing_escape_nl():
    pf = PropertiesFile.loads('key = value\\\n')
    pf._check()
    assert dict(pf) == {"key": "value"}
    assert pf.dumps() == 'key = value\\\n'

def test_propfile_add_after_trailing_escape_nl():
    pf = PropertiesFile.loads('key = value\\\n')
    pf._check()
    pf["new"] = "old"
    pf._check()
    assert dict(pf) == {"key": "value", "new": "old"}
    assert pf.dumps() == 'key = value\nnew=old\n'

def test_propfile_preserve_trailing_comment_escape_nl():
    pf = PropertiesFile.loads('#key = value\\\n')
    pf._check()
    assert dict(pf) == {}
    assert pf.dumps() == '#key = value\\\n'

def test_propfile_add_after_trailing_comment_escape_nl():
    pf = PropertiesFile.loads('#key = value\\\n')
    pf._check()
    pf["new"] = "old"
    pf._check()
    assert dict(pf) == {"new": "old"}
    assert pf.dumps() == '#key = value\\\nnew=old\n'

def test_propfile_empty_setitem():
    pf = PropertiesFile()
    pf._check()
    pf["key"] = "value"
    pf._check()
    assert len(pf) == 1
    assert bool(pf)
    assert dict(pf) == {"key": "value"}
    assert list(pf) == ["key"]
    assert list(reversed(pf)) == ["key"]
    assert pf.dumps() == 'key=value\n'

def test_propfile_to_ordereddict():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    assert OrderedDict(pf) == OrderedDict([
        ("foo", "second definition"),
        ("bar", "only definition"),
        ("key", "value"),
        ("zebra", "apple"),
    ])

@pytest.mark.parametrize('src,ts', [
    ('', None),
    ('#Thu Mar 16 17:06:52 EDT 2017\n', 'Thu Mar 16 17:06:52 EDT 2017'),
    ('!Thu Mar 16 17:06:52 EDT 2017\n', 'Thu Mar 16 17:06:52 EDT 2017'),
    ('\n \r#Thu Mar 16 17:06:52 EDT 2017\n', 'Thu Mar 16 17:06:52 EDT 2017'),
    (INPUT, 'Thu Mar 16 17:06:52 EDT 2017'),
    (
        '# comment 1\n!comment 2\n# Thu Mar 16 17:06:52 EDT 2017\n',
        ' Thu Mar 16 17:06:52 EDT 2017',
    ),
    ('key=value\n#Thu Mar 16 17:06:52 EDT 2017\n', None),
    (
        '#Thu Mar 16 17:06:52 EDT 2017\n#Tue Feb 25 19:13:27 EST 2020\n',
        'Thu Mar 16 17:06:52 EDT 2017',
    ),
])
def test_propfile_get_timestamp(src, ts):
    pf = PropertiesFile.loads(src)
    pf._check()
    assert pf.timestamp == ts

@pytest.mark.parametrize('src,ts,ts2,result', [
    (
        '',
        'Thu Mar 16 17:06:52 EDT 2017',
        'Thu Mar 16 17:06:52 EDT 2017',
        '#Thu Mar 16 17:06:52 EDT 2017\n',
    ),
    ('', None, None, ''),
    ('', False, None, ''),
    ('', '', None, '#\n'),
    (
        'key=value\n',
        0,
        'Wed Dec 31 19:00:00 EST 1969',
        '#Wed Dec 31 19:00:00 EST 1969\nkey=value\n',
    ),
    (
        'key=value\n',
        1234567890,
        'Fri Feb 13 18:31:30 EST 2009',
        '#Fri Feb 13 18:31:30 EST 2009\nkey=value\n',
    ),
    (
        'key=value\n',
        datetime(2020, 3, 4, 15, 57, 41),
        'Wed Mar 04 15:57:41 EST 2020',
        '#Wed Mar 04 15:57:41 EST 2020\nkey=value\n',
    ),
    (
        'key=value\n',
        datetime(2020, 3, 4, 12, 57, 41,tzinfo=tzstr('PST8PDT,M4.1.0,M10.5.0')),
        'Wed Mar 04 12:57:41 PST 2020',
        '#Wed Mar 04 12:57:41 PST 2020\nkey=value\n',
    ),
    ('key=value\n', None, None, 'key=value\n'),
    ('key=value\n', False, None, 'key=value\n'),
    ('key=value\n', '', None, '#\nkey=value\n'),
    ('key=value\n', 'Not a timestamp', None, '#Not a timestamp\nkey=value\n'),
    ('key=value\n', 'Line 1\n', None, '#Line 1\n#\nkey=value\n'),
    ('key=value\n', 'Line 1\nLine 2', None, '#Line 1\n#Line 2\nkey=value\n'),
    ('key=value\n', 'Line 1\n#Line 2', None, '#Line 1\n#Line 2\nkey=value\n'),
    ('key=value\n', 'Line 1\n!Line 2', None, '#Line 1\n!Line 2\nkey=value\n'),
    (
        '#Comment\n'
        '#Thu Mar 16 17:06:52 EDT 2017\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
        1234567890,
        'Fri Feb 13 18:31:30 EST 2009',
        '#Comment\n'
        '#Fri Feb 13 18:31:30 EST 2009\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
    ),
    (
        '#Comment\n'
        '#Thu Mar 16 17:06:52 EDT 2017\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
        None,
        'Wed Mar 04 12:57:41 PST 2020',
        '#Comment\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
    ),
    (
        '#Comment\n'
        '#Thu Mar 16 17:06:52 EDT 2017\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
        False,
        'Wed Mar 04 12:57:41 PST 2020',
        '#Comment\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
    ),
    (
        '#Comment\n'
        '#Thu Mar 16 17:06:52 EDT 2017\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
        '',
        'Wed Mar 04 12:57:41 PST 2020',
        '#Comment\n'
        '#\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
    ),
    (
        '#Comment\n'
        '#Thu Mar 16 17:06:52 EDT 2017\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
        'Not a timestamp',
        'Wed Mar 04 12:57:41 PST 2020',
        '#Comment\n'
        '#Not a timestamp\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
    ),
    (
        '#Comment\n'
        '#Thu Mar 16 17:06:52 EDT 2017\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
        'Line 1\n',
        'Wed Mar 04 12:57:41 PST 2020',
        '#Comment\n'
        '#Line 1\n'
        '#\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
    ),
    (
        '#Comment\n'
        '#Thu Mar 16 17:06:52 EDT 2017\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
        'Line 1\nLine 2',
        'Wed Mar 04 12:57:41 PST 2020',
        '#Comment\n'
        '#Line 1\n'
        '#Line 2\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
    ),
    (
        '#Comment\n'
        '#Thu Mar 16 17:06:52 EDT 2017\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
        'Line 1\n#Line 2',
        'Wed Mar 04 12:57:41 PST 2020',
        '#Comment\n'
        '#Line 1\n'
        '#Line 2\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
    ),
    (
        '#Comment\n'
        '#Thu Mar 16 17:06:52 EDT 2017\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
        'Line 1\n!Line 2',
        'Wed Mar 04 12:57:41 PST 2020',
        '#Comment\n'
        '#Line 1\n'
        '!Line 2\n'
        '#Comment 2\n'
        '#Wed Mar 04 12:57:41 PST 2020\n'
        'key=value\n',
    ),
    (
        '#Comment\n'
        '\n'
        '#Comment 2\n'
        'key=value\n',
        1234567890,
        'Fri Feb 13 18:31:30 EST 2009',
        '#Comment\n'
        '\n'
        '#Comment 2\n'
        '#Fri Feb 13 18:31:30 EST 2009\n'
        'key=value\n',
    ),
])
def test_propfile_set_timestamp(src, ts, ts2, result):
    pf = PropertiesFile.loads(src)
    pf._check()
    pf.timestamp = ts
    pf._check()
    assert pf.timestamp == ts2
    assert pf.dumps() == result

def test_propfile_set_timestamp_now(fixed_timestamp):
    pf = PropertiesFile.loads('key=value\n')
    pf._check()
    pf.timestamp = True
    pf._check()
    assert pf.timestamp == fixed_timestamp
    assert pf.dumps() == '#' + fixed_timestamp + '\nkey=value\n'

@pytest.mark.parametrize('src,ts2,result', [
    ('', None, ''),
    ('#Thu Mar 16 17:06:52 EDT 2017\n', None, ''),
    ('\n \r#Thu Mar 16 17:06:52 EDT 2017\n', None, '\n \r'),
    (
        INPUT,
        None,
        '# A comment before the timestamp\n'
        '# A comment after the timestamp\n'
        'foo: first definition\n'
        'bar=only definition\n'
        '\n'
        '# Comment between values\n'
        '\n'
        'key = value\n'
        '\n'
        'zebra \\\n'
        '    apple\n'
        'foo : second definition\n'
        '\n'
        '# Comment at end of file\n'
    ),
    (
        '# comment 1\n!comment 2\n# Thu Mar 16 17:06:52 EDT 2017\n',
        None,
        '# comment 1\n!comment 2\n',
    ),
    (
        'key=value\n#Thu Mar 16 17:06:52 EDT 2017\n',
        None,
        'key=value\n#Thu Mar 16 17:06:52 EDT 2017\n',
    ),
    (
        '#Thu Mar 16 17:06:52 EDT 2017\n#Tue Feb 25 19:13:27 EST 2020\n',
        'Tue Feb 25 19:13:27 EST 2020',
        '#Tue Feb 25 19:13:27 EST 2020\n',
    ),
])
def test_propfile_delete_timestamp(src, ts2, result):
    pf = PropertiesFile.loads(src)
    pf._check()
    del pf.timestamp
    pf._check()
    assert pf.timestamp == ts2
    assert pf.dumps() == result

@pytest.mark.parametrize('src,c', [
    ('', None),
    ('#\n', ''),
    ('#\n#comment\n', '\ncomment'),
    ('#comment\n#\n', 'comment\n'),
    (INPUT, ' A comment before the timestamp'),
    (
        '# comment 1\n!comment 2\n# Thu Mar 16 17:06:52 EDT 2017\n',
        ' comment 1\ncomment 2',
    ),
    ('# comment 1\n!comment 2\nkey=value\n', ' comment 1\ncomment 2'),
    ('# comment 1\r\n!comment 2\nkey=value\n', ' comment 1\ncomment 2'),
    ('# comment 1\r!comment 2\nkey=value\n', ' comment 1\ncomment 2'),
    ('# comment 1\n\t\r\n !comment 2\nkey=value\n', ' comment 1\ncomment 2'),
    ('# Thu Mar 16 17:06:52 EDT 2017\n# Comment\n', None),
    ('key=value\n# Comment\n', None),
])
def test_propfile_get_header_comment(src, c):
    pf = PropertiesFile.loads(src)
    pf._check()
    assert pf.header_comment == c

@pytest.mark.parametrize('c,c2,csrc', [
    (None, None, ''),
    ('', '', '#\n'),
    ('This is test text.', 'This is test text.', '#This is test text.\n'),
    ('Line 1\n', 'Line 1\n', '#Line 1\n#\n'),
    ('Line 1\nLine 2', 'Line 1\nLine 2', '#Line 1\n#Line 2\n'),
    ('Line 1\n#Line 2', 'Line 1\nLine 2', '#Line 1\n#Line 2\n'),
    ('Line 1\n!Line 2', 'Line 1\nLine 2', '#Line 1\n!Line 2\n'),
])
@pytest.mark.parametrize('part1', [
    '',
    '#This comment will be deleted.\n',
    '#This will be deleted.\n!This, too\n',
    '#This will be deleted.\n    \r\n#And also that blank line in between.\n',
    '\n\n#This and the blank lines above will be deleted.\n',
    '#This and the blank lines below will be deleted.\n\n\n',
])
@pytest.mark.parametrize('part2', [
    '',
    'key=value\n',
    '#Thu Mar 16 17:06:52 EDT 2017\nkey=value\n'
    'key=value\n#Post-entry comment\n',
])
def test_propfile_set_header_comment(part1, part2, c, c2, csrc):
    pf = PropertiesFile.loads(part1 + part2)
    pf._check()
    pf.header_comment = c
    pf._check()
    assert pf.header_comment == c2
    assert pf.dumps() == csrc + part2

@pytest.mark.parametrize('part1', [
    '',
    '#This comment will be deleted.\n',
    '#This will be deleted.\n!This, too\n',
    '#This will be deleted.\n    \r\n#And also that blank line in between.\n',
    '\n\n#This and the blank lines above will be deleted.\n',
    '#This and the blank lines below will be deleted.\n\n\n',
])
@pytest.mark.parametrize('part2', [
    '',
    'key=value\n',
    '#Thu Mar 16 17:06:52 EDT 2017\nkey=value\n'
    'key=value\n#Post-entry comment\n',
])
def test_propfile_delete_header_comment(part1, part2):
    pf = PropertiesFile.loads(part1 + part2)
    pf._check()
    del pf.header_comment
    pf._check()
    assert pf.header_comment is None
    assert pf.dumps() == part2

# preserving mixtures of line endings
