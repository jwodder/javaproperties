from   collections    import OrderedDict
import pytest
from   javaproperties import dumps_xml

@pytest.mark.parametrize('d,s', [
    (
        {},
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '</properties>\n'
    ),

    (
        {"key": "value"},
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '<entry key="key">value</entry>\n'
        '</properties>\n'
    ),

    (
        [("key", "value"), ("zebra", "apple")],
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '<entry key="key">value</entry>\n'
        '<entry key="zebra">apple</entry>\n'
        '</properties>\n'
    ),

    (
        [("zebra", "apple"), ("key", "value")],
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '<entry key="zebra">apple</entry>\n'
        '<entry key="key">value</entry>\n'
        '</properties>\n'
    ),

    (
        OrderedDict([("key","value"), ("zebra","apple")]),
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '<entry key="key">value</entry>\n'
        '<entry key="zebra">apple</entry>\n'
        '</properties>\n'
    ),

    (
        OrderedDict([("zebra","apple"), ("key","value")]),
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '<entry key="zebra">apple</entry>\n'
        '<entry key="key">value</entry>\n'
        '</properties>\n'
    ),

    (
        [
            ('key', 'value'),
            ('edh', '\xF0'),
            ('snowman', '\u2603'),
            ('goat', '\U0001F410'),
        ],
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '<entry key="key">value</entry>\n'
        '<entry key="edh">\xF0</entry>\n'
        '<entry key="snowman">\u2603</entry>\n'
        '<entry key="goat">\U0001F410</entry>\n'
        '</properties>\n'
    ),

    (
        [
            ('key', 'value'),
            ('\xF0', 'edh'),
            ('\u2603', 'snowman'),
            ('\U0001F410', 'goat'),
        ],
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '<entry key="key">value</entry>\n'
        '<entry key="\xF0">edh</entry>\n'
        '<entry key="\u2603">snowman</entry>\n'
        '<entry key="\U0001F410">goat</entry>\n'
        '</properties>\n'
    ),
])
def test_dumps_xml(d,s):
    assert dumps_xml(d) == s

@pytest.mark.parametrize('d,s', [
    (
        {"key": "value", "zebra": "apple"},
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '<entry key="key">value</entry>\n'
        '<entry key="zebra">apple</entry>\n'
        '</properties>\n'
    ),

    (
        [("key", "value"), ("zebra", "apple")],
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '<entry key="key">value</entry>\n'
        '<entry key="zebra">apple</entry>\n'
        '</properties>\n'
    ),

    (
        [("zebra", "apple"), ("key", "value")],
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '<entry key="key">value</entry>\n'
        '<entry key="zebra">apple</entry>\n'
        '</properties>\n'
    ),

    (
        OrderedDict([("key", "value"), ("zebra", "apple")]),
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '<entry key="key">value</entry>\n'
        '<entry key="zebra">apple</entry>\n'
        '</properties>\n'
    ),

    (
        OrderedDict([("zebra", "apple"), ("key", "value")]),
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        '<entry key="key">value</entry>\n'
        '<entry key="zebra">apple</entry>\n'
        '</properties>\n'
    ),
])
def test_dumps_xml_sorted(d,s):
    assert dumps_xml(d, sort_keys=True) == s

def test_dumps_xml_comment():
    assert dumps_xml({"key": "value"}, comment='This is a comment.') == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<comment>This is a comment.</comment>
<entry key="key">value</entry>
</properties>
'''

def test_dumps_xml_entities():
    assert dumps_xml({'&<>"\'': '&<>"\''}, comment='&<>"\'') == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<comment>&amp;&lt;&gt;"'</comment>
<entry key="&amp;&lt;&gt;&quot;'">&amp;&lt;&gt;"'</entry>
</properties>
'''
