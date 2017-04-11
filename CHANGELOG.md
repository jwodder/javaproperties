v0.3.0 (in development)
-----------------------
- Added `PropertiesFile` class for preserving comments in files [#1]
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
