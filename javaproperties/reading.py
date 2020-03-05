from   __future__  import unicode_literals
from   collections import namedtuple
import re
from   struct      import pack
from   six         import binary_type, StringIO, BytesIO, text_type, unichr
from   .util       import CONTINUED_RGX, ascii_splitlines

def load(fp, object_pairs_hook=dict):
    """
    Parse the contents of the `~io.IOBase.readline`-supporting file-like object
    ``fp`` as a simple line-oriented ``.properties`` file and return a `dict`
    of the key-value pairs.

    ``fp`` may be either a text or binary filehandle, with or without universal
    newlines enabled.  If it is a binary filehandle, its contents are decoded
    as Latin-1.

    By default, the key-value pairs extracted from ``fp`` are combined into a
    `dict` with later occurrences of a key overriding previous occurrences of
    the same key.  To change this behavior, pass a callable as the
    ``object_pairs_hook`` argument; it will be called with one argument, a
    generator of ``(key, value)`` pairs representing the key-value entries in
    ``fp`` (including duplicates) in order of occurrence.  `load` will then
    return the value returned by ``object_pairs_hook``.

    .. versionchanged:: 0.5.0
        Invalid ``\\uXXXX`` escape sequences will now cause an
        `InvalidUEscapeError` to be raised

    :param fp: the file from which to read the ``.properties`` document
    :type fp: file-like object
    :param callable object_pairs_hook: class or function for combining the
        key-value pairs
    :rtype: `dict` of text strings or the return value of ``object_pairs_hook``
    :raises InvalidUEscapeError: if an invalid ``\\uXXXX`` escape sequence
        occurs in the input
    """
    return object_pairs_hook(
        (kv.key, kv.value) for kv in parse(fp) if isinstance(kv, KeyValue)
    )

def loads(s, object_pairs_hook=dict):
    """
    Parse the contents of the string ``s`` as a simple line-oriented
    ``.properties`` file and return a `dict` of the key-value pairs.

    ``s`` may be either a text string or bytes string.  If it is a bytes
    string, its contents are decoded as Latin-1.

    By default, the key-value pairs extracted from ``s`` are combined into a
    `dict` with later occurrences of a key overriding previous occurrences of
    the same key.  To change this behavior, pass a callable as the
    ``object_pairs_hook`` argument; it will be called with one argument, a
    generator of ``(key, value)`` pairs representing the key-value entries in
    ``s`` (including duplicates) in order of occurrence.  `loads` will then
    return the value returned by ``object_pairs_hook``.

    .. versionchanged:: 0.5.0
        Invalid ``\\uXXXX`` escape sequences will now cause an
        `InvalidUEscapeError` to be raised

    :param string s: the string from which to read the ``.properties`` document
    :param callable object_pairs_hook: class or function for combining the
        key-value pairs
    :rtype: `dict` of text strings or the return value of ``object_pairs_hook``
    :raises InvalidUEscapeError: if an invalid ``\\uXXXX`` escape sequence
        occurs in the input
    """
    fp = BytesIO(s) if isinstance(s, binary_type) else StringIO(s)
    return load(fp, object_pairs_hook=object_pairs_hook)

TIMESTAMP_RGX = re.compile(
    r'\A[ \t\f]*[#!][ \t\f]*'
    r'(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)'
    r' (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
    r' (?:[012][0-9]|3[01])'
    r' (?:[01][0-9]|2[0-3]):[0-5][0-9]:(?:[0-5][0-9]|6[01])'
    r' (?:[A-Za-z_0-9]{3})?'
    r' [0-9]{4,}'
    r'[ \t\f]*\r?\n?\Z'
)

class PropertiesElement(object):
    """
    .. versionadded:: 0.7.0

    Superclass of objects returned by `parse()`
    """
    __slots__ = ()


class Comment(PropertiesElement, namedtuple('Comment', 'source')):
    """
    .. versionadded:: 0.7.0

    Subclass of `PropertiesElement` representing a comment

    .. attribute:: source

        The raw, unmodified input line (including trailing newlines)
    """

    __slots__ = ()

    @property
    def value(self):
        """
        Returns the contents of the comment, with the comment marker, any
        whitespace leading up to it, and the trailing newline removed
        """
        s = self.source.lstrip(' \t\f')
        if s.startswith(('#', '!')):
            s = s[1:]
        return s.rstrip('\r\n')

    @property
    def source_stripped(self):
        """
        Like `source`, but with the final trailing newline (if any) removed
        """
        return self.source.rstrip('\r\n')

    def is_timestamp(self):
        """
        Returns `True` iff the comment's value appears to be a valid timestamp
        as produced by Java 8's ``Date.toString()``
        """
        return bool(TIMESTAMP_RGX.match(self.source))


class Whitespace(PropertiesElement, namedtuple('Whitespace', 'source')):
    """
    .. versionadded:: 0.7.0

    Subclass of `PropertiesElement` representing a line that is either empty or
    contains only whitespace (and possibly some line continuations)

    .. attribute:: source

        The raw, unmodified input line (including trailing newlines)
    """

    __slots__ = ()

    @property
    def source_stripped(self):
        """
        Like `source`, but with the final trailing newline and line
        continuation (if any) removed
        """
        s = self.source.rstrip('\r\n')
        if CONTINUED_RGX.search(s):
            s = s[:-1]
        return s


class KeyValue(PropertiesElement, namedtuple('KeyValue', 'key value source')):
    """
    .. versionadded:: 0.7.0

    Subclass of `PropertiesElement` representing a key-value entry

    .. attribute:: key

        The entry's key, after processing escape sequences

    .. attribute:: value

        The entry's value, after processing escape sequences

    .. attribute:: source

        The concatenation of the raw, unmodified lines in the input (including
        trailing newlines) from which the key and value were extracted
    """

    __slots__ = ()

    @property
    def source_stripped(self):
        """
        Like `source`, but with the final trailing newline and line
        continuation (if any) removed
        """
        s = self.source.rstrip('\r\n')
        if CONTINUED_RGX.search(s):
            s = s[:-1]
        return s


