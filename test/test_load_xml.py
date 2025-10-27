from io import BytesIO
import pytest
from javaproperties import load_xml

# The only thing special about `load_xml` compared to `loads_xml` is encoding,
# so that's the only thing we'll test here.


@pytest.mark.parametrize(
    "b",
    [
        b"""\
<?xml version="1.0" encoding="ASCII" standalone="no"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="edh">&#240;</entry>
<entry key="snowman">&#9731;</entry>
<entry key="goat">&#128016;</entry>
</properties>
""",
        b"""\
<?xml version="1.0" encoding="Latin-1" standalone="no"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="edh">\xf0</entry>
<entry key="snowman">&#9731;</entry>
<entry key="goat">&#128016;</entry>
</properties>
""",
        """\
<?xml version="1.0" encoding="UTF-16BE" standalone="no"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="edh">\xf0</entry>
<entry key="snowman">\u2603</entry>
<entry key="goat">\U0001f410</entry>
</properties>
""".encode(
            "utf-16be"
        ),
        b"""\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="edh">\xc3\xb0</entry>
<entry key="snowman">\xe2\x98\x83</entry>
<entry key="goat">\xf0\x9f\x90\x90</entry>
</properties>
""",
    ],
)
def test_load_xml(b):
    assert load_xml(BytesIO(b)) == {
        "key": "value",
        "edh": "\xf0",
        "snowman": "\u2603",
        "goat": "\U0001f410",
    }
