from   __future__     import unicode_literals
import sys
import pytest
from   javaproperties import loads_xml

need_ordereddict = pytest.mark.skipif(
    sys.version_info[:2] < (2,7) or sys.version_info[:2] == (3,0),
    reason='No OrderedDict before 2.7/3.1',
)

def test_loads_xml_nothing():
    assert loads_xml('<properties></properties>') == {}

def test_loads_xml_simple():
    assert loads_xml('<properties><entry key="key">value</entry></properties>') == {"key": "value"}

def test_loads_xml_whitespace_value():
    assert loads_xml('<properties><entry key="key">   </entry></properties>') \
        == {"key": "   "}

def test_loads_xml_newline_value():
    assert loads_xml('<properties><entry key="key">\n</entry></properties>') \
        == {"key": "\n"}

def test_loads_xml_nested_entry():
    assert loads_xml('<properties><entry key="key">\n</entry><not-an-entry><entry key="foo">bar</entry></not-an-entry></properties>') == {"key": "\n"}

def test_loads_xml_bad_root():
    with pytest.raises(ValueError) as excinfo:
        loads_xml('<not-properties><entry key="key">value</entry></not-properties>')
    assert 'not rooted at <properties>' in str(excinfo.value)

def test_loads_xml_no_key():
    with pytest.raises(ValueError) as excinfo:
        loads_xml('<properties><entry>value</entry></properties>')
    assert '<entry> is missing "key" attribute' in str(excinfo.value)

def test_loads_xml_extra_whitespace():
    assert loads_xml('''
<properties>
    <entry key="key">value</entry>
</properties>
''') == {"key": "value"}

def test_loads_xml_multiple():
    assert loads_xml('<properties><entry key="key">value</entry><entry key="foo">bar</entry></properties>') == {"key": "value", "foo": "bar"}

@need_ordereddict
def test_loads_xml_multiple_ordereddict():
    from collections import OrderedDict
    assert loads_xml('''
<properties>
    <entry key="key">value</entry>
    <entry key="foo">bar</entry>
</properties>
''', object_pairs_hook=OrderedDict) == \
        OrderedDict([("key", "value"), ("foo", "bar")])

@need_ordereddict
def test_loads_xml_multiple_ordereddict_rev():
    from collections import OrderedDict
    assert loads_xml('''
<properties>
    <entry key="foo">bar</entry>
    <entry key="key">value</entry>
</properties>
''', object_pairs_hook=OrderedDict) == \
        OrderedDict([("foo", "bar"), ("key", "value")])

def test_loads_xml_reassign():
    assert loads_xml('''
<properties>
    <entry key="key">value1</entry>
    <entry key="key">value2</entry>
</properties>
''') == {"key": "value2"}

def test_loads_xml_entities():
    assert loads_xml('''
<properties>
    <entry key="ampersand">&amp;</entry>
    <entry key="less than">&lt;</entry>
    <entry key="greater than">&gt;</entry>
    <entry key="&quot;">"</entry>
    <entry key="snowman">&#x2603;</entry>
</properties>
''') == {
    "ampersand": "&",
    "less than": "<",
    "greater than": ">",
    '"': '"',
    "snowman": "\u2603",
}

def test_loads_xml_ignore_escapes():
    assert loads_xml('''
<properties>
    <entry key="escapes">\\n\\r\\t\\u2603\\f\\\\</entry>
</properties>
''') == {"escapes": "\\n\\r\\t\\u2603\\f\\\\"}

def test_loads_xml_commented():
    assert loads_xml('''
<properties>
    <comment>This is a comment.</comment>
    <entry key="key">value</entry>
</properties>
''') == {"key": "value"}

def test_loads_xml_unknown_tag():
    assert loads_xml('''
<properties>
    <entry key="key">value</entry>
    <something-else key="foo">bar</something-else>
</properties>
''') == {"key": "value"}

def test_loads_xml_astral_plane():
    assert loads_xml('''
<properties>
    <entry key="goat">&#x1F410;</entry>
</properties>
''') == {"goat": "\U0001F410"}
