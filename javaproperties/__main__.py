from   __future__ import print_function
import re
import click
from   six        import iteritems
from   .          import __version__
from   .reading   import load, parse, unescape
from   .writing   import dump, join_key_value, java_timestamp, to_comment
from   .util      import infile_type, outfile_type

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, '-V', '--version',
                      message='%(prog)s %(version)s')
def javaproperties():
    """ Basic manipulation of Java .properties files """
    pass

@javaproperties.command()
@click.option('-d', '--default-value', metavar='VALUE',
              help='Default value for undefined keys')
@click.option('-D', '--defaults', metavar='FILE', type=infile_type,
              help='.properties file of default values')
@click.option('-e', '--escaped', is_flag=True,
              help='Parse command-line keys & values for escapes')
@click.option('-E', '--encoding', default='iso-8859-1', show_default=True,
              help='Encoding of the .properties files')
@click.option('-P', '--properties', 'as_prop', is_flag=True,
              help='Output a full .properties file instead of just values')
@click.option('-s', '--separator', default='=', show_default=True,
              help='Key-value separator to use in output')
@click.argument('file', type=infile_type)
@click.argument('key', nargs=-1, required=True)
@click.pass_context
def get(ctx, default_value, defaults, escaped, as_prop, separator, file, key,
        encoding):
    """ Query values from a Java .properties file """
    ok = True
    if escaped:
        key = list(map(unescape, key))
        if default_value is not None:
            default_value = unescape(default_value)
    with click.open_file(file, encoding=encoding) as fp:
        props = getproperties(fp, key)
    if defaults is not None:
        with click.open_file(defaults, encoding=encoding) as fp:
            defaults = getproperties(fp, key)
    else:
        defaults = {}
    for k in key:
        v = default_value
        if k in props:
            v = props[k]
        elif k in defaults:
            v = defaults[k]
        if v is None:
            click.echo('javaproperties: {0}: key not found'.format(k), err=True)
            ok = False
        elif as_prop:
            click.echo(join_key_value(k, v, separator=separator))
        else:
            click.echo(v)
    ctx.exit(0 if ok else 1)

@javaproperties.command('set')
@click.option('-e', '--escaped', is_flag=True,
              help='Parse command-line keys & values for escapes')
@click.option('-E', '--encoding', default='iso-8859-1', show_default=True,
              help='Encoding of the .properties files')
@click.option('-s', '--separator', default='=', show_default=True,
              help='Key-value separator to use in output')
@click.option('-o', '--outfile', type=outfile_type, default='-',
              help='Write output to this file')
@click.option('-T', '--preserve-timestamp', is_flag=True,
              help='Keep the timestamp from the input file')
@click.argument('file', type=infile_type)
@click.argument('key')
@click.argument('value')
def setprop(escaped, separator, outfile, preserve_timestamp, file, key, value,
            encoding):
    """ Set values in a Java .properties file """
    if escaped:
        key = unescape(key)
        value = unescape(value)
    with click.open_file(file, encoding=encoding) as fpin:
        with click.open_file(outfile, 'w', encoding=encoding) as fpout:
            setproperties(fpin, fpout, {key: value}, preserve_timestamp,
                          separator)

@javaproperties.command()
@click.option('-e', '--escaped', is_flag=True,
              help='Parse command-line keys & values for escapes')
@click.option('-E', '--encoding', default='iso-8859-1', show_default=True,
              help='Encoding of the .properties files')
@click.option('-o', '--outfile', type=outfile_type, default='-',
              help='Write output to this file')
@click.option('-T', '--preserve-timestamp', is_flag=True,
              help='Keep the timestamp from the input file')
@click.argument('file', type=infile_type)
@click.argument('key', nargs=-1, required=True)
def delete(escaped, outfile, preserve_timestamp, file, key, encoding):
    """ Remove values from a Java .properties file """
    if escaped:
        key = list(map(unescape, key))
    with click.open_file(file, encoding=encoding) as fpin:
        with click.open_file(outfile, 'w', encoding=encoding) as fpout:
            setproperties(fpin, fpout, dict.fromkeys(key), preserve_timestamp)

@javaproperties.command()
@click.option('-E', '--encoding', default='iso-8859-1', show_default=True,
              help='Encoding of the .properties files')
@click.option('-o', '--outfile', type=outfile_type, default='-',
              help='Write output to this file')
@click.option('-s', '--separator', default='=', show_default=True,
              help='Key-value separator to use in output')
@click.argument('file', type=infile_type, default='-')
def format(outfile, separator, file, encoding):
    """ Format/"canonicalize" a Java .properties file """
    with click.open_file(file, encoding=encoding) as fpin:
        with click.open_file(outfile, 'w', encoding=encoding) as fpout:
            dump(load(fpin), fpout, sort_keys=True, separator=separator)

def getproperties(fp, keys):
    keys = set(keys)
    def getprops(seq):
        props = {}
        for k,v in seq:
            if k in keys:
                props[k] = v
        return props
    return load(fp, object_pairs_hook=getprops)

TIMESTAMP_RGX = r'^\s*[#!]\s*\w+ \w+ [ \d]?\d \d\d:\d\d:\d\d \w* \d{4,}\s*$'

def setproperties(fpin, fpout, newprops, preserve_timestamp=False,
                  separator='='):
    in_header = True
    prevsrc = None
    for k, _, src in parse(fpin):
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
                        print(to_comment(java_timestamp()), file=fpout)
                elif not preserve_timestamp:
                    print(to_comment(java_timestamp()), file=fpout)
                in_header = False
        if k in newprops:
            if newprops[k] is not None:
                print(join_key_value(k, newprops[k], separator=separator),
                      file=fpout)
                newprops[k] = None
        else:
            # In case the last line of the file ends with a trailing line
            # continuation:
            src = re.sub(r'(?<!\\)((?:\\\\)*)\\$', r'\1', src)
            print(src.rstrip('\r\n'), file=fpout)
    for key, value in iteritems(newprops):
        if value is not None:
            print(join_key_value(key, value, separator=separator), file=fpout)

if __name__ == '__main__':
    javaproperties()
