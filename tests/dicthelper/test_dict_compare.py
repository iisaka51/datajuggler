import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import aDict, Keylist, Keypath
from datajuggler.dicthelper import d_compare

class TestClass:

    def test_compare_case01(self):
        d1 = {}
        d2 = {}
        result = d_compare(d1, d2)
        assert result == True

    def test_compare_case02(self):
        d1 = {1: 1}
        d2 = {1: 1}
        result = d_compare(d1, d2)
        assert result == True

    def test_compare_case03(self):
        d1 = {'1': 'one'}
        d2 = {'1': 'one'}
        result = d_compare(d1, d2)
        assert result == True

    def test_compare_case04(self):
        d1 = {'1': 'one'}
        d2 = {'1':  2}
        result = d_compare(d1, d2)
        assert result == False

    def test_compare_case05(self):
        d1 = { "a": 1, "b": [1,2,3] }
        d2 = { "a": 1, "b": [1,2,3] }
        result = d_compare(d1, d2)
        assert result == True


    def test_compare_case06(self):
        d1 = { "a": 1,
               "b": 2,
               "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                        "g": { "h": 5, },
                    }
                 },
              }
        d2 = { "a": 1,
               "b": 2,
               "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                        "g": { "h": 5, },
                    }
                 },
              }
        result = d_compare(d1, d2)
        assert result == True

    def test_compare_case07(self):
        d1 = { "a": 1,
               "b": 2,
               "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                        "g": { "h": 5, },
                    }
                 },
              }
        d2 = { "a": 1,
               "b": 2,
               "c": {
                    "d": {
                        "e": 13,
                        "f": 14,
                        "g": { "h": 5, },
                    }
                 },
              }
        result = d_compare(d1, d2, keys='b')
        assert result == True

    def test_compare_case08(self):
        d1 = { "a": 1,
               "b": 2,
               "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                        "g": { "h": 5, },
                    }
                 },
              }
        d2 = { "a": 1,
               "b": 2,
               "c": {
                    "d": {
                        "e": 13,
                        "f": 14,
                        "g": { "h": 5, },
                    }
                 },
              }
        result = d_compare(d1, d2, keys='d')
        assert result == False

    def test_compare_keylist_case01(self):
        d1 = { "a": 1,
               "b": 2,
               "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                        "g": { "h": 5, },
                    }
                 },
              }
        d2 = { "a": 1,
               "b": 2,
               "c": {
                    "d": {
                        "e": 13,
                        "f": 14,
                        "g": { "h": 5, },
                    }
                 },
              }
        result = d_compare(d1, d2, keys=Keylist(['c', 'd', 'g']))
        assert result == True

    def test_compare_keypath_case01(self):
        d1 = { "a": 1,
               "b": 2,
               "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                        "g": { "h": 5, },
                    }
                 },
              }
        d2 = { "a": 1,
               "b": 2,
               "c": {
                    "d": {
                        "e": 13,
                        "f": 14,
                        "g": { "h": 5, },
                    }
                 },
              }
        result = d_compare(d1, d2, keys=Keypath('c.d.g'))
        assert result == True

