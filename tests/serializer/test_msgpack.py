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

msgpack_str = (
    b"\x94\xc0\x80\x94\x01\x02\x03\x04\x86\xa1a\x01\xa1b\x82"
    b"\xae__class_name__\xb9<class 'decimal.Decimal'>"
    b"\xae__dumped_obj__\x82\xa8__type__\xa7Decimal\xa5value\xa12\xa1c\x82"
    b"\xae__class_name__\xbb<class 'datetime.datetime'>"
    b"\xae__dumped_obj__\x82\xa8__type__\xa8datetime"
    b"\xa5value\x96\xcd\x07\xe4\x05\x18\x08\x14\x00\xa1d\x82"
    b"\xae__class_name__\xb7<class 'datetime.date'>"
    b"\xae__dumped_obj__\x82\xa8__type__\xa4date"
    b"\xa5value\x93\xcd\x07\xaa\x01\r\xa1e\x82"
    b"\xae__class_name__\xb7<class 'datetime.time'>"
    b"\xae__dumped_obj__\x82\xa8__type__\xa4time"
    b"\xa5value\x93\x0b\x0c\r\xa1f\x94\x01\x02\x03\x82"
    b"\xae__class_name__\xb9<class 'decimal.Decimal'>"
    b"\xae__dumped_obj__\x82\xa8__type__\xa7Decimal"
    b"\xa5value\xa14"
  )


class TestClass:

    def test_msgpack_encode(self):
        result = io.dumps(data, format='msgpack')
        assert result == msgpack_str

    def test_msgpack_decode(self):
        result = io.loads(msgpack_str, format='msgpack')
        assert result == data


