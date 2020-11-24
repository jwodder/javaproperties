.. currentmodule:: javaproperties

Low-Level Utilities
===================
.. autofunction:: escape
.. autofunction:: java_timestamp
.. autofunction:: join_key_value
.. autofunction:: to_comment
.. autofunction:: unescape
.. autoexception:: InvalidUEscapeError
    :show-inheritance:

Low-Level Parsing
-----------------
.. autofunction:: parse
.. autoclass:: PropertiesElement
.. autoclass:: Comment(source)
.. autoclass:: KeyValue(key, value, source)
.. autoclass:: Whitespace(source)

.. _javapropertiesreplace:
.. index::
    single: javapropertiesreplace

Custom Encoding Error Handler
-----------------------------
.. versionadded:: 0.6.0

Importing `javaproperties` causes a custom error handler,
``'javapropertiesreplace'``, to be automatically defined that can then be
supplied as the *errors* argument to `str.encode`, `open`, or similar
encoding operations in order to cause all unencodable characters to be replaced
by ``\uXXXX`` escape sequences (with non-BMP characters converted to surrogate
pairs first).

This is useful, for example, when calling ``javaproperties.dump(obj, fp,
ensure_ascii=False)`` where ``fp`` has been opened using an encoding that does
not contain all Unicode characters (e.g., Latin-1); in such a case, if
``errors='javapropertiesreplace'`` is supplied when opening ``fp``, then any
characters in a key or value of ``obj`` that exist outside ``fp``'s character
set will be safely encoded as ``.properties`` file format-compatible escape
sequences instead of raising an error.

Note that the hexadecimal value used in a ``\uXXXX`` escape sequences is always
based on the source character's codepoint value in Unicode regardless of the
target encoding:

>>> # Here we see one character encoded to the byte 0x00f0 (because that's
>>> # how the target encoding represents it) and a completely different
>>> # character encoded as the escape sequence \u00f0 (because that's its
>>> # value in Unicode):
>>> 'apple: \uF8FF; edh: \xF0'.encode('mac_roman', 'javapropertiesreplace')
b'apple: \xf0; edh: \\u00f0'

.. autofunction:: javapropertiesreplace_errors
