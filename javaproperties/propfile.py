from   __future__  import print_function
from   collections import OrderedDict
import six
from   .reading    import Comment, KeyValue, loads, parse
from   .util       import CONTINUED_RGX, LinkedList, ascii_splitlines
from   .writing    import java_timestamp, join_key_value, to_comment

if six.PY2:
    from collections     import Mapping, MutableMapping
else:
    from collections.abc import Mapping, MutableMapping

_type_err = 'Keys & values of PropertiesFile instances must be strings'

class PropertiesFile(MutableMapping):
    """
    .. versionadded:: 0.3.0

    A custom mapping class for reading from, editing, and writing to a
    ``.properties`` file while preserving comments & whitespace in the original
    input.

    A `PropertiesFile` instance can be constructed from another mapping and/or
    iterable of pairs, after which it will act like an
    `~collections.OrderedDict`.  Alternatively, an instance can be constructed
    from a file or string with `PropertiesFile.load()` or
    `PropertiesFile.loads()`, and the resulting instance will remember the
    formatting of its input and retain that formatting when written back to a
    file or string with the `~PropertiesFile.dump()` or
    `~PropertiesFile.dumps()` method.  The formatting information attached to
    an instance ``pf`` can be forgotten by constructing another mapping from it
    via ``dict(pf)``, ``OrderedDict(pf)``, or even ``PropertiesFile(pf)`` (Use
    the `copy()` method if you want to create another `PropertiesFile` instance
    with the same data & formatting).

    When not reading or writing, `PropertiesFile` behaves like a normal
    `~collections.abc.MutableMapping` class (i.e., you can do ``props[key] =
    value`` and so forth), except that (a) like `~collections.OrderedDict`, key
    insertion order is remembered and is used when iterating & dumping (and
    `reversed` is supported), and (b) like `Properties`, it may only be used to
    store strings and will raise a `TypeError` if passed a non-string object as
    key or value.

    Two `PropertiesFile` instances compare equal iff both their key-value pairs
    and comment & whitespace lines are equal and in the same order.  When
    comparing a `PropertiesFile` to any other type of mapping, only the
    key-value pairs are considered, and order is ignored.

    `PropertiesFile` currently only supports reading & writing the simple
    line-oriented format, not XML.
    """

    def __init__(self, mapping=None, **kwargs):
        #: mapping from keys to list of LinkedListNode's
        self._key2nodes = OrderedDict()
        #: linked list of PropertiesElement's in order of appearance in file
        self._lines = LinkedList()
        if mapping is not None:
            self.update(mapping)
        self.update(kwargs)

    def _check(self):
        """
        Assert the internal consistency of the instance's data structures.
        This method is for debugging only.
        """
        for k,ns in six.iteritems(self._key2nodes):
            assert k is not None, 'null key'
            assert ns, 'Key does not map to any nodes'
            indices = []
            for n in ns:
                ix = self._lines.find_node(n)
                assert ix is not None, 'Key has node not in line list'
                indices.append(ix)
                assert isinstance(n.value, KeyValue), 'Key maps to comment'
                assert n.value.key == k, 'Key does not map to itself'
                assert n.value.value is not None, 'Key has null value'
            assert indices == sorted(indices), "Key's nodes are not in order"
        for line in self._lines:
            if not isinstance(line, KeyValue):
                assert line.source is not None, 'Comment source not stored'
                assert loads(line.source) == {}, 'Comment source is not comment'
            else:
                assert line.value is not None, 'Key has null value'
                if line.source is not None:
                    assert loads(line.source) == {line.key: line.value}, \
                        'Key source does not deserialize to itself'
                assert line.key in self._key2nodes, 'Key is missing from map'
                assert any(line == n.value for n in self._key2nodes[line.key]),\
                    'Key does not map to itself'  # pragma: no cover

    def __getitem__(self, key):
        if not isinstance(key, six.string_types):
            raise TypeError(_type_err)
        return self._key2nodes[key][-1].value.value

    def __setitem__(self, key, value):
        if not isinstance(key, six.string_types) or \
                not isinstance(value, six.string_types):
            raise TypeError(_type_err)
        try:
            nodes = self._key2nodes[key]
        except KeyError:
            if self._lines.end is not None:
                # We're adding a line to the end of the file, so make sure the
                # line before it ends with a newline and (if it's not a
                # comment) doesn't end with a trailing line continuation.
                lastline = self._lines.end.value
                if lastline.source is not None:
                    lastsrc = lastline.source
                    if isinstance(lastline, KeyValue):
                        lastsrc = CONTINUED_RGX.sub(r'\1', lastsrc)
                    if not lastsrc.endswith(('\r', '\n')):
                        lastsrc += '\n'
                    self._lines.end.value = lastline._replace(source=lastsrc)
            n = self._lines.append(None)
        else:
            # Update the first occurrence of the key and discard the rest.
            # This way, the order in which the keys are listed in the file and
            # dict will be preserved.
            n = nodes.pop(0)
            for n2 in nodes:
                n2.unlink()
        self._key2nodes[key] = [n]
        n.value = KeyValue(key, value, None)

    def __delitem__(self, key):
        if not isinstance(key, six.string_types):
            raise TypeError(_type_err)
        for n in self._key2nodes.pop(key):
            n.unlink()

    def __iter__(self):
        return iter(self._key2nodes)

    def __reversed__(self):
        return reversed(self._key2nodes)

    def __len__(self):
        return len(self._key2nodes)

    def _comparable(self):
        return [
            (n.value.key, n.value.value)
                if isinstance(n.value, KeyValue)
                else (None, n.value.source)
            for n in self._lines.iternodes()
            ### TODO: Also include non-final repeated keys???
            if not isinstance(n.value, KeyValue)
                or n is self._key2nodes[n.value.key][-1]
        ]

    def __eq__(self, other):
        if isinstance(other, PropertiesFile):
            return self._comparable() == other._comparable()
        ### TODO: Special-case OrderedDict?
        elif isinstance(other, Mapping):
            return dict(self) == other
        else:
            return NotImplemented

    def __ne__(self, other):
        return not (self == other)

    @classmethod
    def load(cls, fp):
        """
        Parse the contents of the `~io.IOBase.readline`-supporting file-like
        object ``fp`` as a simple line-oriented ``.properties`` file and return
        a `PropertiesFile` instance.

        ``fp`` may be either a text or binary filehandle, with or without
        universal newlines enabled.  If it is a binary filehandle, its contents
        are decoded as Latin-1.

        .. versionchanged:: 0.5.0
            Invalid ``\\uXXXX`` escape sequences will now cause an
            `InvalidUEscapeError` to be raised

        :param fp: the file from which to read the ``.properties`` document
        :type fp: file-like object
        :rtype: PropertiesFile
        :raises InvalidUEscapeError: if an invalid ``\\uXXXX`` escape sequence
            occurs in the input
        """
        obj = cls()
        for elem in parse(fp):
            n = obj._lines.append(elem)
            if isinstance(elem, KeyValue):
                obj._key2nodes.setdefault(elem.key, []).append(n)
        return obj

    @classmethod
    def loads(cls, s):
        """
        Parse the contents of the string ``s`` as a simple line-oriented
        ``.properties`` file and return a `PropertiesFile` instance.

        ``s`` may be either a text string or bytes string.  If it is a bytes
        string, its contents are decoded as Latin-1.

        .. versionchanged:: 0.5.0
            Invalid ``\\uXXXX`` escape sequences will now cause an
            `InvalidUEscapeError` to be raised

        :param string s: the string from which to read the ``.properties``
            document
        :rtype: PropertiesFile
        :raises InvalidUEscapeError: if an invalid ``\\uXXXX`` escape sequence
            occurs in the input
        """
        if isinstance(s, six.binary_type):
            fp = six.BytesIO(s)
        else:
            fp = six.StringIO(s)
        return cls.load(fp)

    def dump(self, fp, separator='='):
        """
        Write the mapping to a file in simple line-oriented ``.properties``
        format.

        If the instance was originally created from a file or string with
        `PropertiesFile.load()` or `PropertiesFile.loads()`, then the output
        will include the comments and whitespace from the original input, and
        any keys that haven't been deleted or reassigned will retain their
        original formatting and multiplicity.  Key-value pairs that have been
        modified or added to the mapping will be reformatted with
        `join_key_value()` using the given separator.  All key-value pairs are
        output in the order they were defined, with new keys added to the end.

        .. note::

            Serializing a `PropertiesFile` instance with the :func:`dump()`
            function instead will cause all formatting information to be
            ignored, as :func:`dump()` will treat the instance like a normal
            mapping.

        :param fp: A file-like object to write the mapping to.  It must have
            been opened as a text file with a Latin-1-compatible encoding.
        :param separator: The string to use for separating new or modified keys
            & values.  Only ``" "``, ``"="``, and ``":"`` (possibly with added
            whitespace) should ever be used as the separator.
        :type separator: text string
        :return: `None`
        """
        for line in self._lines:
            if line.source is None:
                print(join_key_value(line.key, line.value, separator), file=fp)
            else:
                fp.write(line.source)

    def dumps(self, separator='='):
        """
        Convert the mapping to a text string in simple line-oriented
        ``.properties`` format.

        If the instance was originally created from a file or string with
        `PropertiesFile.load()` or `PropertiesFile.loads()`, then the output
        will include the comments and whitespace from the original input, and
        any keys that haven't been deleted or reassigned will retain their
        original formatting and multiplicity.  Key-value pairs that have been
        modified or added to the mapping will be reformatted with
        `join_key_value()` using the given separator.  All key-value pairs are
        output in the order they were defined, with new keys added to the end.

        .. note::

            Serializing a `PropertiesFile` instance with the :func:`dumps()`
            function instead will cause all formatting information to be
            ignored, as :func:`dumps()` will treat the instance like a normal
            mapping.

        :param separator: The string to use for separating new or modified keys
            & values.  Only ``" "``, ``"="``, and ``":"`` (possibly with added
            whitespace) should ever be used as the separator.
        :type separator: text string
        :rtype: text string
        """
        s = six.StringIO()
        self.dump(s, separator=separator)
        return s.getvalue()

    def copy(self):
        """ Create a copy of the mapping, including formatting information """
        dup = type(self)()
        for elem in self._lines:
            n = dup._lines.append(elem)
            if isinstance(elem, KeyValue):
                dup._key2nodes.setdefault(elem.key, []).append(n)
        return dup

    @property
    def timestamp(self):
        """
        .. versionadded:: 0.7.0

        The value of the timestamp comment, with the comment marker, any
        whitespace leading up to it, and the trailing newline removed.  The
        timestamp comment is the first comment that appears to be a valid
        timestamp as produced by Java 8's ``Date.toString()`` and that does not
        come after any key-value pairs; if there is no such comment, the value
        of this property is `None`.

        The timestamp can be changed by assigning to this property.  Assigning
        a string ``s`` replaces the timestamp comment with the output of
        ``to_comment(s)``; no check is made as to whether the result is a valid
        timestamp comment.  Assigning `None` or `False` causes the timestamp
        comment to be deleted (also achievable with ``del pf.timestamp``).
        Assigning any other value ``x`` replaces the timestamp comment with the
        output of ``to_comment(java_timestamp(x))``.

        >>> pf = PropertiesFile.loads('''\\
        ... #This is a comment.
        ... #Tue Feb 25 19:13:27 EST 2020
        ... key = value
        ... zebra: apple
        ... ''')
        >>> pf.timestamp
        'Tue Feb 25 19:13:27 EST 2020'
        >>> pf.timestamp = 1234567890
        >>> pf.timestamp
        'Fri Feb 13 18:31:30 EST 2009'
        >>> print(pf.dumps(), end='')
        #This is a comment.
        #Fri Feb 13 18:31:30 EST 2009
        key = value
        zebra: apple
        >>> del pf.timestamp
        >>> pf.timestamp is None
        True
        >>> print(pf.dumps(), end='')
        #This is a comment.
        key = value
        zebra: apple
        """
        for elem in self._lines:
            if isinstance(elem, Comment) and elem.is_timestamp():
                return elem.value
            elif isinstance(elem, KeyValue):
                return None
        return None

    @timestamp.setter
    def timestamp(self, value):
        if value is not None and value is not False:
            if not isinstance(value, six.string_types):
                value = java_timestamp(value)
            comments = [
                Comment(c) for c in ascii_splitlines(to_comment(value) + '\n')
            ]
        else:
            comments = []
        for n in self._lines.iternodes():
            if isinstance(n.value, Comment) and n.value.is_timestamp():
                if comments:
                    n.value = comments[0]
                    for c in comments[1:]:
                        n = n.insert_after(c)
                else:
                    n.unlink()
                return
            elif isinstance(n.value, KeyValue):
                for c in comments:
                    n.insert_before(c)
                return
        else:
            for c in comments:
                self._lines.append(c)

    @timestamp.deleter
    def timestamp(self):
        for n in self._lines.iternodes():
            if isinstance(n.value, Comment) and n.value.is_timestamp():
                n.unlink()
                return
            elif isinstance(n.value, KeyValue):
                return
