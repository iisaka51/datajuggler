# -*- coding: utf-8 -*-

import pytest

from datajuggler.dicthelper import d_clone

data = { "a": { "b": { "c": 1, }, }, }

class TestCase:

    def test_clone_case01(self):
        result = d_clone(data)
        assert isinstance(result, dict) == True
        assert result == data

        result["a"]["b"]["c"] = 2

        assert result["a"]["b"]["c"] == 2
        assert data["a"]["b"]["c"] == 1

    def test_clone_case02(self):
        result = d_clone(data, empty=True)
        assert isinstance(result, dict) == True
        assert result == {}

