# -*- coding: utf-8 -*-

import pytest

from datajuggler import aDict
from datajuggler.dicthelper import d_sort

class TestClass:
    data = {
            "a": 8,
            "c": 6,
            "e": 4,
            "g": 2,
            "b": 7,
            "d": 5,
            "f": 3,
            "h": 1,
        }
    def test_sort_case01(self):
        expect  = {
            "a": 8,
            "b": 7,
            "c": 6,
            "d": 5,
            "e": 4,
            "f": 3,
            "g": 2,
            "h": 1,
        }

        result = d_sort(self.data)
        assert result == expect

    def test_sort_case02(self):
        expect  = {
            "a": 8,
            "b": 7,
            "c": 6,
            "d": 5,
            "e": 4,
            "f": 3,
            "g": 2,
            "h": 1,
        }

        data = self.data.copy()
        d_sort(data, inplace=True)
        assert  data == expect

    def test_sort_case03(self):
        expect  = aDict({
            "a": 8,
            "b": 7,
            "c": 6,
            "d": 5,
            "e": 4,
            "f": 3,
            "g": 2,
            "h": 1,
        })

        result = d_sort(self.data, factory=aDict)
        assert result == expect

    def test_sort_case04(self):
        expect  = {
            "h": 1,
            "g": 2,
            "f": 3,
            "e": 4,
            "d": 5,
            "c": 6,
            "b": 7,
            "a": 8,
        }

        result = d_sort(self.data, reverse=True)
        assert result == expect

    def test_sort_case05(self):
        expect  = {
            "h": 1,
            "g": 2,
            "f": 3,
            "e": 4,
            "d": 5,
            "c": 6,
            "b": 7,
            "a": 8,
        }

        result = d_sort(self.data, sort_by="value")
        assert result == expect

