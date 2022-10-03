# -*- coding: utf-8 -*-

import pytest

from datajuggler.dicthelper import d_counts

class TestClass:

    data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
                              {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}

    def test_count_key_case01(self):
        expect = 2
        count = d_counts(self.data, 'aA')
        assert count == expect

    def test_count_key_case02(self):
        expect = 2
        count = d_counts(self.data, 'aA', count_for='key')

    def test_count_key_case03(self):
        expect = 0
        count = d_counts(self.data, 'aa', count_for='key')
        assert count == expect

    def test_count_key_case04(self):
        expect = 2
        count = d_counts(self.data, 'aa', count_for='key', wild=True)
        assert count == expect

    def test_count_key_case05(self):
        expect = {'aA': 2, 'b': 2}
        count = d_counts(self.data, ['aA', 'b'])
        assert count == expect

    def test_count_key_case06(self):
        expect = {'aA': 2, 'b': 2}
        count = d_counts(self.data, ['aA', 'b'], wild=True)
        assert count == expect


    def test_count_key_case07(self):
        expect = {'aA': 2, 'b': 2}
        count = d_counts(self.data, ['a', 'b'], wild=True, verbatim=True)
        assert count == expect


    def test_count_val_case01(self):
        expect = {'v11': 1}
        count = d_counts(self.data, 'v11', count_for='value')
        assert count == expect

    def test_count_val_case02(self):
        expect = {'v1': 3}
        count = d_counts(self.data, 'v1', count_for='value', wild=True)
        assert count == expect

    def test_count_val_case03(self):
        expect = {'v11': 1, 'v12': 1, 'v13': 1}
        count = d_counts(self.data, 'v1', count_for='value',
                                      wild=True, verbatim=True)
        assert count == expect

    def test_count_val_case04(self):
        expect = {100: 2}
        count = d_counts(self.data, 100, count_for='value')
        assert count == expect

