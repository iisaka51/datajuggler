import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import  aDict
from datajuggler.dicthelper import d_rename

class TestClass:

    def test_rename_case01(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = { "A": 1, "b": 2, "c": 3, "d": None, }

        result = d_rename(data, "a", "A")
        assert result == expect

    def test_rename_case02(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = d_rename(data, "a", "a")
        assert result == data

    def test_rename_case03(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = { "a": 1, "B": 2, "c": 3, "d": None, }

        saved = data.copy()
        d_rename(data, "b", "B", inplace=True)
        assert data == expect

    def test_rename_case04(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = ( '"Invalid key: \'b\', key already in dict and '
                   '\'overwrite\' is disabled."' )

        with pytest.raises(KeyError) as e:
            result = d_rename(data, "a", "b", factory=aDict)
        assert str(e.value) == expect

    def test_rename_case05(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = { "A": 1, "B": 2, "c": 3, "d": None, }

        result = d_rename(data, {'a': 'A', 'b': 'B'})
        assert result == expect

    def test_rename_case06(self):
        data = { "First Name": 'jack', "b": 2, "c": 3, "d": None, }
        expect = { "first_name": 'jack', "b": 2, "c": 3, "d": None, }

        result = d_rename(data, "First Name", case_name='snake')
        assert result == expect

    def test_rename_case07(self):
        data = { "First Name": 'jack', 'Last Name': 'bauwer' }
        expect = { "first_name": 'jack', 'last_name': 'bauwer' }

        keys = list(data.keys())
        result = d_rename(data, keys, case_name='snake')
        assert result == expect

    def test_rename_case08(self):
        data = { "First Name": 'jack', 'Last Name': 'bauwer' }
        expect = { "firstName": 'jack', 'lastName': 'bauwer' }

        keys = data.keys()
        result = d_rename(data, keys, case_name='camel')
        assert result == expect


