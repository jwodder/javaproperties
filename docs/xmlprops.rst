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

Functions
---------
.. autofunction:: dump_xml
.. autofunction:: dumps_xml
.. autofunction:: load_xml
.. autofunction:: loads_xml
