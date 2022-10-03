# -*- coding: utf-8 -*-

import pytest

from datajuggler import aDict, uDict

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

    def test_udict_clean_case01_1(self):
        expect = uDict({
            "b": {"x": 1},
            "d": [0, 1],
            "e": 0.0,
            "h": "0",
        })

        result = uDict().clean(self.data)
        assert result == expect

    def test_udict_clean_case01_2(self):
        expect = uDict({
            "b": {"x": 1},
            "d": [0, 1],
            "e": 0.0,
            "h": "0",
        })

        obj = uDict(self.data)
        result = obj.clean()
        assert result == expect


    def test_udict_clean_case02(self):
        expect = uDict({
            "a": {},
            "b": {"x": 1},
            "c": [],
            "d": [0, 1],
            "e": 0.0,
            "h": "0",
        })

        result = uDict(self.data).clean(collections=False)
        assert result == expect

    def test_udict_clean_case03(self):
        expect = uDict({
            "b": {"x": 1},
            "d": [0, 1],
            "e": 0.0,
            "f": "",
            "h": "0",
        })

        result = uDict(self.data).clean(strings=False)
        assert result == expect

    def test_udict_clean_case04(self):
        expect = aDict({
                    "b": {"x": 1},
                    "d": [0, 1],
                    "e": 0.0,
                    "h": "0",
                 })

        result = uDict(self.data).clean(factory=aDict)
        assert result == expect

    def test_udict_clean_case05(self):
        expect = uDict({
            "b": {"x": 1},
            "d": [0, 1],
            "e": 0.0,
            "h": "0",
        })

        # data = self.data.copy()
        obj = uDict(self.data)
        obj.clean(inplace=True)
        assert obj == expect


