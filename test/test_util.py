import pytest
from   javaproperties.util import LinkedList, ascii_splitlines

def test_linkedlist_empty():
    ll = LinkedList()
    assert list(ll) == []
    assert list(ll.iternodes()) == []
    assert ll.start is None
    assert ll.end is None

def test_linkedlist_one_elem():
    ll = LinkedList()
    n = ll.append(42)
    assert list(ll) == [42]
    assert list(ll.iternodes()) == [n]
    assert ll.find_node(n) == 0
    assert ll.start is n
    assert ll.end is n
    assert n.prev is None
    assert n.next is None

def test_linkedlist_two_elem():
    ll = LinkedList()
    n1 = ll.append(42)
    n2 = ll.append('fnord')
    assert list(ll) == [42, 'fnord']
    assert list(ll.iternodes()) == [n1, n2]
    assert ll.find_node(n1) == 0
    assert ll.find_node(n2) == 1
    assert ll.start is n1
    assert ll.end is n2
    assert n1.prev is None
    assert n1.next is n2
    assert n2.prev is n1
    assert n2.next is None

def test_linked_list_three_elem():
    ll = LinkedList()
    n1 = ll.append(42)
    n2 = ll.append('fnord')
    n3 = ll.append([0, 1, 2])
    assert list(ll) == [42, 'fnord', [0, 1, 2]]
    assert list(ll.iternodes()) == [n1, n2, n3]
    assert ll.find_node(n1) == 0
    assert ll.find_node(n2) == 1
    assert ll.find_node(n3) == 2
    assert ll.start is n1
    assert ll.end is n3
    assert n1.prev is None
    assert n1.next is n2
    assert n2.prev is n1
    assert n2.next is n3
    assert n3.prev is n2
    assert n3.next is None

def test_linked_list_unlink_only():
    ll = LinkedList()
    n = ll.append(42)
    n.unlink()
    assert list(ll) == []
    assert list(ll.iternodes()) == []
    assert ll.start is None
    assert ll.end is None
    assert ll.find_node(n) is None

def test_linked_list_unlink_first():
    ll = LinkedList()
    n1 = ll.append(42)
    n2 = ll.append('fnord')
    n3 = ll.append([0, 1, 2])
    n1.unlink()
    assert list(ll) == ['fnord', [0, 1, 2]]
    assert list(ll.iternodes()) == [n2, n3]
    assert ll.find_node(n1) is None
    assert ll.find_node(n2) == 0
    assert ll.find_node(n3) == 1
    assert ll.start is n2
    assert ll.end is n3
    assert n2.prev is None
    assert n2.next is n3
    assert n3.prev is n2
    assert n3.next is None

def test_linked_list_unlink_middle():
    ll = LinkedList()
    n1 = ll.append(42)
    n2 = ll.append('fnord')
    n3 = ll.append([0, 1, 2])
    n2.unlink()
    assert list(ll) == [42, [0, 1, 2]]
    assert list(ll.iternodes()) == [n1, n3]
    assert ll.find_node(n1) == 0
    assert ll.find_node(n2) is None
    assert ll.find_node(n3) == 1
    assert ll.start is n1
    assert ll.end is n3
    assert n1.prev is None
    assert n1.next is n3
    assert n3.prev is n1
    assert n3.next is None

def test_linked_list_unlink_last():
    ll = LinkedList()
    n1 = ll.append(42)
    n2 = ll.append('fnord')
    n3 = ll.append([0, 1, 2])
    n3.unlink()
    assert list(ll) == [42, 'fnord']
    assert list(ll.iternodes()) == [n1, n2]
    assert ll.find_node(n1) == 0
    assert ll.find_node(n2) == 1
    assert ll.find_node(n3) is None
    assert ll.start is n1
    assert ll.end is n2
    assert n1.prev is None
    assert n1.next is n2
    assert n2.prev is n1
    assert n2.next is None

def test_linked_list_insert_before_first():
    ll = LinkedList()
    n1 = ll.append(42)
    n2 = ll.append('fnord')
    n3 = ll.append([0, 1, 2])
    nx = n1.insert_before(3.14)
    assert list(ll) == [3.14, 42, 'fnord', [0, 1, 2]]
    assert list(ll.iternodes()) == [nx, n1, n2, n3]
    assert ll.find_node(n1) == 1
    assert ll.find_node(n2) == 2
    assert ll.find_node(n3) == 3
    assert ll.find_node(nx) == 0
    assert ll.start is nx
    assert ll.end is n3
    assert nx.prev is None
    assert nx.next is n1
    assert n1.prev is nx
    assert n1.next is n2
    assert n2.prev is n1
    assert n2.next is n3
    assert n3.prev is n2
    assert n3.next is None

