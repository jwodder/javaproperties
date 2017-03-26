from   __future__ import print_function
import collections
import re
import six
from   .reading   import loads, parse
from   .writing   import join_key_value

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

_type_err = 'Keys & values of PropertiesFile objects must be strings'

PropertyLine = collections.namedtuple('PropertyLine', 'key value source')

class PropertiesFile(collections.MutableMapping):
    def __init__(self, data=None, **kwargs):
        #: mapping from keys to list of line numbers
        self._indices = OrderedDict()
        #: mapping from line numbers to (key, value, source) tuples
        self._lines = OrderedDict()
        if data is not None:
            self.update(data)
        self.update(kwargs)

    def _check(self):
        """
        Assert the internal consistency of the instance's data structures.
        This method is for debugging only.
        """
        for k,ix in six.iteritems(self._indices):
            assert k is not None, 'null key'
            assert ix, 'Key does not map to any indices'
            assert ix == sorted(ix), "Key's indices are not in order"
            for i in ix:
                assert i in self._lines, 'Key index does not map to line'
                assert self._lines[i].key is not None, 'Key maps to comment'
                assert self._lines[i].key == k, 'Key does not map to itself'
                assert self._lines[i].value is not None, 'Key has null value'
        prev = None
        for i, line in six.iteritems(self._lines):
            assert prev is None or prev < i, 'Line indices out of order'
            prev = i
            if line.key is None:
                assert line.value is None, 'Comment/blank has value'
                assert line.source is not None, 'Comment source not stored'
                assert loads(line.source) == {}, 'Comment source is not comment'
            else:
                assert line.value is not None, 'Key has null value'
                if line.source is not None:
                    assert loads(line.source) == {line.key: line.value}, \
                        'Key source does not deserialize to itself'
                assert line.key in self._indices, 'Key is missing from map'
                assert i in self._indices[line.key], \
                    'Key does not map to itself'

    def __getitem__(self, key):
        if not isinstance(key, six.string_types):
            raise TypeError(_type_err)
        return self._lines[self._indices[key][-1]].value

    def __setitem__(self, key, value):
        if not isinstance(key, six.string_types) or \
                not isinstance(value, six.string_types):
            raise TypeError(_type_err)
        try:
            ixes = self._indices[key]
        except KeyError:
            try:
                lasti = next(reversed(self._lines))
            except StopIteration:
                ix = 0
            else:
                ix = lasti + 1
                # We're adding a line to the end of the file, so make sure the
                # line before it doesn't end with a trailing line continuation.
                lastline = self._lines[lasti]
                if lastline.key is not None and lastline.source is not None:
                    self._lines[lasti] = lastline._replace(
                        source=re.sub(r'(?<!\\)((?:\\\\)*)\\$', r'\1',
                                      lastline.source)
                    )
        else:
            ix = ixes.pop()
            for i in ixes:
                del self._lines[i]
        self._indices[key] = [ix]
        self._lines[ix] = PropertyLine(key, value, None)

    def __delitem__(self, key):
        if not isinstance(key, six.string_types):
            raise TypeError(_type_err)
        for i in self._indices.pop(key):
            del self._lines[i]

    def __iter__(self):
        return iter(self._indices)

    def __reversed__(self):
        return reversed(self._indices)

    def __len__(self):
        return len(self._indices)

    def _comparable(self):
        return [
            (None, line.source) if line.key is None else (line.key, line.value)
            for i, line in six.iteritems(self._lines)
            ### TODO: Also include non-final repeated keys???
            if line.key is None or self._indices[line.key][-1] == i
        ]

    def __eq__(self, other):
        if isinstance(other, PropertiesFile):
            return self._comparable() == other._comparable()
        ### TODO: Special-case OrderedDict?
        elif isinstance(other, collections.Mapping):
            return dict(self) == other
        else:
            return NotImplemented

    def __ne__(self, other):
        return not (self == other)

    #def __repr__(self):

    @classmethod
    def load(cls, fp):
        obj = cls()
        for i, (k, v, src) in enumerate(parse(fp)):
            if k is not None:
                obj._indices.setdefault(k, []).append(i)
            obj._lines[i] = PropertyLine(k, v, src)
        return obj

    @classmethod
    def loads(cls, s):
        if isinstance(s, six.binary_type):
            fp = six.BytesIO(s)
        else:
            fp = six.StringIO(s)
        return cls.load(fp)

    def dump(self, fp, separator='='):
        ### TODO: Support setting the timestamp
        for line in six.itervalues(self._lines):
            if line.source is None:
                print(join_key_value(line.key, line.value, separator), file=fp)
            else:
                fp.write(line.source)
                if not line.source.endswith(('\r', '\n')):
                    fp.write('\n')

    def dumps(self, separator='='):
        s = six.StringIO()
        self.dump(s, separator=separator)
        return s.getvalue()

    def copy(self):
        dup = self.__class__()
        dup._indices = OrderedDict(
            (k, list(v)) for k,v in six.iteritems(self._indices)
        )
        dup._lines = self._lines.copy()
        return dup
