# -*- coding: utf-8 -*-

import pytest

from datajuggler import uDict, aDict

class TestClass:

    def test_filter_case01_1(self):
        is_janfeb = lambda x, y: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2 }
        result = uDict().filter(is_janfeb, data)
        assert result == expect

    def test_filter_case01_2(self):
        is_janfeb = lambda x, y: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2 }
        obj = uDict(data)
        result = obj.filter(is_janfeb)
        assert result == expect

    def test_filter_case02(self):
        is_janfeb = lambda x, y: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2 }
        result = uDict().filter(is_janfeb, data)
        assert result == expect

    def test_filter_case03(self):
        is_janfeb = lambda x, y: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'January': 1, 'February': 2 })
        result = uDict().filter(is_janfeb, data, factory=uDict)
        assert result == expect

    def test_filter_case04(self):
        is_janfeb = lambda x, y: x.endswith('ary')
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = aDict({ 'January': 1, 'February': 2 })
        result =uDict().filter(is_janfeb, data, factory=aDict)
        assert result == expect

    def test_filter_case05(self):
        is_even = lambda x, y: y % 2 == 0
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'February': 2, 'April': 4 }
        result = uDict().filter(is_even, data)
        assert result == expect

