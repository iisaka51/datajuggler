# -*- coding: utf-8 -*-

import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import aDict, uDict

class TestClass:

    def test_udict_move_case01(self):
        data = {
            "a": 1,
            "b": 2,
        }
        expect  = {
            "a": 1,
            "b": 2,
        }
        result = uDict().move("a", "a", data)
        assert result == expect
        obj = uDict(data)
        result = obj.move("a", "a")
        assert result == expect


    def test_udict_move_case02(self):
        data = {
            "a": { "x": 1, "y": 1, },
            "b": { "x": 2, "y": 2, },
            "c": { "x": 3, "y": 3, },
        }
        expect = {
            "b": { "x": 2, "y": 2, },
            "c": { "x": 3, "y": 3, },
            "d": { "x": 1, "y": 1, },
        }

        result = uDict(data).move("a", "d")
        assert result == expect


    def test_udict_move_case03(self):
        data = {
            "a": { "x": 1, "y": 1, },
            "b": { "x": 2, "y": 2, },
            "c": { "x": 3, "y": 3, },
        }
        expect = {
            'b': {'x': 2, 'y': 2},
            'c': {'x': 3, 'y': 3},
            'd': {'x': 1, 'y': 1}
        }

        result = uDict(data).move("a", "d", overwrite=False)
        assert result == expect

    def test_udict_move_case04(self):
        data = {
            "a": { "x": 1, "y": 1, },
            "b": { "x": 2, "y": 2, },
            "c": { "x": 3, "y": 3, },
        }
        expect = {
            "d": { "x": 1, "y": 1, },
            "b": { "x": 2, "y": 2, },
            "c": { "x": 3, "y": 3, },
        }

        obj = uDict(data)
        obj.move("a", "d", inplace=True)
        assert obj == expect

    def test_udict_move_case05(self):
        data = {
            "a": { "x": 1, "y": 1, },
            "b": { "x": 2, "y": 2, },
            "c": { "x": 3, "y": 3, },
        }
        expect = aDict({
            "d": { "x": 1, "y": 1, },
            "b": { "x": 2, "y": 2, },
            "c": { "x": 3, "y": 3, },
        })

        result = uDict(data).move("a", "d", factory=aDict)
        assert result == expect

