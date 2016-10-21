- Write tests
    - Test reading & writing bytes in both Python 2 and Python 3
    - Test utility functions in isolation?
    - Test the command-line programs (or at least their nontrivial components,
      like `setproperty`)
    - Run doctest on the README examples
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
        - Mention that all uses of "whitespace" in the documentation
          specifically refer to CR, LF, FF, TAB, and space
    - Include examples in main docs?
    - Document `javaproperties` command
    - Fill in the commands' arguments' `help` and `description` fields
- Handle "narrow" Python builds (only for Python versions < 3.3)
- Handle files with CR line endings not opened in universal newlines mode?
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
- Add a `javaproperties` command
    - Give all of the subcommands options (`-e`?) for controlling whether
      escape sequences in keys & values on the command line should be
      interpolated or used literally
    - Give `get` an `-n|--no-newline` option?
    - Give `get` an `-o|--outfile <file>` option?
    - `get -P`: Include a timestamp
    - Give `set` and `delete` `--in-place | --outfile <file>` options (with a
      `backup <file>` option for use with `--in-place`)
    - Give `set` an option for setting the separator?
    - Give `set` and `delete` options for reformatting/not preserving
      formatting?
    - Give `format` an option for setting the separator?
    - Give `format` a `--preserve-timestamp` option
    - Add options for completely suppressing the timestamp?
    - Python 2: Handle `sys.argv` encoding

- Support converting between JSON and XML properties
- Support autodetecting whether a properties file is in XML based on file
  extension (or other means?) ?
- Add a command for converting between XML format and "plain" format?
- Give the commands options for setting the properties files' encodings?
