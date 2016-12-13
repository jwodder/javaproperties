# -*- coding: utf-8 -*-
import collections
from   six       import string_types
from   .reading  import load
from   .util     import itemize
from   .writing  import dump
from   .xmlprops import load_xml, dump_xml

_type_err = 'Keys & values of Properties objects must be strings'

class Properties(collections.MutableMapping):
    """
    A port of |java8properties|_ that tries to match its behavior as much as is
    Pythonically possible.  `Properties` behaves like a normal
    `~collections.MutableMapping` class (i.e., you can do ``props[key] =
    value`` and so forth), except that it may only be used to store strings
    (`str <python2:str>` and `unicode <python2:unicode>` in Python 2; just
    `str` in Python 3).  Attempts to use a non-string object as a key or value
    will produce a `~exceptions.TypeError`.

    :param data: A mapping or iterable of ``(key, value)`` pairs with which to
        initialize the `Properties` object.  All keys and values in ``data``
        must be text strings.
    :type data: mapping or `None`
    :param defaults: a set of default properties that will be used as fallback
        for `getProperty`
    :type defaults: `Properties` or `None`

    .. |java8properties| replace:: Java 8's ``java.net.Properties``
    .. _java8properties: https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html
    """

    def __init__(self, data=None, defaults=None):
        self.data = {}
        if data is not None:
            for k,v in itemize(data):
                self[k] = v
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
        *its* `defaults`, etc., until either a value for ``key`` is found or
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

    def load(self, inStream):
        """
        Update the `Properties` object with the entries in a ``.properties``
        file or file-like object.

        ``inStream`` may be either a text or binary filehandle, with or without
        universal newlines enabled.  If it is a binary filehandle, its contents
        are decoded as Latin-1.

        :param inStream: the file from which to read the ``.properties``
            document
        :type inStream: file-like object
        :return: `None`
        """
        self.data.update(load(inStream))

    def propertyNames(self):
        r"""
        Returns a generator of all distinct keys in the `Properties` object and
        its `defaults` (and its `defaults`\ ’s `defaults`, etc.) in unspecified
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
        ``.properties`` format to ``out``, including the current timestamp.

        :param out: A file-like object to write the properties to.  It must
            have been opened as a text file with a Latin-1-compatible encoding.
        :param comments: If non-`None`, ``comments`` will be written to ``out``
            as a comment before any other content
        :type comments: text string or `None`
        :return: `None`
        """
        dump(self.data, out, comments=comments)

    def stringPropertyNames(self):
        r"""
        Returns a `set` of all keys in the `Properties` object and its
        `defaults` (and its `defaults`\ ’s `defaults`, etc.)

        :rtype: `set` of text strings
        """
        names = set(self.data)
        if self.defaults is not None:
            names.update(self.defaults.stringPropertyNames())
        return names

    def loadFromXML(self, inStream):
        """
        Update the `Properties` object with the entries in the XML properties
        file ``inStream``.

        Beyond basic XML well-formedness, `loadFromXML` only checks that the
        root element is named ``properties`` and that all of its ``entry``
        children have ``key`` attributes; no further validation is performed.

        .. note::

            This uses `xml.etree.ElementTree` for parsing, which does not have
            decent support for `unicode <python2:unicode>` input in Python 2.
            Files containing non-ASCII characters need to be opened in binary
            mode in Python 2, while Python 3 accepts both binary and text
            input.

        :param inStream: the file from which to read the XML properties document
        :type inStream: file-like object
        :return: `None`
        :raises ValueError: if the root of the XML tree is not a
            ``<properties>`` tag or an ``<entry>`` element is missing a ``key``
            attribute
        """
        self.data.update(load_xml(inStream))

    def storeToXML(self, out, comment=None, encoding='UTF-8'):
        """
        Write the `Properties` object's entries (in unspecified order) in XML
        properties format to ``out``.

        :param out: a file-like object to write the properties to
        :type out: binary file-like object
        :param comment: if non-`None`, ``comment`` will be output as a
            ``<comment>`` element before the ``<entry>`` elements
        :type comment: text string or `None`
        :param string encoding: the name of the encoding to use for the XML
            document (also included in the XML declaration)
        :return: `None`
        """
        dump_xml(self.data, out, comment=comment, encoding=encoding)
