# -*- coding: utf-8 -*-
"""
:program:`properties2json`
--------------------------

NAME
^^^^

:program:`properties2json` — Convert a Java ``.properties`` file to JSON

SYNOPSIS
^^^^^^^^

.. code-block:: shell

    properties2json [<OPTIONS>] [<infile> [<outfile>]]

.. note::

    If the `javaproperties` package was installed but the
    :program:`properties2json` script is not present, this command can still be
    run by replacing ``properties2json`` with ``python -m
    javaproperties.tojson`` on the command line.

DESCRIPTION
^^^^^^^^^^^

Convert a ``.properties`` file :option:`infile` to a JSON object and
write the results to :option:`outfile`.  If not specified, :option:`infile` and
:option:`outfile` default to `sys.stdin` and `sys.stdout`, respectively.

OPTIONS
^^^^^^^

.. program:: properties2json

.. option:: -E <encoding>, --encoding <encoding>

    .. versionadded:: 0.2.0

    Specifies the encoding of the input file; default value: ``iso-8859-1``
    (a.k.a. Latin-1)
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
