#!/usr/bin/python
import codecs
import io
import json
import sys
from   six      import iteritems, string_types
from   .writing import write_properties

def main():
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        infile = open(sys.argv[1], 'r')
    else:
        infile = sys.stdin

    if len(sys.argv) > 2 and sys.argv[2] != "-":
        outfile = io.open(sys.argv[2], 'wU', encoding='iso-8859-1')
    else:
        outfile = sys.stdout
        if sys.version_info[0] >= 3:
            outfile = outfile.buffer
        ### TODO: Enable universal newlines mode
        outfile = codecs.getwriter('iso-8859-1')(outfile)

    with infile, outfile:
        props = json.load(infile)
        for k,v in iteritems(props):
            if isinstance(v, (list, dict)):
                raise TypeError('Cannot convert lists & dicts to .properties strings')
            elif not isinstance(v, string_types):
                props[k] = json.dumps(v)
        write_properties(props, outfile)

if __name__ == '__main__':
    main()
