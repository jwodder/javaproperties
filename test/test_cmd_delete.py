from   click.testing           import CliRunner
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
'''

def test_cmd_delete_exists():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '-', 'key'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
foo: bar
zebra apple
e\\u00f0=escaped
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
'''

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
    assert r.output_bytes == b'''\
foo: bar
zebra apple
e\\u00f0=escaped
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
'''

def test_cmd_delete_del_bad_surrogate():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '-', 'bad-surrogate'
    ], input=b'good-surrogate = \\uD83D\\uDC10\n'
             b'bad-surrogate = \\uDC10\\uD83D\n')
    assert r.exit_code == 0
    assert r.output_bytes == b'good-surrogate = \\uD83D\\uDC10\n'

def test_cmd_delete_keep_bad_surrogate():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '-', 'good-surrogate'
    ], input=b'good-surrogate = \\uD83D\\uDC10\n'
             b'bad-surrogate = \\uDC10\\uD83D\n')
    assert r.exit_code == 0
    assert r.output_bytes == b'bad-surrogate = \\uDC10\\uD83D\n'

def test_cmd_delete_escaped():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '--escaped', '-', 'e\\u00F0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
foo: bar
key = value
zebra apple
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
'''

def test_cmd_delete_escaped_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '--escaped', '-', 'x\\u00F0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == INPUT

def test_cmd_delete_not_escaped():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '-', 'e\\u00f0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
foo: bar
key = value
zebra apple
e\\u00f0=escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
'''

def test_cmd_delete_not_escaped_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '-', 'x\\u00f0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == INPUT

def test_cmd_delete_utf8():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '-', b'e\xC3\xB0'  # 'e\u00f0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
foo: bar
key = value
zebra apple
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
'''

def test_cmd_delete_utf8_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '-', b'x\xC3\xB0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == INPUT

# --encoding
# --outfile
# --preserve-timestamp when there is a timestamp in input
# no --preserve-timestamp, with & without a timestamp in input
# stripping extra trailing line continuations
# universal newlines?
# deleting a key that appears multiple times in the file
# deleting keys out of order
# reading from a file
# key in source with a non-escaped Latin-1 character
# key with non-BMP character
