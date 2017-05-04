- Write tests
    - Test reading & writing bytes in both Python 2 and Python 3
    - Test utility functions in isolation
    - Run doctest on the README examples somehow?
    - Test the `Properties` class
    - Test on Windows with Appveyor?
    - Test `parse` (primarily handling of comments/blanks, repeated keys, and
      backslash at EOF)
- Documentation:
    - Add docstrings for the private functions
    - Include examples in main docs?
    - Add an example of each format to the format descriptions
- Handle "narrow" Python builds (only for Python versions < 3.3)
- Give `PropertiesFile` a decent `__repr__`
- Try to include the line number (and column number and filename?) in
  `InvalidUEscapeError`s

New Features
------------
- `dump`: Support writing `str`s in Python 2
    - Use `unicode_literals` less?
- Implement `Properties.list`?
- Give the dump functions `charset` and `comment_charset` arguments for
  specifying what characters to convert to `\uXXXX` escapes and what not;
  possible values: `ASCII = 'ascii'`, `LATIN_1 = 'latin-1'`, `UNICODE_BMP =
  'unicode_bmp'`, `UNICODE = 'unicode'`
- Give `load` and `loads` a `timestamp_hook` argument for specifying a callable
  to pass the file's timestamp (if any) to
    - The timestamp is passed as an unparsed string with leading `#` and
      trailing newline (and other whitespace?) removed
- Add a variant of `join_key_value` that escapes as few characters as possible?
- Add a string-reading equivalent of `parse`?
- Add an equivalent of `parse` for XML that can extract the comment?
- Python 3.6: Take advantage of PEP 495 when handling naïve datetimes
- Export `getproperties` and `setproperties` from `javaproperties-cli`?
- Make `parse` return a generator of `KeyValue`, `Whitespace`, and `Comment`
  objects?
    - Give `Comment` an `is_timestamp()` method
- `PropertiesFile`:
    - Support getting, setting (including in `dump`), & deleting the timestamp
        - Use the last timestamp-like line as the value of the timestamp when
          getting but the first timestamp-like line for the location when
          setting, like is done for repeated keys?
    - Support XML
    - Support getting, setting, & deleting comments
    - Support inserting key-value pairs at specific locations?
    - Support concatenating two `PropertiesFile`s?
    - Add an option for preserving the separator used in the input when
      overwriting a key-value pair?
