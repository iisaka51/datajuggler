# -*- coding: utf-8 -*-

import pytest

from datajuggler import Keylist, Keypath
from datajuggler.dicthelper import d_traverse

class TestClass:

    def test_traverse_case01(self):
        def func(obj, key, val, *args, **kwargs):
            if not isinstance(val, dict):
                obj[key] = val + 1

        data = { "a": { "x": 2, "y": 3, "z": { "ok": 5, }, },
                 "b": { "x": 7, "y": 11, "z": { "ok": 13, }, },
                 "c": { "x": 17, "y": 19, "z": { "ok": 23, }, },
               }
        expect = {'a': {'x': 3, 'y': 4, 'z': {'ok': 6}},
                  'b': {'x': 8, 'y': 12, 'z': {'ok': 14}},
                  'c': {'x': 18, 'y': 20, 'z': {'ok': 24}}}

        d_traverse(data, func)
        assert data == expect

    def test_traverse_case02(self):
        def func(obj, key, val, parents, *args, **kwargs):
            nonlocal paths
            if not isinstance(val, dict):
                obj[key] = val + 1
                paths.append(' '.join(parents))

        data = { "a": { "x": 2, "y": 3, "z": { "ok": 5, }, },
                 "b": { "x": 7, "y": 11, "z": { "ok": 13, }, },
                 "c": { "x": 17, "y": 19, "z": { "ok": 23, }, },
               }
        expect = ['a x', 'a y', 'a z ok',
                  'b x', 'b y', 'b z ok',
                  'c x', 'c y', 'c z ok']

        paths = []
        d_traverse(data, func)
        assert paths == expect

    def test_traverse_case03(self):
        def func(obj, index, val, parents, *args, **kwargs):
            if not isinstance(val, list):
                obj[index] = val + 1000

        data = [ 100, [200, [300, 310], 210], 110]
        expect = [ 1100, [1200, [1300, 1310], 1210], 1110]

        d_traverse(data, func)
        assert data == expect

    def test_traverse_case04(self):
        def func(obj, index, val, parents, *args, **kwargs):
            nonlocal paths
            keypath = Keylist(parents).to_keypath()
            paths.append(keypath)

        data = [ 100, [200, [300, 310], 210], 110]

        expect = [ Keypath("[0]"),
                   Keypath("[1]"),
                   Keypath("[1][0]"),
                   Keypath("[1][1]"),
                   Keypath("[1][1][0]"),
                   Keypath("[1][1][1]"),
                   Keypath("[1][2]"),
                   Keypath("[2]"),
                ]

        paths = []
        d_traverse(data, func)
        assert paths == expect

    def test_traverse_case05(self):
        def func(obj, key, val, parents, *args, **kwargs):
            nonlocal paths
            if not isinstance(val, dict) and not isinstance(val, list):
                obj[key] = val + 1

        data = { "a": { "x": [ 100, 200], "y": 3, "z": { "ok": 5, }, },
                 "b": { "x": [ 110, 210], "y": 11, "z": { "ok": 13, }, },
                 "c": { "x": [ 120, 220], "y": 19, "z": { "ok": 13, }, },
               }
        expect = {'a': {'x': [101, 201], 'y': 4, 'z': {'ok': 6}},
                  'b': {'x': [111, 211], 'y': 12, 'z': {'ok': 14}},
                  'c': {'x': [121, 221], 'y': 20, 'z': {'ok': 14}}}

        paths = []
        d_traverse(data, func)
        assert data == expect

    def test_traverse_case06(self):
        def func(obj, key, val, parents, *args, **kwargs):
            nonlocal paths
            if not isinstance(val, dict) and  not isinstance(val, list):
                obj[key] = val + 1
                #index_paths = [ str(x) for x in parents ]
                #paths.append( ' '.join(index_paths))
                keypath = Keylist(parents).to_keypath(separator='_')
                paths.append(keypath)

        data = { "a": { "x": [ 100, 200], "y": 3, "z": { "ok": 5, }, },
                 "b": { "x": [ 110, 210], "y": 11, "z": { "ok": 13, }, },
                 "c": { "x": [ 120, 220], "y": 19, "z": { "ok": 13, }, },
               }
        expect = [ Keypath("a_x[0]"),
                   Keypath("a_x[1]"),
                   Keypath("a_y"),
                   Keypath("a_z_ok"),
                   Keypath("b_x[0]"),
                   Keypath("b_x[1]"),
                   Keypath("b_y"),
                   Keypath("b_z_ok"),
                   Keypath("c_x[0]"),
                   Keypath("c_x[1]"),
                   Keypath("c_y"),
                   Keypath("c_z_ok"),
                ]

        paths = []
        d_traverse(data, func)
        assert paths == expect


