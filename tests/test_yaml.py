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
    def test_adict_yaml_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{April: 4, February: 2, January: 1, March: 3}\n"
        obj = aDict(data)
        result = yaml.safe_dump(obj, default_flow_style=True)
        assert result == expect

    def test_adict_yaml_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{January: 1, February: 2, March: 3, April: 4}\n"
        obj = aDict(data)
        result = yaml.safe_dump(obj, default_flow_style=True,sort_keys=False)
        assert result == expect

    def test_adict_yaml_case03(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{April: 4, February: 2, January: 1, March: 3}\n"
        obj = aDict(data)
        result = obj.to_yaml(default_flow_style=True)
        assert result == expect

    def test_adict_yaml_case04(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{January: 1, February: 2, March: 3, April: 4}\n"
        obj = aDict(data)
        result = obj.to_yaml(default_flow_style=True,sort_keys=False)
        assert result == expect

    def test_adict_yaml_case05(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = ( "!datajuggler.aDict "
                   "{April: 4, February: 2, January: 1, March: 3}\n" )
        obj = aDict(data)
        result = yaml.dump(obj, default_flow_style=True)
        assert result == expect

    def test_adict_yaml_case06(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = ( "!datajuggler.aDict "
                   "{January: 1, February: 2, March: 3, April: 4}\n" )
        obj = aDict(data)
        result = yaml.dump(obj, default_flow_style=True,sort_keys=False)
        assert result == expect

    def test_adict_yaml_case07(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = ( "!datajuggler.aDict "
                   "{April: 4, February: 2, January: 1, March: 3}\n" )
        obj = aDict(data)
        result = obj.to_yaml(Dumper=yaml.Dumper,  default_flow_style=True)
        assert result == expect

    def test_adict_yaml_case08(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = ( "!datajuggler.aDict "
                   "{January: 1, February: 2, March: 3, April: 4}\n" )
        obj = aDict(data)
        result = obj.to_yaml(Dumper=yaml.Dumper,
                             default_flow_style=True, sort_keys=False)
        assert result == expect

    def test_adict_yaml_case09(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = "{one: {two: {three: {four: 4}}}}\n"
        obj = aDict(data)
        result = obj.to_yaml(default_flow_style=True,sort_keys=False)
        assert result  == expect

    def test_adict_yaml_case10(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = ( "!datajuggler.aDict "
                   "{one: {two: {three: {four: 4}}}}\n" )
        obj = aDict(data)
        result = obj.to_yaml(Dumper=yaml.Dumper,
                             default_flow_style=True, sort_keys=False)
        assert result  == expect

    def test_adict_yaml_case11(self):
        yaml_str = ( "!datajuggler.aDict "
                     "{April: 4, February: 2, January: 1, March: 3}\n" )
        expect = "aDict({'April': 4, 'February': 2, 'January': 1, 'March': 3})"
        obj = aDict()
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_adict_yaml_case12(self):
        yaml_str = ( "!python/object:datajuggler.aDict "
                     "{April: 4, February: 2, January: 1, March: 3}\n" )
        expect = "aDict({'April': 4, 'February': 2, 'January': 1, 'March': 3})"
        obj = aDict()
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_adict_yaml_case13(self):
        yaml_str = ( "!datajuggler.aDict "
                     "{January: 1, February: 2, March: 3, April: 4}\n" )
        expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = aDict()
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_adict_yaml_case14(self):
        yaml_str = ( "!python/object:datajuggler.aDict "
                     "{January: 1, February: 2, March: 3, April: 4}\n" )
        expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = aDict()
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_adict_yaml_case15(self):
        yaml_str = ( "!datajuggler.aDict "
                     "{April: 4, February: 2, January: 1, March: 3}\n" )
        expect = "aDict({})"
        obj = aDict()
        _ = obj.from_yaml(yaml_str)
        assert obj.__repr__() == expect

    def test_adict_yaml_case16(self):
        yaml_str = ( "!python/object:datajuggler.aDict "
                     "{January: 1, February: 2, March: 3, April: 4}\n" )
        expect = "aDict({})"
        obj = aDict()
        _ = obj.from_yaml(yaml_str)
        assert obj.__repr__() == expect

    def test_adict_yaml_case17(self):
        yaml_str = ( "!datajuggler.aDict "
                     "{April: 4, February: 2, January: 1, March: 3}\n" )
        expect = "aDict({'April': 4, 'February': 2, 'January': 1, 'March': 3})"
        obj = aDict()
        obj.from_yaml(yaml_str, inplace=True)
        assert obj.__repr__() == expect

    def test_adict_yaml_case18(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        yaml_str = ( "!python/object:datajuggler.aDict "
                     "{January: 1, February: 2, March: 3, April: 4}\n" )
        expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = aDict()
        obj.from_yaml(yaml_str, inplace=True)
        assert obj.__repr__() == expect




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
        expect = ( "!datajuggler.uDict "
                   "{April: 4, February: 2, January: 1, March: 3}\n" )
        obj = uDict(data)
        result = yaml.dump(obj, default_flow_style=True)
        assert result == expect

    def test_udict_yaml_case06(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = ( "!datajuggler.uDict "
                   "{January: 1, February: 2, March: 3, April: 4}\n" )
        obj = uDict(data)
        result = yaml.dump(obj, default_flow_style=True,sort_keys=False)
        assert result == expect

    def test_udict_yaml_case07(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = ( "!datajuggler.uDict "
                   "{April: 4, February: 2, January: 1, March: 3}\n" )
        obj = uDict(data)
        result = obj.to_yaml(Dumper=yaml.Dumper,  default_flow_style=True)
        assert result == expect

    def test_udict_yaml_case08(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = ( "!datajuggler.uDict "
                   "{January: 1, February: 2, March: 3, April: 4}\n" )
        obj = uDict(data)
        result = obj.to_yaml(Dumper=yaml.Dumper,
                             default_flow_style=True, sort_keys=False)
        assert result == expect

    def test_udict_yaml_case09(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = "{one: {two: {three: {four: 4}}}}\n"
        obj = uDict(data)
        result = obj.to_yaml(default_flow_style=True,sort_keys=False)
        assert result  == expect

    def test_udict_yaml_case10(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = ( "!datajuggler.uDict "
                   "{one: {two: {three: {four: 4}}}}\n" )
        obj = uDict(data)
        result = obj.to_yaml(Dumper=yaml.Dumper,
                             default_flow_style=True, sort_keys=False)
        assert result  == expect

    def test_udict_yaml_case11(self):
        yaml_str = ( "!datajuggler.uDict "
                     "{April: 4, February: 2, January: 1, March: 3}\n" )
        expect = "uDict({'April': 4, 'February': 2, 'January': 1, 'March': 3})"
        obj = uDict()
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_udict_yaml_case12(self):
        yaml_str = ( "!python/object:datajuggler.uDict "
                     "{April: 4, February: 2, January: 1, March: 3}\n" )
        expect = "uDict({'April': 4, 'February': 2, 'January': 1, 'March': 3})"
        obj = uDict()
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_udict_yaml_case13(self):
        yaml_str = ( "!datajuggler.uDict "
                     "{January: 1, February: 2, March: 3, April: 4}\n" )
        expect = "uDict({'April': 4, 'February': 2, 'January': 1, 'March': 3})"
        obj = uDict()
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_udict_yaml_case14(self):
        yaml_str = ( "!python/object:datajuggler.uDict "
                     "{January: 1, February: 2, March: 3, April: 4}\n" )
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = uDict()
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_udict_yaml_case15(self):
        yaml_str = ( "!datajuggler.uDict "
                     "{April: 4, February: 2, January: 1, March: 3}\n" )
        expect = "uDict({})"
        obj = uDict()
        _ = obj.from_yaml(yaml_str)
        assert obj.__repr__() == expect

    def test_udict_yaml_case16(self):
        yaml_str = ( "!python/object:datajuggler.uDict "
                     "{January: 1, February: 2, March: 3, April: 4}\n" )
        expect = "uDict({})"
        obj = uDict()
        _ = obj.from_yaml(yaml_str)
        assert obj.__repr__() == expect

    def test_udict_yaml_case17(self):
        yaml_str = ( "!datajuggler.uDict "
                     "{April: 4, February: 2, January: 1, March: 3}\n" )
        expect = "uDict({'April': 4, 'February': 2, 'January': 1, 'March': 3})"
        obj = uDict()
        obj.from_yaml(yaml_str, inplace=True)
        assert obj.__repr__() == expect

    def test_udict_yaml_case18(self):
        yaml_str = ( "!python/object:datajuggler.uDict "
                     "{January: 1, February: 2, March: 3, April: 4}\n" )
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = uDict()
        obj.from_yaml(yaml_str, inplace=True)
        assert obj.__repr__() == expect



    def test_idict_yaml_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{April: 4, February: 2, January: 1, March: 3}\n"
        obj = iDict(data)
        result = yaml.safe_dump(obj, default_flow_style=True)
        assert result == expect

    def test_idict_yaml_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{January: 1, February: 2, March: 3, April: 4}\n"
        obj = iDict(data)
        result = yaml.safe_dump(obj, default_flow_style=True,sort_keys=False)
        assert result == expect

    def test_idict_yaml_case03(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{April: 4, February: 2, January: 1, March: 3}\n"
        obj = iDict(data)
        result = obj.to_yaml(default_flow_style=True)
        assert result == expect

    def test_idict_yaml_case04(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{January: 1, February: 2, March: 3, April: 4}\n"
        obj = iDict(data)
        result = obj.to_yaml(default_flow_style=True,sort_keys=False)
        assert result == expect

    def test_idict_yaml_case05(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = ( "!datajuggler.iDict "
                   "{April: 4, February: 2, January: 1, March: 3}\n" )
        obj = iDict(data)
        result = yaml.dump(obj, default_flow_style=True)
        assert result == expect

    def test_idict_yaml_case06(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = ( "!datajuggler.iDict "
                   "{January: 1, February: 2, March: 3, April: 4}\n" )
        obj = iDict(data)
        result = yaml.dump(obj, default_flow_style=True,sort_keys=False)
        assert result == expect

    def test_idict_yaml_case07(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = ( "!datajuggler.iDict "
                   "{April: 4, February: 2, January: 1, March: 3}\n" )
        obj = iDict(data)
        result = obj.to_yaml(Dumper=yaml.Dumper,  default_flow_style=True)
        assert result == expect

    def test_idict_yaml_case08(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = ( "!datajuggler.iDict "
                   "{January: 1, February: 2, March: 3, April: 4}\n" )
        obj = iDict(data)
        result = obj.to_yaml(Dumper=yaml.Dumper,
                             default_flow_style=True, sort_keys=False)
        assert result == expect

    def test_idict_yaml_case09(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = "{one: {two: {three: {four: 4}}}}\n"
        obj = iDict(data)
        result = obj.to_yaml(default_flow_style=True,sort_keys=False)
        assert result  == expect

    def test_idict_yaml_case10(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = ( "!datajuggler.iDict "
                   "{one: {two: {three: {four: 4}}}}\n" )
        obj = iDict(data)
        result = obj.to_yaml(Dumper=yaml.Dumper,
                             default_flow_style=True, sort_keys=False)
        assert result  == expect

    def test_idict_yaml_case11(self):
        yaml_str = ( "!datajuggler.iDict "
                     "{April: 4, February: 2, January: 1, March: 3}\n" )
        expect = "iDict({'April': 4, 'February': 2, 'January': 1, 'March': 3})"
        obj = iDict()
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_idict_yaml_case12(self):
        yaml_str = ( "!python/object:datajuggler.iDict "
                     "{April: 4, February: 2, January: 1, March: 3}\n" )
        expect = "iDict({'April': 4, 'February': 2, 'January': 1, 'March': 3})"
        obj = iDict()
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_idict_yaml_case13(self):
        yaml_str = ( "!datajuggler.iDict "
                     "{January: 1, February: 2, March: 3, April: 4}\n" )
        expect = "iDict({'April': 4, 'February': 2, 'January': 1, 'March': 3})"
        obj = iDict()
        expect = "iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_idict_yaml_case14(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        yaml_str = ( "!python/object:datajuggler.iDict "
                     "{January: 1, February: 2, March: 3, April: 4}\n" )
        expect = "iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        obj = iDict()
        result = obj.from_yaml(yaml_str)
        assert result.__repr__() == expect

    def test_idict_yaml_case15(self):
        yaml_str = ( "!datajuggler.iDict "
                     "{April: 4, February: 2, January: 1, March: 3}\n" )
        expect = "iDict({})"
        obj = iDict()
        _ = obj.from_yaml(yaml_str)
        assert obj.__repr__() == expect

    def test_idict_yaml_case16(self):
        yaml_str = ( "!python/object:datajuggler.iDict "
                     "{January: 1, February: 2, March: 3, April: 4}\n" )
        expect = "iDict({})"
        obj = iDict()
        _ = obj.from_yaml(yaml_str)
        assert obj.__repr__() == expect

    def test_idict_yaml_case17(self):
        yaml_str = ( "!datajuggler.iDict "
                     "{April: 4, February: 2, January: 1, March: 3}\n" )
        expect = "iDict({})"
        obj = iDict()
        obj.from_yaml(yaml_str, inplace=True)
        assert obj.__repr__() == expect

    def test_idict_yaml_case18(self):
        yaml_str = ( "!python/object:datajuggler.iDict "
                     "{January: 1, February: 2, March: 3, April: 4}\n" )
        # expect = "iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        expect = "iDict({})"
        obj = iDict()
        obj.from_yaml(yaml_str, inplace=True)
        assert obj.__repr__() == expect

