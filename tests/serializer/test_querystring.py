import pytest

from datajuggler import aDict, uDict
from datajuggler import serializer as io


data =  {
    'author': 'Fabio Caccamo',
    'lib': 'python benedict',
    'ok': '1',
    'page': '3',
    'test': '2',
    }

qs = ( 'author=Fabio+Caccamo&lib=python+benedict&'
       'ok=1&page=3&test=2' )


invalid_expect = (
    'Invalid query string: We the People of the United States, '
    'in Order to form a more perfect Union, establish Justice, '
    'insure domestic Tranquility, provide for the common defense, '
    'promote the general Welfare, '
    'and secure the Blessings of Liberty to ourselves '
    'and our Posterity, do ordain and establish this Constitution '
    'for the United States of America.\n' )


class TestClass:
    def test_querystring_loads(self):
        result = io.loads(qs, format='querystring')
        assert result == data
        result = io.loads(qs, format='qs')
        assert result == data

    def test_querystring_dumps(self):
        result = io.dumps(data, format='querystring')
        assert result == qs
        result = io.dumps(data, format='qs')
        assert result == qs


    def test_querystring_adict_loads_case01(self):
        filepath = 'tests/serializer/data/valid-content.qs'
        expect = aDict(data)
        d = aDict(filepath, format='qs')
        assert d == expect

    def test_querystring_adict_loads_case02(self):
        filepath = 'tests/serializer/data/valid-content.qs'
        expect = aDict(data)
        d = aDict(filepath)
        assert d == expect

    def test_querystring_adict_loads_case03(self):
        filepath = 'tests/serializer/data/invalid-content.qs'
        with pytest.raises(ValueError) as e:
            d = aDict(filepath, format='qs')
        assert str(e.value) == invalid_expect

    def test_querystring_udict_loadscase01(self):
        filepath = 'tests/serializer/data/valid-content.qs'
        expect = aDict(data)
        d = uDict(filepath, format='qs')
        assert d == expect

    def test_querystring_udict_loadscase02(self):
        filepath = 'tests/serializer/data/valid-content.qs'
        expect = aDict(data)
        d = uDict(filepath)
        assert d == expect

    def test_querystring_udict_loadscase03(self):
        filepath = 'tests/serializer/data/invalid-content.qs'
        with pytest.raises(ValueError) as e:
            d = uDict(filepath, format='qs')
        assert str(e.value) == invalid_expect
