import sys
import time
import pytest

from datajuggler import uDict, aDict

import toml

data = {'target': {'ip': 'xx.xx.xx.xx',
  'os': {'os': 'win 10', 'Arch': 'x64'},
  'ports': {'ports': ['1', '2'], '1': {'service': 'xxx', 'ver': '5.9'}}}}
toml_str = ( '[target]\nip = "xx.xx.xx.xx"\n\n'
             '[target.os]\nos = "win 10"\nArch = "x64"\n\n'
             '[target.ports]\nports = [ "1", "2",]\n\n'
             '[target.ports.1]\nservice = "xxx"\nver = "5.9"\n' )

class TestClass:
    def test_adict_toml_case01(self):
        obj = aDict(data)
        result = obj.to_toml()
        assert result == toml_str

    def test_adict_toml_case02(self):
        obj = aDict()
        result = obj.to_toml(data)
        assert result == toml_str

    def test_adict_toml_case03(self):
        obj = aDict({1: 2})
        result = obj.to_toml(data)
        assert result == toml_str

    def test_adict_toml_case04(self):
        obj = aDict()
        result = obj.from_toml(toml_str)
        assert result == data

    def test_adict_toml_case05(self):
        obj = aDict()
        obj.from_toml(toml_str, inplace=True)
        assert obj == data



    def test_udict_toml_case01(self):
        obj = uDict(data)
        result = obj.to_toml()
        assert result == toml_str

    def test_udict_toml_case02(self):
        obj = uDict()
        result = obj.to_toml(data)
        assert result == toml_str

    def test_udict_toml_case03(self):
        obj = uDict({1: 2})
        result = obj.to_toml(data)
        assert result == toml_str

    def test_udict_toml_case04(self):
        obj = uDict()
        result = obj.from_toml(toml_str)
        assert result == data

    def test_udict_toml_case05(self):
        obj = uDict()
        obj.from_toml(toml_str, inplace=True)
        assert obj == data



    def test_idict_toml_case01(self):
        obj = iDict(data)
        result = obj.to_toml()
        assert result == toml_str

    def test_idict_toml_case02(self):
        obj = iDict()
        result = obj.to_toml(data)
        assert result == toml_str

    def test_idict_toml_case03(self):
        obj = iDict({1: 2})
        result = obj.to_toml(data)
        assert result == toml_str

    def test_idict_toml_case04(self):
        obj = iDict()
        result = obj.from_toml(toml_str)
        assert result == data

    def test_idict_toml_case05(self):
        obj = iDict()
        obj.from_toml(toml_str, inplace=True)
        assert obj == iDict()

