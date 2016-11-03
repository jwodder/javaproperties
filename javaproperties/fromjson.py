# -*- coding: utf-8 -*-
"""
:program:`json2properties`
--------------------------

NAME
^^^^

:program:`json2properties` — Convert a JSON object to a Java ``.properties``
file

SYNOPSIS
^^^^^^^^

.. code-block:: shell

    json2properties [<OPTIONS>] [<infile> [<outfile>]]

.. note::

    If the `javaproperties` package was installed but the
    :program:`json2properties` script is not present, this command can still be
    run by replacing ``json2properties`` with ``python -m
    javaproperties.fromjson`` on the command line.

DESCRIPTION
^^^^^^^^^^^

Convert a JSON file :option:`infile` to a ``.properties`` file and write the
results to :option:`outfile`.  If not specified, :option:`infile` and
:option:`outfile` default to `sys.stdin` and `sys.stdout`, respectively.

The JSON document must be an object with scalar (i.e., string, numeric,
boolean, and/or null) values; anything else will result in an error.

Output is sorted by key, and numeric, boolean, & null values are output using
their JSON representations; e.g., the input:

.. code-block:: json

    {
        "yes": true,
        "no": "false",
        "nothing": null
    }

becomes:

.. code-block:: properties

    #Mon Sep 26 18:57:44 UTC 2016
    no=false
    nothing=null
    yes=true

OPTIONS
^^^^^^^

.. program:: json2properties

.. option:: -E <encoding>, --encoding <encoding>

    .. versionadded:: 0.2.0

    Use ``<encoding>`` as the output encoding; default value: ``iso-8859-1``
    (a.k.a. Latin-1).  (As all output is *currently* always pure ASCII, this
    option is not very useful.)

.. option:: -s <sep>, --separator <sep>

    .. versionadded:: 0.2.0

    Use ``<sep>`` as the key-value separator in the output; default value:
    ``=``
"""

from   decimal  import Decimal
import json
import click
from   .        import __version__
from   .util    import strify_dict, outfile_type
from   .writing import dump

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('-E', '--encoding', default='iso-8859-1', show_default=True,
              help='Encoding of the .properties file')
@click.option('-s', '--separator', default='=', show_default=True,
              help='Key-value separator to use in output')
@click.argument('infile', type=click.File('r'), default='-')
@click.argument('outfile', type=outfile_type, default='-')
@click.version_option(__version__, '-V', '--version',
                      message='%(prog)s %(version)s')
@click.pass_context
def fromjson(ctx, infile, outfile, separator, encoding):
    """Convert a JSON object to a Java .properties file"""
    with infile:
        props = json.load(infile, parse_float=Decimal)
    if not isinstance(props, dict):
        ctx.fail('Only dicts can be converted to .properties')
    with click.open_file(outfile, 'w', encoding=encoding) as fp:
        dump(sorted(strify_dict(props).items()), fp, separator=separator)

if __name__ == '__main__':
    fromjson()
