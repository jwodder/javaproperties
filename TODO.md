- Write tests
    - Test reading & writing bytes in both Python 2 and Python 3
    - Test reading & writing surrogate pairs
    - Test reading & writing unpaired surrogates
    - Test `load` and `dump` on actual files???
    - Test reading & writing XML in various encodings
    - Test writing the current timestamp with & without python-dateutil
      installed?
    - cf. the tests used in OpenJDK: <http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/tip/test/java/util/Properties>
- Add docstrings
    - Add a module docstring to `__init__.py`
- Add a README
- Set up a Readthedocs site?
- Handle "narrow" Python builds (only for Python versions < 3.3)
- Support Python 3.2?
- Force use of the C locale when generating timestamps
    - cf. <http://stackoverflow.com/a/24070673/744178>
    - Use Babel <http://babel.pocoo.org> ?
- Rename `load_items3` (to `parse`? `scan`? `_load`?)
- Use `lxml` for XML processing if it's installed?
- Look into minimum version requirements for python-dateutil

New Features
------------
- `dump`: Support writing `str`s in Python 2
- Implement `Properties.list`?
- Give the dump functions `ensure_ascii` arguments
- Give `load` and `loads` a `timestamp_key`(?) argument that, if supplied,
  causes the timestamp in a .properties file to be extracted and saved in the
  given key
- Add a variant of `join_key_value` that escapes as few characters as possible?
- Add an inverse of `load_items3` for writing triples?
- Should there be a variant of `dump` (or `dumps`?) that outputs Unicode and
  leaves non-Latin-1 characters as-is?  (cf. the different `store` methods of
  the Java class)
- Should there be a variant of `dumps` that outputs bytes?
- Add string-reading equivalent of `load_items3`?
- Add an equivalent of `load_items3` for XML that can extract the comment?

Commands
--------
- Add a `javaproperties` command (as `javaproperties.__main__`?) with the
  following subcommands:

        get [--defaults <file>] [--no-newline] [--no-key] <file> <key> ...

        set [--in-place | --outfile <file>] [--backup <file>] <file> <key> <value>
        # Include an option for controlling whether to update the timestamp
        # Include an option for setting the separator

        # Deleting entries; rename "del"? "delete"?:
        unset [--in-place | --outfile <file>] [--backup <file>] <file> <key> ...
        # Include an option for controlling whether to update the timestamp

    - Give all of the subcommands options for controlling whether escape
      sequences in keys & values on the command line should be interpolated or
      used literally

- Give all commands `--help` options
- Move the command-line commands back to the top level of the package so that
  they can be invoked with `python -m javaproperties.COMMAND` instead of
  `python -m javaproperties.commands.COMMAND`?
- Support autodetecting whether a properties file is in XML based on file
  extension (or other means?) ?
