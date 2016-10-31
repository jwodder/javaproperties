"""
:program:`json2properties`
--------------------------

.. code-block:: shell

    python -m javaproperties.fromjson [-s|--separator <sep>] [infile [outfile]]
    # or, if the javaproperties package was properly installed:
    json2properties [-s|--separator <sep>] [infile [outfile]]

Convert a JSON file :option:`infile` to a Latin-1 ``.properties`` file and
write the results to :option:`outfile`.  If not specified, :option:`infile` and
:option:`outfile` default to `sys.stdin` and `sys.stdout`, respectively.

The JSON document must be an object with scalar (i.e., string, numeric,
boolean, and/or null) values; anything else will result in an error.

Output is sorted by key, and numeric, boolean, & null values are output using
their JSON representations; e.g., the input:

.. code-block:: json

    {
        "yes": true,
        "no": "false",
        "nothing": null
    }

becomes:

.. code-block:: properties

    #Mon Sep 26 18:57:44 UTC 2016
    no=false
    nothing=null
    yes=true

The key-value separator used in the output defaults to ``=`` and can be
overridden with the :option:`-s` or :option:`--separator` option; e.g.,
supplying ``--separator ': '`` on the command line with the above JSON file as
input produces:

.. code-block:: properties

    #Mon Sep 26 18:57:44 UTC 2016
    no: false
    nothing: null
    yes: true

.. versionchanged:: 0.2.0
    Added the :option:`--separator` option
"""

import argparse
from   decimal  import Decimal
import json
import sys
from   .        import __version__
from   .util    import strify_dict, properties_writer, propout
from   .writing import dump

def main():
    parser = argparse.ArgumentParser(
        description='Convert a JSON object to a Java .properties file'
    )
    parser.add_argument('-s', '--separator', default='=',
                        help='Key-value separator in output; default: "="')
    parser.add_argument('-V', '--version', action='version',
                        version='javaproperties ' + __version__)
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help='JSON file')
    parser.add_argument('outfile', nargs='?', type=properties_writer,
                        default=propout, help='Properties file')
    args = parser.parse_args()
    with args.infile:
        props = json.load(args.infile, parse_float=Decimal)
    if not isinstance(props, dict):
        sys.exit('json2properties: Only dicts can be converted to .properties')
    with args.outfile:
        dump(sorted(strify_dict(props).items()), args.outfile,
             separator=args.separator)

if __name__ == '__main__':
    main()
