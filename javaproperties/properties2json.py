#!/usr/bin/python
import json
import sys
from   .reading import read_properties

# cf. <https://github.com/simplejson/simplejson/blob/master/simplejson/tool.py>

def main():
    ### TODO: Read infile as Latin-1 with universal newlines!
    infile  = open(sys.argv[1], 'rb') if len(sys.argv) > 1 else sys.stdin
    outfile = open(sys.argv[2], 'wb') if len(sys.argv) > 2 else sys.stdout
    with infile, outfile:
        props = read_properties(infile)
        json.dump(props, outfile, sort_keys=True, indent=4,
                                  separators=(',', ': '))
        outfile.write('\n')

if __name__ == '__main__':
    main()
