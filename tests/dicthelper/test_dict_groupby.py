# -*- coding: utf-8 -*-

import pytest

from datajuggler import uDict, aDict
from datajuggler.dicthelper import d_groupby

class TestClass:

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
        result = d_groupby(data, "id")
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
        expect = ( "aDict({1: [aDict({'id': 1, 'name': 'John'}), "
                              "aDict({'id': 1, 'name': 'Eddie'}), "
                              "aDict({'id': 1, 'name': 'Edward'})], "
                          "2: [aDict({'id': 2, 'name': 'Paul'})], "
                          "3: [aDict({'id': 3, 'name': 'David'}), "
                              "aDict({'id': 3, 'name': 'Jack'}), "
                              "aDict({'id': 3, 'name': 'Bob'})], "
                          "4: [aDict({'id': 4, 'name': 'Freddie'}), "
                              "aDict({'id': 4, 'name': 'Maichael'})]})"
                    )
        result = d_groupby(data, "id", factory=aDict)
        assert result.__repr__() == expect


