from   click.testing           import CliRunner
from   javaproperties.__main__ import javaproperties

INPUT = b'''\
foo: bar
key = value
zebra apple
'''

def test_cmd_delete_exists():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '-', 'key'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'foo: bar\nzebra apple\n'

def test_cmd_delete_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '-', 'nonexistent'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == INPUT

def test_cmd_delete_some_exist():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '-', 'key', 'nonexistent'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'foo: bar\nzebra apple\n'


# --encoding
# --outfile
# --escaped
# --preserve-timestamp
# stripping extra trailing line continuations
# universal newlines?
# deleting a key that appears multiple times in the file
# deleting keys out of order
# reading from a file
