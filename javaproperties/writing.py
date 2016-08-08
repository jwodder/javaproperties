from   __future__  import unicode_literals
from   collections import Mapping
import re

def write_properties(props, fp, separator='='):
    ### Add arguments for comment and/or timestamp
    if isinstance(props, Mapping):
        items = (k, props[k] for k in props)
    else:
        items = props
    for k,v in items:
        fp.write(join_key_value(k, v, separator) + '\n')

def join_key_value(key, value, separator='='):
    # Escapes `key` and `value` the same way as java.util.Properties.store()
    return escape(key) \
        + separator \
        + re.sub(r'^ +', lambda m: r'\ ' * m.end(), _base_escape(value))

_escapes = {
    0x09: r'\t',
    0x0A: r'\n',
    0x0C: r'\f',
    0x0D: r'\r',
    0x21: r'\!',
    0x23: r'\#',
    0x3A: r'\:',
    0x3D: r'\=',
    0x5C: r'\\',
}

def _esc(m):
    c = ord(m.group(1))
    try:
        return _escapes[c]
    except KeyError:
        if c > 0xFFFF:
            # Does Python really not have a decent builtin way to calculate
            # surrogate pairs?
            assert c <= 0x10FFFF
            c -= 0x10000
            return r'\u{:04x}\u{:04x}'.format(
                0xD800 + (c >> 10),
                0xDC00 + (c & 0x3FF)
            )
        else:
            return r'\u{:04x}'.format(c)

def _base_escape(field):
    return re.sub(r'([^\x20-\x7E]|[\\#!=:])', _esc, field)

def escape(field):
    # Escapes `field` so that it can be used as either a key or a value
    return _base_escape(field).replace(' ', r'\ ')

### Write a variant of `join_key_value` that escapes as few (ASCII) characters as possible?

### Something for writing triples???
