import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import aDict
from datajuggler.dicthelper import d_swap

class TestClass:

    def test_swap_case01(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = { "a": 2, "b": 1, "c": 3, "d": None, }

        result = d_swap(data, "a", "b")
        assert result == expect

    def test_swap_case02(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = d_swap(data, "a", "a")
        assert result == data

    def test_swap_case03(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = { "a": 2, "b": 1, "c": 3, "d": None, }

        d_swap(data, "a", "b", inplace=True)
        assert data == expect

    def test_swap_case04(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = aDict({ "a": 2, "b": 1, "c": 3, "d": None, })

        result = d_swap(data, "a", "b", factory=aDict)
        assert result == expect
