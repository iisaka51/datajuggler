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
    def test_ordereddict_case01(self):
        data = OrderedDict([('month', 'January'), ('day', 13 )])
        expect = dict({'month': 'January', 'day': 13})
        result = ordereddict_to_dict(data)
        assert result == expect

    def test_ordereddict_case02(self):
        data = OrderedDict([('month', 'January'), ('day', 13 ),
                    ('time', OrderedDict([('hours', 7), ('minutes', 30)]))])
        expect = dict({'month': 'January', 'day': 13,
                       'time': {'hours': 7, 'minutes': 30}})
        result = ordereddict_to_dict(data)
        assert result == expect

    def test_change_dict_keys_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        replace = { 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 3: 3, 4: 4 }
        result = change_dict_keys(data, replace)
        assert result == expect

    def test_change_dict_keys_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        replace = { 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 3: 3, 4: 4 }
        change_dict_keys(data, replace, inplace=True)
        assert data == expect

    def test_change_dict_keys_case03(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4 }
        result = change_dict_keys(data, 'April', 'Apr')
        assert result == expect

    def test_change_dict_keys_case04(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4 }
        change_dict_keys(data, 'April', 'Apr', inplace=True)
        assert data == expect

    def test_adict_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        result = aDict(data)
        assert result == data

    def test_adict_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = 2
        result = aDict(data)
        assert result.February == expect

    def test_adict_case03(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = 4
        result = aDict(data)
        assert result.one.two.three.four == expect

    def test_adict_case04(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = "{'one': {'two': {'three': {'four': 4}}}}"
        result = aDict(data)
        assert result.__str__() == expect

    def test_adict_case05(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = "aDict({'one': aDict({'two': aDict({'three': aDict({'four': 4})})})})"
        result = aDict(data)
        assert result.__repr__() == expect

    def test_adict_case06(self):
        data = {"console": "Nintendo Switch",
                "games": ["The Legend of Zelda", "Mario Golf"]}
        expect = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        obj = aDict(data)
        assert obj.to_json() == expect

    def test_adict_case07(self):
        json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        expect = "aDict({'console': 'Nintendo Switch', 'games': ['The Legend of Zelda', 'Mario Golf']})"
        obj = aDict().from_json(json_data)
        assert obj.__repr__() == expect

    def test_adict_case08(self):
        json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        expect = "aDict({'console': 'Nintendo Switch', 'games': ['The Legend of Zelda', 'Mario Golf']})"
        obj = aDict()
        obj.from_json(json_data, inplace=True)
        assert obj.__repr__() == expect

    def test_adict_case09(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        obj = aDict().fromkeys(data, 2)
        assert obj.__repr__() == expect

    def test_adict_case10(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        obj = aDict()
        obj.fromkeys(data, 2, inplace=True)
        assert obj.__repr__() == expect

    def test_adict_case11(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        obj = aDict().fromvalues(data)
        assert obj.__repr__() == expect

    def test_adict_case12(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})"
        obj = aDict().fromvalues(data, base=0)
        assert obj.__repr__() == expect

    def test_adict_case13(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        obj = aDict()
        obj.fromvalues(data, base=1, inplace=True)
        assert obj.__repr__() == expect

    def test_adict_case14(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = aDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_adict_case15(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = aDict()
        obj.fromlists(keys, values, inplace=True)
        assert obj.__repr__() == expect

    def test_adict_case16(self):
        keys = [ 'January', 'February' ]
        values = [ 1, 2, 3, 4 ]
        expect = "aDict({'January': 1, 'February': 2})"
        obj = aDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_adict_case17(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2 ]
        expect = "aDict({'January': 1, 'February': 2})"
        obj = aDict().fromlists(keys, values)
        assert obj.__repr__() == expect


    def test_udict_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        result = uDict(data)
        assert result == data

    def test_udict_case02(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        assert data == expect

    def test_udict_case03(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4 }
        saved = data.copy()
        result = data.replace_key('April', 'Apr')
        assert ( result == expect
                 and data == saved )

    def test_udict_case04(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        replace = {'January': 'Jan', 'February': 'Feb' }
        expect = { 'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4 }
        saved = data.copy()
        result = data.replace_key_map(replace)
        assert ( result == expect
                 and data == saved )

    def test_udict_case05(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        replace = {'January': 'Jan', 'February': 'Feb' }
        expect = { 'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4 }
        saved = data.copy()
        data.replace_key_map(replace, inplace=True)
        assert ( data == expect
                 and data != saved )

    def test_udict_case06(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(TypeError) as e:
            result = dict({data: 1})
        assert str(e.value) == "unhashable type: 'uDict'"

    def test_udict_case07(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
        result = uDict(data)
        assert result.__str__() == expect

    def test_udict_case08(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        result = uDict(data)
        assert result.__repr__() == expect

    def test_udict_case09(self):
        data = {"console": "Nintendo Switch",
                "games": ["The Legend of Zelda", "Mario Golf"]}
        expect = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        obj = uDict(data)
        assert obj.to_json() == expect

    def test_udict_case10(self):
        json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        expect = "uDict({'console': 'Nintendo Switch', 'games': ['The Legend of Zelda', 'Mario Golf']})"
        new = uDict().from_json(json_data)
        assert new.__repr__() == expect

    def test_udict_case11(self):
        json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        expect = "uDict({'console': 'Nintendo Switch', 'games': ['The Legend of Zelda', 'Mario Golf']})"
        obj = uDict()
        obj.from_json(json_data, inplace=True)
        assert obj.__repr__() == expect

    def test_udict_case12(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        obj = uDict().fromkeys(data, 2)
        assert obj.__repr__() == expect

    def test_udict_case13(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        obj = uDict()
        obj.fromkeys(data, 2, inplace=True)
        assert obj.__repr__() == expect

    def test_udict_case14(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        obj = uDict().fromvalues(data)
        assert obj.__repr__() == expect

    def test_udict_case15(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})"
        obj = uDict().fromvalues(data, base=0)
        assert obj.__repr__() == expect

    def test_udict_case16(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "uDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        obj = uDict()
        obj.fromvalues(data, base=1, inplace=True)
        assert obj.__repr__() == expect

    def test_udict_case17(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = uDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_udict_case18(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = uDict()
        obj.fromlists(keys, values, inplace=True)
        assert obj.__repr__() == expect

    def test_udict_case19(self):
        keys = [ 'January', 'February' ]
        values = [ 1, 2, 3, 4 ]
        expect = "uDict({'January': 1, 'February': 2})"
        obj = uDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_udict_case20(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2 ]
        expect = "uDict({'January': 1, 'February': 2})"
        obj = uDict().fromlists(keys, values)
        assert obj.__repr__() == expect


    def test_idict_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        result = iDict(data)
        assert result == data

    def test_idict_case02(self):
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        result = iDict(January=1, February=2, March=3, April=4)
        assert result == expect

    def test_idict_case03(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        assert data == expect

    def test_idict_case04(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(TypeError) as e:
            data['January'] = 'Jan'
        assert str(e.value) == 'iDict object does not support item assignment'

    def test_idict_case05(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(AttributeError) as e:
            result  = data.pop(0)
        assert str(e.value) == 'iDict object has no attribute pop'

    def test_idict_case06(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(AttributeError) as e:
            data.clear()
        assert str(e.value) == 'iDict object has no attribute clear'

    def test_idict_case07(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(AttributeError) as e:
            data.update({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        assert str(e.value) == 'iDict object has no attribute update'

    def test_idict_case08(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(AttributeError) as e:
            data.setdefault('March', 3)
        assert str(e.value) == 'iDict object has no attribute setdefault'

    def test_idict_case09(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        assert hasattr(data, '__hash__') == True

    def test_idict_case10(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        result = dict({data: 1})
        assert  result[data]  == 1

    def test_idict_case11(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
        result = iDict(data)
        assert result.__str__() == expect

    def test_idict_case12(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        result = iDict(data)
        assert result.__repr__() == expect

    def test_idict_case13(self):
        data = {"console": "Nintendo Switch",
                "games": ["The Legend of Zelda", "Mario Golf"]}
        expect = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        obj = iDict(data)
        assert obj.to_json() == expect

    def test_idict_case14(self):
        json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        expect = "iDict({'console': 'Nintendo Switch', 'games': ['The Legend of Zelda', 'Mario Golf']})"
        result = iDict().from_json(json_data)
        assert result.__repr__() == expect

    def test_idict_case15(self):
        json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        expect = "iDict({})"
        obj = iDict()
        obj.from_json(json_data, inplace=True)
        assert obj.__repr__() == expect

    def test_idict_case16(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "iDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        obj = iDict().fromkeys(data, 2)
        assert obj.__repr__() == expect

    def test_idict_case17(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "iDict({})"
        obj = iDict()
        obj.fromkeys(data, 2, inplace=True)
        assert obj.__repr__() == expect

    def test_idict_case18(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "iDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        obj = iDict().fromvalues(data)
        assert obj.__repr__() == expect

    def test_idict_case19(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "iDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})"
        obj = iDict().fromvalues(data, base=0)
        assert obj.__repr__() == expect

    def test_idict_case20(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "iDict({})"
        obj = iDict()
        obj.fromvalues(data, base=1, inplace=True)
        assert obj.__repr__() == expect

    def test_idict_case21(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = iDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_idict_case22(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "iDict({})"
        obj = iDict()
        obj.fromlists(keys, values, inplace=True)
        assert obj.__repr__() == expect

    def test_idict_case23(self):
        keys = [ 'January', 'February' ]
        values = [ 1, 2, 3, 4 ]
        expect = "iDict({'January': 1, 'February': 2})"
        obj = iDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_idict_case24(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2 ]
        expect = "iDict({'January': 1, 'February': 2})"
        obj = iDict().fromlists(keys, values)
        assert obj.__repr__() == expect

