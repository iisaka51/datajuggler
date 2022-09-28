# -*- coding: utf-8 -*-

import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler.dicthelper import d_clone


class TestCase:

    def test_clone_case01(self):
        data = {
            "a": {
                "b": {
                    "c": 1,
                },
            },
        }

        result = d_clone(data)
        assert isinstance(result, dict) == True
        assert result == data

        result["a"]["b"]["c"] = 2

        assert result["a"]["b"]["c"] == 2
        assert data["a"]["b"]["c"] == 1

    def test_clone_case02(self):
        data = {
            "a": {
                "b": {
                    "c": 1,
                },
            },
        }
        result = d_clone(data, empty=True)
        assert isinstance(result, dict) == True
        assert result == {}

