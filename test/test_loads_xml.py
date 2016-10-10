from   __future__     import unicode_literals
import pytest
from   javaproperties import loads_xml

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


# multiple <entry>s
# multiple <entry>s with the same key
# entities?
# object_pairs_hook=OrderedDict
# non-ASCII/non-Latin-1 characters (not escaped) in source string
# <entry> (or other tag) nested inside another <entry>?
# XML declarations?
# DTD declarations?
