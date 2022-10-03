# -*- coding: utf-8 -*-

import pytest

from datajuggler import aDict, uDict

class TestClass:

    def test_udict_invert_case01(self):
        data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        expect = {1: ['a'], 2: ['b'], 3: ['c'], 4: ['d'], 5: ['e']}
        result = uDict().invert(data)
        assert result == expect

        obj = uDict(data)
        result = obj.invert()
        assert result == expect

    def test_udict_invert_case02(self):
        data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        expect = {1: ['a'], 2: ['b'], 3: ['c'], 4: ['d'], 5: ['e']}
        uDict().invert(data, inplace=True)
        assert data == expect

    def test_udict_invert_case03(self):
        data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        expect = aDict({1: ['a'], 2: ['b'], 3: ['c'], 4: ['d'], 5: ['e']})
        result = uDict().invert(data, factory=aDict)
        assert result == expect

    def test_udict_invert_case04(self):
        data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        expect = { 1: "a", 2: "b", 3: "c", 4: "d", 5: "e"}
        result = uDict().invert(data, flat=True)
        assert result == expect

    def test_udict_invert_case05(self):
        data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        expect = { 1: "a", 2: "b", 3: "c", 4: "d", 5: "e"}
        uDict().invert(data, flat=True, inplace=True)
        assert data == expect

    def test_udict_invert_case06(self):
        data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        expect = aDict({ 1: "a", 2: "b", 3: "c", 4: "d", 5: "e"})
        result = uDict().invert(data, flat=True, factory=aDict)
        assert result == expect

