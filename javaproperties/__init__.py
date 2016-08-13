from .propclass import Properties
from .reading   import (read_properties, iter_properties, parse_properties,
                        unescape)
from .writing   import write_properties, join_key_value, escape, to_comment

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'javaproperties@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/javaproperties'

__all__ = [
    'Properties',
    'escape',
    'iter_properties',
    'join_key_value',
    'parse_properties',
    'read_properties',
    'to_comment',
    'unescape',
    'write_properties',
]
