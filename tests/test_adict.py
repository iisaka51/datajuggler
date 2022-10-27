import sys
import time
import pytest

from datajuggler import uDict, aDict

data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }

class TestClass_Basedict:
    def test_adict_case01(self):
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        d = aDict(data)
        assert d == data
        d.clear()
        assert d == {}
        d.update(data)
        assert d== data

    def test_adict_case02(self):
        expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
        d = aDict(data)
        assert d.__str__() == expect

    def test_adict_case03(self):
        expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        d = aDict(data)
        assert d.__repr__() == expect

    def test_adict_case04(self):
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        d = aDict(January=1, February=2, March=3, April=4)
        assert d == expect

    def test_adict_fromkeys_case01(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'January': 2, 'February': 2, 'March': 2, 'April': 2}
        d = aDict().fromkeys(data, 2)
        assert d == expect

    def test_adict_fromkeys_case02(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'January': 2, 'February': 2, 'March': 2, 'April': 2}
        d = aDict()
        d.fromkeys(data, 2, inplace=True)
        assert d == expect

    def test_adict_fromvalues_case01(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {1: 'January', 2: 'February', 3: 'March', 4: 'April'}
        d = aDict().fromvalues(data)
        assert d == expect

    def test_adict_fromvalues_case02(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {0: 'January', 1: 'February', 2: 'March', 3: 'April'}
        d = aDict().fromvalues(data, base=0)
        assert d == expect

    def test_adict_fromvalues_case03(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {1: 'January', 2: 'February', 3: 'March', 4: 'April'}
        d = aDict()
        d.fromvalues(data, base=1, inplace=True)
        assert d == expect

    def test_adict_fromvalues_case04(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'01': 'January', '02': 'February',
                  '03': 'March', '04': 'April' }
        d = aDict().fromvalues(data, prefix='')
        assert d == expect

    def test_adict_fromvalues_case05(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'month_01': 'January', 'month_02': 'February',
                  'month_03': 'March', 'month_04': 'April'}

        d = aDict().fromvalues(data, prefix='month_')
        assert d == expect

    def test_adict_fromvalues_case06(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = {'month_001': 'January', 'month_002': 'February',
                  'month_003': 'March', 'month_004': 'April'}

        d = aDict().fromvalues(data, prefix='month_', format="{:03}")
        assert d == expect

    def test_adict_fromlists_case01(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = {'January': 1, 'February': 2, 'March': 3, 'April': 4}
        d = aDict().fromlists(keys, values)
        assert d == expect

    def test_adict_fromlists_case02(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2, 3, 4 ]
        expect = {'January': 1, 'February': 2, 'March': 3, 'April': 4}
        d = aDict()
        d.fromlists(keys, values, inplace=True)
        assert d == expect

    def test_adict_fromlists_case03(self):
        keys = [ 'January', 'February' ]
        values = [ 1, 2, 3, 4 ]
        expect = {'January': 1, 'February': 2}
        d = aDict().fromlists(keys, values)
        assert d == expect

    def test_adict_fromlists_case04(self):
        keys = [ 'January', 'February', 'March', 'April' ]
        values = [ 1, 2 ]
        expect = {'January': 1, 'February': 2}
        d = aDict().fromlists(keys, values)
        assert d == expect

class TestClass_Features:

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
        expect = 'aDict frozen object cannot be modified.'
        d = aDict(data)
        d.freeze()
        with pytest.raises(AttributeError) as e:
            d.one.two.three.four = 10
        assert str(e.value) == expect

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

    def test_adict_feature_case10(self):
        data = { 'one': [ { 'two': 2 }, { 'three': 3 } ], 'next':{'four': 4 }}
        d = aDict(data)
        d.freeze()
        assert d.one[0],_check_frozen() == True
        assert d.one[1],_check_frozen() == True
        assert d.next,_check_frozen() == True
