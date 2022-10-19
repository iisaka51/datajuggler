import datetime
import decimal
import pytest
import yaml

from datajuggler import serializer as io
from datajuggler import aDict, uDict

nest_data = [None,
 {},
 [1, 2, 3, 4],
 {'a': 1,
  'b': decimal.Decimal('2'),
  'c': datetime.datetime(2020, 5, 24, 8, 20),
  'd': datetime.date(1962, 1, 13),
  'e': datetime.time(11, 12, 13),
  'f': [1, 2, 3, decimal.Decimal('4')]}]

nest_yaml_encode = (
    b'- null\n'
    b'- {}\n'
    b'- - 1\n'
    b'  - 2\n'
    b'  - 3\n'
    b'  - 4\n'
    b'- a: 1\n'
    b'  b: !!python/object/apply:decimal.Decimal\n'
    b"  - '2'\n"
    b'  c: 2020-05-24 08:20:00\n'
    b'  d: 1962-01-13\n'
    b'  e: !!python/object/apply:datetime.time\n'
    b'  - !!binary |\n    CwwNAAAA\n'
    b'  f:\n'
    b'  - 1\n'
    b'  - 2\n'
    b'  - 3\n'
    b'  - !!python/object/apply:decimal.Decimal\n'
    b"    - '4'\n"
)


nest_yaml = (
    '- null\n'
    '- {}\n'
    '- - 1\n'
    '  - 2\n'
    '  - 3\n'
    '  - 4\n'
    '- a: 1\n'
    '  b: !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    "    __class_name__: <class 'decimal.Decimal'>\n"
    '    __dumped_obj__:\n'
    '      __type__: Decimal\n'
    "      value: '2'\n"
    '  c: !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    "    __class_name__: <class 'datetime.datetime'>\n"
    '    __dumped_obj__:\n'
    '      __type__: datetime\n'
    '      value:\n'
    '      - 2020\n'
    '      - 5\n'
    '      - 24\n'
    '      - 8\n'
    '      - 20\n'
    '      - 0\n'
    '  d: !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    "    __class_name__: <class 'datetime.date'>\n"
    '    __dumped_obj__:\n'
    '      __type__: date\n'
    '      value:\n'
    '      - 1962\n'
    '      - 1\n'
    '      - 13\n'
    '  e: !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    "    __class_name__: <class 'datetime.time'>\n"
    '    __dumped_obj__:\n'
    '      __type__: time\n'
    '      value:\n'
    '      - 11\n'
    '      - 12\n'
    '      - 13\n'
    '  f:\n'
    '  - 1\n'
    '  - 2\n'
    '  - 3\n'
    '  - !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    "    __class_name__: <class 'decimal.Decimal'>\n"
    '    __dumped_obj__:\n'
    '      __type__: Decimal\n'
    "      value: '4'\n"
)

nest_yaml_custom_encode = (
    b'- null\n'
    b'- {}\n'
    b'- - 1\n'
    b'  - 2\n'
    b'  - 3\n'
    b'  - 4\n'
    b'- a: 1\n'
    b'  b: !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    b"    __class_name__: <class 'decimal.Decimal'>\n"
    b'    __dumped_obj__:\n'
    b'      __type__: Decimal\n'
    b"      value: '2'\n"
    b'  c: !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    b"    __class_name__: <class 'datetime.datetime'>\n"
    b'    __dumped_obj__:\n'
    b'      __type__: datetime\n'
    b'      value:\n'
    b'      - 2020\n'
    b'      - 5\n'
    b'      - 24\n'
    b'      - 8\n'
    b'      - 20\n'
    b'      - 0\n'
    b'  d: !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    b"    __class_name__: <class 'datetime.date'>\n"
    b'    __dumped_obj__:\n'
    b'      __type__: date\n'
    b'      value:\n'
    b'      - 1962\n'
    b'      - 1\n'
    b'      - 13\n'
    b'  e: !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    b"    __class_name__: <class 'datetime.time'>\n"
    b'    __dumped_obj__:\n'
    b'      __type__: time\n'
    b'      value:\n'
    b'      - 11\n'
    b'      - 12\n'
    b'      - 13\n'
    b'  f:\n'
    b'  - 1\n'
    b'  - 2\n'
    b'  - 3\n'
    b'  - !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    b"    __class_name__: <class 'decimal.Decimal'>\n"
    b'    __dumped_obj__:\n'
    b'      __type__: Decimal\n'
    b"      value: '4'\n"
)


