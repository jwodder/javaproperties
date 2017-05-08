from   __future__     import unicode_literals
import collections
from   freezegun      import freeze_time
import pytest
from   six            import StringIO
from   javaproperties import Properties

# Making the global INPUT object a StringIO would cause it be exhausted after
# the first test and thereafter appear to be empty.  Thus, a new StringIO must
# be created for each test instead.
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

@freeze_time('2016-11-07 20:29:40')
def test_propclass_empty():
    p = Properties()
    assert len(p) == 0
    assert not bool(p)
    assert dict(p) == {}
    s = StringIO()
    p.store(s)
    assert s.getvalue() == '#Mon Nov 07 15:29:40 EST 2016\n'

def test_propclass_load():
    p = Properties()
    p.load(StringIO(INPUT))
    assert len(p) == 4
    assert bool(p)
    assert dict(p) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }

def test_propclass_setitem():
    p = Properties()
    p.load(StringIO(INPUT))
    p["key"] = "lock"
    assert len(p) == 4
    assert bool(p)
    assert dict(p) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "lock",
        "zebra": "apple",
    }

def test_propclass_additem():
    p = Properties()
    p.load(StringIO(INPUT))
    p["new"] = "old"
    assert len(p) == 5
    assert bool(p)
    assert dict(p) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
        "new": "old",
    }

def test_propclass_delitem():
    p = Properties()
    p.load(StringIO(INPUT))
    del p["key"]
    assert len(p) == 3
    assert bool(p)
    assert dict(p) == {
        "foo": "second definition",
        "bar": "only definition",
        "zebra": "apple",
    }

def test_propclass_from_dict():
    p = Properties({"key": "value", "apple": "zebra"})
    assert len(p) == 2
    assert bool(p)
    assert dict(p) == {"apple": "zebra", "key": "value"}

def test_propclass_from_pairs():
    p = Properties([("key", "value"), ("apple", "zebra")])
    assert len(p) == 2
    assert bool(p)
    assert dict(p) == {"apple": "zebra", "key": "value"}

def test_propclass_copy():
    p = Properties({"Foo": "bar"})
    p2 = p.copy()
    assert p is not p2
    assert isinstance(p2, Properties)
    assert p == p2
    assert dict(p) == dict(p2) == {"Foo": "bar"}
    p2["Foo"] = "gnusto"
    assert dict(p) == {"Foo": "bar"}
    assert dict(p2) == {"Foo": "gnusto"}
    assert p != p2
    p2["fOO"] = "quux"
    assert dict(p) == {"Foo": "bar"}
    assert dict(p2) == {"Foo": "gnusto", "fOO": "quux"}
    assert p != p2

def test_propclass_copy_more():
    p = Properties()
    p.load(StringIO(INPUT))
    p2 = p.copy()
    assert p is not p2
    assert isinstance(p2, Properties)
    assert p == p2
    assert dict(p) == dict(p2) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }
    p2["foo"] = "third definition"
    del p2["bar"]
    p2["key"] = "value"
    p2["zebra"] = "horse"
    p2["new"] = "old"
    assert p != p2
    assert dict(p) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }
    assert dict(p2) == {
        "foo": "third definition",
        "key": "value",
        "zebra": "horse",
        "new": "old",
    }

def test_propclass_eq_empty():
    p = Properties()
    p2 = Properties()
    assert p is not p2
    assert p == p2

def test_propclass_eq_nonempty():
    p = Properties({"Foo": "bar"})
    p2 = Properties({"Foo": "bar"})
    assert p is not p2
    assert p == p2

def test_propclass_eq_self():
    p = Properties()
    p.load(StringIO(INPUT))
    assert p == p

def test_propclass_neq():
    assert Properties({"Foo": "bar"}) != Properties({"Foo": "BAR"})

def test_propclass_eq_dict():
    p = Properties({"Foo": "BAR"})
    assert p == {"Foo": "BAR"}
    assert {"Foo": "BAR"} == p
    assert p != {"Foo": "bar"}
    assert {"Foo": "bar"} != p

def test_propclass_eq_set_nochange():
    p = Properties()
    p.load(StringIO(INPUT))
    p2 = Properties()
    p2.load(StringIO(INPUT))
    assert p == p2
    assert p["key"] == p2["key"] == "value"
    p2["key"] = "value"
    assert p == p2
    assert dict(p) == dict(p2)

def test_propclass_eq_one_comment():
    p = Properties()
    p.load(StringIO('#This is a comment.\nkey=value\n'))
    p2 = Properties()
    p2.load(StringIO('key=value\n'))
    assert p == p2
    assert dict(p) == dict(p2)

