import sys
import time
import pytest

from datajuggler import uDict, aDict
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

bson_str = (
    b"\xe6\x02\x00\x00\x04__bson_follow__"
    b"\x00\xd0\x02\x00\x00\n0\x00\x031\x00\x05\x00\x00\x00\x00"
    b"\x042\x00!\x00\x00\x00\x100\x00\x01\x00\x00\x00\x101\x00"
    b"\x02\x00\x00\x00\x102\x00\x03\x00\x00\x00\x103\x00\x04\x00"
    b"\x00\x00\x00\x033\x00\x99\x02\x00\x00\x10a\x00\x01\x00\x00"
    b"\x00\x03b\x00k\x00\x00\x00\x02__class_name__\x00\x1a\x00\x00\x00"
    b"<class 'decimal.Decimal'>\x00\x03"
    b"__dumped_obj__\x00(\x00\x00\x00\x02"
    b"__type__\x00\x08\x00\x00\x00Decimal\x00\x02"
    b"value\x00\x02\x00\x00\x002\x00\x00\x00\x03c\x00\x97\x00\x00\x00\x02"
    b"__class_name__\x00\x1c\x00\x00\x00"
    b"<class 'datetime.datetime'>\x00\x03"
    b"__dumped_obj__\x00R\x00\x00\x00\x02"
    b"__type__\x00\t\x00\x00\x00datetime\x00\x04"
    b"value\x00/\x00\x00\x00\x100\x00\xe4\x07\x00\x00\x101\x00\x05\x00\x00"
    b"\x00\x102\x00\x18\x00\x00\x00\x103\x00\x08\x00\x00\x00\x104\x00\x14"
    b"\x00\x00\x00\x105\x00\x00\x00\x00\x00\x00\x00\x00\x03d\x00z\x00\x00"
    b"\x00\x02"
    b"__class_name__\x00\x18\x00\x00\x00"
    b"<class 'datetime.date'>\x00\x03"
    b"__dumped_obj__\x009\x00\x00\x00\x02"
    b"__type__\x00\x05\x00\x00\x00date\x00\x04"
    b"value\x00\x1a\x00\x00\x00\x100\x00\xaa\x07\x00\x00\x101\x00\x01\x00"
    b"\x00\x00\x102\x00\r\x00\x00\x00\x00\x00\x00\x03e\x00z\x00\x00\x00\x02"
    b"__class_name__\x00\x18\x00\x00\x00"
    b"<class 'datetime.time'>\x00\x03"
    b"__dumped_obj__\x009\x00\x00\x00\x02"
    b"__type__\x00\x05\x00\x00\x00time\x00\x04"
    b"value\x00\x1a\x00\x00\x00\x100\x00\x0b\x00\x00\x00\x101\x00\x0c\x00"
    b"\x00\x00\x102\x00\r\x00\x00\x00\x00\x00\x00\x04f\x00\x88\x00\x00\x00"
    b"\x100\x00\x01\x00\x00\x00\x101\x00\x02\x00\x00\x00\x102\x00\x03\x00"
    b"\x00\x00\x033\x00k\x00\x00\x00\x02"
    b"__class_name__\x00\x1a\x00\x00\x00"
    b"<class 'decimal.Decimal'>\x00\x03"
    b"__dumped_obj__\x00(\x00\x00\x00\x02"
    b"__type__\x00\x08\x00\x00\x00Decimal"
    b"\x00\x02value\x00\x02\x00\x00\x004\x00\x00\x00\x00\x00\x00\x00"
)

class TestClass:

    def test_bson_encode(self):
        result = io.dumps(data, format='bson')
        assert result == bson_str

    def test_bson_decode(self):
        result = io.loads(bson_str, format='bson')
        assert result == data