nest_yaml_custom = (
    '- null\n'
    '- {}\n'
    '- - 1\n'
    '  - 2\n'
    '  - 3\n'
    '  - 4\n'
    '- a: 1\n'
    '  b: !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    "    __class_name__: <class 'decimal.Decimal'>\n"
    '    __dumped_obj__:\n'
    '      __type__: Decimal\n'
    "      value: '2'\n"
    '  c: !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    "    __class_name__: <class 'datetime.datetime'>\n"
    '    __dumped_obj__:\n'
    '      __type__: datetime\n'
    '      value:\n'
    '      - 2020\n'
    '      - 5\n'
    '      - 24\n'
    '      - 8\n'
    '      - 20\n'
    '      - 0\n'
    '  d: !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    "    __class_name__: <class 'datetime.date'>\n"
    '    __dumped_obj__:\n'
    '      __type__: date\n'
    '      value:\n'
    '      - 1962\n'
    '      - 1\n'
    '      - 13\n'
    '  e: !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    "    __class_name__: <class 'datetime.time'>\n"
    '    __dumped_obj__:\n'
    '      __type__: time\n'
    '      value:\n'
    '      - 11\n'
    '      - 12\n'
    '      - 13\n'
    '  f:\n'
    '  - 1\n'
    '  - 2\n'
    '  - 3\n'
    '  - !<tag:github.com/iisaka51/datajuggler,2022:python/datajuggler>\n'
    "    __class_name__: <class 'decimal.Decimal'>\n"
    '    __dumped_obj__:\n'
    '      __type__: Decimal\n'
    "      value: '4'\n"
)


simple_data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
yaml_data_sorted = "April: 4\nFebruary: 2\nJanuary: 1\nMarch: 3\n"
yaml_data_encode = b"January: 1\nFebruary: 2\nMarch: 3\nApril: 4\n"
yaml_data_sort_encode = b'April: 4\nFebruary: 2\nJanuary: 1\nMarch: 3\n'
yaml_data = 'January: 1\nFebruary: 2\nMarch: 3\nApril: 4\n'



yaml_adict_sorted_encode = (
    b'!!python/object/new:datajuggler.core.aDict\n'
    b'dictitems:\n'
    b'  April: 4\n'
    b'  February: 2\n'
    b'  January: 1\n'
    b'  March: 3\n'
)

yaml_adict_sorted = (
    '!!python/object/new:datajuggler.core.aDict\n'
    'dictitems:\n'
    '  April: 4\n'
    '  February: 2\n'
    '  January: 1\n'
    '  March: 3\n'
)

yamlcustom_adict = (
  '!!python/object/new:datajuggler.core.aDict\n'
  'dictitems:\n'
  '  April: 4\n'
  '  February: 2\n'
  '  January: 1\n'
  '  March: 3\n'
)

yamlcustom_encode = (
  b'!!python/object/new:datajuggler.core.aDict\n'
  b'dictitems:\n'
  b'  April: 4\n'
  b'  February: 2\n'
  b'  January: 1\n'
  b'  March: 3\n'
)

yamlcustom_sorted_encode = (
  b'!!python/object/new:datajuggler.core.aDict\n'
  b'dictitems:\n'
  b'  January: 1\n'
  b'  February: 2\n'
  b'  March: 3\n'
  b'  April: 4\n'
)


