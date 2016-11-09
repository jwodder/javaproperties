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
foo = bar 
test 
 baz = glarch \\
    quux \\
    # comment
xyzzy

plugh = plo\\
    ver \\
        \\
    stuff \\

    dwarf

  \\
   quux

xyzzy = \xC3\xA9

  \\
#: after hash
# = bar

a=b\\
'''

OUTPUT = b'''\
#Mon Nov 07 15:29:40 EST 2016
\\#=after hash
a=b
baz=glarch quux \\# comment
dwarf=
foo=bar 
plugh=plover stuff 
quux=
test=
xyzzy=\\u00c3\\u00a9
'''

@freeze_time('2016-11-07 20:29:40')
def test_cmd_format_stdin():
    r = CliRunner().invoke(javaproperties, ['format'], input=INPUT)
    assert r.exit_code == 0
    assert r.output_bytes == OUTPUT

@freeze_time('2016-11-07 20:29:40')
def test_cmd_format_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('test.properties', 'wb') as fp:
            fp.write(INPUT)
        r = CliRunner().invoke(javaproperties, ['format', 'test.properties'])
        assert r.exit_code == 0
        assert r.output_bytes == OUTPUT

# encoding
# separator
# --outfile
# reading from -
