import sys
from   click.testing           import CliRunner
import pytest
from   javaproperties.__main__ import javaproperties

INPUT = b'''\
foo: bar
key = value
zebra apple
e\\u00f0=escaped
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
bad-surrogate = \\uDC10\\uD83D
'''

def test_cmd_get_exists():
    r = CliRunner().invoke(javaproperties, ['get', '-', 'key'], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'value\n'

def test_cmd_get_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'get', '-', 'nonexistent'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.output_bytes == b'javaproperties: nonexistent: key not found\n'

def test_cmd_get_some_exist():
    r = CliRunner().invoke(javaproperties, [
        'get', '-', 'key', 'nonexistent'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.output_bytes == b'value\njavaproperties: nonexistent: key not found\n'

def test_cmd_get_escaped():
    r = CliRunner().invoke(javaproperties, [
        'get', '--escaped', '-', 'e\\u00F0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'escaped\n'

def test_cmd_get_escaped_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'get', '--escaped', '-', 'x\\u00F0'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.output_bytes == b'javaproperties: x\xC3\xB0: key not found\n'

def test_cmd_get_not_escaped():
    r = CliRunner().invoke(javaproperties, [
        'get', '-', 'e\\u00f0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'not escaped\n'

def test_cmd_get_not_escaped_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'get', '-', 'x\\u00f0'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.output_bytes == b'javaproperties: x\\u00f0: key not found\n'

def test_cmd_get_utf8():
    r = CliRunner().invoke(javaproperties, [
        'get', '-', b'e\xC3\xB0'  # 'e\u00f0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'escaped\n'

def test_cmd_get_utf8_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'get', '-', b'x\xC3\xB0'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.output_bytes == b'javaproperties: x\xC3\xB0: key not found\n'

def test_cmd_get_latin1_output():
    r = CliRunner().invoke(javaproperties, ['get', '-', 'latin-1'], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'\xC3\xB0\n'

def test_cmd_get_bmp_output():
    r = CliRunner().invoke(javaproperties, ['get', '-', 'bmp'], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'\xE2\x98\x83\n'

def test_cmd_get_astral_output():
    r = CliRunner().invoke(javaproperties, ['get', '-', 'astral'], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'\xF0\x9F\x90\x90\n'

@pytest.mark.skipif(sys.version_info[0] > 2, reason='Python 2 only')
def test_cmd_get_bad_surrogate_output_py2():
    r = CliRunner().invoke(javaproperties, [
        'get', '-', 'bad-surrogate'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'\xED\xB0\x90\xED\xA0\xBD\n'

@pytest.mark.xfail(reason='https://github.com/pallets/click/issues/705')
@pytest.mark.skipif(sys.version_info[0] < 3, reason='Python 3 only')
def test_cmd_get_bad_surrogate_output_py3():
    r = CliRunner().invoke(javaproperties, [
        'get', '-', 'bad-surrogate'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'??\n'


# --encoding
# -d
# -D
# universal newlines?
# getting a key that appears multiple times in the file
# getting keys out of order
# reading from a file
# key in source with a non-escaped Latin-1 character
# key with non-BMP character
