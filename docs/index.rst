.. module:: javaproperties

==============================================================
javaproperties — Read & write Java .properties files in Python
==============================================================

`javaproperties` provides support for reading & writing |properties|_ (both the
simple line-oriented format and XML) with a simple API based on the `json`
module — though, for recovering Java addicts, it also includes a `Properties`
class intended to match the behavior of |java8properties|_ as much as is
Pythonically possible.

Previous versions of `javaproperties` included command-line programs for
basic manipulation of ``.properties`` files.  As of version 0.4.0, these
programs have been split off into a separate package, |clipkg|_.

.. note::

    Throughout the following, "text string" means a Unicode character string —
    |unicode|_ in Python 2, `str` in Python 3.

.. toctree::
    :maxdepth: 2

    plain
    xmlprops
    propclass
    propfile
    util
    cli

Indices and tables
==================
* :ref:`genindex`
* :ref:`search`

.. |properties| replace:: Java ``.properties`` files
.. _properties: https://en.wikipedia.org/wiki/.properties

.. |java8properties| replace:: Java 8's ``java.util.Properties``
.. _java8properties: https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html

.. |clipkg| replace:: ``javaproperties-cli``
.. _clipkg: http://javaproperties-cli.readthedocs.io
