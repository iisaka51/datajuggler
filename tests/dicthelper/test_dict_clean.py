# -*- coding: utf-8 -*-

import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import aDict
from datajuggler.dicthelper import d_clean

class TestClass:
    data = {
            "a": {},
            "b": {"x": 1},
            "c": [],
            "d": [0, 1],
            "e": 0.0,
            "f": "",
            "g": None,
            "h": "0",
        }

    def test_clean_case01(self):
        expect = {
            "b": {"x": 1},
            "d": [0, 1],
            "e": 0.0,
            "h": "0",
        }

        result = d_clean(self.data)
        assert result == expect


    def test_clean_case02(self):
        expect = {
            "a": {},
            "b": {"x": 1},
            "c": [],
            "d": [0, 1],
            "e": 0.0,
            "h": "0",
        }

        result = d_clean(self.data, collections=False)
        assert result == expect

    def test_clean_case03(self):
        expect = {
            "b": {"x": 1},
            "d": [0, 1],
            "e": 0.0,
            "f": "",
            "h": "0",
        }

        result = d_clean(self.data, strings=False)
        assert result == expect

    def test_clean_case04(self):
        expect = aDict({
                    "b": {"x": 1},
                    "d": [0, 1],
                    "e": 0.0,
                    "h": "0",
                 })

        result = d_clean(self.data, factory=aDict)
        assert result == expect

    def test_clean_case05(self):
        expect = {
            "b": {"x": 1},
            "d": [0, 1],
            "e": 0.0,
            "h": "0",
        }

        data = self.data.copy()
        d_clean(data, inplace=True)
        assert data == expect


