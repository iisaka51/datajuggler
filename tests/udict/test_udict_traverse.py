import sys
import time
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import uDict

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
            index_paths = [ str(x) for x in parents ]
            paths.append( ' '.join(index_paths))

        data = [ 100, [200, [300, 310], 210], 110]

        expect = ['0', '1', '1 0', '1 1', '1 1 0', '1 1 1', '1 2', '2']

        paths = []
        uDict().traverse(func, data)
        assert paths == expect

    def test_udict_traverse_case05(self):
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
        uDict(data).traverse(func)
        assert data == expect

    def test_udict_traverse_case06(self):
        def func(obj, key, val, parents, *args, **kwargs):
            nonlocal paths
            if not isinstance(val, dict) and  not isinstance(val, list):
                obj[key] = val + 1
                index_paths = [ str(x) for x in parents ]
                paths.append( ' '.join(index_paths))

        data = { "a": { "x": [ 100, 200], "y": 3, "z": { "ok": 5, }, },
                 "b": { "x": [ 110, 210], "y": 11, "z": { "ok": 13, }, },
                 "c": { "x": [ 120, 220], "y": 19, "z": { "ok": 13, }, },
               }
        expect = ['a x 0',
                  'a x 1',
                  'a y',
                  'a z ok',
                  'b x 0',
                  'b x 1',
                  'b y',
                  'b z ok',
                  'c x 0',
                  'c x 1',
                  'c y',
                  'c z ok']

        paths = []
        uDict(data).traverse(func)
        assert paths == expect


