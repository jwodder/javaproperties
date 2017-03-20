import time
from   click.testing           import CliRunner
from   freezegun               import freeze_time
import pytest
from   javaproperties.__main__ import javaproperties

@pytest.fixture(autouse=True)
def set_timezone(monkeypatch):
    monkeypatch.setenv('TZ', 'EST5EDT,M3.2.0/M11.1.0')
    time.tzset()

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

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_exists():
    r = CliRunner().invoke(javaproperties, ['select', '-', 'key'], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'#Mon Nov 07 15:29:40 EST 2016\nkey=value\n'

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'nonexistent'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
javaproperties: nonexistent: key not found
'''

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_some_exist():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'key', 'nonexistent'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
key=value
javaproperties: nonexistent: key not found
'''

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_escaped():
    r = CliRunner().invoke(javaproperties, [
        'select', '--escaped', '-', 'e\\u00F0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
e\\u00f0=escaped
'''

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_escaped_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'select', '--escaped', '-', 'x\\u00F0'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
javaproperties: x\xC3\xB0: key not found
'''

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_not_escaped():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'e\\u00f0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
e\\\\u00f0=not escaped
'''

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_not_escaped_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'x\\u00f0'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
javaproperties: x\\u00f0: key not found
'''

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_utf8():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', b'e\xC3\xB0'  # 'e\u00f0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
e\\u00f0=escaped
'''

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_utf8_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', b'x\xC3\xB0'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
javaproperties: x\xC3\xB0: key not found
'''

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_latin1_output():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'latin-1'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
latin-1=\\u00f0
'''

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_bmp_output():
    r = CliRunner().invoke(javaproperties, ['select', '-', 'bmp'], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
bmp=\\u2603
'''

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_astral_output():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'astral'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
astral=\\ud83d\\udc10
'''

@freeze_time('2016-11-07 20:29:40')
def test_cmd_select_bad_surrogate_output():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'bad-surrogate'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
bad-surrogate=\\udc10\\ud83d
'''

# --encoding
# --outfile
# --separator
# -d
# -D
# universal newlines?
# getting a key that appears multiple times in the file
# getting keys out of order
# reading from a file
# key in source with a non-escaped Latin-1 character
# key with non-BMP character
