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
module — though, for recovering Java addicts, it also includes a ``Properties``
class intended to match the behavior of |java8properties|_ as much as is
Pythonically possible.

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

Command-Line Interface
======================
`javaproperties` includes two command-line programs for converting
``.properties`` files to & from the much more widely-supported JSON format.
Currently, only "plain"/non-XML properties files are supported.

.. module:: javaproperties.fromjson
.. index:: json2properties (command)

:program:`json2properties`
--------------------------

.. code-block:: shell

    python -m javaproperties.fromjson [infile [outfile]]
    # or, if the javaproperties package was properly installed:
    json2properties [infile [outfile]]

Convert a JSON file :option:`infile` to a Latin-1 ``.properties`` file and
write the results to :option:`outfile`.  If not specified, :option:`infile` and
:option:`outfile` default to `sys.stdin` and `sys.stdout`, respectively.

The JSON document must be an object with scalar (i.e., string, numeric,
boolean, and/or null) values; anything else will result in an error.

Output is sorted by key, and numeric, boolean, & null values are output using
their JSON representations; e.g., the input:

.. code-block:: json

    {
        "yes": true,
        "no": "false",
        "nothing": null
    }

becomes:

.. code-block:: properties

    #Mon Sep 26 18:57:44 UTC 2016
    no=false
    nothing=null
    yes=true


.. module:: javaproperties.tojson
.. index:: properties2json (command)

:program:`properties2json`
--------------------------

.. code-block:: shell

    python -m javaproperties.tojson [infile [outfile]]
    # or, if the javaproperties package was properly installed:
    properties2json [infile [outfile]]

Convert a Latin-1 ``.properties`` file :option:`infile` to a JSON object and
write the results to :option:`outfile`.  If not specified, :option:`infile` and
:option:`outfile` default to `sys.stdin` and `sys.stdout`, respectively.


Indices and tables
==================
* :ref:`genindex`
* :ref:`search`

.. |properties| replace:: ``.properties``
.. _properties: https://en.wikipedia.org/wiki/.properties

.. |java8properties| replace:: Java 8's ``java.net.Properties``
.. _java8properties: https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html
