from   __future__ import print_function, unicode_literals
import argparse
import codecs
import io
import sys
import six
from   .reading   import load, parse
from   .writing   import join_key_value

def main():
    stdout = sys.stdout if six.PY2 else sys.stdout.buffer
    stdout = codecs.getwriter('iso-8859-1')(stdout)
    parser = argparse.ArgumentParser()
    cmds = parser.add_subparsers(title='command', dest='cmd')
    cmd_get = cmds.add_parser('get')
    cmd_get.add_argument('-P', '--properties', action='store_true')
    cmd_get.add_argument('file', type=openR)
    cmd_get.add_argument('key', nargs='+')
    cmd_set = cmds.add_parser('set')
    cmd_set.add_argument('-o', '--outfile', type=openW, default=stdout)
    cmd_set.add_argument('file', type=openR)
    cmd_set.add_argument('key')
    cmd_set.add_argument('value')
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
        setproperty(args.file, args.outfile, args.key, args.value)
    else:
        assert False, 'No path defined for command {0!r}'.format(args.cmd)

def openR(fname):
    # based on argparse.FileType
    if fname == '-':
        stdin = sys.stdin if six.PY2 else sys.stdin.buffer
        return codecs.getreader('iso-8859-1')(stdin)
    else:
        try:
            return io.open(fname, 'rt', encoding='iso-8859-1')
        except IOError as e:
            raise argparse.ArgumentTypeError('{0}: {1}'.format(fname, e))

def openW(fname):
    # based on argparse.FileType
    if fname == '-':
        stdout = sys.stdout if six.PY2 else sys.stdout.buffer
        return codecs.getwriter('iso-8859-1')(stdout)
    else:
        try:
            return io.open(fname, 'wt', encoding='iso-8859-1')
        except IOError as e:
            raise argparse.ArgumentTypeError('{0}: {1}'.format(fname, e))

def setproperty(fpin, fpout, key, value):
    # `fpout` must be a text/unicode stream
    for k, v, src in parse(fpin):
        if k == key:
            if value is not None:
                print(join_key_value(key, value), file=fpout)
                value = None
        else:
            print(src, end='', file=fpout)
    if value is not None:
        print(join_key_value(key, value), file=fpout)

if __name__ == '__main__':
    main()
