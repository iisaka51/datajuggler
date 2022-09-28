# -*- coding: utf-8 -*-

import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler.dicthelper import d_nest

class TestClass:

    def test_nest_case01(self):
        data = [
            {"id": 1, "parent_id": None, "name": "John"},
            {"id": 2, "parent_id": 1, "name": "Frank"},
            {"id": 3, "parent_id": 2, "name": "Tony"},
            {"id": 4, "parent_id": 3, "name": "Jimmy"},
            {"id": 5, "parent_id": 1, "name": "Sam"},
            {"id": 6, "parent_id": 3, "name": "Charles"},
            {"id": 7, "parent_id": 2, "name": "Bob"},
            {"id": 8, "parent_id": 3, "name": "Paul"},
            {"id": 9, "parent_id": None, "name": "Michael"},
        ]
        expect = [
            {
                "id": 1,
                "parent_id": None,
                "name": "John",
                "children": [
                    {
                        "id": 2,
                        "parent_id": 1,
                        "name": "Frank",
                        "children": [
                            {
                                "id": 3,
                                "parent_id": 2,
                                "name": "Tony",
                                "children": [
                                    {
                                        "id": 4,
                                        "parent_id": 3,
                                        "name": "Jimmy",
                                        "children": [],
                                    },
                                    {
                                        "id": 6,
                                        "parent_id": 3,
                                        "name": "Charles",
                                        "children": [],
                                    },
                                    {
                                        "id": 8,
                                        "parent_id": 3,
                                        "name": "Paul",
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "id": 7,
                                "parent_id": 2,
                                "name": "Bob",
                                "children": [],
                            },
                        ],
                    },
                    {
                        "id": 5,
                        "parent_id": 1,
                        "name": "Sam",
                        "children": [],
                    },
                ],
            },
            {
                "id": 9,
                "parent_id": None,
                "name": "Michael",
                "children": [],
            },
        ]
        result = d_nest(data, "id", "parent_id", "children")
        assert result == expect

    def test_nest_case02(self):
        data = [
            {"id": 1, "parent_id": None, "name": "John"},
            {"id": 2, "parent_id": 1, "name": "Frank"},
            {"id": 3, "parent_id": 2, "name": "Tony"},
            {"id": 4, "parent_id": 3, "name": "Jimmy"},
            {"id": 5, "parent_id": 1, "name": "Sam"},
            {"id": 6, "parent_id": 3, "name": "Charles"},
            {"id": 7, "parent_id": 2, "name": "Bob"},
            {"id": 8, "parent_id": 3, "name": "Paul"},
            {"id": 9, "parent_id": None, "name": "Michael"},
        ]
        with pytest.raises(ValueError) as e:
            result = d_nest(data, "id", "id", "children")
        assert str(e.value) == ''

        with pytest.raises(ValueError) as e:
            result = d_nest(data, "id", "parent_id", "id")
        assert str(e.value) == ''

        with pytest.raises(ValueError) as e:
            result = d_nest(data, "id", "parent_id", "parent_id")
        assert str(e.value) == ''

    def test_nest_case02(self):
        data = {"id": 1, "parent_id": None, "name": "John"}

        with pytest.raises(ValueError) as e:
            result = d_nest(data, "id", "parent_id", "children")
        assert str(e.value) == 'seq should be a list of dicts.'

    def test_nest_case04(self):
        data = [
            [{"id": 1, "parent_id": None, "name": "John"}],
            [{"id": 2, "parent_id": 1, "name": "Frank"}],
        ]
        with pytest.raises(ValueError) as e:
            result = d_nest(data, "id", "parent_id", "children")
        assert str(e.value) == 'element should be a dict.'
