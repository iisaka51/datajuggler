# -*- coding: utf-8 -*-

import pytest

from datajuggler import Keylist
from datajuggler.dicthelper import keylists

class TestClass:

    def test_keylists_case01(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3, },
                        "d": { "x": 4, "y": 5, },
                      },
                }
        expect = [ ["a"],
                   ["b"],
                   ["b", "c"],
                   ["b", "c", "x"],
                   ["b", "c", "y"],
                   ["b", "d"],
                   ["b", "d", "x"],
                   ["b", "d", "y"],
               ]
        result = keylists(data)
        assert result == expect

    def test_keylists_case02(self):
        data = { 1: { 1: 1, },
                 2: { 2: 1, },
                 3: { 3: 1, },
               }
        expect_list = [[1], [1, 1], [2], [2, 2], [3], [3, 3]]
        expect = [
                Keylist([1]),
                Keylist([1, 1]),
                Keylist([2]),
                Keylist([2, 2]),
                Keylist([3]),
                Keylist([3, 3])
            ]
        result = keylists(data)
        assert result == expect
        assert result == expect_list

    def test_keylists_case03(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3, },
                        "d": { "x": 4, "y": 5, },
                        "e": [ { "x": 1, "y": -1,
                                 "z": [1, 2, 3], },
                               { "x": 2, "y": -2, "z": [2, 3, 4], },
                               { "x": 3, "y": -3, "z": [3, 4, 5], },
                             ],
                      },
               }
        expect = [
            ["a"],
            ["b"],
            ["b", "c"],
            ["b", "c", "x"],
            ["b", "c", "y"],
            ["b", "d"],
            ["b", "d", "x"],
            ["b", "d", "y"],
            ["b", "e"],
            ["b", "e[0]"],
            ["b", "e[0]", "x"],
            ["b", "e[0]", "y"],
            ["b", "e[0]", "z"],
            ["b", "e[0]", "z[0]"],
            ["b", "e[0]", "z[1]"],
            ["b", "e[0]", "z[2]"],
            ["b", "e[1]"],
            ["b", "e[1]", "x"],
            ["b", "e[1]", "y"],
            ["b", "e[1]", "z"],
            ["b", "e[1]", "z[0]"],
            ["b", "e[1]", "z[1]"],
            ["b", "e[1]", "z[2]"],
            ["b", "e[2]"],
            ["b", "e[2]", "x"],
            ["b", "e[2]", "y"],
            ["b", "e[2]", "z"],
            ["b", "e[2]", "z[0]"],
            ["b", "e[2]", "z[1]"],
            ["b", "e[2]", "z[2]"],
        ]
        result  = keylists(data, indexes=True)
        result.sort()
        assert result == expect

    def test_keylists_case04(self):
        data = { "a": { "b": [
                           [1, 2],
                           [3, 4, 5],
                           [ { "x": 1, "y": -1, }, ],
                         ],
                      },
               }
        expect = [ ["a"],
                   ["a", "b"],
                   ["a", "b[0]"],
                   ["a", "b[0][0]"],
                   ["a", "b[0][1]"],
                   ["a", "b[1]"],
                   ["a", "b[1][0]"],
                   ["a", "b[1][1]"],
                   ["a", "b[1][2]"],
                   ["a", "b[2]"],
                   ["a", "b[2][0]"],
                   ["a", "b[2][0]", "x"],
                   ["a", "b[2][0]", "y"],
                ]
        result = keylists(data, indexes=True)
        result.sort()
        assert result == expect

    def test_keylists_case05(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3, },
                        "d": { "x": 4, "y": 5, },
                        "e": [ { "x": 1, "y": -1, "z": [1, 2, 3], },
                               { "x": 2, "y": -2, "z": [2, 3, 4], },
                               { "x": 3, "y": -3, "z": [3, 4, 5], },
                             ],
                      },
              }
        expect = [ ["a"],
                   ["b"],
                   ["b", "c"],
                   ["b", "c", "x"],
                   ["b", "c", "y"],
                   ["b", "d"],
                   ["b", "d", "x"],
                   ["b", "d", "y"],
                   ["b", "e"],
               ]
        result = keylists(data, indexes=False)
        result.sort()
        assert result == expect
