import sys
import time
import pytest

from datajuggler import aDict, uDict
from datajuggler import serializer as io
import datetime
import decimal

data = [
    None,
    {},
    [1, 2, 3, 4],
    {
        "a": 1,
        "b": decimal.Decimal(2),
        "c": datetime.datetime(2020, 5, 24, 8, 20, 0),
        "d": datetime.date(1962, 1, 13),
        "e": datetime.time(11, 12, 13),
        "f": [1, 2, 3, decimal.Decimal(4)],
    },
]

json_data_encode = (
    b'[null, {}, [1, 2, 3, 4], '
    b'{"a": 1, '
    b'"b": {"__class_name__": "<class \'decimal.Decimal\'>", '
    b'"__dumped_obj__": {"__type__": "Decimal", "value": "2"}}, '
    b'"c": {"__class_name__": "<class \'datetime.datetime\'>", '
    b'"__dumped_obj__": {"__type__": "datetime", '
    b'"value": [2020, 5, 24, 8, 20, 0]}}, '
    b'"d": {"__class_name__": "<class \'datetime.date\'>", '
    b'"__dumped_obj__": {"__type__": "date", "value": [1962, 1, 13]}}, '
    b'"e": {"__class_name__": "<class \'datetime.time\'>", '
    b'"__dumped_obj__": {"__type__": "time", "value": [11, 12, 13]}}, '
    b'"f": [1, 2, 3, {"__class_name__": "<class \'decimal.Decimal\'>", '
    b'"__dumped_obj__": {"__type__": "Decimal", "value": "4"}}]}]'
 )

json_data = (
    '[null, {}, [1, 2, 3, 4], '
    '{"a": 1, '
    '"b": {"__class_name__": "<class \'decimal.Decimal\'>", '
    '"__dumped_obj__": {"__type__": "Decimal", "value": "2"}}, '
    '"c": {"__class_name__": "<class \'datetime.datetime\'>", '
    '"__dumped_obj__": {"__type__": "datetime", '
    '"value": [2020, 5, 24, 8, 20, 0]}}, '
    '"d": {"__class_name__": "<class \'datetime.date\'>", '
    '"__dumped_obj__": {"__type__": "date", "value": [1962, 1, 13]}}, '
    '"e": {"__class_name__": "<class \'datetime.time\'>", '
    '"__dumped_obj__": {"__type__": "time", "value": [11, 12, 13]}}, '
    '"f": [1, 2, 3, {"__class_name__": "<class \'decimal.Decimal\'>", '
    '"__dumped_obj__": {"__type__": "Decimal", "value": "4"}}]}]'
 )

simple_data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
simple_json_indent2_sorted_encode = (
    b'{\n'
    b'  "April": 4,\n'
    b'  "February": 2,\n'
    b'  "January": 1,\n'
    b'  "March": 3\n
    b'}'
)

simple_json_indent2_sorted = (
    '{\n'
    '  "April": 4,\n'
    '  "February": 2,\n'
    '  "January": 1,\n'
    '  "March": 3\n
    '}'
)

class TestClass:
    def test_json_encode_case01(self):
        result = io.dumps(data, format='json')
        assert result == json_data_encode

    def test_json_encode_case02(self):
        result = io.dumps(data, format='json', encoding='utf-8')
        assert result == json_data

    def test_json_encode_case03(self):
        options = dict(indent=2, sort_keys=True, separators=(",", ": "))
        expect = "dumps() got an unexpected keyword argument 'indent'"
        with pytest.raises(TypeError) as e:
            result = io.dumps(data, format='json', options=options)
        assert str(e.value) == expect

    def test_json_encode_case04(self):
        options = dict(indent=2, sort_keys=True, separators=(",", ": "))
        result = io.dumps(data, format='json:custom', options=options)
        assert result == simple_json_indent2_sorted_encode

    def test_json_encode_case05(self):
        options = dict(indent=2, sort_keys=True, separators=(",", ": "))
        result = io.dumps(data, format='json:custom',
                                encoding='utf-8', options=options)
        assert result == simple_json_indent2_sorted



    def test_json_decode_case01(self):
        result = io.loads(json_data_encode, format='json')
        assert result == data

    def test_json_decode_case02(self):
        expect = "'str' object has no attribute 'decode'"
        with pytest.raises(AttributeError) as e:
            result = io.loads(json_data, format='json')
        assert str(e.value) == expect

    def test_json_decode_case03(self):
        result = io.loads(json_data, format='json', encoding='utf-8')
        assert result == data

    def test_json_decode_case04(self):
        result = io.loads(json_data, format='json:custom')
        assert result == data

    def test_json_decode_case05(self):
        result = io.loads(json_data, format='json:custom', encoding='utf-8')
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
        expect = 'Expecting value: line 1 column 1 (char 0)'
        with pytest.raises(ValueError) as e:
            d = aDict(filepath, format='json')
        assert str(e.value) == expect

    def test_json_adict_decode_case04(self):
        filepath = 'tests/serializer/data/invalid-content.missing'
        expect = 'Expecting value: line 1 column 1 (char 0)'
        expect = ('Invalid data or url or filepath argument: '
                  'tests/serializer/data/invalid-content.missing\n'
                  "Invalid data type: <class 'str'>, expected dict or list." )

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
        expect = 'Expecting value: line 1 column 1 (char 0)'
        with pytest.raises(ValueError) as e:
            d = uDict(filepath, format='json')
        assert str(e.value) == expect

    def test_json_udict_decode_case04(self):
        filepath = 'tests/serializer/data/invalid-content.missing'
        expect = 'Expecting value: line 1 column 1 (char 0)'
        expect = ('Invalid data or url or filepath argument: '
                  'tests/serializer/data/invalid-content.missing\n'
                  "Invalid data type: <class 'str'>, expected dict or list." )

        with pytest.raises(ValueError) as e:
            d = uDict(filepath, format='json')
        assert str(e.value) == expect

