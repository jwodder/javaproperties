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

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, '-V', '--version',
                      message='%(prog)s %(version)s')
@click.argument('infile', type=click.File('r', encoding='iso-8859-1'),
                default='-')
@click.argument('outfile', type=click.File('w'), default='-')
def tojson(infile, outfile):
    """Convert a Java .properties file to JSON"""
    with infile:
        props = load(infile)
    with outfile:
        json.dump(props, outfile, sort_keys=True, indent=4,
                  separators=(',', ': '))
        outfile.write('\n')

if __name__ == '__main__':
    tojson()
