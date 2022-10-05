import datetime

import pytest
import yaml

from datajuggler import serializer as io
from datajuggler import aDict, uDict


data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
yaml_data_sorted = "April: 4\nFebruary: 2\nJanuary: 1\nMarch: 3\n"
yaml_data = "January: 1\nFebruary: 2\nMarch: 3\nApril: 4\n"

valid_content  = uDict({'invoice': 34843, 'date': datetime.date(2001, 1, 23), 'bill-to': uDict({'given': 'Chris', 'family': 'Dumars', 'address': uDict({'lines': '458 Walkman Dr.\nSuite #292\n', 'city': 'Royal Oak', 'state': 'MI', 'postal': 48046})}), 'ship-to': uDict({'given': 'Chris', 'family': 'Dumars', 'address': uDict({'lines': '458 Walkman Dr.\nSuite #292\n', 'city': 'Royal Oak', 'state': 'MI', 'postal': 48046})}), 'product': [{'sku': 'BL394D', 'quantity': 4, 'description': 'Basketball', 'price': 450.0}, {'sku': 'BL4438H', 'quantity': 1, 'description': 'Super Hoop', 'price': 2392.0}], 'tax': 251.42, 'total': 4443.52, 'comments': 'Late afternoon is best. Backup contact is Nancy Billsmer @ 338-4338.'})

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

    def test_yaml_decode_adict_case04(self):
        filepath='tests/serializer/data/valid-content.yml'
        d = aDict(filepath, format='yaml')
        assert d == data

    def test_yaml_decode_adict_case05(self):
        filepath='tests/serializer/data/valid-content.yml'
        d = aDict(filepath, format='yml')
        assert d == data

    def test_yaml_decode_adict_case06(self):
        filepath='tests/serializer/data/valid-content.yml'
        d = aDict(filepath)
        assert d == data

    def test_yaml_decode_adict_case07(self):
        filepath='tests/serializer/data/invalid-content.yml'
        d = aDict(filepath, format='yaml')
        assert d == data



    def test_yaml_decode_udict_case01(self):
        yaml_str = ( "!datajuggler.uDict "
                     "{'January': 1, 'February': 2, 'March': 3, 'April': 4}" )
        d = uDict(yaml_str, format='yaml')
        assert d == data

    def test_yaml_decode_udict_case02(self):
        yaml_str = ( "!python/object:datajuggler.uDict "
                     "{'January': 1, 'February': 2, 'March': 3, 'April': 4}" )
        d = uDict(yaml_str, format='yaml')
        assert d == data

    def test_yaml_decode_udict_case03(self):
        yaml_str = ( "!python/object/new:datajuggler.uDict "
                     "{'January': 1, 'February': 2, 'March': 3, 'April': 4}" )
        d = uDict(yaml_str, format='yaml')
        assert d == data

    def test_yaml_decode_udict_case04(self):
        filepath='tests/serializer/data/valid-content.yml'
        d = uDict(filepath, format='yaml')
        assert d == valid_content

    def test_yaml_decode_udict_case05(self):
        filepath='tests/serializer/data/valid-content.yml'
        d = uDict(filepath, format='yml')
        assert d == valid_content

    def test_yaml_decode_udict_case06(self):
        filepath='tests/serializer/data/valid-content.yml'
        d = uDict(filepath)
        assert d == valid_content

    def test_yaml_decode_udict_case07(self):
        expect = ("Invalid data or url or filepath argument: "
                  "tests/serializer/data/invalid-content.yml\n"
                  "Invalid data type: <class 'str'>, expected dict or list.")

        filepath='tests/serializer/data/invalid-content.yml'
        with pytest.raises(ValueError) as e:
            d = uDict(filepath, format='yaml')
        assert str(e.value) == expect
