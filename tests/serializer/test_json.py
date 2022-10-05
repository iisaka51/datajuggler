import sys
import time
import pytest

from datajuggler import aDict, uDict
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

    def test_json_adict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.json'
        expect = aDict({'a': 1, 'b': 2, 'c': 3, 'x': 7, 'y': 8, 'z': 9})
        d = aDict(filepath, format='json')
        assert d == expect

    def test_json_adict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.json'
        expect = aDict({'a': 1, 'b': 2, 'c': 3, 'x': 7, 'y': 8, 'z': 9})
        d = aDict(filepath)
        assert d == expect

    def test_json_adict_decode_case03(self):
        filepath = 'tests/serializer/data/invalid-content.json'
        expect = ( "Invalid data or url or filepath argument: "
                   "tests/serializer/data/invalid-content.json\n"
                   "Expecting value: line 1 column 1 (char 0)" )
        with pytest.raises(ValueError) as e:
            d = aDict(filepath, format='json')
        assert str(e.value) == expect

    def test_json_udict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.json'
        expect = uDict({'a': 1, 'b': 2, 'c': 3, 'x': 7, 'y': 8, 'z': 9})
        d = uDict(filepath, format='json')
        assert d == expect

    def test_json_udict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.json'
        expect = uDict({'a': 1, 'b': 2, 'c': 3, 'x': 7, 'y': 8, 'z': 9})
        d = uDict(filepath)
        assert d == expect

    def test_json_udict_decode_case03(self):
        filepath = 'tests/serializer/data/invalid-content.json'
        expect = ( "Invalid data or url or filepath argument: "
                   "tests/serializer/data/invalid-content.json\n"
                   "Expecting value: line 1 column 1 (char 0)" )
        with pytest.raises(ValueError) as e:
            d = uDict(filepath, format='json')
        assert str(e.value) == expect
