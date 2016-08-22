- Add functions for reading from & writing to strings instead of files?
- Write tests
    - Test working with both `str` and `unicode` in Python 2
    - Test reading & writing surrogate pairs
    - Test reading & writing unpaired surrogates
    - cf. the tests used in OpenJDK: <http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/tip/test/java/util/Properties>
- Add docstrings
    - Add a module docstring to `__init__.py`
- Add a command for setting/unsetting entries in a .properties file:

        setproperty [-d] [-i | -o <outfile>] <file> <key> [<value>]

    - Include an option for controlling whether to update the timestamp

- Add a command (`getproperty`) for printing out specified values in a
  .properties file
- Add a variant of `join_key_value` that escapes as few characters as possible?
- Add an inverse of `readitems3` for writing triples?
- Support `str` keys & values for `Properties` in Python 2
- `readitems3`: Support files not opened in universal newlines mode
- `readitems3`: Support files opened in binary mode
- `write`: Support files opened in binary mode
- Add a README
- Finish the Properties class
    - Support reading & writing properties as XML
    - Implement the `list` method?
- Give the commands `--help` options
- Should there be a variant of `write` that outputs Unicode and leaves
  non-Latin-1 characters as-is?  (cf. the different `store` methods of the Java
  class)
