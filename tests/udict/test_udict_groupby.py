# -*- coding: utf-8 -*-

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

        expect = uDict({1: [uDict({'id': 1, 'name': 'John'}),
                            uDict({'id': 1, 'name': 'Eddie'}),
                            uDict({'id': 1, 'name': 'Edward'})],
                        2: [uDict({'id': 2, 'name': 'Paul'})],
                        3: [uDict({'id': 3, 'name': 'David'}),
                            uDict({'id': 3, 'name': 'Jack'}),
                            uDict({'id': 3, 'name': 'Bob'})],
                        4: [uDict({'id': 4, 'name': 'Freddie'}),
                            uDict({'id': 4, 'name': 'Maichael'})]})

        result = uDict().groupby(data, "id")
        assert result == expect

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

        expect = ( "uDict({1: [uDict({'id': 1, 'name': 'John'}), "
                              "uDict({'id': 1, 'name': 'Eddie'}), "
                              "uDict({'id': 1, 'name': 'Edward'})], "
                          "2: [uDict({'id': 2, 'name': 'Paul'})], "
                          "3: [uDict({'id': 3, 'name': 'David'}), "
                              "uDict({'id': 3, 'name': 'Jack'}), "
                              "uDict({'id': 3, 'name': 'Bob'})], "
                          "4: [uDict({'id': 4, 'name': 'Freddie'}), "
                              "uDict({'id': 4, 'name': 'Maichael'})]})"
                    )

        result = uDict().groupby(data, "id")
        assert result.__repr__() == expect

    def test_udict_groupby_case03(self):

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
        result = uDict().groupby(data, "id", factory=aDict)
        assert result.__repr__() == expect


