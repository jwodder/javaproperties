import collections
import json
import numbers
from   six import string_types

def strify_dict(d):
    strdict = {}
    for k,v in itemize(d):
        if isinstance(k, (numbers.Number, bool, type(None))):
            k = json.dumps(k)
        elif not isinstance(k, string_types):
            raise TypeError('.properties keys must be scalars')
        if isinstance(v, (list, dict)):
            raise TypeError('Cannot convert list/dict to .properties value')
        elif isinstance(v, string_types):
            strdict[k] = v
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
