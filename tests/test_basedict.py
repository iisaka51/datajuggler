import sys
import time
import pytest

from datajuggler.core import BaseDict

data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }

class TestClass:
    def test_basedict_case01(self):
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        d = BaseDict(data)
        assert d == data
        d.clear()
        assert d == {}
        d.update(data)
        assert d== data

    def test_basedict_case02(self):
        expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
        d = BaseDict(data)
        assert d.__str__() == expect

    def test_basedict_case03(self):
        expect = "BaseDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        d = BaseDict(data)
        assert d.__repr__() == expect

    def test_basedict_case04(self):
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        d = BaseDict(January=1, February=2, March=3, April=4)
        assert d == expect

    def test_basedict_fromkeys_case01(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'January': 2, 'February': 2, 'March': 2, 'April': 2}
        d = BaseDict().fromkeys(data, 2)
        assert d == expect

    def test_basedict_fromkeys_case02(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'January': 2, 'February': 2, 'March': 2, 'April': 2}
        d = BaseDict()
        d.fromkeys(data, 2, inplace=True)
        assert d == expect

    def test_basedict_fromvalues_case01(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {1: 'January', 2: 'February', 3: 'March', 4: 'April'}
        d = BaseDict().fromvalues(data)
        assert d == expect

    def test_basedict_fromvalues_case02(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {0: 'January', 1: 'February', 2: 'March', 3: 'April'}
        d = BaseDict().fromvalues(data, base=0)
        assert d == expect

    def test_basedict_fromvalues_case03(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {1: 'January', 2: 'February', 3: 'March', 4: 'April'}
        d = BaseDict()
        d.fromvalues(data, base=1, inplace=True)
        assert d == expect

    def test_basedict_fromvalues_case04(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'01': 'January', '02': 'February',
                  '03': 'March', '04': 'April' }
        d = BaseDict().fromvalues(data, prefix='')
        assert d == expect

    def test_basedict_fromvalues_case05(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'month_01': 'January', 'month_02': 'February',
                  'month_03': 'March', 'month_04': 'April'}

        d = BaseDict().fromvalues(data, prefix='month_')
        assert d == expect

    def test_basedict_fromvalues_case06(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'month_001': 'January', 'month_002': 'February',
                  'month_003': 'March', 'month_004': 'April'}

        d = BaseDict().fromvalues(data, prefix='month_', format="{:03}")
        assert d == expect

    def test_basedict_fromlists_case01(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = {'January': 1, 'February': 2, 'March': 3, 'April': 4}
        d = BaseDict().fromlists(keys, values)
        assert d == expect

    def test_basedict_fromlists_case02(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = {'January': 1, 'February': 2, 'March': 3, 'April': 4}
        d = BaseDict()
        d.fromlists(keys, values, inplace=True)
        assert d == expect

    def test_basedict_fromlists_case03(self):
        keys = [ 'January', 'February' ]
        values = [ 1, 2, 3, 4 ]
        expect = {'January': 1, 'February': 2}
        d = BaseDict().fromlists(keys, values)
        assert d == expect

    def test_basedict_fromlists_case04(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2 ]
        expect = {'January': 1, 'February': 2}
        d = BaseDict().fromlists(keys, values)
        assert d == expect
