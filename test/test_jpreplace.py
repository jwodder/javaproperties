import sys
import pytest
import javaproperties  # noqa

@pytest.mark.parametrize('s,enc,b', [
    ('foobar',             'us-ascii',   b'foobar'),
    ('f\xFCbar',           'us-ascii',   b'f\\u00fcbar'),
    ('f\xFC\xDFar',        'us-ascii',   b'f\\u00fc\\u00dfar'),
    ('killer \u2603',      'us-ascii',   b'killer \\u2603'),
    ('kid \U0001F410',     'us-ascii',   b'kid \\ud83d\\udc10'),

    ('foobar',             'iso-8859-1', b'foobar'),
    ('f\xFCbar',           'iso-8859-1', b'f\xFCbar'),
    ('f\xFC\xDFar',        'iso-8859-1', b'f\xFC\xDFar'),
    ('killer \u2603',      'iso-8859-1', b'killer \\u2603'),
    ('kid \U0001F410',     'iso-8859-1', b'kid \\ud83d\\udc10'),

    ('foobar',             'utf-8',      b'foobar'),
    ('f\xFCbar',           'utf-8',      b'f\xC3\xBCbar'),
    ('f\xFC\xDFar',        'utf-8',      b'f\xC3\xBC\xC3\x9Far'),
    ('killer \u2603',      'utf-8',      b'killer \xE2\x98\x83'),
    ('kid \U0001F410',     'utf-8',      b'kid \xF0\x9F\x90\x90'),

    ('foobar',             'utf-16be',   'foobar'.encode('utf-16be')),
    ('f\xFCbar',           'utf-16be',   'f\xFCbar'.encode('utf-16be')),
    ('f\xFC\xDFar',        'utf-16be',   'f\xFC\xDFar'.encode('utf-16be')),
    ('killer \u2603',      'utf-16be',   'killer \u2603'.encode('utf-16be')),
    ('kid \U0001F410',     'utf-16be',   'kid \U0001F410'.encode('utf-16be')),

    ('foobar',             'mac_roman',  b'foobar'),
    ('f\xFCbar',           'mac_roman',  b'f\x9Fbar'),
    ('f\xFC\xDFar',        'mac_roman',  b'f\x9F\xA7ar'),
    ('killer \u2603',      'mac_roman',  b'killer \\u2603'),
    ('kid \U0001F410',     'mac_roman',  b'kid \\ud83d\\udc10'),
    ('e\xF0',              'mac_roman',  b'e\\u00f0'),
    ('\u201CHello!\u201D', 'mac_roman',  b'\xD2Hello!\xD3'),

    ('foobar',             'cp500',      'foobar'.encode('cp500')),
    ('f\xFCbar',           'cp500',      'f\xFCbar'.encode('cp500')),
    ('f\xFC\xDFar',        'cp500',      'f\xFC\xDFar'.encode('cp500')),
    ('killer \u2603',      'cp500',      'killer \\u2603'.encode('cp500')),
    ('kid \U0001F410',     'cp500',      'kid \\ud83d\\udc10'.encode('cp500')),
])
def test_javapropertiesreplace(s, enc, b):
    assert s.encode(enc, 'javapropertiesreplace') == b

@pytest.mark.parametrize('s,esc', [
    ('\uD83D\uDC10',  '\\ud83d\\udc10'),
    ('\uD83D+\uDC10', '\\ud83d+\\udc10'),
    ('\uDC10\uD83D',  '\\udc10\\ud83d'),
])
@pytest.mark.parametrize('enc', [
    'us-ascii',
    'iso-8859-1',
    'utf-8',
    pytest.param(
        'utf-16be',
        marks=[
            # Certain versions of pypy3.6 (including the one on Travis as of
            # 2020-02-23) have a bug in their handling of encoding errors when
            # the target encoding is UTF-16.  The latest known version to
            # feature this bug is 7.1.1 (Python version 3.6.1), and the
            # earliest known version after this to feature a fix is 7.2.0
            # (Python version 3.6.9); I don't *think* there were any releases
            # in between those two versions, but it isn't entirely clear.
            pytest.mark.xfail(
                hasattr(sys, "pypy_version_info")
                    and sys.pypy_version_info[:3] < (7,2,0),
                reason='Broken on this version of PyPy',
            )
        ],
    ),
    'mac_roman',
    'cp500',
])
def test_javaproperties_bad_surrogates(s, enc, esc):
    assert s.encode(enc, 'javapropertiesreplace') == esc.encode(enc)
