import argparse
import json
import sys
from   .reading import load
from   .util    import properties_reader, propin

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=properties_reader,
                        default=propin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout)
    args = parser.parse_args()
    with args.infile:
        props = load(args.infile)
    with args.outfile:
        json.dump(props, args.outfile, sort_keys=True, indent=4,
                                       separators=(',', ': '))
        args.outfile.write('\n')

if __name__ == '__main__':
    main()
