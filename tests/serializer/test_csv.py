import sys
import base64
import pytest

from datajuggler import serializer as io

class TestClass:
    def test_csv_decode(self):
        s = io.CSVSerializer()
        result = s.decode("")
        # TODO
        # assert result == {}

    def test_csv_encode(self):
        s = io.CSVSerializer()
        result = s.encode("")
        # TODO
        # assert result == {}

