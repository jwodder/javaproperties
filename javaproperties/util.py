import json
from   six import iteritems, string_types

def strify_dict(d):
    ### Should this be exported for public consumption?
    ### Rename to `dict2properties`?
    strdict = {}
    for k,v in iteritems(d):
        if not isinstance(k, string_types):
            raise TypeError('.properties keys must be strings')
        if isinstance(v, (list, dict)):
            raise TypeError('Cannot convert lists & dicts to .properties strings')
        elif isinstance(v, string_types):
            strdict[k] = v
        else:
            strdict[k] = json.dumps(v)
    return strdict
