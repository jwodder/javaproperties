from   collections.abc import Iterator
from   io              import BytesIO, StringIO
import pytest
from   javaproperties  import Properties, dumps

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

XML_INPUT = '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
    <comment>Thu Mar 16 17:06:52 EDT 2017</comment>
    <entry key="foo">first definition</entry>
    <entry key="bar">only definition</entry>
    <entry key="key">value</entry>
    <entry key="zebra">apple</entry>
    <entry key="foo">second definition</entry>
</properties>
'''

def test_propclass_empty(fixed_timestamp):
    p = Properties()
    assert len(p) == 0
    assert not bool(p)
    assert dict(p) == {}
    s = StringIO()
    p.store(s)
    assert s.getvalue() == '#' + fixed_timestamp + '\n'

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

def test_propclass_nonempty_load():
    p = Properties({"key": "lock", "horse": "orange"})
    p.load(StringIO(INPUT))
    assert len(p) == 5
    assert bool(p)
    assert dict(p) == {
        "foo": "second definition",
        "bar": "only definition",
        "horse": "orange",
        "key": "value",
        "zebra": "apple",
    }

def test_propclass_loadFromXML():
    p = Properties()
    p.loadFromXML(StringIO(XML_INPUT))
    assert len(p) == 4
    assert bool(p)
    assert dict(p) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }

def test_propclass_nonempty_loadFromXML():
    p = Properties({"key": "lock", "horse": "orange"})
    p.loadFromXML(StringIO(XML_INPUT))
    assert len(p) == 5
    assert bool(p)
    assert dict(p) == {
        "foo": "second definition",
        "bar": "only definition",
        "horse": "orange",
        "key": "value",
        "zebra": "apple",
    }

def test_propclass_getitem():
    p = Properties()
    p.load(StringIO(INPUT))
    assert p["key"] == "value"
    assert p["foo"] == "second definition"
    with pytest.raises(KeyError):
        p["missing"]

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

def test_propclass_delitem_missing():
    p = Properties()
    p.load(StringIO(INPUT))
    with pytest.raises(KeyError):
        del p["missing"]
    assert len(p) == 4
    assert bool(p)
    assert dict(p) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "value",
        "zebra": "apple",
    }

def test_propclass_from_dict():
    p = Properties({"key": "value", "apple": "zebra"})
    assert len(p) == 2
    assert bool(p)
    assert dict(p) == {"apple": "zebra", "key": "value"}

def test_propclass_from_pairs_list():
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
    assert p2 == p

def test_propclass_defaults_neq_empty():
    p = Properties()
    p2 = Properties(defaults=Properties({"key": "lock", "horse": "orange"}))
    assert p != p2
    assert p2 != p

def test_propclass_eq_nonempty():
    p = Properties({"Foo": "bar"})
    p2 = Properties({"Foo": "bar"})
    assert p is not p2
    assert p == p2
    assert p2 == p

def test_propclass_eq_nonempty_defaults():
    p = Properties({"Foo": "bar"}, defaults=Properties({"key": "lock"}))
    p2 = Properties({"Foo": "bar"}, defaults=Properties({"key": "lock"}))
    assert p is not p2
    assert p == p2
    assert p2 == p

def test_propclass_neq_nonempty_neq_defaults():
    p = Properties({"Foo": "bar"}, defaults=Properties({"key": "lock"}))
    p2 = Properties({"Foo": "bar"}, defaults=Properties({"key": "Florida"}))
    assert p != p2
    assert p2 != p

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

def test_propclass_defaults_eq_dict():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"Foo": "BAR"}, defaults=defs)
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

def test_propclass_neq_string():
    p = Properties()
    p.load(StringIO(INPUT))
    assert p != INPUT
    assert INPUT != p

def test_propclass_propertyNames():
    p = Properties({"key": "value", "apple": "zebra", "foo": "bar"})
    names = p.propertyNames()
    assert isinstance(names, Iterator)
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
    assert isinstance(names, Iterator)
    assert sorted(names) == ["apple", "horse", "key"]

def test_propclass_defaults_stringPropertyNames():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    assert p.stringPropertyNames() == set(["key", "apple", "horse"])

def test_propclass_setProperty():
    p = Properties()
    p.load(StringIO(INPUT))
    p.setProperty("key", "lock")
    assert len(p) == 4
    assert bool(p)
    assert dict(p) == {
        "foo": "second definition",
        "bar": "only definition",
        "key": "lock",
        "zebra": "apple",
    }

def test_propclass_defaults_setProperty():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    p.setProperty("apple", "banana")
    assert dict(p) == {"key": "value", "apple": "banana"}
    assert dict(defs) == {"key": "lock", "horse": "orange"}

def test_propclass_defaults_setProperty_overridden():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    p.setProperty("key", "hole")
    assert dict(p) == {"key": "hole", "apple": "zebra"}
    assert dict(defs) == {"key": "lock", "horse": "orange"}

def test_propclass_defaults_setProperty_new():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    p.setProperty("new", "old")
    assert dict(p) == {"key": "value", "apple": "zebra", "new": "old"}
    assert dict(defs) == {"key": "lock", "horse": "orange"}

def test_propclass_defaults_setProperty_new_override():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    p.setProperty("horse", "pony")
    assert dict(p) == {"key": "value", "apple": "zebra", "horse": "pony"}
    assert dict(defs) == {"key": "lock", "horse": "orange"}

def test_propclass_defaults_setitem():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    p["apple"] = "banana"
    assert dict(p) == {"key": "value", "apple": "banana"}
    assert dict(defs) == {"key": "lock", "horse": "orange"}

def test_propclass_defaults_setitem_overridden():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    p["key"] = "hole"
    assert dict(p) == {"key": "hole", "apple": "zebra"}
    assert dict(defs) == {"key": "lock", "horse": "orange"}

def test_propclass_defaults_setitem_new():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    p["new"] = "old"
    assert dict(p) == {"key": "value", "apple": "zebra", "new": "old"}
    assert dict(defs) == {"key": "lock", "horse": "orange"}

def test_propclass_defaults_setitem_new_override():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value", "apple": "zebra"}, defaults=defs)
    p["horse"] = "pony"
    assert dict(p) == {"key": "value", "apple": "zebra", "horse": "pony"}
    assert dict(defs) == {"key": "lock", "horse": "orange"}

def test_propclass_empty_setitem(fixed_timestamp):
    p = Properties()
    p["key"] = "value"
    assert len(p) == 1
    assert bool(p)
    assert dict(p) == {"key": "value"}
    s = StringIO()
    p.store(s)
    assert s.getvalue() == '#' + fixed_timestamp + '\nkey=value\n'

def test_propclass_store(fixed_timestamp):
    p = Properties({"key": "value"})
    s = StringIO()
    p.store(s)
    assert s.getvalue() == '#' + fixed_timestamp + '\nkey=value\n'

def test_propclass_store_comment(fixed_timestamp):
    p = Properties({"key": "value"})
    s = StringIO()
    p.store(s, comments='Testing')
    assert s.getvalue() == \
        '#Testing\n#' + fixed_timestamp + '\nkey=value\n'

def test_propclass_store_defaults(fixed_timestamp):
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value"}, defaults=defs)
    s = StringIO()
    p.store(s)
    assert s.getvalue() == '#' + fixed_timestamp + '\nkey=value\n'

def test_propclass_storeToXML():
    p = Properties({"key": "value"})
    s = BytesIO()
    p.storeToXML(s)
    assert s.getvalue() == b'''\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
