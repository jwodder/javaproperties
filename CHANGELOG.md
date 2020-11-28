v0.8.0 (in development)
-----------------------
- Drop support for Python 2.7, 3.4, and 3.5
- Support Python 3.9
- `ensure_ascii` parameter added to `PropertiesFile.dump()` and
  `PropertiesFile.dumps()`
- **Bugfix**: When parsing XML input, empty `<entry>` tags now produce an empty
  string as a value, not `None`
- Added type annotations
- `Properties` and `PropertiesFile` no longer raise `TypeError` when given a
  non-string key or value, as type correctness is now expected to be enforced
  through static type checking
- The `PropertiesElement` classes returned by `parse()` are no longer
  subclasses of `namedtuple`, but they can still be iterated over to retrieve
  their fields like a tuple

v0.7.0 (2020-03-09)
-------------------
- `parse()` now accepts strings as input
- **Breaking**: `parse()` now returns a generator of custom objects instead of
  triples of strings
- Gave `PropertiesFile` a settable `timestamp` property
- Gave `PropertiesFile` a settable `header_comment` property
- Handle unescaping surrogate pairs on narrow Python builds

v0.6.0 (2020-02-28)
-------------------
- Include changelog in the Read the Docs site
- Support Python 3.8
- When dumping a value that begins with more than one space, only escape the
  first space in order to better match Java's behavior
- Gave `dump()`, `dumps()`, `escape()`, and `join_key_value()` an
  `ensure_ascii` parameter for optionally not escaping non-ASCII characters in
  output
- Gave `dump()` and `dumps()` an `ensure_ascii_comments` parameter for
  controlling what characters in the `comments` parameter are escaped
- Gave `to_comment()` an `ensure_ascii` parameter for controlling what
  characters are escaped
- Added a custom encoding error handler `'javapropertiesreplace'` that encodes
  invalid characters as `\uXXXX` escape sequences

v0.5.2 (2019-04-08)
-------------------
- Added an example of each format to the format descriptions in the docs
- Fix building in non-UTF-8 environments

v0.5.1 (2018-10-25)
-------------------
- **Bugfix**: `java_timestamp()` now properly handles naïve `datetime` objects
  with `fold=1`
- Include installation instructions, examples, and GitHub links in the Read the
  Docs site

v0.5.0 (2018-09-18)
-------------------
- **Breaking**: Invalid `\uXXXX` escape sequences now cause an
  `InvalidUEscapeError` to be raised
- `Properties` instances can now compare equal to `dict`s and other mapping
  types
- Gave `Properties` a `copy` method
- Drop support for Python 2.6 and 3.3
- Fixed a `DeprecationWarning` in Python 3.7

v0.4.0 (2017-04-22)
-------------------
- Split off the command-line programs into a separate package,
  [`javaproperties-cli`](https://github.com/jwodder/javaproperties-cli)

v0.3.0 (2017-04-13)
-------------------
- Added the `PropertiesFile` class for preserving comments in files [#1]
- The `ordereddict` package is now required under Python 2.6

v0.2.1 (2017-03-20)
-------------------
- **Bugfix** to `javaproperties` command: Don't die horribly on missing
  non-ASCII keys
- PyPy now supported

v0.2.0 (2016-11-14)
-------------------
- Added a `javaproperties` command for basic command-line manipulating of
  `.properties` files
- Gave `json2properties` a `--separator` option
- Gave `json2properties` and `properties2json` `--encoding` options
- Exported the `java_timestamp()` function
- `to_comment` now converts CR LF and CR line endings inside comments to LF
- Some minor documentation improvements

v0.1.0 (2016-10-02)
-------------------
Initial release
