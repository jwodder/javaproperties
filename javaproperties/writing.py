# -*- coding: utf-8 -*-
from   __future__ import print_function, unicode_literals
from   datetime   import datetime
import numbers
import re
import time
from   six        import StringIO
from   .util      import itemize

def dump(props, fp, separator='=', comments=None, timestamp=True,
         sort_keys=False, ensure_ascii=True, ensure_ascii_comments=None):
    """
    Write a series of key-value pairs to a file in simple line-oriented
    ``.properties`` format.

    .. versionchanged:: 0.6.0
        ``ensure_ascii`` and ``ensure_ascii_comments`` parameters added

    :param props: A mapping or iterable of ``(key, value)`` pairs to write to
        ``fp``.  All keys and values in ``props`` must be text strings.  If
        ``sort_keys`` is `False`, the entries are output in iteration order.
    :param fp: A file-like object to write the values of ``props`` to.  It must
        have been opened as a text file.
    :param separator: The string to use for separating keys & values.  Only
        ``" "``, ``"="``, and ``":"`` (possibly with added whitespace) should
        ever be used as the separator.
    :type separator: text string
    :param comments: if non-`None`, ``comments`` will be written to ``fp`` as a
        comment before any other content
    :type comments: text string or `None`
    :param timestamp: If neither `None` nor `False`, a timestamp in the form of
        ``Mon Sep 02 14:00:54 EDT 2016`` is written as a comment to ``fp``
        after ``comments`` (if any) and before the key-value pairs.  If
        ``timestamp`` is `True`, the current date & time is used.  If it is a
        number, it is converted from seconds since the epoch to local time.  If
        it is a `datetime.datetime` object, its value is used directly, with
        naïve objects assumed to be in the local timezone.
    :type timestamp: `None`, `bool`, number, or `datetime.datetime`
    :param bool sort_keys: if true, the elements of ``props`` are sorted
        lexicographically by key in the output
    :param bool ensure_ascii: if true, all non-ASCII characters will be
        replaced with ``\\uXXXX`` escape sequences in the output; if false,
        non-ASCII characters will be passed through as-is
    :param ensure_ascii_comments: if true, all non-ASCII characters in
        ``comments`` will be replaced with ``\\uXXXX`` escape sequences in the
        output; if `None`, only non-Latin-1 characters will be escaped; if
        false, no characters will be escaped
    :return: `None`
    """
    if comments is not None:
        print(to_comment(comments, ensure_ascii=ensure_ascii_comments), file=fp)
    if timestamp is not None and timestamp is not False:
        print(to_comment(java_timestamp(timestamp)), file=fp)
    for k,v in itemize(props, sort_keys=sort_keys):
        print(
            join_key_value(k, v, separator, ensure_ascii=ensure_ascii),
            file=fp,
        )

def dumps(props, separator='=', comments=None, timestamp=True, sort_keys=False,
          ensure_ascii=True, ensure_ascii_comments=None):
    """
    Convert a series of key-value pairs to a text string in simple
    line-oriented ``.properties`` format.

    .. versionchanged:: 0.6.0
        ``ensure_ascii`` and ``ensure_ascii_comments`` parameters added

    :param props: A mapping or iterable of ``(key, value)`` pairs to serialize.
        All keys and values in ``props`` must be text strings.  If
        ``sort_keys`` is `False`, the entries are output in iteration order.
    :param separator: The string to use for separating keys & values.  Only
        ``" "``, ``"="``, and ``":"`` (possibly with added whitespace) should
        ever be used as the separator.
    :type separator: text string
    :param comments: if non-`None`, ``comments`` will be output as a comment
        before any other content
    :type comments: text string or `None`
    :param timestamp: If neither `None` nor `False`, a timestamp in the form of
        ``Mon Sep 02 14:00:54 EDT 2016`` is output as a comment after
        ``comments`` (if any) and before the key-value pairs.  If ``timestamp``
        is `True`, the current date & time is used.  If it is a number, it is
        converted from seconds since the epoch to local time.  If it is a
        `datetime.datetime` object, its value is used directly, with naïve
        objects assumed to be in the local timezone.
    :type timestamp: `None`, `bool`, number, or `datetime.datetime`
    :param bool sort_keys: if true, the elements of ``props`` are sorted
        lexicographically by key in the output
    :param bool ensure_ascii: if true, all non-ASCII characters will be
        replaced with ``\\uXXXX`` escape sequences in the output; if false,
        non-ASCII characters will be passed through as-is
    :param ensure_ascii_comments: if true, all non-ASCII characters in
        ``comments`` will be replaced with ``\\uXXXX`` escape sequences in the
        output; if `None`, only non-Latin-1 characters will be escaped; if
        false, no characters will be escaped
    :rtype: text string
    """
    s = StringIO()
    dump(props, s, separator=separator, comments=comments, timestamp=timestamp,
         sort_keys=sort_keys, ensure_ascii=ensure_ascii,
         ensure_ascii_comments=ensure_ascii_comments)
    return s.getvalue()

