import pytest

import javaproperties  # noqa


@pytest.mark.parametrize(
    "s,enc,b",
    [
        ("foobar", "us-ascii", b"foobar"),
        ("f\xfcbar", "us-ascii", b"f\\u00fcbar"),
        ("f\xfc\xdfar", "us-ascii", b"f\\u00fc\\u00dfar"),
        ("killer \u2603", "us-ascii", b"killer \\u2603"),
        ("kid \U0001f410", "us-ascii", b"kid \\ud83d\\udc10"),
        ("foobar", "iso-8859-1", b"foobar"),
        ("f\xfcbar", "iso-8859-1", b"f\xfcbar"),
        ("f\xfc\xdfar", "iso-8859-1", b"f\xfc\xdfar"),
        ("killer \u2603", "iso-8859-1", b"killer \\u2603"),
        ("kid \U0001f410", "iso-8859-1", b"kid \\ud83d\\udc10"),
        ("foobar", "utf-8", b"foobar"),
        ("f\xfcbar", "utf-8", b"f\xc3\xbcbar"),
        ("f\xfc\xdfar", "utf-8", b"f\xc3\xbc\xc3\x9far"),
        ("killer \u2603", "utf-8", b"killer \xe2\x98\x83"),
        ("kid \U0001f410", "utf-8", b"kid \xf0\x9f\x90\x90"),
        ("foobar", "utf-16be", "foobar".encode("utf-16be")),
        ("f\xfcbar", "utf-16be", "f\xfcbar".encode("utf-16be")),
        ("f\xfc\xdfar", "utf-16be", "f\xfc\xdfar".encode("utf-16be")),
        ("killer \u2603", "utf-16be", "killer \u2603".encode("utf-16be")),
        ("kid \U0001f410", "utf-16be", "kid \U0001f410".encode("utf-16be")),
        ("foobar", "mac_roman", b"foobar"),
        ("f\xfcbar", "mac_roman", b"f\x9fbar"),
        ("f\xfc\xdfar", "mac_roman", b"f\x9f\xa7ar"),
        ("killer \u2603", "mac_roman", b"killer \\u2603"),
        ("kid \U0001f410", "mac_roman", b"kid \\ud83d\\udc10"),
        ("e\xf0", "mac_roman", b"e\\u00f0"),
        ("\u201cHello!\u201d", "mac_roman", b"\xd2Hello!\xd3"),
        ("foobar", "cp500", "foobar".encode("cp500")),
        ("f\xfcbar", "cp500", "f\xfcbar".encode("cp500")),
        ("f\xfc\xdfar", "cp500", "f\xfc\xdfar".encode("cp500")),
        ("killer \u2603", "cp500", "killer \\u2603".encode("cp500")),
        ("kid \U0001f410", "cp500", "kid \\ud83d\\udc10".encode("cp500")),
    ],
)
def test_javapropertiesreplace(s, enc, b):
    assert s.encode(enc, "javapropertiesreplace") == b


@pytest.mark.parametrize(
    "s,esc",
    [
        ("\ud83d\udc10", "\\ud83d\\udc10"),
        ("\ud83d+\udc10", "\\ud83d+\\udc10"),
        ("\udc10\ud83d", "\\udc10\\ud83d"),
    ],
)
@pytest.mark.parametrize(
    "enc",
    [
        "us-ascii",
        "iso-8859-1",
        "utf-8",
        "utf-16be",
        "mac_roman",
        "cp500",
    ],
)
def test_javaproperties_bad_surrogates(s, enc, esc):
    assert s.encode(enc, "javapropertiesreplace") == esc.encode(enc)
