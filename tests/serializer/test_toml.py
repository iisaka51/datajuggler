import sys
import time
import pytest

from datajuggler import uDict, aDict
from datajuggler import serializer as io
import datetime
import toml

simple_data = {
    'target': {
        'ip': 'xx.xx.xx.xx',
        'os': {'os': 'win 10', 'Arch': 'x64'},
        'ports': {'ports': ['1', '2'],
              '1': {'service': 'xxx', 'ver': '5.9'}
         }
    }
}

simple_toml_str = ( '[target]\nip = "xx.xx.xx.xx"\n\n'
             '[target.os]\nos = "win 10"\nArch = "x64"\n\n'
             '[target.ports]\nports = [ "1", "2",]\n\n'
             '[target.ports.1]\nservice = "xxx"\nver = "5.9"\n' )

invalid_expect = (
    "Found invalid character in key name: 't'. "
    "Try quoting the key name. (line 1 column 4 char 3)" )

data = {
    'title': 'TOML Example',
    'owner': {
        'name': 'Tom Preston-Werner',
        'dob': datetime.datetime(1979, 5, 27, 7, 32)
        },
        'database': {
            'server': '192.168.1.1',
            'ports': [8001, 8001, 8002],
            'connection_max': 5000, 'enabled': True
        },
        'servers': {
            'alpha': {
                'ip': '10.0.0.1',
                'dc': 'eqdc10'
            },
            'beta': {'ip': '10.0.0.2', 'dc': 'eqdc10'}
        },
        'clients': {
            'data': [['gamma', 'delta'], [1, 2]],
            'hosts': ['alpha', 'omega']
        }
    }

toml_str = io.read_file('tests/serializer/valid-content.toml')

class TestClass:

    def test_toml_decode(self):
        result = io.loads(simple_toml_str, format='toml')
        assert result == simple_data

    def test_toml_encode(self):
        result = io.dumps(simple_data, format='toml')
        assert result == simple_toml_str


    def test_toml_adict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.toml'
        expect = aDict(data)
        d = aDict(filepath, format='toml')
        assert d == expect

    def test_toml_adict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.toml'
        expect = aDict(data)
        d = aDict(filepath)
        assert d == expect

    def test_toml_adict_decode_case03(self):
        filepath = 'tests/serializer/data/invalid-content.toml'
        with pytest.raises(ValueError) as e:
            d = aDict(filepath, format='toml')
        assert str(e.value) == invalid_expect

    def test_toml_udict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.toml'
        expect = uDict(data)
        d = uDict(filepath, format='toml')
        assert d == expect

    def test_toml_udict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.toml'
        expect = uDict(data)
        d = uDict(filepath)
        assert d == expect

    def test_toml_udict_decode_case03(self):
        filepath = 'tests/serializer/data/invalid-content.toml'
        with pytest.raises(ValueError) as e:
            d = uDict(filepath, format='toml')
        assert str(e.value) == invalid_expect
