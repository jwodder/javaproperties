# -*- coding: utf-8 -*-
from   __future__ import print_function, unicode_literals
from   datetime   import datetime
import numbers
import re
import time
from   six        import StringIO
from   .util      import itemize

def dump(props, fp, separator='=', comments=None, timestamp=True,
         sort_keys=False):
    """
    Write a series of key-value pairs to a file in ``.properties`` format.

    :param props: A mapping or iterable of ``(key, value)`` pairs to write to
        ``fp``.  All keys and values in ``props`` must be text strings.
    :param fp: A file-like object to write the values of ``props`` to.  It must
        have been opened as a text file with a Latin-1-compatible encoding.
    :param separator: the string to use for separating keys & values.  Only
        ``" "``, ``"="``, and ``":"`` (possibly with added whitespace) should
        ever be used as the separator.
    :type separator: text string
    :param comments: if non-`None`, ``comments`` will be written to ``fp`` as a
        comment before any other content
    :type comments: text string or `None`
    :param timestamp: If neither `None` nor `False`, a timestamp in the form of
        ``Mon Sep 12 14:00:54 EDT 2016`` is written as a comment to ``fp``
        after ``comments`` (if any) and before the key-value pairs.  If
        ``timestamp`` is `True`, the current date & time is used.  If it is a
        number, it is converted from seconds since the epoch to local time.  If
        it is a `datetime.datetime` object, its value is used directly, with
        naïve objects assumed to be in the local timezone.
    :type timestamp: `None`, `bool`, number, or `datetime.datetime`
    :param bool sort_keys: if true, the elements of ``props`` are sorted
        lexicographically by key in the output
    :return: `None`
    """
    if comments is not None:
        print(to_comment(comments), file=fp)
    if timestamp is not None and timestamp is not False:
        print(to_comment(_show_timestamp(timestamp)), file=fp)
    for k,v in itemize(props, sort_keys=sort_keys):
        print(join_key_value(k, v, separator), file=fp)

def dumps(props, separator='=', comments=None, timestamp=True, sort_keys=False):
    """
    Convert a series of key-value pairs to a text string in ``.properties``
    format.

    :param props: A mapping or iterable of ``(key, value)`` pairs to serialize.
        All keys and values in ``props`` must be text strings.
    :param separator: the string to use for separating keys & values.  Only
        ``" "``, ``"="``, and ``":"`` (possibly with added whitespace) should
        ever be used as the separator.
    :type separator: text string
    :param comments: if non-`None`, ``comments`` will be output as a comment
        before any other content
    :type comments: text string or `None`
    :param timestamp: If neither `None` nor `False`, a timestamp in the form of
        ``Mon Sep 12 14:00:54 EDT 2016`` is output as a comment after
        ``comments`` (if any) and before the key-value pairs.  If ``timestamp``
        is `True`, the current date & time is used.  If it is a number, it is
        converted from seconds since the epoch to local time.  If it is a
        `datetime.datetime` object, its value is used directly, with naïve
        objects assumed to be in the local timezone.
    :type timestamp: `None`, `bool`, number, or `datetime.datetime`
    :param bool sort_keys: if true, the elements of ``props`` are sorted
        lexicographically by key in the output
    :rtype: text string
    """
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
    ``.properties`` file.  No trailing newline is added.

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

TIMESTAMP_FMT = '%a %b %d %H:%M:%S %Z %Y'

def _show_timestamp(timestamp):
    ### TODO: Make strftime use the C locale
    ### Make this public?
    # All uses of `time.strftime` assume that `time.tzname` is
    # meaningful/useful.
    if timestamp is True:
        return time.strftime(TIMESTAMP_FMT)
    elif isinstance(timestamp, numbers.Number):
        return time.strftime(TIMESTAMP_FMT, time.localtime(timestamp))
    elif isinstance(timestamp, datetime):
        if timestamp.tzinfo is None:
            # Mapping `timetuple` through `mktime` and `localtime` is necessary
            # for determining whether DST is in effect (which, in turn, is
            # necessary for determining which timezone name to use).  The only
            # downside to using standard functions instead of `python-dateutil`
            # is that `mktime`, apparently, handles times duplicated by DST
            # non-deterministically (cf. <https://git.io/vixsE>), but there's
            # no right way to deal with those anyway, so...
            return time.strftime(
                TIMESTAMP_FMT,
                time.localtime(time.mktime(timestamp.timetuple())),
            )
        else:
            # Assumes `timestamp.tzinfo.tzname()` is meaningful/useful
            return timestamp.strftime(TIMESTAMP_FMT)
    else:
        raise TypeError('Timestamp must be number or datetime.datetime object')
