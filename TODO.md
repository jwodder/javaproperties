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
    - Look for an official term for the "plain" format ("simple line-oriented
      format"?)
- Handle "narrow" Python builds (only for Python versions < 3.3)
- Handle files with CR line endings not opened in universal newlines mode?
- Test against & add support for pypy?
- Use `lxml` for XML processing if it's installed?
- Raise an error/warning if an invalid separator is passed to a function and/or
  command-line program?
- Restrict `TIMESTAMP_RGX` to only match C locale timestamps?
- Restrict `TIMESTAMP_RGX` to only consider `[ \t\f]` as whitespace?
- Export (and test) `getproperties` and `setproperties`?

New Features
------------
- `dump`: Support writing `str`s in Python 2
- Implement `Properties.list`?
- Give the dump functions `ensure_ascii` arguments
- Give the dump functions `keep_unicode`(?) arguments (mutually exclusive with
  `ensure_ascii`) for outputting Unicode and leaving non-Latin-1 characters
  as-is  (cf. the different `store` methods of the Java class)
- Give `load` and `loads` a `timestamp_hook` argument for specifying a callable
  to pass the file's timestamp (if any) to
    - The timestamp is passed as an unparsed string with leading `#` and
      trailing newline (and other whitespace?) removed
- Add a variant of `join_key_value` that escapes as few characters as possible?
- Add an inverse of `parse` for writing triples?
- Add a string-reading equivalent of `parse`?
- Add an equivalent of `parse` for XML that can extract the comment?
- Python 3.6: Take advantage of PEP 495 when handling naïve datetimes

Commands
--------
- `javaproperties`:
    - Give `get` an `-n|--no-newline` option?
    - Give `get` a `-0|--null` option?
    - Give `set`, `delete`, and `format` (and `select`?) `--in-place` options
      (with optional `--backup <file>`) as an alternative to `--outfile`
    - Give `set` and `delete` options for reformatting/not preserving
      formatting?
    - Give `format` and `select` `--preserve-timestamp` options
    - Add options for completely suppressing the timestamp?
    - Give `select` an option for preserving formatting? (Preserve by default?)

- Support XML properties files:
    - Support converting between JSON and XML properties
    - Add a command for converting between XML format and "plain" format
    - Support autodetecting whether a properties file is in XML based on file
      extension (or other means?) ?
    - Support by just adding `properties2xml` and `xml2properties` commands?
