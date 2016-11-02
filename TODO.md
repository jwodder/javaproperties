- Write tests
    - Test reading & writing bytes in both Python 2 and Python 3
    - Test utility functions in isolation?
    - Test the command-line programs (or at least their nontrivial components,
      like `setproperties`)
        - See <http://click.pocoo.org/6/testing/>
    - Run doctest on the README examples
    - Test the `Properties` class
    - cf. the tests used in OpenJDK: <http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/tip/test/java/util/Properties>
- Documentation:
    - Add docstrings for the private functions
    - Figure out exactly what types of filehandles & strings
      `xml.etree.ElementTree` can parse and add them to the `load*_xml` and
      `loadFromXML` documentation
    - Include examples in main docs?
    - Document `javaproperties` command
    - Mention that dicts (when not sorted) are output in the order they're
      iterated over, so OrderedDicts are respected
    - Look for an official term for the "plain" format
    - Mention the command-line programs in the README
- Handle "narrow" Python builds (only for Python versions < 3.3)
- Handle files with CR line endings not opened in universal newlines mode?
- Use `lxml` for XML processing if it's installed?
- Raise an error if an invalid separator is passed to a function and/or
  command-line program?
- Test against & add support for pypy?

New Features
------------
- `dump`: Support writing `str`s in Python 2
- Implement `Properties.list`?
- Give the dump functions `ensure_ascii` arguments
- Give the dump functions `keep_unicode`(?) arguments (mutually exclusive with
  `ensure_ascii`) for outputting Unicode and leaving non-Latin-1 characters
  as-is  (cf. the different `store` methods of the Java class)
- Give `load` and `loads` a `timestamp_key` (and/or `timestamp_hook`?) argument
  that, if supplied, causes the timestamp in a .properties file to be extracted
  and saved in the given key
- Add a variant of `join_key_value` that escapes as few characters as possible?
- Add an inverse of `parse` for writing triples?
- Add a string-reading equivalent of `parse`?
- Add an equivalent of `parse` for XML that can extract the comment?
- Python 3.6: Take advantage of PEP 495 when handling naïve datetimes

Commands
--------
- Add a `javaproperties` command
    - Give `get` an `-n|--no-newline` option?
    - Give `get` an `-o|--outfile <file>` option?
    - `get -P`: Include a timestamp (and support `--preserve-timestamp`)
    - Give `set` and `delete` `--in-place | --outfile <file>` options (with a
      `backup <file>` option for use with `--in-place`)
    - Give `set` and `delete` options for reformatting/not preserving
      formatting?
    - Give `format` a `--preserve-timestamp` option
    - Add options for completely suppressing the timestamp?
    - `get`: What effect should `-E` have on the output encoding when `-P` is
      given?
    - Split `get`'s `-P` functionality into a `select` command?

- Support XML properties files:
    - Support converting between JSON and XML properties
    - Add a command for converting between XML format and "plain" format?
    - Support autodetecting whether a properties file is in XML based on file
      extension (or other means?) ?
    - Support by just adding `properties2xml` and `xml2properties` commands?
