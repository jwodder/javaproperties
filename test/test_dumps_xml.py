from   __future__     import unicode_literals
import sys
import pytest
from   javaproperties import dumps_xml

need_ordereddict = pytest.mark.skipif(
    sys.version_info[:2] < (2,7) or sys.version_info[:2] == (3,0),
    reason='No OrderedDict before 2.7/3.1',
)

def test_dumps_xml_nothing():
    assert dumps_xml({}) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
</properties>
'''

def test_dumps_xml_simple():
    assert dumps_xml({"key": "value"}) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
</properties>
'''

def test_dumps_xml_two_simple():
    assert dumps_xml([("key", "value"), ("zebra", "apple")]) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="zebra">apple</entry>
</properties>
'''

def test_dumps_xml_two_simple_rev():
    assert dumps_xml([("zebra", "apple"), ("key", "value")]) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="zebra">apple</entry>
<entry key="key">value</entry>
</properties>
'''

def test_dumps_xml_two_simple_sorted():
    assert dumps_xml(
        [("key", "value"), ("zebra", "apple")],
        sort_keys=True,
    ) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="zebra">apple</entry>
</properties>
'''

def test_dumps_xml_two_simple_rev_sorted():
    assert dumps_xml(
        [("zebra", "apple"), ("key", "value")],
        sort_keys=True,
    ) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="zebra">apple</entry>
</properties>
'''

@need_ordereddict
def test_dumps_xml_ordereddict():
    from collections import OrderedDict
    assert dumps_xml(OrderedDict([("key","value"), ("zebra","apple")])) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="zebra">apple</entry>
</properties>
'''

@need_ordereddict
def test_dumps_xml_ordereddict_rev():
    from collections import OrderedDict
    assert dumps_xml(OrderedDict([("zebra","apple"), ("key","value")])) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="zebra">apple</entry>
<entry key="key">value</entry>
</properties>
'''

@need_ordereddict
def test_dumps_xml_ordereddict_sorted():
    from collections import OrderedDict
    assert dumps_xml(
        OrderedDict([("key", "value"), ("zebra", "apple")]),
        sort_keys=True,
    ) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="zebra">apple</entry>
</properties>
'''

@need_ordereddict
def test_dumps_xml_ordereddict_rev_sorted():
    from collections import OrderedDict
    assert dumps_xml(
        OrderedDict([("zebra", "apple"), ("key", "value")]),
        sort_keys=True,
    ) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="zebra">apple</entry>
</properties>
'''

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
