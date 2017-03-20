.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active - The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://travis-ci.org/jwodder/javaproperties.svg?branch=master
    :target: https://travis-ci.org/jwodder/javaproperties

.. image:: https://coveralls.io/repos/github/jwodder/javaproperties/badge.svg?branch=master
    :target: https://coveralls.io/github/jwodder/javaproperties?branch=master

.. image:: https://img.shields.io/pypi/pyversions/javaproperties.svg
    :target: https://pypi.python.org/pypi/javaproperties

.. image:: https://img.shields.io/github/license/jwodder/javaproperties.svg?maxAge=2592000
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/javaproperties>`_
| `PyPI <https://pypi.python.org/pypi/javaproperties>`_
| `Documentation <https://javaproperties.readthedocs.io/en/v0.2.1>`_
| `Issues <https://github.com/jwodder/javaproperties/issues>`_

``javaproperties`` provides support for reading & writing Java |properties|_
files (both the simple line-oriented format and XML) with a simple API based on
the ``json`` module — though, for recovering Java addicts, it also includes a
``Properties`` class intended to match the behavior of |propclass|_ as much as
is Pythonically possible.

Also included are three command-line programs for basic manipulation of
``.properties`` files (getting & setting values, etc.) as well as converting to
& from the much more widely-supported JSON format.


Installation
============

Just use `pip <https://pip.pypa.io>`_ (You have pip, right?) to install
``javaproperties`` and its dependencies::

    pip install javaproperties


Examples
========

Dump some keys & values (output order not guaranteed)::

    >>> properties = {"key": "value", "host:port": "127.0.0.1:80", "snowman": "☃", "goat": "🐐"}
    >>> print(javaproperties.dumps(properties))
    #Mon Sep 26 14:57:44 EDT 2016
    key=value
    goat=\ud83d\udc10
    host\:port=127.0.0.1\:80
    snowman=\u2603

Load some keys & values::

    >>> javaproperties.loads('''
    ... #Mon Sep 26 14:57:44 EDT 2016
    ... key = value
    ... goat: \\ud83d\\udc10
    ... host\\:port=127.0.0.1:80
    ... #foo = bar
    ... snowman   ☃
    ... ''')
    {'goat': '🐐', 'host:port': '127.0.0.1:80', 'key': 'value', 'snowman': '☃'}

Dump some properties to a file and read them back in again::

    >>> with open('example.properties', 'w', encoding='latin-1') as fp:
    ...     javaproperties.dump(properties, fp)
    ...
    >>> with open('example.properties', 'r', encoding='latin-1') as fp:
    ...     javaproperties.load(fp)
    ...
    {'goat': '🐐', 'host:port': '127.0.0.1:80', 'key': 'value', 'snowman': '☃'}

Sort the properties you're dumping::

    >>> print(javaproperties.dumps(properties, sort_keys=True))
    #Mon Sep 26 14:57:44 EDT 2016
    goat=\ud83d\udc10
    host\:port=127.0.0.1\:80
    key=value
    snowman=\u2603

Turn off the timestamp::

    >>> print(javaproperties.dumps(properties, timestamp=None))
    key=value
    goat=\ud83d\udc10
    host\:port=127.0.0.1\:80
    snowman=\u2603

Use your own timestamp (automatically converted to local time)::

    >>> print(javaproperties.dumps(properties, timestamp=1234567890))
    #Fri Feb 13 18:31:30 EST 2009
    key=value
    goat=\ud83d\udc10
    host\:port=127.0.0.1\:80
    snowman=\u2603

Dump as XML::

    >>> print(javaproperties.dumps_xml(properties))
    <!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
    <properties>
    <entry key="key">value</entry>
    <entry key="goat">🐐</entry>
    <entry key="host:port">127.0.0.1:80</entry>
    <entry key="snowman">☃</entry>
    </properties>

`And more! <https://javaproperties.readthedocs.io>`_


.. |properties| replace:: ``.properties``
.. _properties: https://en.wikipedia.org/wiki/.properties

.. |propclass| replace:: Java 8's ``java.net.Properties``
.. _propclass: https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html
