import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import aDict, uDict

class TestClass:

    def test_udict_swap_case01(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = { "a": 2, "b": 1, "c": 3, "d": None, }

        result = uDict().swap("a", "b", data)
        assert result == expect
        obj = uDict(data)
        result = obj.swap("a", "b")
        assert result == expect

    def test_udict_swap_case02(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = uDict(data).swap("a", "a")
        assert result == data

    def test_udict_swap_case03(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = { "a": 2, "b": 1, "c": 3, "d": None, }

        obj = uDict(data)
        obj.swap("a", "b", inplace=True)
        assert obj == expect

    def test_udict_swap_case04(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = aDict({ "a": 2, "b": 1, "c": 3, "d": None, })

        result = uDict(data).swap("a", "b", factory=aDict)
        assert result == expect
