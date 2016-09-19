from   __future__ import print_function, unicode_literals
from   datetime   import datetime
import re
from   six        import StringIO
from   .util      import itemize

def dump(props, fp, separator='=', comments=None, timestamp=True,
         sort_keys=False):
    """ TODO """
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
    """ TODO """
    s = StringIO()
    dump(props, s, separator=separator, comments=comments, timestamp=timestamp,
         sort_keys=sort_keys)
    return s.getvalue()

def to_comment(comment):
    """
    Convert a string to a ``.properties`` file comment.  All non-Latin-1
    characters in the string are escaped using ``\\uXXXX`` escapes (after
    converting non-BMP characters to surrogate pairs), a ``#`` is prepended to
    the string, and a ``#`` is inserted after any line breaks in the string not
    already followed by a ``#`` or ``!``.

    :param comment: the string to convert to a comment
    :type comment: text string
    :rtype: text string
    """
    return '#' + re.sub(r'[^\x00-\xFF]', _esc,
                        re.sub(r'(\r\n?|\n)(?![#!])', r'\1#', comment))

def join_key_value(key, value, separator='='):
    """
    Join a key and value together into a single line suitable for adding to a
    ``.properties`` file.

    :param key: the key
    :type key: text string
    :param value: the value
    :type value: text string
    :param separator: the string to use for separating the key & value.  Only
        ``" "``, ``"="``, and ``":"`` (possibly with added whitespace) should
        ever be used as the separator.
    :type separator: text string
    :rtype: text string
    """
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
    """
    Escape a string so that it can be safely used as either a key or value in a
    ``.properties`` file.  All non-ASCII characters, all nonprintable or space
    characters, and the characters ``\\ # ! = :`` are all escaped using either
    ``\\uXXXX`` escapes (after converting non-BMP characters to surrogate
    pairs) or the single-character escapes recognized by `unescape`.

    :param field: the string to escape
    :type field: text string
    :rtype: text string
    """
    return _base_escape(field).replace(' ', r'\ ')
