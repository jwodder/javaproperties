import re
from   six import PY2

if PY2:
    from collections     import Mapping
else:
    from collections.abc import Mapping

CONTINUED_RGX = re.compile(r'(?<!\\)((?:\\\\)*)\\\r?\n?\Z')

EOL_RGX = re.compile(r'\r\n?|\n')

class LinkedList(object):
    def __init__(self):
        self.start = None
        self.end = None

    def __iter__(self):
        return (n.value for n in self.iternodes())

    def iternodes(self):
        n = self.start
        while n is not None:
            yield n
            n = n.next

    def append(self, value):
        n = LinkedListNode(value, self)
        if self.start is None:
            self.start = n
        else:
            assert self.end is not None
            self.end.next = n
            n.prev = self.end
        self.end = n
        return n

    def find_node(self, node):
        for i,n in enumerate(self.iternodes()):
            if n is node:
                return i
        return None


class LinkedListNode(object):
    def __init__(self, value, lst):
        self.value = value
        self.lst = lst
        self.prev = None
        self.next = None

    def unlink(self):
        if self.prev is not None:
            self.prev.next = self.next
        if self.next is not None:
            self.next.prev = self.prev
        if self is self.lst.start:
            self.lst.start = self.next
        if self is self.lst.end:
            self.lst.end = self.prev

    def insert_after(self, value):
        """ Inserts a new node with value ``value`` after the node ``self`` """
        n = LinkedListNode(value, self.lst)
        n.prev = self
        n.next = self.next
        self.next = n
        if n.next is not None:
            n.next.prev = n
        else:
            assert self is self.lst.end
            self.lst.end = n
        return n

    def insert_before(self, value):
        """
        Inserts a new node with value ``value`` before the node ``self``
        """
        n = LinkedListNode(value, self.lst)
        n.next = self
        n.prev = self.prev
        self.prev = n
        if n.prev is not None:
            n.prev.next = n
        else:
            assert self is self.lst.start
            self.lst.start = n
        return n


def itemize(kvs, sort_keys=False):
    if isinstance(kvs, Mapping):
        items = ((k, kvs[k]) for k in kvs)
    else:
        items = kvs
    if sort_keys:
        items = sorted(items)
    return items

def ascii_splitlines(s):
    """
    Like `str.splitlines(True)`, except it only treats LF, CR LF, and CR as
    line endings
    """
    lines = []
    lastend = 0
    for m in EOL_RGX.finditer(s):
        lines.append(s[lastend:m.end()])
        lastend = m.end()
    if lastend < len(s):
        lines.append(s[lastend:])
    return lines
