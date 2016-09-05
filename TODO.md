- Write tests
    - Test working with both `str` and `unicode` in Python 2
    - Test working with bytes in both Python 2 and Python 3
    - Test reading & writing surrogate pairs
    - Test reading & writing unpaired surrogates
    - Test `load` and `dump` on actual files???
    - Test writing timestamps with & without python-dateutil installed
    - cf. the tests used in OpenJDK: <http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/tip/test/java/util/Properties>
- Add docstrings
    - Add a module docstring to `__init__.py`
- Add a README
- `dump`: Support writing `str`s in Python 2
- Finish the Properties class
    - Support reading & writing properties as XML
    - Implement the `list` method?
- Handle "narrow" Python builds (only for Python versions < 3.3)
- Support Python 3.2?
- Force use of the C locale when generating timestamps
- Rename `load_items3` (to `parse`?)
- Give `dump` and `dumps` `ensure_ascii` arguments
- Give `dump` and `dumps` `sort_keys` arguments?
- `Properties.__init__`: Convert numeric, boolean, and null keys in `data` to
  strings

New Functions
-------------
- Add a variant of `join_key_value` that escapes as few characters as possible?
- Add an inverse of `load_items3` for writing triples?
- Should there be a variant of `dump` that outputs Unicode and leaves
  non-Latin-1 characters as-is?  (cf. the different `store` methods of the Java
  class)
- Should there be a variant of `dumps` that outputs bytes?
- Add string-reading equivalent of `load_items3`?

Commands
--------
- Add a command for setting/unsetting entries in a .properties file:

        setproperty [-d] [-i | -o <outfile>] <file> <key> [<value>]

    - Include an option for controlling whether to update the timestamp
    - Include an option for setting the separator

- Add a command (`getproperty`) for printing out specified values in a
  .properties file
- Give the commands `--help` options
- Move the command-line commands back to the top level of the package so that
  they can be invoked with `python -m javaproperties.COMMAND` instead of
  `python -m javaproperties.commands.COMMAND`?
- Support autodetecting whether a properties file is in XML based on file
  extension (or other means?) ?
