from   collections    import OrderedDict
import pytest
from   javaproperties import loads_xml

@pytest.mark.parametrize('s,d', [
    ('<properties></properties>', {}),
    (
        '<properties><entry key="key">value</entry></properties>',
        {"key": "value"},
    ),
    (
        '<properties><entry key="key">   </entry></properties>',
        {"key": "   "},
    ),
    (
        '<properties><entry key="key">\n</entry></properties>',
        {"key": "\n"},
    ),
    (
        '<properties><entry key="key"></entry></properties>',
        {"key": ""},
    ),
    (
        '<properties><entry key="key"/></properties>',
        {"key": ""},
    ),
    (
        '<properties>'
        '<entry key="key">\n</entry>'
        '<not-an-entry><entry key="foo">bar</entry></not-an-entry>'
        '</properties>',
        {"key": "\n"},
    ),
    (
        '<properties>\n    <entry key="key">value</entry>\n</properties>\n',
        {"key": "value"},
    ),
    (
        '<properties>'
        '<entry key="key">value</entry>'
        '<entry key="foo">bar</entry>'
        '</properties>',
        {"key": "value", "foo": "bar"},
    ),
    (
        '<properties>\n'
        '    <entry key="key">value1</entry>\n'
        '    <entry key="key">value2</entry>\n'
        '</properties>\n',
        {"key": "value2"}
    ),
    (
        '<properties>\n'
        '    <entry key="ampersand">&amp;</entry>\n'
        '    <entry key="less than">&lt;</entry>\n'
        '    <entry key="greater than">&gt;</entry>\n'
        '    <entry key="&quot;">"</entry>\n'
        '    <entry key="snowman">&#x2603;</entry>\n'
        '</properties>\n',
        {
            "ampersand": "&",
            "less than": "<",
            "greater than": ">",
            '"': '"',
            "snowman": "\u2603",
        },
    ),
    (
        '<properties>\n'
        '    <entry key="escapes">\\n\\r\\t\\u2603\\f\\\\</entry>\n'
        '</properties>\n',
        {"escapes": "\\n\\r\\t\\u2603\\f\\\\"},
    ),
    (
        '<properties>\n'
        '    <comment>This is a comment.</comment>\n'
        '    <entry key="key">value</entry>\n'
        '</properties>\n',
        {"key": "value"},
    ),
    (
        '<properties>\n'
        '    <entry key="key">value</entry>\n'
        '    <something-else key="foo">bar</something-else>\n'
        '</properties>\n',
        {"key": "value"},
    ),
    (
        '<properties><entry key="goat">&#x1F410;</entry></properties>',
        {"goat": "\U0001F410"},
    ),
])
def test_loads_xml(s,d):
    assert loads_xml(s) == d

def test_loads_xml_bad_root():
    with pytest.raises(ValueError) as excinfo:
        loads_xml('<not-properties><entry key="key">value</entry></not-properties>')
    assert 'not rooted at <properties>' in str(excinfo.value)

def test_loads_xml_no_key():
    with pytest.raises(ValueError) as excinfo:
        loads_xml('<properties><entry>value</entry></properties>')
    assert '<entry> is missing "key" attribute' in str(excinfo.value)

def test_loads_xml_multiple_ordereddict():
    assert loads_xml('''
<properties>
    <entry key="key">value</entry>
    <entry key="foo">bar</entry>
</properties>
''', object_pairs_hook=OrderedDict) == \
        OrderedDict([("key", "value"), ("foo", "bar")])

def test_loads_xml_multiple_ordereddict_rev():
    assert loads_xml('''
<properties>
    <entry key="foo">bar</entry>
    <entry key="key">value</entry>
</properties>
''', object_pairs_hook=OrderedDict) == \
        OrderedDict([("foo", "bar"), ("key", "value")])
