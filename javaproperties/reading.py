from   __future__ import unicode_literals
import re
from   six        import unichr

def read_properties(fp):
    return dict(iter_properties(fp))

def iter_properties(fp):
    for k,v,_ in parse_properties(fp):
        if k is not None:
            yield (k,v)

def parse_properties(fp):
    # `fp` must have been opened as Latin-1 in universal newlines mode.
    # Returns an iterator of `(key, value, source_lines)` tuples; blank lines &
    # comments have `key` & `value` values of `None`
    while True:
        line = source = fp.readline()
        if line == '':
            return
        if re.match(r'^[ \t\f]*(?:[#!]|$)', line):
            yield (None, None, source)
            continue
        line = line.lstrip(' \t\f').rstrip('\n')
        while re.search(r'(?<!\\)(?:\\\\)*\\$', line):
            line = line[:-1]
            nextline = fp.readline()  # '' at EOF
            source += nextline
            line += nextline.lstrip(' \t\f').rstrip('\n')
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

def unescape(field):
    ### TODO: Handle surrogate pairs somehow???
    return re.sub(r'\\(u[0-9A-Fa-f]{4}|.)', _unesc, field)