def test_linked_list_insert_before_middle():
    ll = LinkedList()
    n1 = ll.append(42)
    n2 = ll.append('fnord')
    n3 = ll.append([0, 1, 2])
    nx = n2.insert_before(3.14)
    assert list(ll) == [42, 3.14, 'fnord', [0, 1, 2]]
    assert list(ll.iternodes()) == [n1, nx, n2, n3]
    assert ll.find_node(n1) == 0
    assert ll.find_node(n2) == 2
    assert ll.find_node(n3) == 3
    assert ll.find_node(nx) == 1
    assert ll.start is n1
    assert ll.end is n3
    assert n1.prev is None
    assert n1.next is nx
    assert nx.prev is n1
    assert nx.next is n2
    assert n2.prev is nx
    assert n2.next is n3
    assert n3.prev is n2
    assert n3.next is None

def test_linked_list_insert_before_last():
    ll = LinkedList()
    n1 = ll.append(42)
    n2 = ll.append('fnord')
    n3 = ll.append([0, 1, 2])
    nx = n3.insert_before(3.14)
    assert list(ll) == [42, 'fnord', 3.14, [0, 1, 2]]
    assert list(ll.iternodes()) == [n1, n2, nx, n3]
    assert ll.find_node(n1) == 0
    assert ll.find_node(n2) == 1
    assert ll.find_node(n3) == 3
    assert ll.find_node(nx) == 2
    assert ll.start is n1
    assert ll.end is n3
    assert n1.prev is None
    assert n1.next is n2
    assert n2.prev is n1
    assert n2.next is nx
    assert nx.prev is n2
    assert nx.next is n3
    assert n3.prev is nx
    assert n3.next is None

def test_linked_list_insert_after_first():
    ll = LinkedList()
    n1 = ll.append(42)
    n2 = ll.append('fnord')
    n3 = ll.append([0, 1, 2])
    nx = n1.insert_after(3.14)
    assert list(ll) == [42, 3.14, 'fnord', [0, 1, 2]]
    assert list(ll.iternodes()) == [n1, nx, n2, n3]
    assert ll.find_node(n1) == 0
    assert ll.find_node(n2) == 2
    assert ll.find_node(n3) == 3
    assert ll.find_node(nx) == 1
    assert ll.start is n1
    assert ll.end is n3
    assert n1.prev is None
    assert n1.next is nx
    assert nx.prev is n1
    assert nx.next is n2
    assert n2.prev is nx
    assert n2.next is n3
    assert n3.prev is n2
    assert n3.next is None

def test_linked_list_insert_after_middle():
    ll = LinkedList()
    n1 = ll.append(42)
    n2 = ll.append('fnord')
    n3 = ll.append([0, 1, 2])
    nx = n2.insert_after(3.14)
    assert list(ll) == [42, 'fnord', 3.14, [0, 1, 2]]
    assert list(ll.iternodes()) == [n1, n2, nx, n3]
    assert ll.find_node(n1) == 0
    assert ll.find_node(n2) == 1
    assert ll.find_node(n3) == 3
    assert ll.find_node(nx) == 2
    assert ll.start is n1
    assert ll.end is n3
    assert n1.prev is None
    assert n1.next is n2
    assert n2.prev is n1
    assert n2.next is nx
    assert nx.prev is n2
    assert nx.next is n3
    assert n3.prev is nx
    assert n3.next is None

def test_linked_list_insert_after_last():
    ll = LinkedList()
    n1 = ll.append(42)
    n2 = ll.append('fnord')
    n3 = ll.append([0, 1, 2])
    nx = n3.insert_after(3.14)
    assert list(ll) == [42, 'fnord', [0, 1, 2], 3.14]
    assert list(ll.iternodes()) == [n1, n2, n3, nx]
    assert ll.find_node(n1) == 0
    assert ll.find_node(n2) == 1
    assert ll.find_node(n3) == 2
    assert ll.find_node(nx) == 3
    assert ll.start is n1
    assert ll.end is nx
    assert n1.prev is None
    assert n1.next is n2
    assert n2.prev is n1
    assert n2.next is n3
    assert n3.prev is n2
    assert n3.next is nx
    assert nx.prev is n3
    assert nx.next is None

@pytest.mark.parametrize('s,lines', [
    ('', []),
    ('foobar', ['foobar']),
    ('foo\n', ['foo\n']),
    ('foo\r', ['foo\r']),
    ('foo\r\n', ['foo\r\n']),
    ('foo\n\r', ['foo\n', '\r']),
    ('foo\nbar', ['foo\n', 'bar']),
    ('foo\rbar', ['foo\r', 'bar']),
    ('foo\r\nbar', ['foo\r\n', 'bar']),
    ('foo\n\rbar', ['foo\n', '\r', 'bar']),
    (
        'Why\vare\fthere\x1Cso\x1Ddang\x1Emany\x85line\u2028separator\u2029'
        'characters?',
        ['Why\vare\fthere\x1Cso\x1Ddang\x1Emany\x85line\u2028separator\u2029'
         'characters?'],
    ),
])
def test_ascii_splitlines(s, lines):
    assert ascii_splitlines(s) == lines
