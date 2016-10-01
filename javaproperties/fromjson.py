#!/usr/bin/python
import codecs
import io
import json
import sys
from   .util    import strify_dict
from   .writing import dump

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
        outfile = codecs.getwriter('iso-8859-1')(outfile)
    with infile:
        props = json.load(infile)
    if not isinstance(props, dict):
        raise TypeError('Can only convert dicts to .properties files')
    with outfile:
        dump(sorted(strify_dict(props).items()), outfile)

if __name__ == '__main__':
    main()
