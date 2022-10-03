# -*- coding: utf-8 -*-

import pytest

from datajuggler import uDict, aDict
from datajuggler.dicthelper import d_map

class TestClass:

    def test_map_items_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 1: 'January', 2: 'February', 3: 'March', 4: 'April' }
        result = d_map(reversed, data)
        assert result == expect

    def test_map_items_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 1: 'January', 2: 'February', 3: 'March', 4: 'April' })
        result = d_map(reversed, data, factory=uDict)
        assert result == expect

    def test_map_items_case03(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 1: 'January', 2: 'February', 3: 'March', 4: 'April' }
        result = d_map(reversed, data, inplace=True)
        assert data == expect

    def test_map_key_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = uDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
        result = d_map(str.upper, data, map_for="key")
        assert result == expect


    def test_map_value_case01(self):
        data = { 'Jack': [10, 11, 12], 'John': [8, 15, 3] }
        expect = { 'Jack': 33, 'John': 26 }
        result = d_map(sum, data, map_for="value")
        assert result == expect

