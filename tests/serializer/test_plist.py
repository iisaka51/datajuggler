import sys
import pytest

from datajuggler import serializer as io

class TestClass:
    def test_plist_decode(self):
        s = io.PListSerializer()
        result = s.decode("")
        # TODO
        # assert result == {}

    def test_plist_encode(self):
        s = io.PListSerializer()
        result = s.encode("")
        # TODO
        # assert result == {}