yaml_udict_sorted = (
  '!!python/object/new:datajuggler.core.uDict\n'
  'dictitems:\n'
  '  April: 4\n'
  '  February: 2\n'
  '  January: 1\n'
  '  March: 3\n'
  'state:\n'
  '  keypath_separator: /\n'
)

yaml_udict = (
  '!!python/object/new:datajuggler.core.uDict\n'
  'state:\n'
  '  __keypath_separator: /\n'
  'dictitems:\n'
  '  January: 1\n'
  '  February: 2\n'
  '  March: 3\n'
  '  April: 4\n'
)

yaml_udict_encode = (
  b'!!python/object/new:datajuggler.core.uDict\n'
  b'state:\n'
  b'  __keypath_separator: /\n'
  b'dictitems:\n'
  b'  January: 1\n'
  b'  February: 2\n'
  b'  March: 3\n'
  b'  April: 4\n'
)


unicode_data = { 3: '3月', 2: '2月', 1: '1月', }
yaml_unicode_sort = '1: "1\\u6708"\n2: "2\\u6708"\n3: "3\\u6708"\n'
yaml_unicode = '1: 1月\n2: 2月\n3: 3月\n'

valid_content  = uDict({'invoice': 34843, 'date': datetime.date(2001, 1, 23), 'bill-to': uDict({'given': 'Chris', 'family': 'Dumars', 'address': uDict({'lines': '458 Walkman Dr.\nSuite #292\n', 'city': 'Royal Oak', 'state': 'MI', 'postal': 48046})}), 'ship-to': uDict({'given': 'Chris', 'family': 'Dumars', 'address': uDict({'lines': '458 Walkman Dr.\nSuite #292\n', 'city': 'Royal Oak', 'state': 'MI', 'postal': 48046})}), 'product': [{'sku': 'BL394D', 'quantity': 4, 'description': 'Basketball', 'price': 450.0}, {'sku': 'BL4438H', 'quantity': 1, 'description': 'Super Hoop', 'price': 2392.0}], 'tax': 251.42, 'total': 4443.52, 'comments': 'Late afternoon is best. Backup contact is Nancy Billsmer @ 338-4338.'})

