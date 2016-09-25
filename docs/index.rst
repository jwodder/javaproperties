.. module:: javaproperties

==============================================================
javaproperties — Read & write Java .properties files in Python
==============================================================

Contents:

.. contents::
   :depth: 2
   :local:

.. todo::

    Document the CLI commands

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
