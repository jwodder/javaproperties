from   __future__            import absolute_import, print_function, \
                                    unicode_literals
import codecs
import xml.etree.ElementTree as ET
from   xml.sax.saxutils      import escape, quoteattr
from   .util                 import itemize

def load_xml(fp, object_pairs_hook=dict):
    tree = ET.parse(fp)
    return object_pairs_hook(_fromXML(tree.getroot()))

def loads_xml(s, object_pairs_hook=dict):
    elem = ET.fromstring(s)
    return object_pairs_hook(_fromXML(elem))

def _fromXML(root):
    if root.tag != 'properties':
        raise ValueError('XML tree is not rooted at <properties>')
    for entry in root.findall('entry'):
        key = entry.get('key')
        if key is None:
            raise ValueError('<entry> is missing "key" attribute')
        yield (key, entry.text)

def dump_xml(props, fp, comment=None, encoding='UTF-8', sort_keys=False):
    # `fp` must be a binary filehandle
    fp = codecs.lookup(encoding).streamwriter(fp, errors='xmlcharrefreplace')
    print('<?xml version="1.0" encoding={0} standalone="no"?>'\
          .format(quoteattr(encoding)), file=fp)
    for s in _stream_xml(props, comment, sort_keys):
        print(s, file=fp)

def dumps_xml(props, comment=None, sort_keys=False):
    return ''.join(s + '\n' for s in _stream_xml(props, comment, sort_keys))

def _stream_xml(props, comment=None, sort_keys=False):
    yield '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">'
    yield '<properties>'
    if comment is not None:
        yield '<comment>' + escape(comment) + '</comment>'
    for k,v in itemize(props, sort_keys=sort_keys):
        yield '<entry key={0}>{1}</entry>'.format(quoteattr(k), escape(v))
    yield '</properties>'
