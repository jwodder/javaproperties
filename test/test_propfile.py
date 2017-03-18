from   __future__     import unicode_literals
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

def test_propfile_loads():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    assert dict(pf) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }

def test_propfile_dumps():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
bar=only definition

# Comment between values

key = value

zebra \\
    apple
foo : second definition

# Comment at end of file
'''

def test_propfile_setitem():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    pf["key"] = "lock"
    pf._check()
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
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
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
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
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
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
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
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
    assert pf.dumps() == '''\
# A comment before the timestamp
#Thu Mar 16 17:06:52 EDT 2017
# A comment after the timestamp
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
bar=only definition
key=value
zebra=apple
foo=second definition
'''

def test_propfile_set_repeated_key():
    pf = PropertiesFile.loads(INPUT)
    pf._check()
    pf["foo"] = "redefinition"
    pf._check()
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
