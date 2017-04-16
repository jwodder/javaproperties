- Write tests
    - Test reading & writing bytes in both Python 2 and Python 3
    - Test utility functions in isolation
    - Run doctest on the README examples somehow?
    - Test the `Properties` class
    - Test on Windows with Appveyor?
- Documentation:
    - Add docstrings for the private functions
    - Include examples in main docs?
- Handle "narrow" Python builds (only for Python versions < 3.3)

New Features
------------
- `dump`: Support writing `str`s in Python 2
    - Use `unicode_literals` less?
- Implement `Properties.list`?
- Give the dump functions `charset` and `comment_charset` arguments for
  specifying what characters to convert to `\uXXXX` escapes and what not;
  possible values: `ASCII = 'ascii'`, `LATIN_1 = 'latin-1'`, `BMP = 'bmp'`,
  `UNICODE = 'unicode'`
- Give `load` and `loads` a `timestamp_hook` argument for specifying a callable
  to pass the file's timestamp (if any) to
    - The timestamp is passed as an unparsed string with leading `#` and
      trailing newline (and other whitespace?) removed
- Add a variant of `join_key_value` that escapes as few characters as possible?
- Add a string-reading equivalent of `parse`?
- Add an equivalent of `parse` for XML that can extract the comment?
- Python 3.6: Take advantage of PEP 495 when handling naïve datetimes
- Export `getproperties` and `setproperties`
- Make `parse` return a generator of `KeyValue`, `Whitespace`, and `Comment`
  objects?
    - Give `Comment` an `is_timestamp()` method