</properties>
'''

def test_propclass_storeToXML_comment():
    p = Properties({"key": "value"})
    s = BytesIO()
    p.storeToXML(s, comment='Testing')
    assert s.getvalue() == b'''\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<comment>Testing</comment>
<entry key="key">value</entry>
</properties>
'''

def test_propclass_storeToXML_defaults():
    defs = Properties({"key": "lock", "horse": "orange"})
    p = Properties({"key": "value"}, defaults=defs)
    s = BytesIO()
    p.storeToXML(s)
    assert s.getvalue() == b'''\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
</properties>
'''

def test_propclass_dumps_function():
    assert dumps(Properties({"key": "value"}), timestamp=False) == 'key=value\n'

@pytest.mark.parametrize('data', [
    {},
    {"foo": "bar"},
    {"foo": "bar", "key": "value"},
])
@pytest.mark.parametrize('defaults', [
    None,
    Properties(),
    Properties({"zebra": "apple"}),
])
def test_propclass_repr(data, defaults):
    p = Properties(data, defaults=defaults)
    assert repr(p) == (
        f'javaproperties.propclass.Properties({data!r}, defaults={defaults!r})'
    )

def test_propclass_repr_noinit():
    p = Properties()
    assert repr(p) == 'javaproperties.propclass.Properties({}, defaults=None)'

# defaults with defaults
