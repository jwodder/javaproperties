.. currentmodule:: javaproperties

XML ``.properties`` Format
==========================

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

An example XML ``.properties`` file:

.. code-block:: xml

    <!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
    <properties>
    <comment>This is a comment.</comment>
    <entry key="foo">bar</entry>
    <entry key="snowman">☃</entry>
    <entry key="goat">🐐</entry>
    <entry key="host:port">127.0.0.1:80</entry>
    </properties>

This corresponds to the Python `dict`:

.. code-block:: python

    {
        "foo": "bar",
        "snowman": "☃",
        "goat": "🐐",
        "host:port": "127.0.0.1:80",
    }

Functions
---------
.. autofunction:: dump_xml
.. autofunction:: dumps_xml
.. autofunction:: load_xml
.. autofunction:: loads_xml
