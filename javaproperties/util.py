import collections
import re

def itemize(kvs, sort_keys=False):
    if isinstance(kvs, collections.Mapping):
        items = ((k, kvs[k]) for k in kvs)
    else:
        items = kvs
    if sort_keys:
        items = sorted(items)
    return items

def ascii_splitlines(s, keepends=False):
    lines = []
    lastend = 0
    for m in re.finditer(r'\r\n?|\n', s):
        if keepends:
            lines.append(s[lastend:m.end()])
        else:
            lines.append(s[lastend:m.start()])
        lastend = m.end()
    if lastend < len(s):
        lines.append(s[lastend:])
    return lines
