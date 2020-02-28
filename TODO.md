- Write tests
    - Test reading & writing bytes in both Python 2 and Python 3
    - Run doctest on the README examples somehow?
    - Test `parse()` (primarily handling of comments/blanks, repeated keys, and
      backslash at EOF)
    - Test `dump()` and `load()`
- Documentation:
    - Add docstrings for the private functions
- Try to include the line number (and column number and filename?) in
  `InvalidUEscapeError`s
- Update `Properties` to match the latest Java version?

New Features
------------
- `dump()`: Support `str`s as input in Python 2
    - Use `unicode_literals` less?
- Give `load` and `loads` a `timestamp_hook` argument for specifying a callable
  to pass the file's timestamp (if any) to
    - The timestamp is passed as an unparsed string with leading `#` and
      trailing newline (and other whitespace?) removed
- Make `parse()` accept strings as input
- Add an equivalent of `parse()` for XML that can extract the comment?
- Export `getproperties` and `setproperties` from `javaproperties-cli`?
- Make `parse` return a generator of `KeyValue`, `Whitespace`, and `Comment`
  objects?
    - Give `Comment` an `is_timestamp()` method
    - All objects have a `source: str` attribute (including trailing newline)
    - Give `Comment` an attribute for getting the text without the leading `#`
      or `!` (and with escapes unescaped?) ?
    - `KeyValue` objects have `key` and `value` attributes storing the
      unescaped values
    - Give `KeyValue` objects an attribute for whether they end with a trailing
      line continuation? / an attribute for the `source` without any trailing
      continuations (and also without trailing newline?) ?
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
    - Should instances stringify to their `dump` representations?
- Should `Properties` instances stringify to their `dump` representations?
- Give `escape()` an option (named `is_value`? `escape_spaces`?) for
  controlling whether to perform the more minimal escaping used for values
  rather than keys
