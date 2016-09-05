import json
import numbers
from   six import iteritems, string_types

def strify_dict(d):
    strdict = {}
    for k,v in iteritems(d):
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
