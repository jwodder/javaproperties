from   click.testing           import CliRunner
from   javaproperties.__main__ import javaproperties

INPUT = b'''\
foo: bar
key = value
zebra apple
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


# --encoding
# --escaped
# -d
# -D
# universal newlines?
# getting a key that appears multiple times in the file
# getting keys out of order
# reading from -
