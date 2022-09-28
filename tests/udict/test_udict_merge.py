# -*- coding: utf-8 -*-

import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import aDict, uDict

class TestClass:

    def test_udict_merge_case01(self):
        d1 = {
            "a": 1,
            "b": 1,
        }
        d2 = {
            "b": 2,
            "c": 3,
        }
        expect = uDict({
            "a": 1,
            "b": 2,
            "c": 3,
        })
        result = uDict().merge(d2, d1)
        assert result == expect
        obj = uDict(d1)
        result = obj.merge(d2)
        assert result == expect

    def test_udict_merge_case02(self):
        d1 = {
            "a": 1,
            "b": 1,
        }
        d2 = {
            "b": 2,
            "c": 3,
        }
        expect = aDict({
            "a": 1,
            "b": 2,
            "c": 3,
        })
        result = uDict(d1).merge(d2, factory=aDict)
        assert result == expect

    def test_udict_merge_case03(self):
        d1 = {
            "a": 1,
            "b": 1,
        }
        d2 = {
            "b": 2,
            "c": 3,
        }
        expect = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        obj = uDict(d1)
        obj.merge(d2, inplace=True)
        assert obj == expect

    def test_udict_merge_case04(self):
        d1 = {
            "a": [0, 1, 2],
            "b": [5, 6, 7],
            "c": [],
            "d": [],
        }
        d2 = {
            "a": [3, 4, 5],
            "b": [8, 9, 0],
            "c": [-1],
        }
        expect = {
            "a": [3, 4, 5],
            "b": [8, 9, 0],
            "c": [-1],
            "d": [],
        }
        result = uDict(d1).merge(d2)
        assert result == expect

    def test_udict_merge_case05(self):
        d1 = {
            "a": [0, 1, 2],
            "b": [5, 6, 7],
            "c": [],
            "d": [],
        }
        d2 = {
            "a": [3, 4, 5],
            "b": [8, 9, 0],
            "c": [-1],
        }
        expect = {
            "a": [0, 1, 2, 3, 4, 5],
            "b": [5, 6, 7, 8, 9, 0],
            "c": [-1],
            "d": [],
        }
        result = uDict(d1).merge(d2, concat=True)
        assert result == expect

    def test_udict_merge_case06(self):
        d1 = {
            "a": 1,
            "b": 1,
        }
        d2 = {
            "b": 2,
            "c": 3,
            "d": 3,
        }
        d3 = {
            "d": 5,
            "e": 5,
        }
        d4 = {
            "d": 4,
            "f": 6,
        }
        expect = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
        }
        result = uDict(d1).merge([d2, d3, d4])
        assert result == expect

    def test_udict_merge_case07(self):
        d1 = {
            "a": 1,
            "b": 1,
        }
        d2 = {
            "b": 2,
            "c": 3,
            "d": 3,
        }
        d3 = {
            "d": 5,
            "e": 5,
        }
        d4 = {
            "d": 4,
            "f": 6,
        }
        expect = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
        }
        result = uDict(d1).merge((d2, d3, d4))
        assert result == expect


    def test_udict_merge_case08(self):
        d1 = {
            "a": 1,
            "b": {
                "c": {
                    "x": 2,
                    "y": 3,
                },
                "d": {
                    "x": 4,
                    "y": 5,
                },
                "e": {
                    "x": 6,
                    "y": 7,
                },
            },
        }
        d2 = {
            "a": 0,
            "b": {
                "c": 1,
                "d": {
                    "y": 1,
                    "z": 2,
                },
                "e": {
                    "f": {
                        "x": 2,
                        "y": 3,
                    },
                    "g": {
                        "x": 4,
                        "y": 5,
                    },
                },
            },
        }
        expect = {
            "a": 0,
            "b": {
                "c": 1,
                "d": {
                    "x": 4,
                    "y": 1,
                    "z": 2,
                },
                "e": {
                    "f": {
                        "x": 2,
                        "y": 3,
                    },
                    "g": {
                        "x": 4,
                        "y": 5,
                    },
                    "x": 6,
                    "y": 7,
                },
            },
        }
        result = uDict(d1).merge(d2)
        assert result == expect

    def test_udict_merge_case09(self):
        d1 = {
            "a": 1,
            "b": {
                "c": {
                    "x": 2,
                    "y": 3,
                },
                "d": {
                    "x": 4,
                    "y": 5,
                },
                "e": {
                    "x": 6,
                    "y": 7,
                },
            },
        }
        d2 = {
            "a": 0,
            "b": {
                "c": 1,
                "d": {
                    "y": 1,
                    "z": 2,
                },
                "e": {
                    "f": {
                        "x": 2,
                        "y": 3,
                    },
                    "g": {
                        "x": 4,
                        "y": 5,
                    },
                },
            },
        }
        expect = {
            "a": 1,
            "b": {
                "c": {
                    "x": 2,
                    "y": 3,
                },
                "d": {
                    "x": 4,
                    "y": 5,
                    "z": 2,
                },
                "e": {
                    "f": {
                        "x": 2,
                        "y": 3,
                    },
                    "g": {
                        "x": 4,
                        "y": 5,
                    },
                    "x": 6,
                    "y": 7,
                },
            },
        }
        result = uDict(d1).merge(d2, overwrite=False)
        assert result == expect
