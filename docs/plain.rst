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

Unicode characters outside the Basic Multilingual Plane can be represented by a
pair of ``\uXXXX`` escape sequences encoding the corresponding UTF-16 surrogate
pair.

If a backslash is followed by character other than those listed above, the
backslash is discarded.

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

File Encoding
-------------

Although the `load()` and `loads()` functions accept arbitrary Unicode
characters in their input, by default the `dump()` and `dumps()` functions
limit the characters in their output as follows:

- When ``ensure_ascii`` is `True` (the default), `dump()` and `dumps()` output
  keys & values in pure ASCII; non-ASCII and unprintable characters are escaped
  with the escape sequences listed above.  When ``ensure_ascii`` is `False`,
  the functions instead pass all non-ASCII characters through as-is;
  unprintable characters are still escaped.

- When ``ensure_ascii_comments`` is `None` (the default), `dump()` and
  `dumps()` output the ``comments`` argument (if set) using only Latin-1
  (ISO-8859-1) characters; all other characters are escaped.  When
  ``ensure_ascii_comments`` is `True`, the functions instead escape all
  non-ASCII characters in ``comments``.  When ``ensure_ascii_comments`` is
  `False`, the functions instead pass all characters in ``comments`` through
  as-is.

  - Note that, in order to match the behavior of Java's ``Properties`` class,
    unprintable ASCII characters in ``comments`` are always passed through
    as-is rather than escaped.

  - Newlines inside ``comments`` are not escaped, but a ``#`` is inserted
    after every one not already followed by a ``#`` or ``!``.

When writing properties to a file, you must either (a) open the file using an
encoding that supports all of the characters in the formatted output or else
(b) open the file using the :ref:`'javapropertiesreplace' error handler
<javapropertiesreplace>` defined by this module.  The latter option allows one
to write valid simple-format properties files in any encoding without having to
worry about whether the properties or comment contain any characters not
representable in the encoding.

Functions
---------
.. autofunction:: dump
.. autofunction:: dumps
.. autofunction:: load
.. autofunction:: loads
