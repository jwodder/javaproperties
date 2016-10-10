- Write tests
    - Test reading & writing bytes in both Python 2 and Python 3
    - Test `load` and `dump` on actual files???
    - Test utility functions in isolation?
    - cf. the tests used in OpenJDK: <http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/tip/test/java/util/Properties>
- Documentation:
    - Add docstrings for the private functions
    - Fix the Sphinx HTML documentation sidebar
    - Figure out exactly what types of filehandles & strings
      `xml.etree.ElementTree` can parse and add them to the `load*_xml` and
      `loadFromXML` documentation
    - Add simple descriptions of/introductions to the `.properties` and XML
      formats to the documentation sections for reading & writing the
      respective formats
    - Include examples in main docs?
        - Use doctest on examples?
    - Add module docstrings to `fromjson.py` and `tojson.py`
    - Document `javaproperties` command
    - Fill in the commands' `help` and `description` fields
- Handle "narrow" Python builds (only for Python versions < 3.3)
- Support Python 3.2?
- Handle files with CR line endings not opened in universal newlines mode?
- Force use of the C locale when generating timestamps
    - cf. <http://stackoverflow.com/a/24070673/744178>
    - Use Babel <http://babel.pocoo.org> ?
- Use `lxml` for XML processing if it's installed?
- Look into the minimum version of the argparse package needed for Python 2.6
    - v1.1 or higher is required for `argparse.ArgumentTypeError`

New Features
------------
- `dump`: Support writing `str`s in Python 2
- Implement `Properties.list`?
- Give the dump functions `ensure_ascii` arguments
- Give the dump functions `keep_unicode`(?) arguments (mutually exclusive with
  `ensure_ascii`) for outputting Unicode and leaving non-Latin-1 characters
  as-is  (cf. the different `store` methods of the Java class)
- Give `load` and `loads` a `timestamp_key`(?) argument that, if supplied,
  causes the timestamp in a .properties file to be extracted and saved in the
  given key
- Add a variant of `join_key_value` that escapes as few characters as possible?
- Add an inverse of `parse` for writing triples?
- Add a string-reading equivalent of `parse`?
- Add an equivalent of `parse` for XML that can extract the comment?
- Python 3.6: Take advantage of PEP 495 when handling naïve datetimes

Commands
--------
- Add a `javaproperties` command (as `javaproperties.__main__`?) with the
  following subcommands:

        get [-D|--defaults <file>]
            [-d|--default <value>]
            [-P|--properties]
            [-o|--outfile <file>]  # ?
            [-n|--no-newline]
            <file> <key> ...

        set [--in-place | --outfile <file>]
            [--backup <file>]
            # Include an option for setting the separator
            <file> <key> <value>

        delete [--in-place | --outfile <file>]
               [--backup <file>]
               <file> <key> ...

    - Give all of the subcommands options (`-e`?) for controlling whether
      escape sequences in keys & values on the command line should be
      interpolated or used literally
    - Give `set` and `unset` options for controlling whether to update the
      timestamp (`-T`/`--preserve-timestamp`?)

- Support converting between JSON and XML properties
- Support autodetecting whether a properties file is in XML based on file
  extension (or other means?) ?
- Add a command for converting between XML format and "plain" format?
- Give the commands options for setting the properties files' encodings?
