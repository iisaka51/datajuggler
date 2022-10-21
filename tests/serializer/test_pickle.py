import pickle
import decimal
import datetime
import pytest

from datajuggler import aDict, uDict
from datajuggler import serializer as io

data = {'date': datetime.datetime(1985, 4, 3, 0, 0)}

nested_data = [
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

pickled_data = (
 b'\x80\x04\x95\xfd\x01\x00\x00\x00\x00\x00\x00]\x94(N}\x94]\x94(K\x01K\x02'
 b'K\x03K\x04e}\x94(\x8c\x01a\x94K\x01\x8c\x01b\x94\x8c\x08builtins'
 b"\x94\x8c\x07getattr\x94\x93\x94\x8c'datajuggler.serializer.class_serializ"
 b'er\x94\x8c\x16DecimalClassSerializer\x94\x93\x94)\x81\x94}\x94\x8c\x06for'
 b'mat\x94\x8c\x07Decimal\x94sb\x8c\x06decode\x94\x86\x94R\x94}\x94(\x8c\x08__'
 b'type__\x94\x8c\x07Decimal\x94\x8c\x05value\x94\x8c\x012\x94u\x85\x94'
 b'R\x94\x8c\x01c\x94h\x08h\t\x8c\x17DatetimeClassSerializer\x94\x93\x94)\x81'
 b'\x94}\x94h\x0e\x8c\x08datetime\x94sbh\x10\x86\x94R\x94}\x94(h\x14\x8c\x08d'
 b'atetime\x94h\x16]\x94(M\xe4\x07K\x05K\x18K\x08K\x14K\x00eu\x85\x94R\x94'
 b'\x8c\x01d\x94h\x08h\t\x8c\x13DateClassSerializer\x94\x93\x94)\x81\x94}'
 b'\x94h\x0e\x8c\x04date\x94sbh\x10\x86\x94R\x94}\x94(h\x14\x8c\x04dat'
 b'e\x94h\x16]\x94(M\xaa\x07K\x01K\reu\x85\x94R\x94\x8c\x01e\x94h\x08h\t'
 b'\x8c\x13TimeClassSerializer\x94\x93\x94)\x81\x94}\x94h\x0e\x8c\x04time\x94sb'
 b'h\x10\x86\x94R\x94}\x94(h\x14\x8c\x04time\x94h\x16]\x94(K\x0bK\x0cK\reu\x85'
 b'\x94R\x94\x8c\x01f\x94]\x94(K\x01K\x02K\x03h\x12}\x94(h\x14h\x15h\x16\x8c'
 b'\x014\x94u\x85\x94R\x94eue.')

class TestClass:
    def test_pickle_decode(self):
        result = io.loads(pickled_data, format='pickle')
        assert result == nested_data

    def test_pickle_encode(self):
        result = io.dumps(nested_data, format='pickle')
        assert result == pickled_data

    def test_pickle_adict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.pickle'
        expect = aDict(data)
        d = aDict(filepath)
        assert d == expect

    def test_pickle_adict_decode_case03(self):
        filepath = 'tests/serializer/data/invalid-content.pickle'
        expect = "invalid load key, 'W'."
        with pytest.raises(pickle.UnpicklingError) as e:
            d = aDict(filepath, format='pickle')
        assert str(e.value) == expect

    def test_pickle_udict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.pickle'
        expect = aDict(data)
        d = uDict(filepath, format='pickle')
        assert d == expect

    def test_pickle_udict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.pickle'
        expect = aDict(data)
        d = uDict(filepath)
        assert d == expect

    def test_pickle_udict_decode_case03(self):
        filepath = 'tests/serializer/data/invalid-content.pickle'
        expect = "invalid load key, 'W'."
        with pytest.raises(pickle.UnpicklingError) as e:
            d = uDict(filepath, format='pickle')
        assert str(e.value) == expect
