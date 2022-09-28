import sys
import time
import pytest

from datajuggler import uDict, aDict

class TestClass:

    def test_udict_groupby_case01(self):
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

        expect = ( "uDict({1: [{'id': 1, 'name': 'John'}, "
                              "{'id': 1, 'name': 'Eddie'}, "
                              "{'id': 1, 'name': 'Edward'}], "
                          "2: [{'id': 2, 'name': 'Paul'}], "
                          "3: [{'id': 3, 'name': 'David'}, "
                              "{'id': 3, 'name': 'Jack'}, "
                              "{'id': 3, 'name': 'Bob'}], "
                          "4: [{'id': 4, 'name': 'Freddie'}, "
                              "{'id': 4, 'name': 'Maichael'}]})")

        result = uDict().groupby(data, "id")
        assert result.__repr__() == expect

    def test_udict_groupby_case02(self):
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
        expect = ( "aDict({1: [{'id': 1, 'name': 'John'}, "
                              "{'id': 1, 'name': 'Eddie'}, "
                              "{'id': 1, 'name': 'Edward'}], "
                          "2: [{'id': 2, 'name': 'Paul'}], "
                          "3: [{'id': 3, 'name': 'David'}, "
                              "{'id': 3, 'name': 'Jack'}, "
                              "{'id': 3, 'name': 'Bob'}], "
                          "4: [{'id': 4, 'name': 'Freddie'}, "
                              "{'id': 4, 'name': 'Maichael'}]})" )
        result = uDict().groupby(data, "id", factory=aDict)
        assert result.__repr__() == expect


