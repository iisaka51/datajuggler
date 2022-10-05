# -*- coding: utf-8 -*-

import pytest

from datajuggler import uDict, Keylist, Keypath

class TestClass:
    data = { "a": 1,
             "b": { "c": { "x": 2, "y": 3, },
                    "d": { "x": 4, "y": 5, },
                    "e": [ { "x": 1, "y": -1, "z": [1, 2, 3], },
                           { "x": 2, "y": -2, "z": [2, 3, 4], },
                           { "x": 3, "y": -3, "z": [3, 4, 5], },
                         ],
                  },
          }

    def test_dict_access_get_values_case01_1(self):
        d = uDict(self.data)
        assert d.get_values('a') == 1

    def test_dict_access_get_values_case01_2(self):
        assert uDict().get_values('a', self.data) == 1


    def test_dict_access_get_values_case02(self):
        d = uDict(self.data)
        assert d.get_values(('b', 'c')) == None

    def test_dict_access_get_values_case03(self):
        expect = { "x": 2, "y": 3, }
        d = uDict(self.data)
        assert d.get_values(Keylist(['b', 'c'])) == expect

    def test_dict_access_get_values_case04(self):
        d = uDict(self.data)
        assert d.get_values(Keylist(['b', 'e[1]', 'z[2]'])) == 4

    def test_dict_access_get_values_case05(self):
        expect = { "x": 2, "y": 3, }
        d = uDict(self.data)
        assert d.get_values(Keypath('b.c')) == expect

    def test_dict_access_get_values_case06(self):
        d = uDict(self.data)
        assert d.get_values(Keypath('b.e[1].z[2]')) == 4

