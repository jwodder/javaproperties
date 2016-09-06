from   __future__ import print_function, unicode_literals
from   datetime   import datetime
import re
from   six        import StringIO
from   .util      import itemize

def dump(props, fp, separator='=', comments=None, timestamp=True,
         sort_keys=False):
    # `fp` must have been opened as a text file with a Latin-1-compatible
    # encoding.
    if comments is not None:
        print(to_comment(comments), file=fp)
    if timestamp:
        if not isinstance(timestamp, datetime):
            try:
                from dateutil.tz import tzlocal
            except ImportError:
                tz = None
            else:
                tz = tzlocal()
            timestamp = datetime.now(tz)
        ### TODO: Make strftime use the C locale
        print(to_comment(timestamp.strftime('%a %b %d %H:%M:%S %Z %Y')
                                  .replace('  ', ' ')), file=fp)
    for k,v in itemize(props, sort_keys=sort_keys):
        print(join_key_value(k, v, separator), file=fp)

def dumps(props, separator='=', comments=None, timestamp=True, sort_keys=False):
    s = StringIO()
    dump(props, s, separator=separator, comments=comments, timestamp=timestamp,
         sort_keys=sort_keys)
    return s.getvalue()

def to_comment(comment):
    return '#' + re.sub(r'[^\x00-\xFF]', _esc,
                        re.sub(r'(\r\n?|\n)(?![#!])', r'\1#', comment))

def join_key_value(key, value, separator='='):
    # Escapes `key` and `value` the same way as java.util.Properties.store()
    return escape(key) \
        + separator \
        + re.sub(r'^ +', lambda m: r'\ ' * m.end(), _base_escape(value))

_escapes = {
    '\t': r'\t',
    '\n': r'\n',
    '\f': r'\f',
    '\r': r'\r',
    '!': r'\!',
    '#': r'\#',
    ':': r'\:',
    '=': r'\=',
    '\\': r'\\',
}

def _esc(m):
    c = m.group()
    try:
        return _escapes[c]
    except KeyError:
        c = ord(c)
        if c > 0xFFFF:
            # Does Python really not have a decent builtin way to calculate
            # surrogate pairs?
            assert c <= 0x10FFFF
            c -= 0x10000
            return '\\u{0:04x}\\u{1:04x}'.format(
                0xD800 + (c >> 10),
                0xDC00 + (c & 0x3FF)
            )
        else:
            return '\\u{0:04x}'.format(c)

def _base_escape(field):
    return re.sub(r'[^\x20-\x7E]|[\\#!=:]', _esc, field)

def escape(field):
    # Escapes `field` so that it can be used as either a key or a value
    return _base_escape(field).replace(' ', r'\ ')
