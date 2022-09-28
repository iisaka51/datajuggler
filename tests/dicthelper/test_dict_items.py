import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import aDict
from datajuggler.dicthelper import (
    get_items, set_items,  del_items, pop_items,
)

class TestClass:

    def test_setitem_case01(self):
        expect = {'a': None}
        obj = dict()
        set_items(obj, 'a', None)
        assert obj == expect

    def test_setitem_case02(self):
        expect = aDict({'a': None})
        obj = dict()
        set_items(obj, 'a', None, factory=aDict)
        assert obj == expect

    def test_setitem_case03(self):
        obj = dict()
        expect = {'a': {'b': {'c': 0}}}
        set_items(obj, ['a', 'b', 'c'], 0)
        assert obj == expect

    def test_setitem_case04(self):
        data = { 'a': 1, 'b': 2}
        expect = { 'a': 2, 'b': 2}
        set_items(data, 'a', 2 )
        assert data == expect

    def test_setitem_case05(self):
        data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }] }
        expect = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }], 'c': 3 }
        set_items(data, 'c', 3)
        assert data == expect

    def test_setitem_case06(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
        set_items(data, ['x', 'y', 'z', 'a'], 'v11')
        assert data == expect

    def test_setitem_case07(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
        set_items(data, 'x.y.z.a', 'v11')
        assert data == expect

    def test_setitem_case08(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
        set_items(data, 'x y z a', 'v11', separator=' ')
        assert data == expect

    def test_setitem_case09(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
        set_items(data, ['x','y','z','a'], 'v11')
        assert data == expect



    def test_getitem_case01(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 3, 'b': 2}
        result = get_items(data, 'a', 3)
        assert result == expect

    def test_getitem_case02(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 1, 'b': 2, 'c': 3}
        result = get_items(data, 'c', 3)
        assert result == expect

    def test_getitem_case03(self):
        data = {}
        expect = {'a': 1}
        result = get_items(data, 'a', 1)
        assert result == expect

    def test_getitem_case04(self):
        data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }] }
        expect = {'a': 1, 'b': 2}
        result = get_items(data, 'b', 2)
        assert result == expect

    def test_getitem_case05(self):
        data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }] }
        expect = {'a': 1, 'b': [{'c': 11, 'd': 12},
                                {'c': 22, 'd': 22}], 'c': 33}
        result = get_items(data, 'c', 33)
        assert result == expect

    def test_getitem_case06(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'a': 'v11', 'b': 'v2', 'c': 'v3'}
        result = get_items(data, 'x.y.z.a', 'v11')
        assert result == expect

    def test_getitem_case07(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'a': 'v11', 'b': 'v2', 'c': 'v3'}
        result = get_items(data, 'x_y_z_a', 'v11', separator='_')
        assert result == expect

    def test_getitem_case08(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'a': 'v11', 'b': 'v2', 'c': 'v3'}
        result = get_items(data, ['x','y','z','a'], 'v11')
        assert result == expect


    def test_delitem_case01(self):
        data = { 'a': 1, 'b': 2}
        expect = {'b': 2}
        result = del_items(data, 'a')
        assert result == expect

    def test_delitem_case02(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 1, 'b': 2}
        result = del_items(data, 'c')
        assert result == expect

    def test_delitem_case03(self):
        data = { 'a': 1, 'b': 2}
        expect = {'b': 2}
        del_items(data, 'a', inplace=True)
        assert data == expect

    def test_delitem_case04(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 1, 'b': 2}
        del_items(data, 'c', inplace=True)
        assert data == expect

    def test_delitem_case05(self):
        data = { 'a': 1, 'b': 2}
        expect = aDict({'b': 2})
        result = del_items(data, 'a', factory=aDict)
        assert result == expect

    def test_delitem_case06(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        result = del_items(data, 'a')
        assert result == expect

    def test_delitem_case07(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'b': 'v2', 'c': 'v3'}}}}
        result = del_items(data, 'x.y.z.a')
        assert result == expect

    def test_delitem_case08(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'b': 'v2', 'c': 'v3'}}}}
        result = del_items(data, 'x_y_z_a', separator='_')
        assert result == expect


    def test_delitem_case09(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'b': 'v2', 'c': 'v3'}}}}
        result = del_items(data, ['x','y','z','a'])
        assert result == expect
