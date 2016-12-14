- Write tests
    - Test reading & writing bytes in both Python 2 and Python 3
    - Test utility functions in isolation?
    - Test the command-line programs
        - Handle the fact that `output_bytes` will contain CR LF line endings
          (I think) on Windows
    - Test the command-line programs' nontrivial components (e.g.,
      `setproperties`) in isolation?
    - Test `properties2json` and `json2properties`
    - Run doctest on the README examples somehow?
    - Test the `Properties` class
    - Make sure that the CLI tests that assume UTF-8 encoding for I/O will work
      on non-sane platforms
- Documentation:
    - Add docstrings for the private functions
    - Include examples in main docs?
    - Look for an official term for the "plain" format ("simple line-oriented
      format"?)
- Handle "narrow" Python builds (only for Python versions < 3.3)
- Test against & add support for pypy?
- Restrict `TIMESTAMP_RGX` to only match C locale timestamps?
- Restrict `TIMESTAMP_RGX` to only consider `[ \t\f]` as whitespace?
- Split the CLI into a separate package???
- Generate manpages for the CLI commands?

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
- Add a string-reading equivalent of `parse`?
- Add an equivalent of `parse` for XML that can extract the comment?
- Python 3.6: Take advantage of PEP 495 when handling naïve datetimes
- Export `getproperties` and `setproperties`?

Commands
--------
- `javaproperties`:
    - Give `set`, `delete`, and `format` (and `select`?) `--in-place` options
      (with optional `--backup <file>`) as an alternative to `--outfile`
    - Give `set` and `delete` a `--format` option for also reformatting
    - Give `format` and `select` `--preserve-timestamp` options
    - Add options for completely suppressing the timestamp
    - Give `select` an option for preserving formatting? (Preserve by default?)
    - `select`: Don't output a timestamp if none of the given keys are defined?
    - Give `get` an option for escaping output values?

- Support XML properties files:
    - Support converting between JSON and XML properties
    - Add a command for converting between XML format and "plain" format
    - Support autodetecting whether a properties file is in XML based on file
      extension (or other means?) ?
    - Support by just adding `properties2xml` and `xml2properties` commands?

- Add a command for merging two (or more?) properties files?
