.. module:: javaproperties

==============================================================
javaproperties — Read & write Java .properties files in Python
==============================================================

`GitHub <https://github.com/jwodder/javaproperties>`_
| `PyPI <https://pypi.org/project/javaproperties>`_
| `Documentation <https://javaproperties.readthedocs.io>`_
| `Issues <https://github.com/jwodder/javaproperties/issues>`_
| :doc:`Changelog <changelog>`

.. toctree::
    :hidden:

    plain
    xmlprops
    propclass
    propfile
    util
    cli
    changelog

`javaproperties` provides support for reading & writing |properties|_ (both the
simple line-oriented format and XML) with a simple API based on the `json`
module — though, for recovering Java addicts, it also includes a `Properties`
class intended to match the behavior of |java8properties|_ as much as is
Pythonically possible.

Previous versions of `javaproperties` included command-line programs for
basic manipulation of ``.properties`` files.  As of version 0.4.0, these
programs have been split off into a separate package, |clipkg|_.

Installation
============

Just use `pip <https://pip.pypa.io>`_ (You have pip, right?) to install
``javaproperties`` and its dependencies::

    pip install javaproperties


Examples
========

Dump some keys & values (output order not guaranteed):

>>> properties = {"key": "value", "host:port": "127.0.0.1:80", "snowman": "☃", "goat": "🐐"}
>>> print(javaproperties.dumps(properties))
#Mon Sep 26 14:57:44 EDT 2016
key=value
goat=\ud83d\udc10
host\:port=127.0.0.1\:80
snowman=\u2603

Load some keys & values:

>>> javaproperties.loads('''
... #Mon Sep 26 14:57:44 EDT 2016
... key = value
... goat: \\ud83d\\udc10
... host\\:port=127.0.0.1:80
... #foo = bar
... snowman   ☃
... ''')
{'goat': '🐐', 'host:port': '127.0.0.1:80', 'key': 'value', 'snowman': '☃'}

Dump some properties to a file and read them back in again:

>>> with open('example.properties', 'w', encoding='latin-1') as fp:
...     javaproperties.dump(properties, fp)
...
>>> with open('example.properties', 'r', encoding='latin-1') as fp:
...     javaproperties.load(fp)
...
{'goat': '🐐', 'host:port': '127.0.0.1:80', 'key': 'value', 'snowman': '☃'}

Sort the properties you're dumping:

>>> print(javaproperties.dumps(properties, sort_keys=True))
#Mon Sep 26 14:57:44 EDT 2016
goat=\ud83d\udc10
host\:port=127.0.0.1\:80
key=value
snowman=\u2603

Turn off the timestamp:

>>> print(javaproperties.dumps(properties, timestamp=None))
key=value
goat=\ud83d\udc10
host\:port=127.0.0.1\:80
snowman=\u2603

Use your own timestamp (automatically converted to local time):

>>> print(javaproperties.dumps(properties, timestamp=1234567890))
#Fri Feb 13 18:31:30 EST 2009
key=value
goat=\ud83d\udc10
host\:port=127.0.0.1\:80
snowman=\u2603

Dump as XML:

>>> print(javaproperties.dumps_xml(properties))
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<entry key="key">value</entry>
<entry key="goat">🐐</entry>
<entry key="host:port">127.0.0.1:80</entry>
<entry key="snowman">☃</entry>
</properties>

New in v0.6.0: Dump Unicode characters as-is instead of escaping them:

>>> print(javaproperties.dumps(properties, ensure_ascii=False))
#Tue Feb 25 19:13:27 EST 2020
key=value
goat=🐐
host\:port=127.0.0.1\:80
snowman=☃


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
