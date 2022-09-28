import sys
import time
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import uDict

class TestClass:

    def test_udict_find_case01_1(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = 2

        result = uDict().find("b", 0, data)
        assert result == 2

    def test_udict_find_case01_2(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = 2

        result = uDict(data).find("b", 0)
        assert result == 2

    def test_udict_find_case02(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = uDict(data).find("e", 0)
        assert result == 0

    def test_udict_find_case03(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = uDict(data).find(["x", "y", "b", "z"], 5)
        assert result == 2

    def test_udict_find_case04(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = uDict(data).find(["a", "x", "b", "y"], 5)
        assert result == 1

    def test_udict_find_case05(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = uDict(data).find( ["x", "y", "z"])
        assert result == None

    def test_udict_find_case06(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = uDict(data).find(["a", "b", "c"], first_one=True)
        assert result == 1

    def test_udict_find_case07(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = { 'a': 1, 'b': 2, 'c': 3 }

        result = uDict(data).find(["a", "b", "c"], first_one=False)
        assert result == expect

