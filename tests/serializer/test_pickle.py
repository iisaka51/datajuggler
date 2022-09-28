import sys
import pytest

from datajuggler import serializer as io

class TestClass:
    def test_pickle_decode(self):
        s = io.PickleSerializer()
        result = s.decode("")
        # TODO
        # assert result == {}

    def test_pickle_encode(self):
        s = io.PickleSerializer()
        result = s.encode("")
        # TODO
        # assert result == {}

