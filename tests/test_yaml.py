import sys
import time
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import (
    uDict, iDict, aDict,
    change_dict_keys, ordereddict_to_dict,
)

from collections import OrderedDict
import pandas as pd
import yaml

class TestClass:
    def test_udict_yaml_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{April: 4, February: 2, January: 1, March: 3}\n"
        obj = uDict(data)
        result = yaml.safe_dump(obj, default_flow_style=True)
        assert result == expect

    def test_udict_yaml_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{January: 1, February: 2, March: 3, April: 4}\n"
        obj = uDict(data)
        result = yaml.safe_dump(obj, default_flow_style=True,sort_keys=False)
        assert result == expect

    def test_udict_yaml_case03(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{April: 4, February: 2, January: 1, March: 3}\n"
        obj = uDict(data)
        result = obj.to_yaml(default_flow_style=True)
        assert result == expect

    def test_udict_yaml_case04(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{January: 1, February: 2, March: 3, April: 4}\n"
        obj = uDict(data)
        result = obj.to_yaml(default_flow_style=True,sort_keys=False)
        assert result == expect

    def test_udict_yaml_case05(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "!uDict {April: 4, February: 2, January: 1, March: 3}\n"
        obj = uDict(data)
        result = yaml.dump(obj, default_flow_style=True)
        assert result == expect

    def test_udict_yaml_case06(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "!uDict {January: 1, February: 2, March: 3, April: 4}\n"
        obj = uDict(data)
        result = yaml.dump(obj, default_flow_style=True,sort_keys=False)
        assert result == expect

    def test_udict_yaml_case07(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "!uDict {April: 4, February: 2, January: 1, March: 3}\n"
        obj = uDict(data)
        result = obj.to_yaml(Dumper=yaml.Dumper,  default_flow_style=True)
        assert result == expect

    def test_udict_yaml_case08(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "!uDict {January: 1, February: 2, March: 3, April: 4}\n"
        obj = uDict(data)
        result = obj.to_yaml(Dumper=yaml.Dumper,
                             default_flow_style=True, sort_keys=False)
        assert result == expect

    def test_udict_yaml_case09(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        yaml_str = "!uDict {April: 4, February: 2, January: 1, March: 3}\n"
        obj = uDict()
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_udict_yaml_case10(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "!uDict {January: 1, February: 2, March: 3, April: 4}\n"
        obj = uDict(data)
        result = obj.to_yaml(Dumper=yaml.Dumper,
                             default_flow_style=True, sort_keys=False)
        assert result == expect
