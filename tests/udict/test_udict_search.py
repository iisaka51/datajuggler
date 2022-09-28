import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import uDict

class TestClass:

    def test_udict_search_case01(self):
        data =  {
            "a": "January",
            "b": "january!",
            "c": {
                "d": True,
                "e": " january february ",
                "f": {
                    "g": ['January', 'February', 'March', 'April' ],
                    "january": 12345,
                    "February": True,
                },
            },
            "x": "Peter Piper picked a peck of pickled peppers.",
            "y": { "x": { "y": 5, "z": 6, }, },
            "January February": "march",
        }
        expect = {}
        result = uDict().search("jarnuary", data, search_for="value")
        assert result == expect
        obj = uDict(data)
        result = obj.search("jarnuary", search_for="value")
        assert result == expect

    def test_udict_search_case02(self):
        data =  {
            "a": "January",
            "b": "january!",
            "c": {
                "d": True,
                "e": " january february ",
                "f": {
                    "g": ['January', 'February', 'March', 'April' ],
                    "january": 12345,
                    "February": True,
                },
            },
            "x": "Peter Piper picked a peck of pickled peppers.",
            "y": { "x": { "y": 5, "z": 6, }, },
            "January February": "march",
        }
        expect = {'a': 'January',
                  'b': 'january!',
                  'c f g 0': 'January'}
        result = uDict(data).search("january",
                          search_for="value", ignore_case=True)
        assert result == expect

    def test_udict_search_case03(self):
        data =  {
            "a": "January",
            "b": "january!",
            "c": {
                "d": True,
                "e": " january february ",
                "f": {
                    "g": ['January', 'February', 'March', 'April' ],
                    "january": 12345,
                    "February": True,
                },
            },
            "x": "Peter Piper picked a peck of pickled peppers.",
            "y": { "x": { "y": 5, "z": 6, }, },
            "January February": "march",
        }
        expect = {}
        result = uDict(data).search("january",
                          search_for="value", exact=True)
        assert result == expect

    def test_udict_search_case04(self):
        data =  {
            "a": "January",
            "b": "january!",
            "c": {
                "d": True,
                "e": " january february ",
                "f": {
                    "g": {1: 'January', 2: 'February' },
                    "january": 12345,
                    "February": True,
                },
            },
            "x": "Peter Piper picked a peck of pickled peppers.",
            "y": { "x": { "y": 5, "z": 6, }, },
            "January February": "march",
        }
        expect = {'a': 'January',
                  'b': 'january!',
                  'c f g 1': 'January'}

        result = uDict(data).search("january",
                             search_for="value", ignore_case=True)
        assert result == expect

