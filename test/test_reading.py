from javaproperties import loads

def test_loads_simple():
    assert loads('foo=bar') == {"foo": "bar"}

def test_loads_key_only():
    assert loads("foo") == {"foo": ""}

def test_loads_space_equals():
    assert loads("foo =bar") == {"foo": "bar"}

def test_loads_equals_space():
    assert loads("foo= bar") == {"foo": "bar"}

def test_loads_padded_equals():
    assert loads("foo = bar") == {"foo": "bar"}

def test_loads_nokey():
    assert loads("=bar") == {"": "bar"}

def test_loads_spacekey():
    assert loads(" =bar") == {"": "bar"}

def test_loads_trailing_space():
    assert loads("foo=bar ") == {"foo": "bar "}

def test_loads_leading_space():
    assert loads(" foo=bar") == {"foo": "bar"}

def test_loads_space_equals_space():
    assert loads(' = ') == {"": ""}
