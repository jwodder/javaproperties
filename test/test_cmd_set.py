from   click.testing           import CliRunner
from   javaproperties.__main__ import javaproperties

INPUT = b'''\
foo: bar
key = value
zebra apple
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
nonexistent=mu
'''

# --encoding
# --separator
# --outfile
# --escaped
# --preserve-timestamp when there is a timestamp in input
# no --preserve-timestamp, with & without a timestamp in input
# stripping extra trailing line continuations
# universal newlines?
# setting a key that appears multiple times in the file
# reading from a file
# non-ASCII characters on command line
# non-ASCII output
