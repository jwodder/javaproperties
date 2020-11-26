from   io             import BytesIO
import pytest
from   javaproperties import dump_xml

# The only thing special about `dump_xml` compared to `dumps_xml` is encoding,
# so that's the only thing we'll test here.

@pytest.mark.parametrize('enc', ['ASCII', 'Latin-1', 'UTF-16BE', 'UTF-8'])
def test_dump_xml_encoding(enc):
    fp = BytesIO()
    dump_xml([
        ('key', 'value'),
        ('edh', '\xF0'),
        ('snowman', '\u2603'),
        ('goat', '\U0001F410'),
    ], fp, encoding=enc)
    assert fp.getvalue() == '''\
<?xml version="1.0" encoding="{}" standalone="no"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="edh">\xF0</entry>
<entry key="snowman">\u2603</entry>
<entry key="goat">\U0001F410</entry>
</properties>
'''.format(enc).encode(enc, 'xmlcharrefreplace')
