.. javaproperties documentation master file, created by
   sphinx-quickstart on Mon Sep 19 00:47:10 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. module:: javaproperties

==========================================
Welcome to javaproperties's documentation!
==========================================

Contents:

.. toctree::
   :maxdepth: 2

.. todo::

    Document the CLI commands

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
.. autofunction:: load_items3
.. autofunction:: to_comment
.. autofunction:: unescape

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
