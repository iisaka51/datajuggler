import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import aDict, uDict

class TestClass:
    def test_udict_setitem_case01(self):
        expect = {'a': None}
        obj = dict()
        uDict().set_items('a', None, obj)
        assert obj == expect

        obj = uDict({})
        obj.set_items('a', None)
        assert obj == expect

    def test_udict_setitem_case02(self):
        expect = aDict({'a': None})
        obj = uDict(())
        obj.set_items('a', None, factory=aDict)
        assert obj == expect

    def test_udict_setitem_case03(self):
        expect = {'a': {'b': {'c': 0}}}
        obj = uDict(())
        obj.set_items(['a', 'b', 'c'], 0)
        assert obj == expect

    def test_udict_setitem_case04(self):
        data = { 'a': 1, 'b': 2}
        expect = { 'a': 2, 'b': 2}
        obj = uDict(data)
        obj.set_items('a', 2 )
        assert obj == expect

    def test_udict_setitem_case05(self):
        data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }] }
        expect = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }], 'c': 3 }
        obj = uDict(data)
        obj.set_items('c', 3)
        assert obj == expect

    def test_udict_setitem_case06(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
        obj = uDict(data)
        obj.set_items(['x', 'y', 'z', 'a'], 'v11')
        assert obj == expect

    def test_udict_setitem_case07(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
        obj = uDict(data)
        obj.set_items('x.y.z.a', 'v11')
        assert obj == expect

    def test_udict_setitem_case08(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
        obj = uDict(data)
        obj.set_items('x y z a', 'v11', separator=' ')
        assert obj == expect

    def test_udict_setitem_case09(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
        obj = uDict(data)
        obj.set_items(['x','y','z','a'], 'v11')
        assert obj == expect



    def test_udict_getitem_case01(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 3, 'b': 2}
        expect_repr = "uDict({'a': 3, 'b': 2})"
        result = uDict().get_items('a', 3, data)
        assert result == expect
        obj = uDict(data)
        result = obj.get_items('a', 3)
        assert result == expect
        assert result.__repr__() == expect_repr

    def test_udict_getitem_case02(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 1, 'b': 2, 'c': 3}
        result = uDict(data).get_items('c', 3)
        assert result == expect

    def test_udict_getitem_case03(self):
        data = {}
        expect = {'a': 1}
        result = uDict(data).get_items('a', 1)
        assert result == expect

    def test_udict_getitem_case04(self):
        data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }] }
        expect = {'a': 1, 'b': 2}
        result = uDict(data).get_items('b', 2)
        assert result == expect

    def test_udict_getitem_case05(self):
        data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }] }
        expect = {'a': 1, 'b': [{'c': 11, 'd': 12},
                                {'c': 22, 'd': 22}], 'c': 33}
        result = uDict(data).get_items('c', 33)
        assert result == expect

    def test_udict_getitem_case06(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'a': 'v11', 'b': 'v2', 'c': 'v3'}
        result = uDict(data).get_items('x.y.z.a', 'v11')
        assert result == expect

    def test_udict_getitem_case07(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'a': 'v11', 'b': 'v2', 'c': 'v3'}
        result = uDict(data).get_items('x_y_z_a', 'v11', separator='_')
        assert result == expect

    def test_udict_getitem_case08(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'a': 'v11', 'b': 'v2', 'c': 'v3'}
        result = uDict(data).get_items(['x','y','z','a'], 'v11')
        assert result == expect


    def test_udict_delitem_case01(self):
        data = { 'a': 1, 'b': 2}
        expect = {'b': 2}
        result = uDict().del_items('a', data)
        assert result == expect
        obj = uDict(data)
        result = obj.del_items('a')
        assert result == expect

    def test_udict_delitem_case02(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 1, 'b': 2}
        result = uDict(data).del_items('c')
        assert result == expect

    def test_udict_delitem_case03(self):
        data = { 'a': 1, 'b': 2}
        expect = {'b': 2}
        obj = uDict(data)
        obj.del_items('a', inplace=True)
        assert obj == expect

    def test_udict_delitem_case04(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 1, 'b': 2}
        uDict().del_items('c', data, inplace=True)
        assert data == expect

    def test_udict_delitem_case05(self):
        data = { 'a': 1, 'b': 2}
        expect = aDict({'b': 2})
        result = uDict().del_items('a', data, factory=aDict)
        assert result == expect

    def test_udict_delitem_case06(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        result = uDict(data).del_items('a')
        assert result == expect

    def test_udict_delitem_case07(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'b': 'v2', 'c': 'v3'}}}}
        result = uDict(data).del_items('x.y.z.a')
        assert result == expect

    def test_udict_delitem_case08(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'b': 'v2', 'c': 'v3'}}}}
        result = uDict(data).del_items('x_y_z_a', separator='_')
        assert result == expect

    def test_udict_delitem_case09(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'b': 'v2', 'c': 'v3'}}}}
        result = uDict(data).del_items(['x','y','z','a'])
        assert result == expect
