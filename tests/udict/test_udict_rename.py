import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import  aDict, uDict

class TestClass:

    def test_udict_rename_case01(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = { "A": 1, "b": 2, "c": 3, "d": None, }

        result = uDict().rename("a", "A", data)
        assert result == expect
        obj = uDict(data)
        result = obj.rename("a", "A")
        assert result == expect

    def test_udict_rename_case02(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }

        result = uDict(data).rename("a", "a")
        assert result == data

    def test_udict_rename_case03(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = { "a": 1, "B": 2, "c": 3, "d": None, }

        obj = uDict(data)
        obj.rename("b", "B", inplace=True)
        assert obj == expect

    def test_udict_rename_case04(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = ( '"Invalid key: \'b\', key already in dict and '
                   '\'overwrite\' is disabled."' )

        with pytest.raises(KeyError) as e:
            result = uDict(data).rename("a", "b", factory=aDict)
        assert str(e.value) == expect

    def test_udict_rename_case05(self):
        data = { "a": 1, "b": 2, "c": 3, "d": None, }
        expect = { "A": 1, "B": 2, "c": 3, "d": None, }

        result = uDict(data).rename({'a': 'A', 'b': 'B'})
        assert result == expect

    def test_udict_rename_case06(self):
        data = { "First Name": 'jack', "b": 2, "c": 3, "d": None, }
        expect = { "first_name": 'jack', "b": 2, "c": 3, "d": None, }

        result = uDict(data).rename("First Name", case_name='snake')
        assert result == expect

    def test_udict_rename_case07(self):
        data = { "First Name": 'jack', 'Last Name': 'bauwer' }
        expect = { "first_name": 'jack', 'last_name': 'bauwer' }

        keys = list(data.keys())
        result = uDict(data).rename(keys, case_name='snake')
        assert result == expect

    def test_udict_rename_case08(self):
        data = { "First Name": 'jack', 'Last Name': 'bauwer' }
        expect = { "firstName": 'jack', 'lastName': 'bauwer' }

        keys = data.keys()
        result = uDict(data).rename(keys, case_name='camel')
        assert result == expect


