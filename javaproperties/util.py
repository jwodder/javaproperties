import codecs
import collections
from   decimal import Decimal
import io
import json
import sys
from   six     import PY2, string_types

def strify_dict(d):
    strdict = {}
    for k,v in itemize(d):
        assert isinstance(k, string_types)
        if isinstance(v, (list, dict)):
            raise TypeError('Cannot convert list/dict to .properties value')
        elif isinstance(v, string_types):
            strdict[k] = v
        elif isinstance(v, Decimal):
            strdict[k] = str(v)
        else:
            strdict[k] = json.dumps(v)
    return strdict

def itemize(kvs, sort_keys=False):
    if isinstance(kvs, collections.Mapping):
        items = ((k, kvs[k]) for k in kvs)
    else:
        items = kvs
    if sort_keys:
        items = sorted(items)
    return items

if PY2:
    propin  = codecs.getreader('iso-8859-1')(sys.stdin)
    propout = codecs.getwriter('iso-8859-1')(sys.stdout)
else:
    propin  = codecs.getreader('iso-8859-1')(sys.stdin.buffer)
    propout = codecs.getwriter('iso-8859-1')(sys.stdout.buffer)

def properties_reader(fname):
    # based on argparse.FileType
    if fname == '-':
        return propin
    else:
        try:
            return io.open(fname, 'rt', encoding='iso-8859-1')
        except IOError as e:
            import argparse
            raise argparse.ArgumentTypeError('{0}: {1}'.format(fname, e))

def properties_writer(fname):
    # based on argparse.FileType
    if fname == '-':
        return propout
    else:
        try:
            return io.open(fname, 'wt', encoding='iso-8859-1')
        except IOError as e:
            import argparse
            raise argparse.ArgumentTypeError('{0}: {1}'.format(fname, e))