NON_ASCII_RGX = re.compile(r'[^\x00-\x7F]')
NON_LATIN1_RGX = re.compile(r'[^\x00-\xFF]')
NEWLINE_OLD_COMMENT_RGX = re.compile(r'\n(?![#!])')
NON_N_EOL_RGX = re.compile(r'\r\n?')

def to_comment(comment, ensure_ascii=None):
    """
    Convert a string to a ``.properties`` file comment.  Non-Latin-1 or
    non-ASCII characters in the string may be escaped using ``\\uXXXX`` escapes
    (depending on the value of ``ensure_ascii``), a ``#`` is prepended to the
    string, any CR LF or CR line breaks in the string are converted to LF, and
    a ``#`` is inserted after any line break not already followed by a ``#`` or
    ``!``.  No trailing newline is added.

    >>> to_comment('They say foo=bar,\\r\\nbut does bar=foo?')
    '#They say foo=bar,\\n#but does bar=foo?'

    .. versionchanged:: 0.6.0
        ``ensure_ascii`` parameter added

    :param comment: the string to convert to a comment
    :type comment: text string
    :param ensure_ascii: if true, all non-ASCII characters will be replaced
        with ``\\uXXXX`` escape sequences in the output; if `None`, only
        non-Latin-1 characters will be escaped; if false, no characters will be
        escaped
    :rtype: text string
    """
    comment = NON_N_EOL_RGX.sub('\n', comment)
    comment = NEWLINE_OLD_COMMENT_RGX.sub('\n#', comment)
    if ensure_ascii is None:
        comment = NON_LATIN1_RGX.sub(_esc, comment)
    elif ensure_ascii:
        comment = NON_ASCII_RGX.sub(_esc, comment)
    return '#' + comment

def join_key_value(key, value, separator='=', ensure_ascii=True):
    r"""
    Join a key and value together into a single line suitable for adding to a
    simple line-oriented ``.properties`` file.  No trailing newline is added.

    >>> join_key_value('possible separators', '= : space')
    'possible\\ separators=\\= \\: space'

    .. versionchanged:: 0.6.0
        ``ensure_ascii`` parameter added

    :param key: the key
    :type key: text string
    :param value: the value
    :type value: text string
    :param separator: the string to use for separating the key & value.  Only
        ``" "``, ``"="``, and ``":"`` (possibly with added whitespace) should
        ever be used as the separator.
    :type separator: text string
    :param bool ensure_ascii: if true, all non-ASCII characters will be
        replaced with ``\\uXXXX`` escape sequences in the output; if false,
        non-ASCII characters will be passed through as-is
    :rtype: text string
    """
    # Escapes `key` and `value` the same way as java.util.Properties.store()
    value = _base_escape(value, ensure_ascii=ensure_ascii)
    if value.startswith(' '):
        value = '\\' + value
    return escape(key, ensure_ascii=ensure_ascii) + separator + value

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
        return _to_u_escape(c)

def _to_u_escape(c):
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

NEEDS_ESCAPE_ASCII_RGX = re.compile(r'[^\x20-\x7E]|[\\#!=:]')
NEEDS_ESCAPE_UNICODE_RGX = re.compile(r'[\x00-\x1F\x7F]|[\\#!=:]')

