from   __future__ import print_function, unicode_literals
import argparse
import re
import sys
from   six        import iteritems
from   .reading   import load, parse
from   .writing   import join_key_value, _show_timestamp, to_comment
from   .util      import properties_reader, properties_writer, propout

def main():
    parser = argparse.ArgumentParser()
    cmds = parser.add_subparsers(title='command', dest='cmd')
    cmd_get = cmds.add_parser('get')
    cmd_get.add_argument('-P', '--properties', action='store_true')
    cmd_get.add_argument('file', type=properties_reader)
    cmd_get.add_argument('key', nargs='+')
    cmd_set = cmds.add_parser('set')
    cmd_set.add_argument('-o', '--outfile', type=properties_writer,
                         default=propout)
    cmd_set.add_argument('-T', '--preserve-timestamp', action='store_true')
    cmd_set.add_argument('file', type=properties_reader)
    cmd_set.add_argument('key')
    cmd_set.add_argument('value')
    cmd_del = cmds.add_parser('delete')
    cmd_del.add_argument('-o', '--outfile', type=properties_writer,
                         default=propout)
    cmd_del.add_argument('-T', '--preserve-timestamp', action='store_true')
    cmd_del.add_argument('file', type=properties_reader)
    cmd_del.add_argument('key', nargs='+')
    args = parser.parse_args()
    if args.cmd == 'get':
        ok = True
        props = load(args.file)
        for k in args.key:
            if k in props:
                if args.properties:
                    print(join_key_value(k, props[k]))
                else:
                    print(props[k])
            else:
                print('javaproperties: {0!r}: key not found'.format(k),
                      file=sys.stderr)
                ok = False
        sys.exit(0 if ok else 1)
    elif args.cmd == 'set':
        setproperty(args.file, args.outfile, {args.key: args.value},
                    args.preserve_timestamp)
    elif args.cmd == 'delete':
        setproperty(args.file, args.outfile, {k: None for k in args.key},
                    args.preserve_timestamp)
    else:
        assert False, 'No path defined for command {0!r}'.format(args.cmd)

TIMESTAMP_RGX = r'^\s*[#!]\s*\w+ \w+ [ \d]?\d \d\d:\d\d:\d\d \w+ \d{4,}\s*$'

def setproperty(fpin, fpout, newprops, preserve_timestamp=False):
    in_header = True
    prevsrc = None
    for k, v, src in parse(fpin):
        if in_header:
            if k is None:
                if prevsrc is not None:
                    print(prevsrc, end='', file=fpout)
                prevsrc = src
                continue
            else:
                if prevsrc is not None:
                    if preserve_timestamp:
                        print(prevsrc, end='', file=fpout)
                    else:
                        if not re.match(TIMESTAMP_RGX, prevsrc, flags=re.U):
                            print(prevsrc, end='', file=fpout)
                        print(to_comment(_show_timestamp(True)), file=fpout)
                elif not preserve_timestamp:
                    print(to_comment(_show_timestamp(True)), file=fpout)
                in_header = False
        if k in newprops:
            if newprops[k] is not None:
                print(join_key_value(k, newprops[k]), file=fpout)
                newprops[k] = None
        else:
            print(src, end='', file=fpout)
    for key, value in iteritems(newprops):
        if value is not None:
            print(join_key_value(key, value), file=fpout)

if __name__ == '__main__':
    main()
