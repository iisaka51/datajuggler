# -*- coding: utf-8 -*-

import pytest

from datajuggler import uDict


data = { "a": { "b": { "c": 1, }, }, }

class TestCase:
    def test_clone_case01(self):
        d1 = uDict(data)
        d2 = d1.clone()
        assert isinstance(d2, dict) == True
        assert d2 == data

        d2["a"]["b"]["c"] = 2
        assert d2["a"]["b"]["c"] == 2
        assert d1["a"]["b"]["c"] == 1

    def test_clone_case02(self):
        result = uDict().clone(data, empty=True)
        assert isinstance(result, dict) == True
        assert result == {}

