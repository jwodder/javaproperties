from   __future__ import print_function, unicode_literals
import argparse
import sys
from   six        import iteritems
from   .reading   import load, parse
from   .writing   import join_key_value
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
    cmd_set.add_argument('file', type=properties_reader)
    cmd_set.add_argument('key')
    cmd_set.add_argument('value')
    cmd_del = cmds.add_parser('delete')
    cmd_del.add_argument('-o', '--outfile', type=properties_writer,
                         default=propout)
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
                print('{0}: {1!r}: key not found'.format(sys.argv[0], k),
                      file=sys.stderr)
                ok = False
        sys.exit(0 if ok else 1)
    elif args.cmd == 'set':
        setproperty(args.file, args.outfile, {args.key: args.value})
    elif args.cmd == 'delete':
        setproperty(args.file, args.outfile, {k: None for k in args.key})
    else:
        assert False, 'No path defined for command {0!r}'.format(args.cmd)

def setproperty(fpin, fpout, newprops):
    for k, v, src in parse(fpin):
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
