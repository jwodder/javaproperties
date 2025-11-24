from __future__ import annotations
from io import BytesIO
import pytest
from javaproperties import dump_xml

# The only thing special about `dump_xml` compared to `dumps_xml` is encoding,
# so that's the only thing we'll test here.


@pytest.mark.parametrize("enc", ["ASCII", "Latin-1", "UTF-16BE", "UTF-8"])
def test_dump_xml_encoding(enc: str) -> None:
    fp = BytesIO()
    dump_xml(
        [
            ("key", "value"),
            ("edh", "\xf0"),
            ("snowman", "\u2603"),
            ("goat", "\U0001f410"),
        ],
        fp,
        encoding=enc,
    )
    assert fp.getvalue() == (
        f'<?xml version="1.0" encoding="{enc}" standalone="no"?>\n'
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        "<properties>\n"
        '<entry key="key">value</entry>\n'
        '<entry key="edh">\xf0</entry>\n'
        '<entry key="snowman">\u2603</entry>\n'
        '<entry key="goat">\U0001f410</entry>\n'
        "</properties>\n"
    ).encode(enc, "xmlcharrefreplace")
