- Add functions for reading from & writing to strings instead of files?
- Add a setup.py file
    - requirement: six
    - extra requirement: python-dateutil
- Write tests
    - Test working with both `str` and `unicode` in Python 2
    - Test reading & writing surrogate pairs
    - Test reading & writing unpaired surrogates
    - cf. the tests used in OpenJDK?
- Add docstrings
- Add a command for converting JSON to .properties (stringifying scalar values,
  erroring on aggregate values)
    - Add a function (`dict2properties`?) that converts a `dict` to .properties
      using the same rules?
- Add a command for setting/unsetting entries in a .properties file:

        setproperty [-d] [-i | -o <outfile>] <file> <key> [<value>]

    - Include an option for setting whether to update the timestamp?

- Add a command for printing out specified values in a .properties file?
- Add a variant of `join_key_value` that escapes as few characters as possible?
- Add an inverse of `parse_properties` for writing triples?
- Support `str` keys & values for `Properties` in Python 2?