def _base_escape(field, ensure_ascii=True):
    rgx = NEEDS_ESCAPE_ASCII_RGX if ensure_ascii else NEEDS_ESCAPE_UNICODE_RGX
    return rgx.sub(_esc, field)

def escape(field, ensure_ascii=True):
    """
    Escape a string so that it can be safely used as either a key or value in a
    ``.properties`` file.  All non-ASCII characters, all nonprintable or space
    characters, and the characters ``\\ # ! = :`` are all escaped using either
    the single-character escapes recognized by `unescape` (when they exist) or
    ``\\uXXXX`` escapes (after converting non-BMP characters to surrogate
    pairs).

    .. versionchanged:: 0.6.0
        ``ensure_ascii`` parameter added

    :param field: the string to escape
    :type field: text string
    :param bool ensure_ascii: if true, all non-ASCII characters will be
        replaced with ``\\uXXXX`` escape sequences in the output; if false,
        non-ASCII characters will be passed through as-is
    :rtype: text string
    """
    return _base_escape(field, ensure_ascii=ensure_ascii).replace(' ', r'\ ')

DAYS_OF_WEEK = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

MONTHS = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
]

def java_timestamp(timestamp=True):
    """
    .. versionadded:: 0.2.0

    Returns a timestamp in the format produced by |date_tostring|_, e.g.::

        Mon Sep 02 14:00:54 EDT 2016

    If ``timestamp`` is `True` (the default), the current date & time is
    returned.

    If ``timestamp`` is `None` or `False`, an empty string is returned.

    If ``timestamp`` is a number, it is converted from seconds since the epoch
    to local time.

    If ``timestamp`` is a `datetime.datetime` object, its value is used
    directly, with naïve objects assumed to be in the local timezone.

    The timestamp is always constructed using the C locale.

    :param timestamp: the date & time to display
    :type timestamp: `None`, `bool`, number, or `datetime.datetime`
    :rtype: text string

    .. |date_tostring| replace:: Java 8's ``Date.toString()``
    .. _date_tostring: https://docs.oracle.com/javase/8/docs/api/java/util/Date.html#toString--
    """
    if timestamp is None or timestamp is False:
        return ''
    if isinstance(timestamp, datetime) and timestamp.tzinfo is not None:
        timebits = timestamp.timetuple()
        # Assumes `timestamp.tzinfo.tzname()` is meaningful/useful
        tzname = timestamp.tzname()
    else:
        if timestamp is True:
            timestamp = None
        elif isinstance(timestamp, datetime):
            try:
                # Use `datetime.timestamp()` if it's available, as it (unlike
                # `datetime.timetuple()`) takes `fold` into account for naïve
                # datetimes
                timestamp = timestamp.timestamp()
            except AttributeError:  # Pre-Python 3.3
                # Mapping `timetuple` through `mktime` and `localtime` is
                # necessary for determining whether DST is in effect (which, in
                # turn, is necessary for determining which timezone name to
                # use).  The only downside to using standard functions instead
                # of `python-dateutil` is that `mktime`, apparently, handles
                # times duplicated by DST non-deterministically (cf.
                # <https://git.io/vixsE>), but there's no right way to deal
                # with those anyway, so...
                timestamp = time.mktime(timestamp.timetuple())
        elif not isinstance(timestamp, numbers.Number):
            raise TypeError('Timestamp must be number or datetime.datetime')
        timebits = time.localtime(timestamp)
        try:
            tzname = timebits.tm_zone
        except AttributeError:
            # This assumes that `time.tzname` is meaningful/useful.
            tzname = time.tzname[timebits.tm_isdst > 0]
    assert 1 <= timebits.tm_mon <= 12, 'invalid month'
    assert 0 <= timebits.tm_wday <= 6, 'invalid day of week'
    return '{wday} {mon} {t.tm_mday:02d}' \
           ' {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}' \
           ' {tz} {t.tm_year:04d}'.format(
                t=timebits,
                tz=tzname,
                mon=MONTHS[timebits.tm_mon-1],
                wday=DAYS_OF_WEEK[timebits.tm_wday]
            )

def javapropertiesreplace_errors(e):
    if isinstance(e, UnicodeEncodeError):
        return (''.join(map(_to_u_escape, e.object[e.start:e.end])), e.end)
    else:
        raise e
