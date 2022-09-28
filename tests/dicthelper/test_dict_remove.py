# -*- coding: utf-8 -*-

import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import aDict
from datajuggler.dicthelper import d_remove

class TestClass:

    def test_remove_case01(self):
        data = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        expect = {
            "a": 1,
            "b": 2,
        }

        result = d_remove(data, "c")
        assert result == expect

    def test_remove_case02(self):
        data = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        expect = {
            "a": 1,
            "b": 2,
        }

        d_remove(data, "c", inplace=True)
        assert data == expect

    def test_remove_case03(self):
        data = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        expect = aDict({
            "a": 1,
            "b": 2,
        })

        result = d_remove(data, "c", factory=aDict)
        assert result == expect


    def test_remove_case04(self):
        data = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
        }
        expect = {
            "a": 1,
            "b": 2,
        }
        result = d_remove(data, ["c", "d", "e"])
        assert result == expect

    def test_remove_case05(self):
        data = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
        }
        expect = {
            "a": 1,
            "b": 2,
        }
        result = d_remove(data, ("c", "d", "e"))
        assert result == expect
