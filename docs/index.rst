.. module:: javaproperties

==============================================================
javaproperties — Read & write Java .properties files in Python
==============================================================

Contents:

.. contents::
   :depth: 2
   :local:

``javaproperties`` provides support for reading & writing Java |properties|_
files (both the "plain" format and XML) with a simple API based on the ``json``
module — though, for recovering Java addicts, it also includes a ``Properties``
class intended to match the behavior of |java8properties|_ as much as is
Pythonically possible.

.. todo::

    Document the CLI commands

.. note::

    Throughout the following, "text string" means a Unicode character string —
    `unicode <python2:unicode>` in Python 2, `str` in Python 3.

Reading & Writing ``.properties`` Files
=======================================
.. autofunction:: dump
.. autofunction:: dumps
.. autofunction:: load
.. autofunction:: loads

Reading & Writing ``.properties`` Files as XML
==============================================
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
.. autofunction:: join_key_value
.. autofunction:: parse
.. autofunction:: to_comment
.. autofunction:: unescape

Indices and tables
==================
* :ref:`genindex`
* :ref:`search`

.. |properties| replace:: ``.properties``
.. _properties: https://en.wikipedia.org/wiki/.properties

.. |java8properties| replace:: Java 8's ``java.net.Properties``
.. _java8properties: https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html
