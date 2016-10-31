"""
:program:`properties2json`
--------------------------

.. code-block:: shell

    python -m javaproperties.tojson [infile [outfile]]
    # or, if the javaproperties package was properly installed:
    properties2json [infile [outfile]]

Convert a Latin-1 ``.properties`` file :option:`infile` to a JSON object and
write the results to :option:`outfile`.  If not specified, :option:`infile` and
:option:`outfile` default to `sys.stdin` and `sys.stdout`, respectively.
"""

import argparse
import json
import sys
from   .        import __version__
from   .reading import load
from   .util    import properties_reader, propin

def main():
    parser = argparse.ArgumentParser(
        description='Convert a Java .properties file to JSON'
    )
    parser.add_argument('-V', '--version', action='version',
                        version='javaproperties ' + __version__)
    parser.add_argument('infile', nargs='?', type=properties_reader,
                        default=propin, help='Properties file')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, help='JSON file')
    args = parser.parse_args()
    with args.infile:
        props = load(args.infile)
    with args.outfile:
        json.dump(props, args.outfile, sort_keys=True, indent=4,
                                       separators=(',', ': '))
        args.outfile.write('\n')

if __name__ == '__main__':
    main()
