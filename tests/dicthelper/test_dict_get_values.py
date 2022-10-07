# -*- coding: utf-8 -*-

import pytest

from datajuggler import uDict, Keylist, Keypath
from datajuggler.dicthelper import get_values

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

    def test_dict_access_get_values_case01(self):
        assert get_values(self.data, 'a') == 1

    def test_dict_access_get_values_case02(self):
        expect = { "x": 2, "y": 3, }
        assert get_values(self.data, ('b', 'c')) == None

    def test_dict_access_get_values_case03(self):
        expect = { "x": 2, "y": 3, }
        assert get_values(self.data, Keylist(['b', 'c'])) == expect

    def test_dict_access_get_values_case04(self):
        assert get_values(self.data, Keylist(['b', 'e[1]', 'z[2]'])) == 4

    def test_dict_access_get_values_case05(self):
        expect = { "x": 2, "y": 3, }
        assert get_values(self.data, Keypath('b.c')) == expect

    def test_dict_access_get_values_case06(self):
        assert get_values(self.data, Keypath('b.e[1].z[2]')) == 4

