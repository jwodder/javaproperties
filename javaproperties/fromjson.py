"""
:program:`json2properties`
--------------------------

.. code-block:: shell

    python -m javaproperties.fromjson [infile [outfile]]
    # or, if the javaproperties package was properly installed:
    json2properties [infile [outfile]]

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
"""

import argparse
from   decimal  import Decimal
import json
import sys
from   .util    import strify_dict, properties_writer, propout
from   .writing import dump

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=properties_writer,
                        default=propout)
    args = parser.parse_args()
    with args.infile:
        props = json.load(args.infile, parse_float=Decimal)
    if not isinstance(props, dict):
        raise TypeError('Can only convert dicts to .properties files')
    with args.outfile:
        dump(sorted(strify_dict(props).items()), args.outfile)

if __name__ == '__main__':
    main()
