import sys
import pytest

from datajuggler import serializer as io

class TestClass:
    def test_xml_decode(self):
        s = io.XMLSerializer()
        result = s.decode("")
        # TODO
        # assert result == {}

    def test_xml_encode(self):
        s = io.XMLSerializer()
        result = s.encode("")
        # TODO
        # assert result == {}

