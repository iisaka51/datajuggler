import sys
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler.dicthelper import get_keys

class TestClass:

    def test_getkeys_case01(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3, },
                        "d": { "x": 4, "y": 5, },
                      },
                }
        expect = ['a', 'b', 'c', 'x', 'y', 'd', 'x', 'y']
        result = get_keys(data)
        assert result == expect

    def test_getkeys_case02(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3, },
                        "d": { "x": 4, "y": 5, },
                      },
                }
        expect = ['a', 'b', 'c', 'x', 'y', 'd', 'x', 'y']
        expect = [['a'],
                  ['b'],
                  ['b', 'c'],
                  ['b', 'c', 'x'],
                  ['b', 'c', 'y'],
                  ['b', 'd'],
                  ['b', 'd', 'x'],
                  ['b', 'd', 'y']
                ]
        result = get_keys(data, output_for="keylist")
        assert result == expect

    def test_getkeys_case03(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3, },
                        "d": { "x": 4, "y": 5, },
                      },
                }
        expect = ['a',
                  'b',
                  'b.c',
                  'b.c.x',
                  'b.c.y',
                  'b.d',
                  'b.d.x',
                  'b.d.y']
        result = get_keys(data, output_for="keypath")
        assert result == expect

    def test_getkeys_case04(self):
        data = { "a": 1,
                 "b": { "c": { "x": 2, "y": 3, },
                        "d": { "x": 4, "y": 5, },
                      },
                }
        expect = ['a',
                  'b',
                  'b_c',
                  'b_c_x',
                  'b_c_y',
                  'b_d',
                  'b_d_x',
                  'b_d_y']
        result = get_keys(data, output_for="keypath", separator='_')
        assert result == expect

