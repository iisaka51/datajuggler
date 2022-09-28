import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import aDict, uDict

class TestClass:

    def test_udict_subset_case01(self):
        data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        expect = { 'b': 2 }
        result = uDict().subset('b', None, data)
        assert result == expect
        obj = uDict(data)
        result = obj.subset('b')
        assert result == expect

    def test_udict_subset_case02(self):
        data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        expect = { 'b': 2, 'd': 4 }
        result = uDict(data).subset(['b', 'd'])
        assert result == expect

    def test_udict_subset_case03(self):
        data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        expect = { 'b': 2, 'd': 4 }
        result = uDict(data).subset(('b', 'd'))
        assert result == expect

    def test_udict_subset_case04(self):
        data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        expect = { 'b': 2, 'd': 4 }
        obj = uDict(data)
        obj.subset(('b', 'd'), inplace=True)
        assert obj == expect

    def test_udict_subset_case05(self):
        data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        expect = aDict({ 'b': 2, 'd': 4 })
        result = uDict(data).subset(('b', 'd'), factory=aDict)
        assert result == expect

    def test_udict_subset_case06(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3 },
                        "d": { "x": 4, "y": 5 },
                 },
        }
        expect = {'z': {}}
        result = uDict(data).subset(keys='z', default={})
        assert result == expect

    def test_udict_subset_case07(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3 },
                        "d": { "x": 4, "y": 5 },
                 },
        }
        expect = '"Multiple keys founded.\'x\'"'
        with pytest.raises(KeyError) as e:
            result = uDict(data).subset(keys='x', default={})
        assert str(e.value) == expect

    def test_udict_subset_case08(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3 },
                        "d": { "x": 4, "y": 5 },
                 },
        }
        expect = {'b.c.x': 2, 'b.d.x': 4}
        result = uDict(data).subset(keys='x', default={}, use_keypath=True)
        assert result == expect


    def test_udict_subset_case09(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3 },
                        "d": { "x": 4, "y": 5 },
                 },
        }
        expect = {'c': {'x': 2, 'y': 3}}
        result = uDict(data).subset(keys='c')
        assert result == expect

    def test_udict_subset_case10(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3 },
                        "d": { "x": 4, "y": 5 },
                 },
        }
        expect = {'c': {'x': 2, 'y': 3},
                  'd': { 'x': 4,'y': 5}
                  }
        result = uDict(data).subset(keys=['c', 'd'])
        assert result == expect

    def test_udict_subset_case11(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3 },
                        "d": { "x": 4, "y": 5 },
                 },
        }
        expect = {'b.c': {'x': 2, 'y': 3},
                  'b.d': { 'x': 4,'y': 5}
                  }
        result = uDict(data).subset(keys=['c', 'd'], use_keypath=True)
        assert result == expect

    def test_udict_subset_case12(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3 },
                        "d": { "x": 4, "y": 5 },
                 },
        }
        expect = {'b c': {'x': 2, 'y': 3},
                  'b d': { 'x': 4,'y': 5}
                  }
        result = uDict(data).subset(keys=['c', 'd'],
                                   use_keypath=True, separator=' ')
        assert result == expect