COMMENT_RGX = re.compile(r'^[ \t\f]*[#!]')
BLANK_RGX = re.compile(r'^[ \t\f]*\r?\n?\Z')
SEPARATOR_RGX = re.compile(r'(?<!\\)(?:\\\\)*([ \t\f]*[=:]|[ \t\f])[ \t\f]*')

def parse(src):
    """
    Parse the given data as a simple line-oriented ``.properties`` file and
    return a generator of `PropertiesElement` objects representing the
    key-value pairs (as `KeyValue` objects), comments (as `Comment` objects),
    and blank lines (as `Whitespace` objects) in the input in order of
    occurrence.

    If the same key appears multiple times in the input, a separate `KeyValue`
    object is emitted for each entry.

    ``src`` may be a text string, a bytes string, or a text or binary
    filehandle/file-like object supporting the `~io.IOBase.readline` method
    (with or without universal newlines enabled).  Bytes input is decoded as
    Latin-1.


    .. versionchanged:: 0.5.0
        Invalid ``\\uXXXX`` escape sequences will now cause an
        `InvalidUEscapeError` to be raised

    .. versionchanged:: 0.7.0
        `parse()` now accepts strings as input, and it now returns a generator
        of custom objects instead of triples of strings

    :param src: the ``.properties`` document
    :type src: string or file-like object
    :rtype: Iterable[PropertiesElement]
    :raises InvalidUEscapeError: if an invalid ``\\uXXXX`` escape sequence
        occurs in the input
    """
    if isinstance(src, binary_type):
        liter = iter(ascii_splitlines(src.decode('iso-8859-1')))
    elif isinstance(src, text_type):
        liter = iter(ascii_splitlines(src))
    else:
        def lineiter():
            while True:
                ln = src.readline()
                if isinstance(ln, binary_type):
                    ln = ln.decode('iso-8859-1')
                if ln == '':
                    return
                for l in ascii_splitlines(ln):
                    yield l
        liter = lineiter()
    for source in liter:
        line = source
        if COMMENT_RGX.match(line):
            yield Comment(source)
            continue
        elif BLANK_RGX.match(line):
            yield Whitespace(source)
            continue
        line = line.lstrip(' \t\f').rstrip('\r\n')
        while CONTINUED_RGX.search(line):
            line = line[:-1]
            nextline = next(liter, '')
            source += nextline
            line += nextline.lstrip(' \t\f').rstrip('\r\n')
        if line == '':  # series of otherwise-blank lines with continuations
            yield Whitespace(source)
            continue
        m = SEPARATOR_RGX.search(line)
        if m:
            yield KeyValue(
                unescape(line[:m.start(1)]),
                unescape(line[m.end():]),
                source,
            )
        else:
            yield KeyValue(unescape(line), '', source)

SURROGATE_PAIR_RGX = re.compile(r'[\uD800-\uDBFF][\uDC00-\uDFFF]')
ESCAPE_RGX = re.compile(r'\\(u.{0,4}|.)')
U_ESCAPE_RGX = re.compile(r'^u[0-9A-Fa-f]{4}\Z')

def unescape(field):
    """
    Decode escape sequences in a ``.properties`` key or value.  The following
    escape sequences are recognized::

        \\t \\n \\f \\r \\uXXXX \\\\

    If a backslash is followed by any other character, the backslash is
    dropped.

    In addition, any valid UTF-16 surrogate pairs in the string after
    escape-decoding are further decoded into the non-BMP characters they
    represent.  (Invalid & isolated surrogate code points are left as-is.)

    .. versionchanged:: 0.5.0
        Invalid ``\\uXXXX`` escape sequences will now cause an
        `InvalidUEscapeError` to be raised

    :param field: the string to decode
    :type field: text string
    :rtype: text string
    :raises InvalidUEscapeError: if an invalid ``\\uXXXX`` escape sequence
        occurs in the input
    """
    return SURROGATE_PAIR_RGX.sub(_unsurrogate, ESCAPE_RGX.sub(_unesc, field))

_unescapes = {'t': '\t', 'n': '\n', 'f': '\f', 'r': '\r'}

def _unesc(m):
    esc = m.group(1)
    if esc[0] == 'u':
        if not U_ESCAPE_RGX.match(esc):
            # We can't rely on `int` failing, because it succeeds when `esc`
            # has trailing whitespace or a leading minus.
            raise InvalidUEscapeError('\\' + esc)
        return unichr(int(esc[1:], 16))
    else:
        return _unescapes.get(esc, esc)

def _unsurrogate(m):
    c,d = map(ord, m.group())
    uord = ((c - 0xD800) << 10) + (d - 0xDC00) + 0x10000
    try:
        return unichr(uord)
    except ValueError:
        # Narrow Python build (only a thing pre-3.3)
        return pack('i', uord).decode('utf-32')


class InvalidUEscapeError(ValueError):
    """
    .. versionadded:: 0.5.0

    Raised when an invalid ``\\uXXXX`` escape sequence (i.e., a ``\\u`` not
    immediately followed by four hexadecimal digits) is encountered in a simple
    line-oriented ``.properties`` file
    """

    def __init__(self, escape):
        #: The invalid ``\uXXXX`` escape sequence encountered
        self.escape = escape
        super(InvalidUEscapeError, self).__init__(escape)

    def __str__(self):
        return 'Invalid \\u escape sequence: ' + self.escape
