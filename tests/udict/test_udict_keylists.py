# -*- coding: utf-8 -*-

import pytest

from datajuggler import uDict, Keylist

class TestClass:

    def test_udict_keylists_case01(self):
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
        result = uDict().keylists(data)
        assert result == expect

        obj = uDict(data)
        result = obj.keylists()
        assert result == expect

    def test_udict_keylists_case02(self):
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
        result = uDict().keylists(data)
        assert result == expect
        assert result == expect_list

    def test_udict_keylists_case03(self):
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
            Keylist(["a"]),
            Keylist(["b"]),
            Keylist(["b", "c"]),
            Keylist(["b", "c", "x"]),
            Keylist(["b", "c", "y"]),
            Keylist(["b", "d"]),
            Keylist(["b", "d", "x"]),
            Keylist(["b", "d", "y"]),
            Keylist(["b", "e"]),
            Keylist(["b", "e[0]"]),
            Keylist(["b", "e[0]", "x"]),
            Keylist(["b", "e[0]", "y"]),
            Keylist(["b", "e[0]", "z"]),
            Keylist(["b", "e[0]", "z[0]"]),
            Keylist(["b", "e[0]", "z[1]"]),
            Keylist(["b", "e[0]", "z[2]"]),
            Keylist(["b", "e[1]"]),
            Keylist(["b", "e[1]", "x"]),
            Keylist(["b", "e[1]", "y"]),
            Keylist(["b", "e[1]", "z"]),
            Keylist(["b", "e[1]", "z[0]"]),
            Keylist(["b", "e[1]", "z[1]"]),
            Keylist(["b", "e[1]", "z[2]"]),
            Keylist(["b", "e[2]"]),
            Keylist(["b", "e[2]", "x"]),
            Keylist(["b", "e[2]", "y"]),
            Keylist(["b", "e[2]", "z"]),
            Keylist(["b", "e[2]", "z[0]"]),
            Keylist(["b", "e[2]", "z[1]"]),
            Keylist(["b", "e[2]", "z[2]"]),
        ]
        result  = uDict().keylists(data, indexes=True)
        result.sort()
        assert result == expect

    def test_udict_keylists_case04(self):
        data = { "a": { "b": [
                           [1, 2],
                           [3, 4, 5],
                           [ { "x": 1, "y": -1, }, ],
                         ],
                      },
               }
        expect = [
                Keylist(["a"]),
                Keylist(["a", "b"]),
                Keylist(["a", "b[0]"]),
                Keylist(["a", "b[0][0]"]),
                Keylist(["a", "b[0][1]"]),
                Keylist(["a", "b[1]"]),
                Keylist(["a", "b[1][0]"]),
                Keylist(["a", "b[1][1]"]),
                Keylist(["a", "b[1][2]"]),
                Keylist(["a", "b[2]"]),
                Keylist(["a", "b[2][0]"]),
                Keylist(["a", "b[2][0]", "x"]),
                Keylist(["a", "b[2][0]", "y"]),
            ]
        result = uDict().keylists(data, indexes=True)
        result.sort()
        assert result == expect

    def test_udict_keylists_case05(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3, },
                        "d": { "x": 4, "y": 5, },
                        "e": [ { "x": 1, "y": -1, "z": [1, 2, 3], },
                               { "x": 2, "y": -2, "z": [2, 3, 4], },
                               { "x": 3, "y": -3, "z": [3, 4, 5], },
                             ],
                      },
              }
        expect = [
                Keylist(["a"]),
                Keylist(["b"]),
                Keylist(["b", "c"]),
                Keylist(["b", "c", "x"]),
                Keylist(["b", "c", "y"]),
                Keylist(["b", "d"]),
                Keylist(["b", "d", "x"]),
                Keylist(["b", "d", "y"]),
                Keylist(["b", "e"]),
               ]
        result = uDict().keylists(data, indexes=False)
        result.sort()
        assert result == expect


    def test_udict_access_by_keylist_case01(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3, },
                        "d": { "x": 4, "y": 5, },
                        "e": [ { "x": 1, "y": -1, "z": [1, 2, 3], },
                               { "x": 2, "y": -2, "z": [2, 3, 4], },
                               { "x": 3, "y": -3, "z": [3, 4, 5], },
                             ],
                      },
              }
        obj = uDict(data)
        assert obj['a'] == 1
        assert obj['b', 'c'] == None
        assert obj['b', 'c', 'x'] == None
        assert obj['b', 'd', 'x'] == None

    def test_udict_access_by_keylist_case02(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3, },
                        "d": { "x": 4, "y": 5, },
                        "e": [ { "x": 1, "y": -1, "z": [1, 2, 3], },
                               { "x": 2, "y": -2, "z": [2, 3, 4], },
                               { "x": 3, "y": -3, "z": [3, 4, 5], },
                             ],
                      },
              }
        obj = uDict(data)
        assert obj[Keylist(['a'])] == 1
        assert obj[Keylist(['b', 'c'])] == { "x": 2, "y": 3, }
        assert obj[Keylist(['b', 'c', 'x'])] == 2
        assert obj[Keylist(['b', 'd', 'x'])] == 4

    def test_udict_access_by_keylist_case03(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3, },
                        "d": { "x": 4, "y": 5, },
                        "e": [ { "x": 1, "y": -1, "z": [1, 2, 3], },
                               { "x": 2, "y": -2, "z": [2, 3, 4], },
                               { "x": 3, "y": -3, "z": [3, 4, 5], },
                             ],
                      },
              }
        obj = uDict(data)
        assert obj[Keylist(['b', 'e[1]', 'z[2]'])] == 4

    def test_udict_access_by_keylist_case04(self):
        data = { "a.b": { "c.d": 1,
                          "e.f": 2, },
                 "g.h": { "i.j": 3,
                          "k.l": 4, },
               }

        obj = uDict(data)
        assert obj[Keylist(['a.b', 'c.d'], separator='/')] == 1

