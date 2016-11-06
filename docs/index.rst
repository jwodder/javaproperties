.. module:: javaproperties

==============================================================
javaproperties — Read & write Java .properties files in Python
==============================================================

`javaproperties` provides support for reading & writing Java |properties|_
files (both the "plain" format and XML) with a simple API based on the `json`
module — though, for recovering Java addicts, it also includes a `Properties`
class intended to match the behavior of |java8properties|_ as much as is
Pythonically possible.

Also included are three command-line programs for basic manipulation of
``.properties`` files (getting & setting values, etc.) as well as converting to
& from the much more widely-supported JSON format.

.. note::

    Throughout the following, "text string" means a Unicode character string —
    `unicode <python2:unicode>` in Python 2, `str` in Python 3.

.. toctree::
    :maxdepth: 2

    plain
    xmlprops
    propclass
    util
    cli

Indices and tables
==================
* :ref:`genindex`
* :ref:`search`

.. |properties| replace:: ``.properties``
.. _properties: https://en.wikipedia.org/wiki/.properties

.. |java8properties| replace:: Java 8's ``java.net.Properties``
.. _java8properties: https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html
