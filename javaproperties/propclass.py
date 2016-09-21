import collections
from   six      import string_types
from   .reading import load
from   .util    import strify_dict
from   .writing import dump
from   .xml     import load_xml, dump_xml

_type_err = 'Keys & values of Properties objects must be strings'

class Properties(collections.MutableMapping):
    """
    A port of |Properties|_ that tries to match its behavior as much as is
    Pythonically possible.  `Properties` behaves like a normal
    `~collections.MutableMapping` class (i.e., you can do ``props[key] =
    value`` and so forth), except that it may only be used to store strings
    (`str` and `unicode` in Python 2; just `str` in Python 3).  Attempts to use
    a non-string object as a key or value will produce a
    `~exceptions.TypeError`.

    :param data: A mapping or iterable of ``(key, value)`` pairs with which to
        initialize the `Properties` object.  Numeric, boolean, and `None` keys
        and non-`list`, non-`dict` values will be coverted to strings with
        `json.dumps`.  Any other non-string keys or values will produce a
        `~exceptions.TypeError`.
    :type data: mapping or `None`
    :param defaults: a set of default properties that will be used as fallback
        for `getProperty`
    :type defaults: `Properties` or `None`

    .. |Properties| replace:: Java 8's ``java.net.Properties`` class
    .. _Properties: https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html
    """

    def __init__(self, data=None, defaults=None):
        self.data = {}
        if data is not None:
            self.data.update(strify_dict(data))
        #: A `Properties` subobject used as fallback for `getProperty`.  Only
        #: `getProperty`, `propertyNames`, and `stringPropertyNames` use this
        #: attribute; all other methods (including the standard mapping
        #: methods) ignore it.
        self.defaults = defaults

    def __getitem__(self, key):
        if not isinstance(key, string_types):
            raise TypeError(_type_err)
        return self.data[key]

    def __setitem__(self, key, value):
        if not isinstance(key, string_types) or \
                not isinstance(value, string_types):
            raise TypeError(_type_err)
        self.data[key] = value

    def __delitem__(self, key):
        if not isinstance(key, string_types):
            raise TypeError(_type_err)
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return'{0}.{1.__class__.__name__}({1.data!r}, defaults={1.defaults!r})'\
                .format(__package__, self)

    def __eq__(self, other):
        return type(self) is type(other) and \
                self.data == other.data and \
                self.defaults == other.defaults

    def __ne__(self, other):
        return not (self == other)

    def __nonzero__(self):
        return bool(self.data)

    __bool__ = __nonzero__

    def getProperty(self, key, defaultValue=None):
        """
        Fetch the value associated with the key ``key`` in the `Properties`
        object.  If the key is not present, `defaults` is checked, and then
        _its_ `defaults`, etc., until either a value for ``key`` is found or
        the next `defaults` is `None`, in which case `defaultValue` is
        returned.

        :param key: the key to look up the value of
        :type key: text string
        :param defaultValue: the value to return if ``key`` is not found in the
            `Properties` object
        :rtype: text string (if ``key`` was found)
        :raises TypeError: if ``key`` is not a string
        """
        try:
            return self[key]
        except KeyError:
            if self.defaults is not None:
                return self.defaults.getProperty(key, defaultValue)
            else:
                return defaultValue

    def load(self, fp):
        """
        Update the `Properties` object with the entries in a ``.properties``
        file or file-like object.

        ``fp`` may be either a text or binary filehandle, with or without
        universal newlines enabled.  If it is a binary filehandle, its contents
        are decoded as Latin-1.

        :param fp: the file from which to read the ``.properties`` document
        :type fp: file-like object
        :rtype: `None`
        """
        self.data.update(load(fp))

    def propertyNames(self):
        """
        Returns a generator of all distinct keys in the `Properties` object and
        its `defaults` (and its `defaults`\ 's `defaults`, etc.) in unspecified
        order

        :rtype: generator of text strings
        """
        for k in self.data:
            yield k
        if self.defaults is not None:
            for k in self.defaults.propertyNames():
                if k not in self.data:
                    yield k

    def setProperty(self, key, value):
        """ Equivalent to ``self[key] = value`` """
        self[key] = value

    def store(self, out, comments=None):
        """
        Write the `Properties` object's entries (in unspecified order) in
        ``.properties`` format to ``fp``, including the current timestamp.

        :param fp: A file-like object to write the properties to.  It must have
            been opened as a text file with a Latin-1-compatible encoding.
        :param comments: If non-`None`, ``comments`` will be written to ``fp``
            as a comment before any other content
        :type comments: text string or `None`
        :rtype: `None`
        """
        dump(self.data, out, comments=comments)

    def stringPropertyNames(self):
        """
        Returns a `set` of all keys in the `Properties` object and its
        `defaults` (and its `defaults`\ 's `defaults`, etc.)

        :rtype: `set` of text strings
        """
        names = set(self.data)
        if self.defaults is not None:
            names.update(self.defaults.stringPropertyNames())
        return names

    def loadFromXML(self, fp):
        """ TODO """
        self.data.update(load_xml(fp))

    def storeToXML(self, out, comment=None, encoding='UTF-8'):
        """ TODO """
        dump_xml(self.data, out, comment=comment, encoding=encoding)

    ###def list(self, out):
    ###    ???
