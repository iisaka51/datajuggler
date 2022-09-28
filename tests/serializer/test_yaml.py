import sys
import pytest

from datajuggler import serializer as io

import yaml

data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
yaml_data = "{April: 4,\n February: 2,\n January: 1,\n March: 3}\n"

class TestClass:
    def test_yaml_encode(self):
        s = io.YAMLSerializer()
        result = s.encode(data)
        assert result == yaml_data

    def test_yaml_decode(self):
        s = io.YAMLSerializer()
        result = s.decode(yaml_data)
        assert result == data
