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
bad-surrogate = \\uDC10\\uD83D
'''

def test_cmd_set_exists():
    r = CliRunner().invoke(javaproperties, [
        'set', '--preserve-timestamp', '-', 'key', 'other value'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
foo: bar
key=other value
zebra apple
e\\u00f0=escaped
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
bad-surrogate = \\uDC10\\uD83D
'''

def test_cmd_set_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'set', '--preserve-timestamp', '-', 'nonexistent', 'mu'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
foo: bar
key = value
zebra apple
e\\u00f0=escaped
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
bad-surrogate = \\uDC10\\uD83D
nonexistent=mu
'''

def test_cmd_set_escaped_exists():
    r = CliRunner().invoke(javaproperties, [
        'set', '--preserve-timestamp', '--escaped', '-', 'e\\u00F0', '\\u00A1new!'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
foo: bar
key = value
zebra apple
e\\u00f0=\\u00a1new\\!
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
bad-surrogate = \\uDC10\\uD83D
'''

def test_cmd_set_escaped_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'set', '--preserve-timestamp', '--escaped', '-', 'x\\u00F0', '\\u00A1new!'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
foo: bar
key = value
zebra apple
e\\u00f0=escaped
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
bad-surrogate = \\uDC10\\uD83D
x\\u00f0=\\u00a1new\\!
'''

def test_cmd_set_not_escaped_exists():
    r = CliRunner().invoke(javaproperties, [
        'set', '--preserve-timestamp', '-', 'e\\u00f0', '\\u00A1new!'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
foo: bar
key = value
zebra apple
e\\u00f0=escaped
e\\\\u00f0=\\\\u00A1new\\!
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
bad-surrogate = \\uDC10\\uD83D
'''

def test_cmd_set_not_escaped_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'set', '--preserve-timestamp', '-', 'x\\u00F0', '\\u00A1new!'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
foo: bar
key = value
zebra apple
e\\u00f0=escaped
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
bad-surrogate = \\uDC10\\uD83D
x\\\\u00F0=\\\\u00A1new\\!
'''

def test_cmd_set_utf8_exists():
    r = CliRunner().invoke(javaproperties, [
        'set', '--preserve-timestamp', '-', b'e\xC3\xB0', b'\xC2\xA1new!'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
foo: bar
key = value
zebra apple
e\\u00f0=\\u00a1new\\!
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
bad-surrogate = \\uDC10\\uD83D
'''

def test_cmd_set_utf8_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'set', '--preserve-timestamp', '-', b'x\xC3\xB0', b'\xC2\xA1new!'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
foo: bar
key = value
zebra apple
e\\u00f0=escaped
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
bad-surrogate = \\uDC10\\uD83D
x\\u00f0=\\u00a1new\\!
'''

# --encoding
# --separator
# --outfile
# --preserve-timestamp when there is a timestamp in input
# no --preserve-timestamp, with & without a timestamp in input
# stripping extra trailing line continuations
# universal newlines?
# setting a key that appears multiple times in the file
# reading from a file
# key in source with a non-escaped Latin-1 character
# key with non-BMP character
# setting to a non-BMP character
# setting to a bad surrogate pair?
