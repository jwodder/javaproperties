from .propclass import Properties
from .reading   import load, loads, load_items3, unescape
from .writing   import dump, dumps, join_key_value, escape, to_comment
from .xml       import load_xml, loads_xml, dump_xml, dumps_xml

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'javaproperties@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/javaproperties'

__all__ = [
    'Properties',
    'dump',
    'dump_xml',
    'dumps',
    'dumps_xml',
    'escape',
    'join_key_value',
    'load',
    'load_items3',
    'load_xml',
    'loads',
    'loads_xml',
    'to_comment',
    'unescape',
]
