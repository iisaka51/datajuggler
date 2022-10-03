# -*- coding: utf-8 -*-

import pytest

from datajuggler import uDict

data = { "a": 1,
         "b": { "c": { "x": 2, "y": 3, },
                "d": { "x": 4, "y": 5, },
              },
       }

class TestClass:

    def test_getkeys_case01(self):
        expect = ['a', 'b', 'c', 'x', 'y', 'd', 'x', 'y']
        result = uDict().get_keys(data)
        assert result == expect
        result = uDict(data).get_keys()
        assert result == expect

    def test_getkeys_case02(self):
        expect = [['a'],
                  ['b'],
                  ['b', 'c'],
                  ['b', 'c', 'x'],
                  ['b', 'c', 'y'],
                  ['b', 'd'],
                  ['b', 'd', 'x'],
                  ['b', 'd', 'y']
                ]
        result = uDict(data).get_keys(output_as="keylist")
        assert result == expect

    def test_getkeys_case03(self):
        expect = ['a',
                  'b',
                  'b.c',
                  'b.c.x',
                  'b.c.y',
                  'b.d',
                  'b.d.x',
                  'b.d.y']
        result = uDict(data).get_keys(output_as="keypath")
        assert result == expect

    def test_getkeys_case04(self):
        expect = ['a',
                  'b',
                  'b_c',
                  'b_c_x',
                  'b_c_y',
                  'b_d',
                  'b_d_x',
                  'b_d_y']
        result = uDict(data).get_keys(data, output_as="keypath",
                                            separator='_')
        assert result == expect

