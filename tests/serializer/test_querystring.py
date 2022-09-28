import sys
import pytest

from datajuggler import serializer as io

class TestClass:
    def test_querystring_decode(self):
        s = io.QueryStringSerializer()
        result = s.decode("")
        # TODO
        # assert result == {}

    def test_querystring_encode(self):
        s = io.QueryStringSerializer()
        result = s.encode("")
        # TODO
        # assert result == {}

