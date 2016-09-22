from __future__     import unicode_literals
from javaproperties import loads_xml

def test_loads_xml_nothing():
    assert loads_xml('<properties></properties>') == {}

def test_loads_xml_simple():
    assert loads_xml('<properties><entry key="key">value</entry></properties>') == {"key": "value"}

def test_loads_xml_whitespace_value():
    assert loads_xml('<properties><entry key="key">   </entry></properties>') == {"key": "   "}

def test_loads_xml_newline_value():
    assert loads_xml('<properties><entry key="key">\n</entry></properties>') == {"key": "\n"}


# error on <entry> without key=
# error on non-<properties> root

# multiple <entry>s
# multiple <entry>s with the same key
# <entry> tag nested inside another tag
# entities?
# object_pairs_hook=OrderedDict ?
