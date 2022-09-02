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
    def test_idict_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        obj = iDict(data)
        assert obj == data

    def test_idict_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
        obj = iDict(data)
        assert obj.__str__() == expect

    def test_idict_case03(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = iDict(data)
        assert obj.__repr__() == expect

    def test_idict_case04(self):
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        obj = iDict(January=1, February=2, March=3, April=4)
        assert obj == expect

    def test_idict_case05(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        assert data == expect

    def test_idict_case06(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = ( "iDict("
                   "{'one': {'two': {'three': {'four': 4}}}}"
                   ")" )
        obj = iDict(data)
        assert obj.__repr__() == expect

    def test_idict_case07(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "iDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        obj = iDict().fromkeys(data, 2)
        assert obj.__repr__() == expect

    def test_idict_case08(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "iDict({})"
        obj = iDict()
        obj.fromkeys(data, 2, inplace=True)
        assert obj.__repr__() == expect

    def test_idict_case09(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "iDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        obj = iDict().fromvalues(data)
        assert obj.__repr__() == expect

    def test_idict_case10(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "iDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})"
        obj = iDict().fromvalues(data, base=0)
        assert obj.__repr__() == expect

    def test_idict_case11(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "iDict({})"
        obj = iDict()
        obj.fromvalues(data, base=1, inplace=True)
        assert obj.__repr__() == expect

    def test_idict_case12(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = ( "iDict("
                   "{'1': 'January', '2': 'February', "
                    "'3': 'March', '4': 'April'})" )
        obj = iDict().fromvalues(data, prefix='')
        assert obj.__repr__() == expect

    def test_idict_case13(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = ( "iDict("
                   "{'month_1': 'January', 'month_2': 'February', "
                    "'month_3': 'March', 'month_4': 'April'})" )

        obj = iDict().fromvalues(data, prefix='month_')
        assert obj.__repr__() == expect

    def test_idict_case14(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = iDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_idict_case15(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "iDict({})"
        obj = iDict()
        obj.fromlists(keys, values, inplace=True)
        assert obj.__repr__() == expect

    def test_idict_case16(self):
        keys = [ 'January', 'February' ]
        values = [ 1, 2, 3, 4 ]
        expect = "iDict({'January': 1, 'February': 2})"
        obj = iDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_idict_case17(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2 ]
        expect = "iDict({'January': 1, 'February': 2})"
        obj = iDict().fromlists(keys, values)
        assert obj.__repr__() == expect


    def test_idict_features_case01(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(TypeError) as e:
            data['January'] = 'Jan'
        assert str(e.value) == 'iDict object does not support item assignment'

    def test_idict_features_case02(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(AttributeError) as e:
            result  = data.pop(0)
        assert str(e.value) == 'iDict object has no attribute pop'

    def test_idict_features_case03(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(AttributeError) as e:
            data.clear()
        assert str(e.value) == 'iDict object has no attribute clear'

    def test_idict_features_case04(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(AttributeError) as e:
            data.update({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        assert str(e.value) == 'iDict object has no attribute update'

    def test_idict_features_case05(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(AttributeError) as e:
            data.setdefault('March', 3)
        assert str(e.value) == 'iDict object has no attribute setdefault'

    def test_idict_features_case06(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        assert hasattr(data, '__hash__') == True

    def test_idict_features_case07(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        result = dict({data: 1})
        assert  result[data]  == 1
