from   __future__     import unicode_literals
from   javaproperties import PropertiesFile, dumps

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

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
    assert dict(pf) == {}
    assert list(pf) == []
    assert list(reversed(pf)) == []
    assert pf.dumps() == ''

def test_propfile_loads():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
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

def test_propfile_setitem():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    pf["key"] = "lock"
    pf._check()
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

def test_propfile_move_item():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    del pf["key"]
    pf._check()
    pf["key"] = "recreated"
    pf._check()
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
    pf["key"] = "value"
    pf._check()
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
    assert list(pf) == ["foo", "bar", "key", "zebra"]
    assert list(reversed(pf)) == ["zebra", "key", "bar", "foo"]
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
bar=only definition

# Comment between values

key = value

zebra \\
    apple
foo=redefinition

# Comment at end of file
'''

def test_propfile_from_ordereddict():
    pf = PropertiesFile(OrderedDict([('key', 'value'), ('apple', 'zebra')]))
    pf._check()
    assert dict(pf) == {"apple": "zebra", "key": "value"}
    assert list(pf) == ["key", "apple"]
    assert list(reversed(pf)) == ["apple", "key"]
    assert pf.dumps() == 'key=value\napple=zebra\n'

def test_propfile_from_kwarg():
    pf = PropertiesFile(key='value')
    pf._check()
    assert dict(pf) == {"key": "value"}
    assert list(pf) == ["key"]
    assert list(reversed(pf)) == ["key"]
    assert pf.dumps() == 'key=value\n'

def test_propfile_from_ordereddict_and_kwarg():
    pf = PropertiesFile(OrderedDict([('key', 'value'), ('apple', 'zebra')]),
                        key='lock')
    pf._check()
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