class TestClass:
    def test_yaml_dumps_case01(self):
        result = io.dumps(nest_data, format='yaml')
        assert result == nest_yaml_encode

    def test_yaml_dumps_case02(self):
        result = io.dumps(simple_data, format='yaml')
        assert result == yaml_data_sort_encode

    def test_yaml_dumps_case03(self):
        expect = "dumps() got an unexpected keyword argument 'sort_keys'"
        with pytest.raises(TypeError) as e:
            result = io.dumps(simple_data, format='yaml', sort_keys=False)
        assert str(e.value) == expect

    def test_yaml_custom_dumps_case01(self):
        result = io.dumps(nest_data, format='yaml:custom')
        assert result == nest_yaml

    def test_yaml_custom_dumps_case02(self):
        result = io.dumps(nest_data, format='yaml:custom', encoding='utf-8')
        assert result == nest_yaml_custom

    def test_yaml_custom_dumps_case03(self):
        result = io.dumps(simple_data, format='yaml:custom')
        assert result == yaml_data_sorted

    def test_yaml_custom_dumps_case04(self):
        result = io.dumps(simple_data, format='yaml:custom', sort_keys=False)
        assert result == yaml_data

    def test_yaml_custom_dumps_case05(self):
        result = io.dumps(unicode_data, format='yaml:custom')
        assert result == yaml_unicode_sort

    def test_yaml_custom_dumps_case06(self):
        result = io.dumps(unicode_data, format='yaml:custom', allow_unicode=True)
        assert result == yaml_unicode



    def test_yaml_loads_case01(self):
        result = io.loads(nest_yaml_encode, format='yaml')
        assert result == nest_data

    def test_yaml_loads_case02(self):
        result = io.loads(nest_yaml_encode, format='yaml', encoding='utf-8')
        assert result == nest_data

    def test_yaml_custom_loads_case01(self):
        result = io.loads(nest_yaml_encode, format='yaml:custom')
        assert result == nest_data

    def test_yaml_custom_loads_case02(self):
        result = io.loads(nest_yaml, format='yaml:custom')
        assert result == nest_data

    def test_yaml_custom_loads_case03(self):
        result = io.loads(nest_yaml, format='yaml:custom', encoding='utf-8')
        assert result == nest_data

    def test_yaml_custom_loads_case04(self):
        result = io.loads(yaml_data_sorted, format='yaml:custom')
        assert result == simple_data

    def test_yaml_custom_loads_case05(self):
        result = io.loads(yaml_unicode_sort, format='yaml:custom')
        assert result == unicode_data



    def test_yaml_loads_adict_case01(self):
        d = aDict(yaml_adict_sorted_encode, format='yaml')
        assert d == aDict(simple_data)

    def test_yaml_loads_adict_case02(self):
        d = aDict(yaml_adict_sorted, format='yaml')
        assert d == aDict(simple_data)

    def test_yaml_loads_adict_case03(self):
        filepath='tests/serializer/data/valid-content.yml'
        d = aDict(filepath, format='yaml')
        assert d == valid_content

    def test_yaml_loads_adict_case04(self):
        filepath='tests/serializer/data/valid-content.yml'
        d = aDict(filepath, format='yml')
        assert d == valid_content

    def test_yaml_loads_adict_case05(self):
        filepath='tests/serializer/data/valid-content.yml'
        d = aDict(filepath)
        assert d == valid_content

    def test_yaml_loads_adict_case06(self):
        expect = (
          'Invalid data or url or filepath argument: '
          'We the People of the United '
          'States, in Order to form a more perfect Union, '
          'establish Justice, insure '
          'domestic Tranquility, provide for the common defense, '
          'promote the general Welfare, '
          'and secure the Blessings of Liberty to ourselves and our Posterity, '
          'do ordain and establish this Constitution for '
          'the United States of America.\n'
          "Invalid data type: <class 'str'>, expected dict or list.")

        filepath='tests/serializer/data/invalid-content.yml'
        with pytest.raises(ValueError) as e:
            d = aDict(filepath, format='yaml')
        assert str(e.value) == expect


    def test_yaml_loads_udict_case01(self):
        d = uDict(yaml_udict_encode, format='yaml')
        assert d == uDict(simple_data)

    def test_yaml_loads_udict_case02(self):
        d = uDict(yaml_udict, format='yaml')
        assert d == uDict(simple_data)

    def test_yaml_loads_udict_case03(self):
        filepath='tests/serializer/data/valid-content.yml'
        d = uDict(filepath, format='yaml')
        assert d == valid_content

    def test_yaml_loads_udict_case04(self):
        filepath='tests/serializer/data/valid-content.yml'
        d = uDict(filepath, format='yml')
        assert d == valid_content

    def test_yaml_loads_udict_case05(self):
        filepath='tests/serializer/data/valid-content.yml'
        d = uDict(filepath)
        assert d == valid_content

    def test_yaml_loads_udict_case06(self):
        expect = (
          'Invalid data or url or filepath argument: '
          'We the People of the United '
          'States, in Order to form a more perfect Union, '
          'establish Justice, insure '
          'domestic Tranquility, provide for the common defense, '
          'promote the general Welfare, '
          'and secure the Blessings of Liberty to ourselves and our Posterity, '
          'do ordain and establish this Constitution for '
          'the United States of America.\n'
          "Invalid data type: <class 'str'>, expected dict or list.")

        filepath='tests/serializer/data/invalid-content.yml'
        with pytest.raises(ValueError) as e:
            d = uDict(filepath, format='yaml')
        assert str(e.value) == expect

