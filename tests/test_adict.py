import sys
import time
import pytest

from datajuggler import uDict, aDict

import pandas as pd

class TestClass:
    def test_adict_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        d = aDict(data)
        assert d == data
        d.clear()
        assert d == {}
        d.update(data)
        assert d== data

    def test_adict_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
        d = aDict(data)
        assert d.__str__() == expect

    def test_adict_case03(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        d = aDict(data)
        assert d.__repr__() == expect

    def test_adict_case04(self):
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        d = aDict(January=1, February=2, March=3, April=4)
        assert d == expect

    def test_adict_case05(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        assert data == expect

    def test_adict_case06(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect_repr = ( "aDict({'one': "
                     "aDict({'two': "
                       "aDict({'three': "
                         "aDict({'four': 4})})})})" )
        expect_str = "{'one': {'two': {'three': {'four': 4}}}}"
        d = aDict(data)
        assert d.__repr__() == expect_repr
        assert repr(d) == expect_repr
        assert d.__str__() == expect_str
        assert str(d) == expect_str

    def test_adict_case07(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        d = aDict().fromkeys(data, 2)
        assert d.__repr__() == expect

    def test_adict_case08(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
        d = aDict()
        d.fromkeys(data, 2, inplace=True)
        assert d.__repr__() == expect

    def test_adict_case09(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        d = aDict().fromvalues(data)
        assert d.__repr__() == expect

    def test_adict_case10(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})"
        d = aDict().fromvalues(data, base=0)
        assert d.__repr__() == expect

    def test_adict_case11(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = "aDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
        d = aDict()
        d.fromvalues(data, base=1, inplace=True)
        assert d.__repr__() == expect

    def test_adict_case12(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = ( "aDict("
                   "{'1': 'January', '2': 'February', "
                    "'3': 'March', '4': 'April'})" )
        d = aDict().fromvalues(data, prefix='')
        assert d.__repr__() == expect

    def test_adict_case13(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = ( "aDict("
                   "{'month_1': 'January', 'month_2': 'February', "
                    "'month_3': 'March', 'month_4': 'April'})" )

        d = aDict().fromvalues(data, prefix='month_')
        assert d.__repr__() == expect

    def test_adict_case14(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        d = aDict().fromlists(keys, values)
        assert d.__repr__() == expect

    def test_adict_case15(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        d = aDict()
        d.fromlists(keys, values, inplace=True)
        assert d.__repr__() == expect

    def test_adict_case16(self):
        keys = [ 'January', 'February' ]
        values = [ 1, 2, 3, 4 ]
        expect = "aDict({'January': 1, 'February': 2})"
        d = aDict().fromlists(keys, values)
        assert d.__repr__() == expect

    def test_adict_case17(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2 ]
        expect = "aDict({'January': 1, 'February': 2})"
        d = aDict().fromlists(keys, values)
        assert d.__repr__() == expect


    def test_adict_features_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = 2
        d = aDict(data)
        assert d.February == expect

    def test_adict_features_case02(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = { 'two': { 'three': { 'four': 4 }}}
        d = aDict(data)
        assert d.one == expect

    def test_adict_features_case03(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = {'three': {'four': 4}}
        d = aDict(data)
        assert d.one.two == expect

    def test_adict_features_case04(self):
        data = {'one': aDict({'two': aDict({'three': aDict({'four': 4 })})})}
        expect = ( "aDict({'one': "
                     "aDict({'two': "
                       "aDict({'three': "
                         "aDict({'four': 4})})})})" )
        d = aDict(data)
        assert d.__repr__() == expect

    def test_adict_features_case05(self):
        data = {'one': aDict({'two': aDict({'three': aDict({'four': 4 })})})}
        d = aDict(data)
        assert d.one.two.three.four == 4

    def test_adict_features_case06(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        d = aDict(data)
        d.one.two.three.four = 10
        assert d.one.two.three.four == 10

    def test_adict_features_case06(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        d = aDict(data)
        d.freeze()
        with pytest.raises(AttributeError) as e:
            d.one.two.three.four = 10
        assert str(e.value) == 'aDict frozen object cannot be modified.'

    def test_adict_features_case07(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        d = aDict(data)
        d.freeze()
        result = hash(d)
        assert isinstance(result, int) == True

    def test_adict_features_case08(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        d = aDict(data)
        with pytest.raises(AttributeError) as e:
            result = hash(d)
        assert str(e.value) == 'unhashable not frozen object.'

    def test_adict_features_case09(self):
        data = {'a': [{'b': 3}, {'b': 4}]}
        d = aDict(data)
        assert d.a[1].b == 4
        d.one.two.three.four = 10
        assert d.one.two.three.four == 10
