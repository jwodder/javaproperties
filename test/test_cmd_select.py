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


# --encoding
# --escaped
# --outfile
# --separator
# -d
# -D
# universal newlines?
# getting a key that appears multiple times in the file
# getting keys out of order
# reading from -
