import sys
import time
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import (
    uDict, iDict, aDict,
    change_dict_keys, ordereddict_to_dict,
)

from collections import OrderedDict
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
        expect = ( "uDict("
                   "{'one': {'two': {'three': {'four': 4}}}}"
                   ")" )
        obj = uDict(data)
        assert obj.__repr__() == expect

    def test_udict_case07(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        obj = uDict().fromkeys(data, 2)
        assert obj.__repr__() == expect

    def test_udict_case08(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        obj = uDict()
        obj.fromkeys(data, 2, inplace=True)
        assert obj.__repr__() == expect

    def test_udict_case09(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        obj = uDict().fromvalues(data)
        assert obj.__repr__() == expect

    def test_udict_case10(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})"
        obj = uDict().fromvalues(data, base=0)
        assert obj.__repr__() == expect

    def test_udict_case11(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        obj = uDict()
        obj.fromvalues(data, base=1, inplace=True)
        assert obj.__repr__() == expect

    def test_udict_case12(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = ( "uDict("
                   "{'1': 'January', '2': 'February', "
                    "'3': 'March', '4': 'April'})" )
        obj = uDict().fromvalues(data, prefix='')
        assert obj.__repr__() == expect

    def test_udict_case13(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = ( "uDict("
                   "{'month_1': 'January', 'month_2': 'February', "
                    "'month_3': 'March', 'month_4': 'April'})" )

        obj = uDict().fromvalues(data, prefix='month_')
        assert obj.__repr__() == expect

    def test_udict_case14(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = uDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_udict_case15(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = uDict()
        obj.fromlists(keys, values, inplace=True)
        assert obj.__repr__() == expect

    def test_udict_case16(self):
        keys = [ 'January', 'February' ]
        values = [ 1, 2, 3, 4 ]
        expect = "uDict({'January': 1, 'February': 2})"
        obj = uDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_udict_case17(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2 ]
        expect = "uDict({'January': 1, 'February': 2})"
        obj = uDict().fromlists(keys, values)
        assert obj.__repr__() == expect


    def test_udict_features_case01(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4 }
        saved = data.copy()
        result = data.replace_key('April', 'Apr')
        assert ( result == expect
                 and data == saved )

    def test_udict_features_case02(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        replace = {'January': 'Jan', 'February': 'Feb' }
        expect = { 'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4 }
        saved = data.copy()
        result = data.replace_key_map(replace)
        assert ( result == expect
                 and data == saved )

    def test_udict_features_case03(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        replace = {'January': 'Jan', 'February': 'Feb' }
        expect = { 'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4 }
        saved = data.copy()
        data.replace_key_map(replace, inplace=True)
        assert ( data == expect
                 and data != saved )

    def test_udict_features_case04(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(TypeError) as e:
            result = dict({data: 1})
        assert str(e.value) == "unhashable type: 'uDict'"

    def test_udict_features_case05(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
        obj = uDict(data)
        saved = obj.copy()
        result = obj.map_keys(str.upper)
        assert ( result == expect and data == saved )

    def test_udict_features_case06(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
        result = uDict().map_keys(str.upper, data)
        assert result == expect

    def test_udict_features_case07(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = iDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
        result = uDict().map_keys(str.upper, data, factory=iDict)
        assert result == expect

    def test_udict_features_case08(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
        obj = uDict(data)
        obj.map_keys(str.upper, inplace=True)
        assert ( obj == expect )

    def test_udict_features_case09(self):
        data = { 'Jack': [10, 11, 12], 'John': [8, 15, 3] }
        expect = { 'Jack': 33, 'John': 26 }
        obj = uDict(data)
        saved = obj.copy()
        result = obj.map_values(sum)
        assert ( result == expect and data == saved )

    def test_udict_features_case10(self):
        data = { 'Jack': [10, 11, 12], 'John': [8, 15, 3] }
        expect = { 'Jack': 33, 'John': 26 }
        obj = uDict(data)
        saved = obj.copy()
        obj.map_values(sum, inplace=True)
        assert ( obj == expect )

    def test_udict_features_case11(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 1: 'January', 2: 'February', 3: 'March', 4: 'April' })
        obj = uDict(data)
        saved = obj.copy()
        result = obj.map_items(reversed)
        assert ( result == expect and obj == saved )

    def test_udict_features_case12(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 1: 'January', 2: 'February', 3: 'March', 4: 'April' })
        result = uDict().map_items(reversed, data)
        assert result == expect

    def test_udict_features_case13(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = aDict({ 1: 'January', 2: 'February', 3: 'March', 4: 'April' })
        result = uDict().map_items(reversed, data, factory=aDict)
        assert result == expect

    def test_udict_features_case14(self):
        is_janfeb = lambda x: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'January': 1, 'February': 2 })
        obj = uDict(data)
        saved = obj.copy()
        result = obj.filter_keys(is_janfeb)
        assert ( result == expect and obj == saved )

    def test_udict_features_case15(self):
        is_janfeb = lambda x: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'January': 1, 'February': 2 })
        obj = uDict(data)
        obj.filter_keys(is_janfeb, inplace=True)
        assert obj == expect

    def test_udict_features_case16(self):
        is_janfeb = lambda x: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'January': 1, 'February': 2 })
        result = uDict().filter_keys(is_janfeb, data)
        assert result == expect

    def test_udict_features_case17(self):
        is_janfeb = lambda x: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = aDict({ 'January': 1, 'February': 2 })
        result = uDict().filter_keys(is_janfeb, data, factory=aDict)
        assert result == expect

    def test_udict_features_case18(self):
        is_even = lambda x: x % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'February': 2, 'April': 4 })
        obj = uDict(data)
        saved = obj.copy()
        result = obj.filter_values(is_even)
        assert ( result == expect and obj == saved )

    def test_udict_features_case19(self):
        is_even = lambda x: x % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'February': 2, 'April': 4 })
        obj = uDict(data)
        obj.filter_values(is_even, inplace=True)
        assert obj == expect

    def test_udict_features_case20(self):
        is_even = lambda x: x % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'February': 2, 'April': 4 })
        result = uDict().filter_values(is_even, data)
        assert result == expect

    def test_udict_features_case21(self):
        is_even = lambda x: x % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = aDict({ 'February': 2, 'April': 4 })
        result = uDict().filter_values(is_even, data, factory=aDict)
        assert result == expect


    def is_valid(self, item):
        k, v = item
        return k.endswith('ary') and v % 2 == 0

    def test_udict_features_case22(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'February': 2 })
        obj = uDict(data)
        saved = obj.copy()
        result = obj.filter_items(self.is_valid)
        assert ( result == expect and obj == saved )

    def test_udict_features_case23(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'February': 2 })
        obj = uDict(data)
        obj.filter_items(self.is_valid, inplace=True)
        assert obj == expect

    def test_udict_features_case24(self):
        is_even = lambda x: x % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'February': 2 })
        result = uDict().filter_items(self.is_valid, data)
        assert result == expect

    def test_udict_features_case25(self):
        is_even = lambda x: x % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = aDict({ 'February': 2 })
        result = uDict().filter_items(self.is_valid, data, factory=aDict)
        assert result == expect

