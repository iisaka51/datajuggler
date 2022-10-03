# -*- coding: utf-8 -*-

import pytest

from datajuggler import aDict
from datajuggler.dicthelper import d_move

class TestClass:

    def test_move_case01(self):
        data = {
            "a": 1,
            "b": 2,
        }
        expect  = {
            "a": 1,
            "b": 2,
        }
        result = d_move(data, "a", "a")
        assert result == expect


    def test_move_case02(self):
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

        result = d_move(data, "a", "d")
        assert result == expect


    def test_move_case03(self):
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

        result = d_move(data, "a", "d", overwrite=False)
        assert result == expect

    def test_move_case04(self):
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

        d_move(data, "a", "d", inplace=True)
        assert data == expect

    def test_move_case05(self):
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

        result = d_move(data, "a", "d", factory=aDict)
        assert result == expect

