import sys
import time
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import (
    uDict, iDict, aDict,
    change_dict_keys, ordereddict_to_dict,
)

from collections import OrderedDict
import pandas as pd

class TestClass:
    def test_adict_json_case01(self):
        data = {"console": "Nintendo Switch",
                "games": ["The Legend of Zelda", "Mario Golf"]}
        expect = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        obj = aDict(data)
        assert obj.to_json() == expect

    def test_adict_json_case02(self):
        json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        expect = "aDict({'console': 'Nintendo Switch', 'games': ['The Legend of Zelda', 'Mario Golf']})"
        obj = aDict().from_json(json_data)
        assert obj.__repr__() == expect

    def test_adict_json_case03(self):
        json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        expect = "aDict({'console': 'Nintendo Switch', 'games': ['The Legend of Zelda', 'Mario Golf']})"
        obj = aDict()
        obj.from_json(json_data, inplace=True)
        assert obj.__repr__() == expect

    def test_udict_json_case01(self):
        data = {"console": "Nintendo Switch",
                "games": ["The Legend of Zelda", "Mario Golf"]}
        expect = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        obj = uDict(data)
        assert obj.to_json() == expect

    def test_udict_json_case02(self):
        json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        expect = "uDict({'console': 'Nintendo Switch', 'games': ['The Legend of Zelda', 'Mario Golf']})"
        new = uDict().from_json(json_data)
        assert new.__repr__() == expect

    def test_udict_json_case03(self):
        json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        expect = "uDict({'console': 'Nintendo Switch', 'games': ['The Legend of Zelda', 'Mario Golf']})"
        obj = uDict()
        obj.from_json(json_data, inplace=True)
        assert obj.__repr__() == expect

    def test_idict_json_case01(self):
        data = {"console": "Nintendo Switch",
                "games": ["The Legend of Zelda", "Mario Golf"]}
        expect = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        obj = iDict(data)
        assert obj.to_json() == expect

    def test_idict_json_case02(self):
        json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        expect = "iDict({'console': 'Nintendo Switch', 'games': ['The Legend of Zelda', 'Mario Golf']})"
        result = iDict().from_json(json_data)
        assert result.__repr__() == expect

    def test_idict_json_case03(self):
        json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'
        expect = "iDict({})"
        obj = iDict()
        obj.from_json(json_data, inplace=True)
        assert obj.__repr__() == expect
