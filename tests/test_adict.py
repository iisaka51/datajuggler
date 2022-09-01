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
    def test_adict_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        obj = aDict(data)
        assert obj == data

    def test_adict_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
        obj = aDict(data)
        assert obj.__str__() == expect

    def test_adict_case03(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = aDict(data)
        assert obj.__repr__() == expect

    def test_adict_case04(self):
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        obj = aDict(January=1, February=2, March=3, April=4)
        assert obj == expect

    def test_adict_case05(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        assert data == expect

    def test_adict_case06(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = ( "aDict("
                   "{'one': {'two': {'three': {'four': 4}}}}"
                   ")" )
        obj = aDict(data)
        assert obj.__repr__() == expect

    def test_adict_case07(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        obj = aDict().fromkeys(data, 2)
        assert obj.__repr__() == expect

    def test_adict_case08(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        obj = aDict()
        obj.fromkeys(data, 2, inplace=True)
        assert obj.__repr__() == expect

    def test_adict_case09(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        obj = aDict().fromvalues(data)
        assert obj.__repr__() == expect

    def test_adict_case10(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})"
        obj = aDict().fromvalues(data, base=0)
        assert obj.__repr__() == expect

    def test_adict_case11(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        obj = aDict()
        obj.fromvalues(data, base=1, inplace=True)
        assert obj.__repr__() == expect

    def test_adict_case12(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = aDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_adict_case13(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = aDict()
        obj.fromlists(keys, values, inplace=True)
        assert obj.__repr__() == expect

    def test_adict_case14(self):
        keys = [ 'January', 'February' ]
        values = [ 1, 2, 3, 4 ]
        expect = "aDict({'January': 1, 'February': 2})"
        obj = aDict().fromlists(keys, values)
        assert obj.__repr__() == expect

    def test_adict_case15(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2 ]
        expect = "aDict({'January': 1, 'February': 2})"
        obj = aDict().fromlists(keys, values)
        assert obj.__repr__() == expect


    def test_adict_features_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = 2
        obj = aDict(data)
        assert obj.February == expect

    def test_adict_features_case02(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = { 'two': { 'three': { 'four': 4 }}}
        obj = aDict(data)
        assert obj.one == expect

    def test_adict_features_case03(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = "{'one': {'two': {'three': {'four': 4}}}}"
        obj = aDict(data)
        with pytest.raises(AttributeError) as e:
            result = obj.one.two
        assert str(e.value) == "'dict' object has no attribute 'two'"

    def test_adict_features_case04(self):
        data = {'one': aDict({'two': aDict({'three': aDict({'four': 4 })})})}
        expect = ( "aDict({'one': "
                     "aDict({'two': "
                       "aDict({'three': "
                         "aDict({'four': 4})})})})" )
        obj = aDict(data)
        assert obj.__repr__() == expect

    def test_adict_features_case05(self):
        data = {'one': aDict({'two': aDict({'three': aDict({'four': 4 })})})}
        expect = 4
        obj = aDict(data)
        assert obj.one.two.three.four == expect

    def test_adict_features_case06(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = ( "aDict({'one': "
                     "aDict({'two': "
                       "aDict({'three': "
                         "aDict({'four': 4})})})})" )
        obj = aDict(data, as_default_dict=True)
        assert obj.__repr__() == expect

    def test_adict_features_case07(self):
        expect = ( "aDict({'one': "
                     "aDict({'two': "
                       "aDict({'three': "
                         "aDict({'four': 4})})})})" )
        obj = aDict(as_default_dict=True,
                    one={ 'two': { 'three': { 'four': 4 }}} )
        assert obj.__repr__() == expect

    def test_adict_features_case08(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = 4
        obj = aDict(data, as_default_dict=True)
        assert obj.one.two.three.four == expect

