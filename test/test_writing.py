from __future__     import unicode_literals
from javaproperties import dumps

def test_dumps_nothing():
    assert dumps({}, timestamp=False) == ''

def test_dumps_simple():
    assert dumps({"key": "value"}, timestamp=False) == 'key=value\n'

def test_dumps_two_simple():
    assert dumps([("key", "value"), ("zebra", "apple")], timestamp=False) == \
        'key=value\nzebra=apple\n'

def test_dumps_two_simple_rev():
    assert dumps([("zebra", "apple"), ("key", "value")], timestamp=False) == \
        'zebra=apple\nkey=value\n'

def test_dumps_astral_plane():
    assert dumps({"goat": "\U0001F410"}, timestamp=False) == \
        'goat=\\ud83d\\udc10\n'


# characters outside the [\x20-\xFF] range
# backslashes
# '#' and '!'
# \n, \r, etc.
# spaces in keys
# spaces in values
# timestamps with & without a timezone
# comments
# `str`s in Python 2 (Separate test file?)
# custom separator?
