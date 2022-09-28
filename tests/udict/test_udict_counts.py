import sys
import time
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import uDict

class TestClass:

    def test_udict_counts_key_case01_1(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = 2
        count = uDict().counts('aA', data)
        assert count == expect

    def test_udict_counts_key_case01_2(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = 2
        obj = uDict(data)
        count = obj.counts('aA')
        assert count == expect

    def test_udict_counts_key_case02(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = 2
        count = uDict().counts('aA', data, count_for='key')

    def test_udict_counts_key_case03(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = 0
        count = uDict().counts('aa', data, count_for='key')
        assert count == expect

    def test_udict_counts_key_case04(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = 2
        count = uDict().counts('aa', data, count_for='key', wild=True)
        assert count == expect

    def test_udict_counts_key_case05(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'aA': 2, 'b': 2}
        count = uDict().counts(['aA', 'b'], data)
        assert count == expect

    def test_udict_counts_key_case06(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'aA': 2, 'b': 2}
        count = uDict().counts(['aA', 'b'], data, wild=True)
        assert count == expect


    def test_udict_counts_key_case07(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'aA': 2, 'b': 2}
        count = uDict().counts(['a', 'b'], data, wild=True, verbatim=True)
        assert count == expect


    def test_udict_counts_val_case01(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'v11': 1}
        count = uDict().counts('v11', data, count_for='value')
        assert count == expect

    def test_udict_counts_val_case02(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'v1': 3}
        count = uDict().counts('v1', data, count_for='value', wild=True)
        assert count == expect

    def test_udict_counts_val_case03(self):
        data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                                  {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
        expect = {'v11': 1, 'v12': 1, 'v13': 1}
        count = uDict().counts('v1', data, count_for='value',
                                      wild=True, verbatim=True)
        assert count == expect

    def test_udict_counts_val_case04(self):
        data = {'x': {'y': {'z': [{'aA': 100, 'b': 101, 'c': 103},
                                  {'aA': 100, 'b': 101, 'c': 103}]} }}
        expect = {100: 2}
        count = uDict().counts(100, data, count_for='value')
        assert count == expect

