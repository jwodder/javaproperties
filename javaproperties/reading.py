from   __future__ import unicode_literals
import re
from   six        import binary_type, StringIO, unichr

def load(fp, object_pairs_hook=dict):
    return object_pairs_hook(
        (k,v) for k,v,_ in load_items3(fp)
              if k is not None
    )

def loads(s, object_pairs_hook=dict):
    return load(StringIO(s), object_pairs_hook=object_pairs_hook)

def load_items3(fp):
    # `fp` may be either a text or binary filehandle, with or without universal
    # newlines support, but it must support the `readline` method.  If `fp` is
    # a binary filehandle, its contents are assumed to be in Latin-1.  If it is
    # a text filehandle, it is assumed to have been opened as Latin-1.
    # Returns an iterator of `(key, value, source_lines)` tuples; blank lines &
    # comments have `key` & `value` values of `None`
    def readline():
        ln = fp.readline()
        if isinstance(ln, binary_type):
            ln = ln.decode('iso-8859-1')
        return ln
    while True:
        line = source = readline()
        if line == '':
            return
        if re.match(r'^[ \t\f]*(?:[#!]|\r?\n?$)', line):
            yield (None, None, source)
            continue
        line = line.lstrip(' \t\f').rstrip('\r\n')
        while re.search(r'(?<!\\)(?:\\\\)*\\$', line):
            line = line[:-1]
            nextline = readline()  # '' at EOF
            source += nextline
            line += nextline.lstrip(' \t\f').rstrip('\r\n')
        if line == '':  # series of otherwise-blank lines with continuations
            yield (None, None, source)
            continue
        m = re.search(r'(?<!\\)(?:\\\\)*([ \t\f]*[=:]|[ \t\f])[ \t\f]*', line)
        if m:
            yield (unescape(line[:m.start()]), unescape(line[m.end():]), source)
        else:
            yield (unescape(line), '', source)

_unescapes = {'t': '\t', 'n': '\n', 'f': '\f', 'r': '\r'}

def _unesc(m):
    esc = m.group(1)
    if len(esc) == 1:
        return _unescapes.get(esc, esc)
    else:
        return unichr(int(esc[1:], 16))

def _unsurrogate(m):
    c,d = map(ord, m.group())
    return unichr(((c - 0xD800) << 10) + (d - 0xDC00) + 0x10000)

def unescape(field):
    return re.sub(r'[\uD800-\uDBFF][\uDC00-\uDFFF]', _unsurrogate,
                  re.sub(r'\\(u[0-9A-Fa-f]{4}|.)', _unesc, field))
