from .propclass import Properties
from .reading   import read, readitems, readitems3, unescape
from .writing   import write, join_key_value, escape, to_comment

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'javaproperties@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/javaproperties'

__all__ = [
    'Properties',
    'escape',
    'join_key_value',
    'read',
    'readitems',
    'readitems3',
    'to_comment',
    'unescape',
    'write',
]
