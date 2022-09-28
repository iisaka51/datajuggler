import sys
import time
import pytest

from datajuggler import serializer as io

data = {"console": "Nintendo Switch",
        "games": ["The Legend of Zelda", "Mario Golf"]}
json_data = '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'

class TestClass:
    def test_json_encode(self):
        s = io.JSONSerializer()
        result = s.encode(data)
        assert result == json_data

    def test_json_decode(self):
        s = io.JSONSerializer()
        result = s.decode(json_data)
        assert result == data

