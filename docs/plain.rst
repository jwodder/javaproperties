.. currentmodule:: javaproperties

Simple Line-Oriented ``.properties`` Format
===========================================

Format Overview
---------------

The simple line-oriented ``.properties`` file format consists of a series of
key-value string pairs, one (or fewer) per line, with the key & value separated
by the first occurrence of an equals sign (``=``, optionally with surrounding
whitespace), a colon (``:``, optionally with surrounding whitespace), or
non-leading whitespace.  A line without a separator is treated as a key whose
value is the empty string.  If the same key occurs more than once in a single
file, only its last value is used.

.. note::

    Lines are terminated by ``\n`` (LF), ``\r\n`` (CR LF), or ``\r`` (CR).

.. note::

    For the purposes of this format, only the space character (ASCII 0x20), the
    tab character (ASCII 0x09), and the form feed character (ASCII 0x0C) count
    as whitespace.

Leading whitespace on a line is ignored, but trailing whitespace (after
stripping trailing newlines) is not.  Lines whose first non-whitespace
character is ``#`` or ``!`` (not escaped) are comments and are ignored.

Entries can be extended across multiple lines by ending all but the last line
with a backslash; the backslash, the line ending after it, and any leading
whitespace on the next line will all be discarded.  A backslash at the end of a
comment line has no effect.  A comment line after a line that ends with a
backslash is treated as part of a normal key-value entry, not as a comment.

Occurrences of ``=``, ``:``, ``#``, ``!``, and whitespace inside a key or value
are escaped with a backslash.  In addition, the following escape sequences are
recognized::

    \t \n \f \r \uXXXX \\

If a backslash is followed by any other character, the backslash is dropped.

By default, keys & values in ``.properties`` files are encoded in ASCII, and
comments are encoded in Latin-1; characters outside these ranges, along with
any unprintable characters, are escaped with the escape sequences listed above.
Unicode characters outside the Basic Multilingual Plane are first converted to
UTF-16 surrogate pairs before escaping with ``\uXXXX`` escapes.

An example simple line-oriented ``.properties`` file:

.. code-block:: properties

    #This is a comment.
    foo=bar
    baz: quux
    gnusto cleesh
    snowman = \u2603
    goat = \ud83d\udc10
    novalue
    host\:port=127.0.0.1\:80

This corresponds to the Python `dict`:

.. code-block:: python

    {
        "foo": "bar",
        "baz": "quux",
        "gnusto": "cleesh",
        "snowman": "☃",
        "goat": "🐐",
        "novalue": "",
        "host:port": "127.0.0.1:80",
    }

Functions
---------
.. autofunction:: dump
.. autofunction:: dumps
.. autofunction:: load
.. autofunction:: loads
