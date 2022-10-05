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

class TestClass:
    def test_querystring_decode(self):
        s = io.QueryStringSerializer()
        result = s.decode(qs)
        assert result == data

    def test_querystring_encode(self):
        s = io.QueryStringSerializer()
        result = s.encode(data)
        assert result == qs


    def test_querystring_adict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.qs'
        expect = aDict(data)
        d = aDict(filepath, format='qs')
        assert d == expect

    def test_querystring_adict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.qs'
        expect = aDict(data)
        d = aDict(filepath)
        assert d == expect

    def test_querystring_adict_decode_case03(self):
        filepath = 'tests/serializer/data/invalid-content.qs'
        expect = (
          "Invalid data or url or filepath argument: "
          "tests/serializer/data/invalid-content.qs\n"
          "Invalid query string: "
          "Lorem ipsum consectetur sint id aute officia sed "
          "excepteur consectetur labore laboris dolore in "
          "labore consequat ut in eu ut deserunt.\n"
          "Elit aliqua velit aliquip voluptate consequat "
          "reprehenderit occaecat dolor ut esse aute laboris "
          "cillum fugiat esse est laborum." )

        with pytest.raises(ValueError) as e:
            d = aDict(filepath, format='qs')
        assert str(e.value) == expect

    def test_querystring_udict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.qs'
        expect = aDict(data)
        d = uDict(filepath, format='qs')
        assert d == expect

    def test_querystring_udict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.qs'
        expect = aDict(data)
        d = uDict(filepath)
        assert d == expect

    def test_querystring_udict_decode_case03(self):
        filepath = 'tests/serializer/data/invalid-content.qs'
        expect = (
          "Invalid data or url or filepath argument: "
          "tests/serializer/data/invalid-content.qs\n"
          "Invalid query string: "
          "Lorem ipsum consectetur sint id aute officia sed "
          "excepteur consectetur labore laboris dolore in "
          "labore consequat ut in eu ut deserunt.\n"
          "Elit aliqua velit aliquip voluptate consequat "
          "reprehenderit occaecat dolor ut esse aute laboris "
          "cillum fugiat esse est laborum." )

        with pytest.raises(ValueError) as e:
            d = uDict(filepath, format='qs')
        assert str(e.value) == expect
