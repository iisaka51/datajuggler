import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import Keylist, Keypath

class TestClass:

    def test_key_list2path_case01(self):
        data = ['x', 'y', 'z']
        expect = 'x.y.z'
        result = Keylist.list2path(data)
        assert result == expect

    def test_key_list2path_case02(self):
        data = ['x', 'y', 'z']
        expect = 'x_y_z'
        result = Keylist.list2path(data, separator='_')
        assert result == expect

    def test_key_list2path_case03(self):
        data = [['x', 'y', 'z'], ['a', 'b', 'c']]
        expect = ['x.y.z', 'a.b.c']
        result = Keylist.list2path(data)
        assert result == expect

    def test_key_list2path_case04(self):
        data = [['x.1', 'y.2', 'z.3'], ['a.b', 'c.d', 'e.f']]
        expect = ['x.1/y.2/z.3', 'a.b/c.d/e.f']
        result = Keylist.list2path(data, separator='/')
        assert result == expect

    def test_key_list2path_case05(self):
        data = ['a', 'b', 'c[0]' ]
        expect = 'a.b.c[0]'
        result = Keylist.list2path(data)
        assert result == expect

    def test_key_list2path_case06(self):
        data = ['a', 'b', 'c', '[0]' ]
        expect = 'a.b.c[0]'
        result = Keylist.list2path(data)
        assert result == expect

    def test_key_list2path_case07(self):
        data = ['a', 'b', 'c', 0 ]
        expect = 'a.b.c[0]'
        result = Keylist.list2path(data)
        assert result == expect



    def test_key_path2list_case01(self):
        data = 'x.y.z'
        expect = ['x', 'y', 'z']
        result = Keypath.path2list(data)
        assert result == expect

    def test_key_path2list_case02(self):
        data = 'a.b.c[0]'
        expect = ['a', 'b', 'c', 0]
        result = Keypath.path2list(data)
        assert result == expect

    def test_key_path2list_case03(self):
        data = 'x_y_z'
        expect = ['x', 'y', 'z']
        result = Keypath.path2list(data, separator='_')
        assert result == expect

    def test_key_path2list_case04(self):
        data = ['x.y.z', 'a.b.c']
        expect = [['x', 'y', 'z'], ['a', 'b', 'c']]
        result = Keypath.path2list(data)
        assert result == expect

    def test_key_path2list_case05(self):
        data = ['x.1/y.2/z.3', 'a.b/c.d/e.f']
        expect = [['x.1', 'y.2', 'z.3'], ['a.b', 'c.d', 'e.f']]
        result = Keypath.path2list(data, separator='/')
        assert result == expect

