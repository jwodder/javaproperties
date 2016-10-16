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