def test_propclass_eq_different_comments():
    p = Properties()
    p.load(StringIO('#This is a comment.\nkey=value\n'))
    p2 = Properties()
    p2.load(StringIO('#This is also a comment.\nkey=value\n'))
    assert p == p2
    assert dict(p) == dict(p2)

def test_propclass_eq_one_repeated_key():
    p = Properties()
    p.load(StringIO('key = value\nkey: other value\n'))
    p2 = Properties()
    p2.load(StringIO('key other value'))
    assert p == p2
    assert dict(p) == dict(p2) == {"key": "other value"}

def test_propclass_eq_repeated_keys():
    p = Properties()
    p.load(StringIO('key = value\nkey: other value\n'))
    p2 = Properties()
    p2.load(StringIO('key: whatever\nkey other value'))
    assert p == p2
    assert dict(p) == dict(p2) == {"key": "other value"}

def test_propclass_load_eq_from_dict():
    p = Properties()
    p.load(StringIO(INPUT))
    assert p == Properties({
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    })

def test_propclass_propertyNames():
    p = Properties({"key": "value", "apple": "zebra", "foo": "bar"})
    names = p.propertyNames()
    assert isinstance(names, collections.Iterator)
    assert sorted(names) == ["apple", "foo", "key"]

def test_propclass_stringPropertyNames():
    p = Properties({"key": "value", "apple": "zebra", "foo": "bar"})
    assert p.stringPropertyNames() == set(["key", "apple", "foo"])

def test_propclass_getProperty():
    p = Properties({"key": "value", "apple": "zebra", "foo": "bar"})
    assert p.getProperty("key") == "value"

def test_propclass_getProperty_default():
    p = Properties({"key": "value", "apple": "zebra", "foo": "bar"})
    assert p.getProperty("key", "default") == "value"

def test_propclass_getProperty_missing():
    p = Properties({"key": "value", "apple": "zebra", "foo": "bar"})
    assert p.getProperty("missing") is None

def test_propclass_getProperty_missing_default():
    p = Properties({"key": "value", "apple": "zebra", "foo": "bar"})
    assert p.getProperty("missing", "default") == "default"

def test_propclass_nonstring_key():
    p = Properties({"key": "value", "apple": "zebra", "foo": "bar"})
    with pytest.raises(TypeError) as excinfo:
        p[42] = 'forty-two'
    assert str(excinfo.value) == \
        'Keys & values of Properties objects must be strings'

def test_propclass_nonstring_value():
    p = Properties({"key": "value", "apple": "zebra", "foo": "bar"})
    with pytest.raises(TypeError) as excinfo:
        p['forty-two'] = 42
    assert str(excinfo.value) == \
        'Keys & values of Properties objects must be strings'

def test_propclass_from_nonstring_key():
    with pytest.raises(TypeError) as excinfo:
        Properties({"key": "value", 42: "forty-two"})
    assert str(excinfo.value) == \
        'Keys & values of Properties objects must be strings'

def test_propclass_from_nonstring_value():
    with pytest.raises(TypeError) as excinfo:
        Properties({"key": "value", "forty-two": 42})
    assert str(excinfo.value) == \
        'Keys & values of Properties objects must be strings'

def test_propclass_defaults():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    assert len(p) == 2
    assert bool(p)
    assert dict(p) == {"key": "value", "apple": "zebra"}

def test_propclass_defaults_getitem():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    assert p["apple"] == "zebra"

def test_propclass_defaults_getitem_overridden():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    assert p["key"] == "value"

def test_propclass_defaults_getitem_defaulted():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    with pytest.raises(KeyError):
        p["horse"]

def test_propclass_defaults_getProperty():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    assert p.getProperty("apple") == "zebra"

def test_propclass_defaults_getProperty_overridden():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    assert p.getProperty("key") == "value"

def test_propclass_defaults_getProperty_defaulted():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    assert p.getProperty("horse") == "orange"

def test_propclass_defaults_propertyNames():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    names = p.propertyNames()
    assert isinstance(names, collections.Iterator)
    assert sorted(names) == ["apple", "horse", "key"]

def test_propclass_defaults_stringPropertyNames():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    assert p.stringPropertyNames() == set(["key", "apple", "horse"])

# store() when non-empty (with & without comment)
# dumps() function?
# defaults with defaults
# asserting `load` and `setitem` don't affect `defaults`
# setitem on an empty instance
# get/delete nonexistent key
# equality when `defaults` is involved
# setProperty
# loadFromXML
# storeToXML (with & without comment)
# load() on a nonempty instance
# getitem
