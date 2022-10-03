# -*- coding: utf-8 -*-

import pytest

from datajuggler import uDict

class TestClass:

    def test_udict_unique_case01(self):
        data = { "a": { "x": 1, "y": 1, },
                 "b": { "x": 2, "y": 2, },
                 "c": { "x": 1, "y": 1, },
                 "d": { "x": 1, },
                 "e": { "x": 1, "y": 1, "z": 1, },
                 "f": { "x": 2, "y": 2, },
        }
        expect = [{'x': 1, 'y': 1},
                  {'x': 2, 'y': 2},
                  {'x': 1},
                  {'x': 1, 'y': 1, 'z': 1}]

        result = uDict().unique(data)
        assert result == expect
        obj = uDict(data)
        result = obj.unique()
        assert result == expect

