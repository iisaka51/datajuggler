import sys
import time
import pytest

from datajuggler import uDict, aDict

import pandas as pd

class TestClass:
    def test_udict_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        obj = uDict(data)
        assert obj == data

    def test_udict_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
        obj = uDict(data)
        assert obj.__str__() == expect

    def test_udict_case03(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = uDict(data)
        assert obj.__repr__() == expect

    def test_udict_case04(self):
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        obj = uDict(January=1, February=2, March=3, April=4)
        assert obj == expect

    def test_udict_case05(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        assert data == expect

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


    def test_udict_fromkeys_case01(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        obj = uDict().fromkeys(data, 2)
        assert obj.__repr__() == expect

    def test_udict_fromkeys_case02(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        obj = uDict()
        obj.fromkeys(data, 2, inplace=True)
        assert obj.__repr__() == expect

    def test_udict_fromvalues_case01(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        obj = uDict().fromvalues(data)
        assert obj.__repr__() == expect

    def test_udict_fromvalues_case02(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})"
        obj = uDict().fromvalues(data, base=0)
        assert obj.__repr__() == expect

    def test_udict_fromvalues_case03(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        obj = uDict()
        obj.fromvalues(data, base=1, inplace=True)
        assert obj.__repr__() == expect

    def test_udict_fromvalues_case04(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = ( "uDict("
                   "{'01': 'January', '02': 'February', "
                    "'03': 'March', '04': 'April'})" )
        obj = uDict().fromvalues(data, prefix='')
        assert obj.__repr__() == expect

    def test_udict_fromvalues_case05(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = ( "uDict("
                   "{'month_01': 'January', 'month_02': 'February', "
                    "'month_03': 'March', 'month_04': 'April'})" )

        obj = uDict().fromvalues(data, prefix='month_')
        assert obj.__repr__() == expect

    def test_udict_fromlists_case01(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = uDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_udict_fromlists_case02(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = uDict()
        obj.fromlists(keys, values, inplace=True)
        assert obj.__repr__() == expect

    def test_udict_fromlists_case03(self):
        keys = [ 'January', 'February' ]
        values = [ 1, 2, 3, 4 ]
        expect = "uDict({'January': 1, 'February': 2})"
        obj = uDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_udict_fromlists_case04(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2 ]
        expect = "uDict({'January': 1, 'February': 2})"
        obj = uDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_udict_fromlists_case05(self):
        obj = uDict()
        result = obj[('a', 'b', 'c')]
        assert result == None

