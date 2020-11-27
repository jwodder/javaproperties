- Write tests
    - Test reading & writing bytes
    - Run doctest on the README examples somehow?
    - Test `dump()` and `load()`
- Add docstrings for the private functions
- Try to include the line number (and column number and filename?) in
  `InvalidUEscapeError`s
- Update `Properties` to match the latest Java version?

New Features
------------
- Give `load` and `loads` a `timestamp_hook` argument for specifying a callable
  to pass the file's timestamp (if any) to
    - The timestamp is passed as an unparsed string with leading `#` and
      trailing newline (and other whitespace?) removed
- Add an equivalent of `parse()` for XML that can extract the comment?
- Export `getproperties` and `setproperties` from `javaproperties-cli`?
- `PropertiesFile`:
    - Support XML
    - Support getting, setting, & deleting individual comments
    - Support inserting key-value pairs at specific locations?
    - Support concatenating two `PropertiesFile`s?
    - Add an option for preserving the separator used in the input when
      overwriting a key-value pair?
    - When setting a key's value, add a way to specify whether to take the
      place of the first occurrence of the key or the last
    - Add a method for reformatting in-place?
    - Add a method for deleting all but a given set of keys?
    - Support setting the separator and `ensure_ascii` on a per-entry basis?
- Give `escape()` an option (named `is_value`? `escape_spaces`?) for
  controlling whether to perform the more minimal escaping used for values
  rather than keys
- Instead of accepting file-like objects with `readline()` methods, accept
  iterables of `str`/`bytes`?
