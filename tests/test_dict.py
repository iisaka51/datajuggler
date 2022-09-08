import sys
import time
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import (
    uDict, iDict, aDict,
    change_dict_keys, ordereddict_to_dict, groupby
)

from collections import OrderedDict
import pandas as pd

class TestClass:
    def test_ordereddict_case01(self):
        data = OrderedDict([('month', 'January'), ('day', 13 )])
        expect = dict({'month': 'January', 'day': 13})
        result = ordereddict_to_dict(data)
        assert result == expect

    def test_ordereddict_case02(self):
        data = OrderedDict([('month', 'January'), ('day', 13 ),
                    ('time', OrderedDict([('hours', 7), ('minutes', 30)]))])
        expect = dict({'month': 'January', 'day': 13,
                       'time': {'hours': 7, 'minutes': 30}})
        result = ordereddict_to_dict(data)
        assert result == expect

    def test_change_dict_keys_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        replace = { 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 3: 3, 4: 4 }
        result = change_dict_keys(data, replace)
        assert result == expect

    def test_change_dict_keys_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        replace = { 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 3: 3, 4: 4 }
        change_dict_keys(data, replace, inplace=True)
        assert data == expect

    def test_change_dict_keys_case03(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4 }
        result = change_dict_keys(data, 'April', 'Apr')
        assert result == expect

    def test_change_dict_keys_case04(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4 }
        change_dict_keys(data, 'April', 'Apr', inplace=True)
        assert data == expect


    def test_groupby_case01(self):
        data = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Paul"},
            {"id": 3, "name": "David"},
            {"id": 4, "name": "Freddie"},
            {"id": 3, "name": "Jack"},
            {"id": 1, "name": "Eddie"},
            {"id": 3, "name": "Bob"},
            {"id": 4, "name": "Maichael"},
            {"id": 1, "name": "Edward"},
        ]
        expect = ( "{1: [{'id': 1, 'name': 'John'}, "
                        "{'id': 1, 'name': 'Eddie'}, "
                        "{'id': 1, 'name': 'Edward'}], "
                    "2: [{'id': 2, 'name': 'Paul'}], "
                    "3: [{'id': 3, 'name': 'David'}, "
                        "{'id': 3, 'name': 'Jack'}, "
                        "{'id': 3, 'name': 'Bob'}], "
                    "4: [{'id': 4, 'name': 'Freddie'}, "
                        "{'id': 4, 'name': 'Maichael'}]}" )
        result = groupby(data, "id")
        assert result.__repr__() == expect


    def test_groupby_case02(self):
        data = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Paul"},
            {"id": 3, "name": "David"},
            {"id": 4, "name": "Freddie"},
            {"id": 3, "name": "Jack"},
            {"id": 1, "name": "Eddie"},
            {"id": 3, "name": "Bob"},
            {"id": 4, "name": "Maichael"},
            {"id": 1, "name": "Edward"},
        ]
        expect = ( "iDict({1: [{'id': 1, 'name': 'John'}, "
                              "{'id': 1, 'name': 'Eddie'}, "
                              "{'id': 1, 'name': 'Edward'}], "
                          "2: [{'id': 2, 'name': 'Paul'}], "
                          "3: [{'id': 3, 'name': 'David'}, "
                              "{'id': 3, 'name': 'Jack'}, "
                              "{'id': 3, 'name': 'Bob'}], "
                          "4: [{'id': 4, 'name': 'Freddie'}, "
                              "{'id': 4, 'name': 'Maichael'}]})" )
        result = groupby(data, "id", factory=iDict)
        assert result.__repr__() == expect


