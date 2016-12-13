from   click.testing           import CliRunner
from   javaproperties.__main__ import javaproperties

INPUT = b'''\
foo: bar
key = value
zebra apple
e\\u00f0=escaped
e\\\\u00f0=not escaped
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


# --encoding
# -d
# -D
# universal newlines?
# getting a key that appears multiple times in the file
# getting keys out of order
# reading from -
# non-ASCII output
