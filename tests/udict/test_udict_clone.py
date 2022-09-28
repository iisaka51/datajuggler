# -*- coding: utf-8 -*-

import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import uDict


class TestCase:

    def test_udict_clone_case01_1(self):
        data = { "a": { "b": { "c": 1, }, }, }
        expect = uDict({ "a": { "b": { "c": 1, }, }, })

        result = uDict().clone(data)
        assert isinstance(result, dict) == True
        assert result == expect

        result["a"]["b"]["c"] = 2

        assert result["a"]["b"]["c"] == 2
        assert data["a"]["b"]["c"] == 1


    def test_udict_clone_case01_2(self):
        data = { "a": { "b": { "c": 1, }, }, }
        expect = uDict({ "a": { "b": { "c": 1, }, }, })

        result = uDict(data).clone()
        assert isinstance(result, dict) == True
        assert result == expect

        result["a"]["b"]["c"] = 2

        assert result["a"]["b"]["c"] == 2
        assert data["a"]["b"]["c"] == 1

    def test_udict_clone_case01_3(self):
        data = {
            "a": {
                "b": {
                    "c": 1,
                },
            },
        }

        obj = uDict(data)
        result = obj.clone()
        assert isinstance(result, dict) == True
        assert result == data

        result["a"]["b"]["c"] = 2

        assert result["a"]["b"]["c"] == 2
        assert data["a"]["b"]["c"] == 1

    def test_udict_clone_case02(self):
        data = {
            "a": {
                "b": {
                    "c": 1,
                },
            },
        }
        result = uDict().clone(data, empty=True)
        assert isinstance(result, dict) == True
        assert result == {}

