# -*- coding: utf-8 -*-

import pytest

from datajuggler.dicthelper import d_find

class TestClass:

    def test_find_case01(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = 2

        result = d_find(data, "b", 0)
        assert result == 2

    def test_find_case02(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = d_find(data, "e", 0)
        assert result == 0

    def test_find_case03(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = d_find(data, ["x", "y", "b", "z"], 5)
        assert result == 2

    def test_find_case04(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = d_find(data, ["a", "x", "b", "y"], 5)
        assert result == 1

    def test_find_case05(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = d_find(data, ["x", "y", "z"])
        assert result == None

    def test_find_case06(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = d_find(data, ["a", "b", "c"], first_one=True)
        assert result == 1

    def test_find_case07(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = { 'a': 1, 'b': 2, 'c': 3 }

        result = d_find(data, ["a", "b", "c"], first_one=False)
        assert result == expect

