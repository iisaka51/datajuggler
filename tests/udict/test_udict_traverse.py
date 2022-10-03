# -*- coding: utf-8 -*-

import pytest

from datajuggler import uDict, Keylist

class TestClass:

    def test_udict_traverse_case01_1(self):
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

        obj = uDict(data)
        obj.traverse(func)
        assert obj == expect

    def test_udict_traverse_case01_2(self):
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

        uDict().traverse(func, data)
        assert data == expect

    def test_udict_traverse_case02(self):
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
        uDict(data).traverse(func)
        assert paths == expect

    def test_udict_traverse_case03(self):
        def func(obj, index, val, parents, *args, **kwargs):
            if not isinstance(val, list):
                obj[index] = val + 1000

        data = [ 100, [200, [300, 310], 210], 110]
        expect = [ 1100, [1200, [1300, 1310], 1210], 1110]

        uDict().traverse(func, data)
        assert data == expect

    def test_udict_traverse_case04(self):
        def func(obj, index, val, parents, *args, **kwargs):
            nonlocal paths
            keypath = Keylist(parents).to_keypath().value()
            paths.append( f'{keypath}={val}' )

        data = [ 100, [200, [300, 310], 210], 110]

        expect = ['[0]=100',
                  '[1]=[200, [300, 310], 210]',
                  '[1][0]=200',
                  '[1][1]=[300, 310]',
                  '[1][1][0]=300',
                  '[1][1][1]=310',
                  '[1][2]=210',
                  '[2]=110']

        paths = []
        uDict().traverse(func, data)
        assert paths == expect

    def test_udict_traverse_case05(self):
        def func(obj, key, val, parents, *args, **kwargs):
            nonlocal paths
            if not isinstance(val, dict) and  not isinstance(val, list):
                obj[key] = val + 1

        data = { "a": { "x": [ 100, 200], "y": 3, "z": { "ok": 5, }, },
                 "b": { "x": [ 110, 210], "y": 11, "z": { "ok": 13, }, },
                 "c": { "x": [ 120, 220], "y": 19, "z": { "ok": 13, }, },
               }
        expect = {'a': {'x': [101, 201], 'y': 4, 'z': {'ok': 6}},
                  'b': {'x': [111, 211], 'y': 12, 'z': {'ok': 14}},
                  'c': {'x': [121, 221], 'y': 20, 'z': {'ok': 14}}}

        paths = []
        obj = uDict(data)
        obj.traverse(func)
        assert obj == expect

    def test_udict_traverse_case06(self):
        def func(obj, key, val, parents, *args, **kwargs):
            nonlocal paths
            if not isinstance(val, dict) and  not isinstance(val, list):
                obj[key] = val + 1
                keypath = Keylist(parents).to_keypath(separator='_')
                paths.append(keypath)

        data = { "a": { "x": [ 100, 200], "y": 3, "z": { "ok": 5, }, },
                 "b": { "x": [ 110, 210], "y": 11, "z": { "ok": 13, }, },
                 "c": { "x": [ 120, 220], "y": 19, "z": { "ok": 13, }, },
               }
        expect = ['a_x[0]',
                  'a_x[1]',
                  'a_y',
                  'a_z_ok',
                  'b_x[0]',
                  'b_x[1]',
                  'b_y',
                  'b_z_ok',
                  'c_x[0]',
                  'c_x[1]',
                  'c_y',
                  'c_z_ok']

        paths = []
        uDict(data).traverse(func)
        assert paths == expect


