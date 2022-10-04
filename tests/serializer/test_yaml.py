import sys
import pytest

from datajuggler import serializer as io
from datajuggler import aDict, uDict

import yaml

data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
yaml_data_sorted = "April: 4\nFebruary: 2\nJanuary: 1\nMarch: 3\n"
yaml_data = "January: 1\nFebruary: 2\nMarch: 3\nApril: 4\n"

class TestClass:
    def test_yaml_encode_case01(self):
        s = io.YAMLSerializer()
        result = s.encode(data)
        assert result == yaml_data_sorted

    def test_yaml_encode_case02(self):
        s = io.YAMLSerializer()
        result = s.encode(data, sort_keys=False)
        assert result == yaml_data

    def test_yaml_decode_case01(self):
        s = io.YAMLSerializer()
        result = s.decode(yaml_data)
        assert result == data

    def test_yaml_decode_adict_case01(self):
        yaml_str = ( "!datajuggler.aDict "
                     "{'January': 1, 'February': 2, 'March': 3, 'April': 4}" )
        d = aDict(yaml_str, format='yaml')
        assert d == data

    def test_yaml_decode_adict_case02(self):
        yaml_str = ( "!python/object:datajuggler.aDict "
                     "{'January': 1, 'February': 2, 'March': 3, 'April': 4}" )
        d = aDict(yaml_str, format='yaml')
        assert d == data

    def test_yaml_decode_adict_case03(self):
        yaml_str = ( "!python/object/new:datajuggler.aDict "
                     "{'January': 1, 'February': 2, 'March': 3, 'April': 4}" )
        d = aDict(yaml_str, format='yaml')
        assert d == data

    def test_yaml_decode_udict_case01(self):
        yaml_str = ( "!datajuggler.uDict "
                     "{'January': 1, 'February': 2, 'March': 3, 'April': 4}" )
        d = uDict(yaml_str, format='yaml')
        assert d == data

    def test_yaml_decode_adict_case02(self):
        yaml_str = ( "!python/object:datajuggler.uDict "
                     "{'January': 1, 'February': 2, 'March': 3, 'April': 4}" )
        d = uDict(yaml_str, format='yaml')
        assert d == data

    def test_yaml_decode_adict_case03(self):
        yaml_str = ( "!python/object/new:datajuggler.uDict "
                     "{'January': 1, 'February': 2, 'March': 3, 'April': 4}" )
        d = uDict(yaml_str, format='yaml')
        assert d == data
