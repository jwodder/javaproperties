.. module:: javaproperties

==============================================================
javaproperties — Read & write Java .properties files in Python
==============================================================

Contents:

.. contents::
   :depth: 2
   :local:

`javaproperties` provides support for reading & writing Java |properties|_
files (both the "plain" format and XML) with a simple API based on the `json`
module — though, for recovering Java addicts, it also includes a `Properties`
class intended to match the behavior of |java8properties|_ as much as is
Pythonically possible.

.. note::

    Throughout the following, "text string" means a Unicode character string —
    `unicode <python2:unicode>` in Python 2, `str` in Python 3.

Reading & Writing ``.properties`` Files
=======================================

Format Overview
---------------

The "plain" ``.properties`` file format consists of a series of key-value
string pairs, one (or fewer) per line, with the key & value separated by the
first occurrence of an equals sign (``=``, optionally with surrounding
whitespace), a colon (``:``, optionally with surrounding whitespace), or
non-leading whitespace.  A line without a separator is treated as a key whose
value is the empty string.  If the same key occurs more than once in a single
file, only its last value is used.

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

Functions
---------
.. autofunction:: dump
.. autofunction:: dumps
.. autofunction:: load
.. autofunction:: loads

Reading & Writing ``.properties`` Files as XML
==============================================

Format Overview
---------------

The XML ``.properties`` file format encodes a series of key-value string pairs
(and optionally also a comment) as an XML document conforming to the following
Document Type Definition (published at
<http://java.sun.com/dtd/properties.dtd>):

.. code-block:: dtd

    <!ELEMENT properties (comment?, entry*)>
    <!ATTLIST properties version CDATA #FIXED "1.0">
    <!ELEMENT comment (#PCDATA)>
    <!ELEMENT entry (#PCDATA)>
    <!ATTLIST entry key CDATA #REQUIRED>

Functions
---------
.. autofunction:: dump_xml
.. autofunction:: dumps_xml
.. autofunction:: load_xml
.. autofunction:: loads_xml

``Properties`` Class
====================
.. autoclass:: Properties

Low-Level Utilities
===================
.. autofunction:: escape
.. autofunction:: java_timestamp
.. autofunction:: join_key_value
.. autofunction:: parse
.. autofunction:: to_comment
.. autofunction:: unescape

Command-Line Interface
======================
`javaproperties` includes two command-line programs for converting
``.properties`` files to & from the much more widely-supported JSON format.
Currently, only "plain"/non-XML properties files are supported.

.. index:: json2properties (command)
.. automodule:: javaproperties.fromjson
    :no-members:

.. index:: properties2json (command)
.. automodule:: javaproperties.tojson
    :no-members:

Indices and tables
==================
* :ref:`genindex`
* :ref:`search`

.. |properties| replace:: ``.properties``
.. _properties: https://en.wikipedia.org/wiki/.properties

.. |java8properties| replace:: Java 8's ``java.net.Properties``
.. _java8properties: https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html
