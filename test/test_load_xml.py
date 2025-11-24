from __future__ import annotations
from io import BytesIO
import pytest
from javaproperties import load_xml

# The only thing special about `load_xml` compared to `loads_xml` is encoding,
# so that's the only thing we'll test here.


@pytest.mark.parametrize(
    "b",
    [
        (
            b'<?xml version="1.0" encoding="ASCII" standalone="no"?>\n'
            b'<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
            b"<properties>\n"
            b'<entry key="key">value</entry>\n'
            b'<entry key="edh">&#240;</entry>\n'
            b'<entry key="snowman">&#9731;</entry>\n'
            b'<entry key="goat">&#128016;</entry>\n'
            b"</properties>\n"
        ),
        (
            b'<?xml version="1.0" encoding="Latin-1" standalone="no"?>\n'
            b'<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
            b"<properties>\n"
            b'<entry key="key">value</entry>\n'
            b'<entry key="edh">\xf0</entry>\n'
            b'<entry key="snowman">&#9731;</entry>\n'
            b'<entry key="goat">&#128016;</entry>\n'
            b"</properties>\n"
        ),
        (
            '<?xml version="1.0" encoding="UTF-16BE" standalone="no"?>\n'
            '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
            "<properties>\n"
            '<entry key="key">value</entry>\n'
            '<entry key="edh">\xf0</entry>\n'
            '<entry key="snowman">\u2603</entry>\n'
            '<entry key="goat">\U0001f410</entry>\n'
            "</properties>\n"
        ).encode("utf-16be"),
        (
            b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            b'<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
            b"<properties>\n"
            b'<entry key="key">value</entry>\n'
            b'<entry key="edh">\xc3\xb0</entry>\n'
            b'<entry key="snowman">\xe2\x98\x83</entry>\n'
            b'<entry key="goat">\xf0\x9f\x90\x90</entry>\n'
            b"</properties>\n"
        ),
    ],
)
def test_load_xml(b: bytes) -> None:
    assert load_xml(BytesIO(b)) == {
        "key": "value",
        "edh": "\xf0",
        "snowman": "\u2603",
        "goat": "\U0001f410",
    }
