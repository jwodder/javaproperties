from __future__     import unicode_literals
from javaproperties import dumps_xml

def test_dumps_xml_nothing():
    assert dumps_xml({}) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
</properties>
'''

def test_dumps_simple():
    assert dumps_xml({"key": "value"}) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
</properties>
'''

def test_dumps_two_simple():
    assert dumps_xml([("key", "value"), ("zebra", "apple")]) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="zebra">apple</entry>
</properties>
'''

def test_dumps_two_simple_rev():
    assert dumps_xml([("zebra", "apple"), ("key", "value")]) == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="zebra">apple</entry>
<entry key="key">value</entry>
</properties>
'''

def test_dumps_comment():
    assert dumps_xml({"key": "value"}, comment='This is a comment.') == '''\
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<comment>This is a comment.</comment>
<entry key="key">value</entry>
</properties>
'''

# test dumping non-ASCII characters?
# test dumping &, <, >, and (in keys) " ?
# all-whitespace value/comment?
# control whitespace in keys, values, & comments?
# OrderedDict
# sorting keys
