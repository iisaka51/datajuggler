import sys
import time
import pytest

from datajuggler import uDict, aDict

data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }

class TestClass_BaseDict:
    def test_udict_case01(self):
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        d = uDict(data)
        assert d == data
        d.clear()
        assert d == {}
        d.update(data)
        assert d== data

    def test_udict_case02(self):
        expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
        d = uDict(data)
        assert d.__str__() == expect

    def test_udict_case03(self):
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        d = uDict(data)
        assert d.__repr__() == expect

    def test_udict_case04(self):
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        d = uDict(January=1, February=2, March=3, April=4)
        assert d == expect

    def test_udict_fromkeys_case01(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'January': 2, 'February': 2, 'March': 2, 'April': 2}
        d = uDict().fromkeys(data, 2)
        assert d == expect

    def test_udict_fromkeys_case02(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'January': 2, 'February': 2, 'March': 2, 'April': 2}
        d = uDict()
        d.fromkeys(data, 2, inplace=True)
        assert d == expect

    def test_udict_fromvalues_case01(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {1: 'January', 2: 'February', 3: 'March', 4: 'April'}
        d = uDict().fromvalues(data)
        assert d == expect

    def test_udict_fromvalues_case02(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {0: 'January', 1: 'February', 2: 'March', 3: 'April'}
        d = uDict().fromvalues(data, base=0)
        assert d == expect

    def test_udict_fromvalues_case03(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {1: 'January', 2: 'February', 3: 'March', 4: 'April'}
        d = uDict()
        d.fromvalues(data, base=1, inplace=True)
        assert d == expect

    def test_udict_fromvalues_case04(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'01': 'January', '02': 'February',
                  '03': 'March', '04': 'April' }
        d = uDict().fromvalues(data, prefix='')
        assert d == expect

    def test_udict_fromvalues_case05(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'month_01': 'January', 'month_02': 'February',
                  'month_03': 'March', 'month_04': 'April'}

        d = uDict().fromvalues(data, prefix='month_')
        assert d == expect

    def test_udict_fromvalues_case06(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'month_001': 'January', 'month_002': 'February',
                  'month_003': 'March', 'month_004': 'April'}

        d = uDict().fromvalues(data, prefix='month_', format="{:03}")
        assert d == expect

    def test_udict_fromlists_case01(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = {'January': 1, 'February': 2, 'March': 3, 'April': 4}
        d = uDict().fromlists(keys, values)
        assert d == expect

    def test_udict_fromlists_case02(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = {'January': 1, 'February': 2, 'March': 3, 'April': 4}
        d = uDict()
        d.fromlists(keys, values, inplace=True)
        assert d == expect

    def test_udict_fromlists_case03(self):
        keys = [ 'January', 'February' ]
        values = [ 1, 2, 3, 4 ]
        expect = {'January': 1, 'February': 2}
        d = uDict().fromlists(keys, values)
        assert d == expect

    def test_udict_fromlists_case04(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2 ]
        expect = {'January': 1, 'February': 2}
        d = uDict().fromlists(keys, values)
        assert d == expect

class TestClass_Features:
    def test_udict_case06(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect_repr = ( "uDict({'one': "
                      "uDict({'two': "
                         "uDict({'three': "
                           "uDict({'four': 4})})})})" )
        expect_str = "{'one': {'two': {'three': {'four': 4}}}}"
        obj = uDict(data)
        assert obj.__repr__() == expect_repr
        assert repr(obj) == expect_repr
        assert obj.__str__() == expect_str
        assert str(obj) == expect_str

    def test_udict_case07(self):
        obj = uDict()
        obj[('a', 'b', 'c')]=1
        result = obj[('a', 'b', 'c')]
        assert result == 1
