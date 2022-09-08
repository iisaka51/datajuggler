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

    def test_udict_features_map_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
        obj = uDict(data)
        saved = obj.copy()
        result = obj.map_keys(str.upper)
        assert ( result == expect and data == saved )

    def test_udict_features_map_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
        result = uDict().map_keys(str.upper, data)
        assert result == expect

    def test_udict_features_map_case03(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = iDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
        result = uDict().map_keys(str.upper, data, factory=iDict)
        assert result == expect

    def test_udict_features_map_case04(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
        obj = uDict(data)
        obj.map_keys(str.upper, inplace=True)
        assert ( obj == expect )

    def test_udict_features_map_case05(self):
        data = { 'Jack': [10, 11, 12], 'John': [8, 15, 3] }
        expect = { 'Jack': 33, 'John': 26 }
        obj = uDict(data)
        saved = obj.copy()
        result = obj.map_values(sum)
        assert ( result == expect and data == saved )

    def test_udict_features_map_case06(self):
        data = { 'Jack': [10, 11, 12], 'John': [8, 15, 3] }
        expect = { 'Jack': 33, 'John': 26 }
        obj = uDict(data)
        saved = obj.copy()
        obj.map_values(sum, inplace=True)
        assert ( obj == expect )

    def test_udict_features_map_case07(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 1: 'January', 2: 'February', 3: 'March', 4: 'April' })
        obj = uDict(data)
        saved = obj.copy()
        result = obj.map_items(reversed)
        assert ( result == expect and obj == saved )

    def test_udict_features_map_case08(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 1: 'January', 2: 'February', 3: 'March', 4: 'April' })
        result = uDict().map_items(reversed, data)
        assert result == expect

    def test_udict_features_map_case09(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = aDict({ 1: 'January', 2: 'February', 3: 'March', 4: 'April' })
        result = uDict().map_items(reversed, data, factory=aDict)
        assert result == expect

    def test_udict_features_filter_case01(self):
        is_janfeb = lambda x: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'January': 1, 'February': 2 })
        obj = uDict(data)
        saved = obj.copy()
        result = obj.filter_keys(is_janfeb)
        assert ( result == expect and obj == saved )

    def test_udict_features_filter_case02(self):
        is_janfeb = lambda x: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'January': 1, 'February': 2 })
        obj = uDict(data)
        obj.filter_keys(is_janfeb, inplace=True)
        assert obj == expect

    def test_udict_features_filter_case03(self):
        is_janfeb = lambda x: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'January': 1, 'February': 2 })
        result = uDict().filter_keys(is_janfeb, data)
        assert result == expect

    def test_udict_features_filter_case04(self):
        is_janfeb = lambda x: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = aDict({ 'January': 1, 'February': 2 })
        result = uDict().filter_keys(is_janfeb, data, factory=aDict)
        assert result == expect

    def test_udict_features_filter_case05(self):
        is_even = lambda x: x % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'February': 2, 'April': 4 })
        obj = uDict(data)
        saved = obj.copy()
        result = obj.filter_values(is_even)
        assert ( result == expect and obj == saved )

    def test_udict_features_filter_case06(self):
        is_even = lambda x: x % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'February': 2, 'April': 4 })
        obj = uDict(data)
        obj.filter_values(is_even, inplace=True)
        assert obj == expect

    def test_udict_features_filter_case06(self):
        is_even = lambda x: x % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'February': 2, 'April': 4 })
        result = uDict().filter_values(is_even, data)
        assert result == expect

    def test_udict_features_filter_case07(self):
        is_even = lambda x: x % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = aDict({ 'February': 2, 'April': 4 })
        result = uDict().filter_values(is_even, data, factory=aDict)
        assert result == expect
        assert result.April == 4

    def is_valid(self, item):
        k, v = item
        return k.endswith('ary') and v % 2 == 0

    def test_udict_features_filter_case08(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'February': 2 })
        obj = uDict(data)
        saved = obj.copy()
        result = obj.filter_items(self.is_valid)
        assert ( result == expect and obj == saved )

    def test_udict_features_filter_case09(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'February': 2 })
        obj = uDict(data)
        obj.filter_items(self.is_valid, inplace=True)
        assert obj == expect

    def test_udict_features_filter_case10(self):
        is_even = lambda x: x % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'February': 2 })
        result = uDict().filter_items(self.is_valid, data)
        assert result == expect

    def test_udict_features_filter_case11(self):
        is_even = lambda x: x % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = aDict({ 'February': 2 })
        result = uDict().filter_items(self.is_valid, data, factory=aDict)
        assert result == expect

    def test_udict_features_get_allkey_case01(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = ['x', 'y', 'z', 'a', 'b', 'c']
        result = uDict().get_allkeys(data)
        assert result == expect

    def test_udict_features_get_allkey_case02(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = ['x', 'y', 'z', 'a', 'b', 'c']
        result = uDict(data).get_allkeys()
        assert result == expect

    def test_udict_features_get_allkey_case03(self):
        data = {'x': {'y': {'z': [{'a': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'a': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect =  ['x', 'y', 'z', 'a', 'b', 'c', 'a', 'b', 'c']
        result = uDict(data).get_allkeys()
        assert result == expect

    def test_udict_features_get_values_case01(self):
        data = {'x': {'y': {'z': [{'a': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'a': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = ['v11', 'v21']
        result = uDict().get_values('a', data)
        assert result == expect

    def test_udict_features_get_values_case02(self):
        data = {'x': {'y': {'z': [{'a': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'a': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = ['v11', 'v21']
        result = uDict(data).get_values('a')
        assert result == expect

    def test_udict_features_get_values_case03(self):
        data = {'x': {'y': {'z': [{'a': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'a': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'a': ['v11', 'v21']}
        result = uDict().get_values('a', data, with_keys=True)
        assert result == expect

    def test_udict_features_get_values_case04(self):
        data = {'x': {'y': {'z': [{'a': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'a': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'a': ['v11', 'v21']}
        result = uDict(data).get_values('a', with_keys=True)
        assert result == expect

    def test_udict_features_get_values_case05(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = ['v11', 'v21']
        result = uDict().get_values('a', data, wild=True)
        assert result == expect

    def test_udict_features_get_values_case06(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = ['v11', 'v21']
        result = uDict(data).get_values('a', wild=True)
        assert result == expect

    def test_udict_features_get_values_case07(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = ['v11', 'v21']
        result = uDict().get_values('aa', data, wild=True)
        assert result == expect

    def test_udict_features_get_values_case08(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = ['v11', 'v21']
        result = uDict(data).get_values('aa', wild=True)
        assert result == expect

    def test_udict_features_get_values_case09(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'aA': ['v11', 'v21'], 'b': ['v12', 'v22']}
        result = uDict(data).get_values(['aA', 'b'])
        assert result == expect

    def test_udict_features_get_values_case10(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'aA': ['v11', 'v21'], 'b': ['v12', 'v22']}
        result = uDict(data).get_values(('aA', 'b'))
        assert result == expect

    def test_udict_features_get_values_case10(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'a': ['v11', 'v21'], 'b': ['v12', 'v22']}
        result = uDict(data).get_values(('a', 'b'), wild=True)
        assert result == expect

    def test_udict_features_get_values_case11(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'aA': ['v11', 'v21'], 'b': ['v12', 'v22']}
        result = uDict(data).get_values(('a', 'b'), wild=True, verbatim=True)
        assert result == expect

    def test_udict_features_count_case01(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = 2
        count = uDict(data).counts_of_keys('aA')
        assert count == expect

    def test_udict_features_count_case02(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = 2
        count = uDict().counts_of_keys('aA', data)
        assert count == expect

    def test_udict_features_count_case03(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = 0
        count = uDict(data).counts_of_keys('aa')
        assert count == expect

    def test_udict_features_count_case04(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = 2
        count = uDict(data).counts_of_keys('aa', wild=True)
        assert count == expect

    def test_udict_features_count_case05(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = 2
        count = uDict(data).counts_of_keys('a', wild=True)
        assert count == expect

    def test_udict_features_count_case06(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'aA': 2, 'b': 2}
        count = uDict().counts_of_keys(['aA', 'b'], data)
        assert count == expect

    def test_udict_features_count_case07(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'aA': 2, 'b': 2}
        count = uDict().counts_of_keys(('aA', 'b'), data)
        assert count == expect

    def test_udict_features_count_case08(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'a': 2, 'b': 2}
        count = uDict().counts_of_keys(['a', 'b'], data, wild=True)
        assert count == expect

    def test_udict_features_count_case09(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'aA': 2, 'b': 2}
        count = uDict().counts_of_keys(['a', 'b'], data,
                        wild=True, verbatim=True)
        assert count == expect



    def test_udict_features_count_case11(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'v11': 1}
        count = uDict(data).counts_of_values('v11')
        assert count == expect

    def test_udict_features_count_case12(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'v11': 1}
        count = uDict().counts_of_values('v11', data)
        assert count == expect

    def test_udict_features_count_case13(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'v1': 3}
        count = uDict().counts_of_values('v1', data, wild=True)
        assert count == expect

    def test_udict_features_count_case14(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'v11': 1, 'v12': 1, 'v13': 1}
        count = uDict().counts_of_values('v1', data, wild=True, verbatim=True)
        assert count == expect

    def test_udict_features_count_case15(self):
        data = {'x': {'y': {'z': [{'aA': 100, 'b': 101, 'c': 103},
                                  {'aA': 100, 'b': 101, 'c': 103}]} }}
        expect = {100: 2}
        count = uDict(data).counts_of_values(100)
        assert count == expect


    def test_udict_features_item_case01(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 3, 'b': 2}
        result = uDict(data).get_items('a', 3)
        assert result == expect

    def test_udict_features_item_case02(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 3, 'b': 2}
        result = uDict().get_items('a', 3, data)
        assert result == expect

    def test_udict_features_item_case04(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 1, 'b': 2, 'c': 3}
        result = uDict(data).get_items('c', 3)
        assert result == expect

    def test_udict_features_item_case05(self):
        data = {}
        expect = {'a': 1}
        result = uDict(data).get_items('a', 1)
        assert result == expect

    def test_udict_features_item_case06(self):
        data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }] }
        expect = {'a': 1, 'b': 2}
        result = uDict(data).get_items('b', 2)
        assert result == expect

    def test_udict_features_item_case06(self):
        data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }] }
        expect = {'a': 1, 'b': [{'c': 11, 'd': 12},
                                {'c': 22, 'd': 22}], 'c': 33}
        result = uDict(data).get_items('c', 33)
        assert result == expect

    def test_udict_features_item_case07(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'a': 'v11', 'b': 'v2', 'c': 'v3'}
        result = uDict(data).get_items('x y z a', 'v11')
        assert result == expect


    def test_udict_features_item_case10(self):
        data = { 'a': 1, 'b': 2}
        expect = {'b': 2}
        result = uDict(data).del_items('a')
        assert result == expect

    def test_udict_features_item_case11(self):
        data = { 'a': 1, 'b': 2}
        expect = {'b': 2}
        result = uDict().del_items('a', data)
        assert result == expect

    def test_udict_features_item_case12(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 1, 'b': 2}
        result = uDict(data).del_items('c')
        assert result == expect

    def test_udict_features_item_case13(self):
        data = { 'a': 1, 'b': 2}
        expect = {'b': 2}
        obj = uDict(data)
        obj.del_items('a', inplace=True)
        assert obj == expect

    def test_udict_features_item_case14(self):
        data = { 'a': 1, 'b': 2}
        expect = {'b': 2}
        obj = uDict(data)
        obj.del_items('a', inplace=True)
        assert obj == expect

    def test_udict_features_item_case15(self):
        data = { 'a': 1, 'b': 2}
        expect = {'a': 1, 'b': 2}
        obj = uDict(data)
        obj.del_items('c', inplace=True)
        assert obj == expect

    def test_udict_features_item_case16(self):
        data = { 'a': 1, 'b': 2}
        expect = "aDict({'b': 2})"
        result = uDict(data).del_items('a', factory=aDict)
        assert result.__repr__() == expect

    def test_udict_features_item_case17(self):
        data = { 'a': 1, 'b': 2}
        expect = "aDict({'b': 2})"
        result = uDict(data).del_items('a', factory=aDict)
        assert result.__repr__() == expect

    def test_udict_features_item_case18(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        result = uDict(data).del_items('a')
        assert result == expect

    def test_udict_features_item_case19(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'b': 'v2', 'c': 'v3'}}}}
        result = uDict(data).del_items('x y z a')
        assert result == expect


    def test_udict_features_item_case20(self):
        data = { 'a': 1, 'b': 2}
        expect = { 'a': 2, 'b': 2}
        result = uDict(data).set_items('a',2 )
        assert result == expect

    def test_udict_features_item_case21(self):
        data = { 'a': 1, 'b': 2}
        expect = { 'a': 2, 'b': 2}
        obj = uDict(data)
        obj.set_items('a',2, inplace=True)
        assert obj == expect

    def test_udict_features_item_case22(self):
        data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }] }
        expect = {'a': 1, 'b': 2}
        result = uDict(data).set_items('b', 2)
        assert result == expect

    def test_udict_features_item_case23(self):
        data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }] }
        expect = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
                               {'c': 22, 'd': 22 }], 'c': 3 }
        result = uDict(data).set_items('c', 3)
        assert result == expect

    def test_udict_features_item_case24(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
        result = uDict(data).set_items('x y z a', 'v11')
        assert result == expect

    def test_udict_features_item_case24(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
        obj = uDict(data)
        obj['x']['y']['z']['a']='v11'
        assert obj == expect

    def test_udict_features_item_case25(self):
        data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
        result = uDict(data).set_items('x y z a', 'v11')
        assert result == expect

    def test_udict_features_compare_case01(self):
        d1 = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        d2 = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        result = uDict().compare(d1, d2)
        assert result == True

    def test_udict_features_compare_case02(self):
        d1 = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        d2 = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        result = uDict(d1).compare(d2)
        assert result == True

    def test_udict_features_compare_case03(self):
        d1 = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                {'aB': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        d2 = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                {'aB': 'd21', 'b': 'd22', 'c': 'd23'}]} }}
        result = uDict().compare(d1, d2, keys='aA')
        assert result == True

    def test_udict_features_compare_case04(self):
        d1 = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                {'aB': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        d2 = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                {'aB': 'd21', 'b': 'd22', 'c': 'd23'}]} }}
        result = uDict().compare(d1, d2, keys=['aA', 'b'])
        assert result == True

    def test_udict_features_compare_case05(self):
        d1 = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
        d2 = {'x': {'y': {'z': {'a': 'v10', 'b': 'v2', 'c': 'v3'}}}}
        expect = "{'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}} is not equal {'x': {'y': {'z': {'a': 'v10', 'b': 'v2', 'c': 'v3'}}}}."
        with pytest.raises(ValueError) as e:
            result = uDict().compare(d1, d2, thrown_error=True)
        assert str(e.value) == expect


    def test_udict_features_groupby_case01(self):
        data = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Paul"},
            {"id": 3, "name": "David"},
            {"id": 4, "name": "Freddie"},
            {"id": 3, "name": "Jack"},
            {"id": 1, "name": "Eddie"},
            {"id": 3, "name": "Bob"},
            {"id": 4, "name": "Maichael"},
            {"id": 1, "name": "Edward"},
        ]
        expect = ( "uDict({1: [{'id': 1, 'name': 'John'}, "
                              "{'id': 1, 'name': 'Eddie'}, "
                              "{'id': 1, 'name': 'Edward'}], "
                          "2: [{'id': 2, 'name': 'Paul'}], "
                          "3: [{'id': 3, 'name': 'David'}, "
                              "{'id': 3, 'name': 'Jack'}, "
                              "{'id': 3, 'name': 'Bob'}], "
                          "4: [{'id': 4, 'name': 'Freddie'}, "
                              "{'id': 4, 'name': 'Maichael'}]})" )
        result = uDict().groupby(data, "id")
        assert result.__repr__() == expect


    def test_udict_features_groupby_case02(self):
        data = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Paul"},
            {"id": 3, "name": "David"},
            {"id": 4, "name": "Freddie"},
            {"id": 3, "name": "Jack"},
            {"id": 1, "name": "Eddie"},
            {"id": 3, "name": "Bob"},
            {"id": 4, "name": "Maichael"},
            {"id": 1, "name": "Edward"},
        ]
        expect = ( "iDict({1: [{'id': 1, 'name': 'John'}, "
                              "{'id': 1, 'name': 'Eddie'}, "
                              "{'id': 1, 'name': 'Edward'}], "
                          "2: [{'id': 2, 'name': 'Paul'}], "
                          "3: [{'id': 3, 'name': 'David'}, "
                              "{'id': 3, 'name': 'Jack'}, "
                              "{'id': 3, 'name': 'Bob'}], "
                          "4: [{'id': 4, 'name': 'Freddie'}, "
                              "{'id': 4, 'name': 'Maichael'}]})" )
        result = uDict().groupby(data, "id", factory=iDict)
        assert result.__repr__() == expect


