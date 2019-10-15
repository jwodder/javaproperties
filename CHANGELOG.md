v0.6.0 (in development)
-----------------------
- Include changelog in the Read the Docs site
- Support Python 3.8

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
