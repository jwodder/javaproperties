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

import json
import click
from   .        import __version__
from   .reading import load
from   .util    import infile_type

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('-E', '--encoding', default='iso-8859-1', show_default=True,
              help='Encoding of the .properties file')
@click.argument('infile', type=infile_type, default='-')
@click.argument('outfile', type=click.File('w'), default='-')
@click.version_option(__version__, '-V', '--version',
                      message='%(prog)s %(version)s')
def tojson(infile, outfile, encoding):
    """Convert a Java .properties file to JSON"""
    with click.open_file(infile, encoding=encoding) as fp:
        props = load(fp)
    with outfile:
        json.dump(props, outfile, sort_keys=True, indent=4,
                  separators=(',', ': '))
        outfile.write('\n')

if __name__ == '__main__':
    tojson()
