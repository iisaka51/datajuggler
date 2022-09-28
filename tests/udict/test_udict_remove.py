# -*- coding: utf-8 -*-

import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import aDict, uDict

class TestClass:

    def test_udict_remove_case01(self):
        data = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        expect = {
            "a": 1,
            "b": 2,
        }

        result = uDict().remove("c", data)
        assert result == expect
        obj = uDict(data)
        result = obj.remove("c")
        assert result == expect

    def test_udict_remove_case02(self):
        data = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        expect = {
            "a": 1,
            "b": 2,
        }

        obj = uDict(data)
        obj.remove("c", inplace=True)
        assert obj == expect

    def test_udict_remove_case03(self):
        data = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        expect = aDict({
            "a": 1,
            "b": 2,
        })

        result = uDict(data).remove("c", factory=aDict)
        assert result == expect


    def test_udict_remove_case04(self):
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
        result = uDict(data).remove(["c", "d", "e"])
        assert result == expect

    def test_udict_remove_case05(self):
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
        result = uDict(data).remove(("c", "d", "e"))
        assert result == expect
