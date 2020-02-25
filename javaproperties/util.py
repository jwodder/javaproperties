import re
from   six import PY2

if PY2:
    from collections     import Mapping
else:
    from collections.abc import Mapping

CONTINUED_RGX = re.compile(r'(?<!\\)((?:\\\\)*)\\$')

EOL_RGX = re.compile(r'\r\n?|\n')

def itemize(kvs, sort_keys=False):
    if isinstance(kvs, Mapping):
        items = ((k, kvs[k]) for k in kvs)
    else:
        items = kvs
    if sort_keys:
        items = sorted(items)
    return items

def ascii_splitlines(s):
    lines = []
    lastend = 0
    for m in EOL_RGX.finditer(s):
        lines.append(s[lastend:m.end()])
        lastend = m.end()
    if lastend < len(s):
        lines.append(s[lastend:])
    return lines
