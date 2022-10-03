# -*- coding: utf-8 -*-

import pytest

from datajuggler import aDict
from datajuggler.dicthelper import d_flatten, d_unflatten

class TestClass:

    def test_flatten_case01(self):
        data = { "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              }
        expect = {
            "a": 1,
            "b": 2,
            "c.d.e": 3,
            "c.d.f": 4,
            "c.d.g.h": 5,
        }
        result = d_flatten(data)
        assert result == expect

    def test_flatten_case02(self):
        data = { "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              }
        expect = {
            "a": 1,
            "b": 2,
            "c_d_e": 3,
            "c_d_f": 4,
            "c_d_g_h": 5,
        }
        result = d_flatten(data, separator="_")
        assert result == expect

    def test_flatten_case03(self):
        data = { "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              }
        expect = {
                "a": 1,
                "b": 2,
                "c.d.e": 3,
                "c.d.f": 4,
                "c.d.g.h": 5,
            }
        d_flatten(data, inplace=True)
        assert data == expect

    def test_flatten_case04(self):
        data = { "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              }
        expect = aDict({
                    "a": 1,
                    "b": 2,
                    "c.d.e": 3,
                    "c.d.f": 4,
                    "c.d.g.h": 5,
                })
        result = d_flatten(data, factory=aDict)
        assert result == expect

    def test_unflatten_case01(self):
        data = {
            "a": 1,
            "b": 2,
            "c.d.e": 3,
            "c.d.f": 4,
            "c.d.g.h": 5,
        }
        expect = { "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              }
        result = d_unflatten(data)
        assert result == expect

    def test_unflatten_case02(self):
        data = {
            "a": 1,
            "b": 2,
            "c_d_e": 3,
            "c_d_f": 4,
            "c_d_g_h": 5,
        }
        expect = { "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              }
        result = d_unflatten(data, separator="_")
        assert result == expect

    def test_unflatten_case03(self):
        data = {
                "a": 1,
                "b": 2,
                "c.d.e": 3,
                "c.d.f": 4,
                "c.d.g.h": 5,
            }
        expect = { "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              }
        d_unflatten(data, inplace=True)
        assert data == expect

    def test_unflatten_case04(self):
        data = aDict({
                    "a": 1,
                    "b": 2,
                    "c.d.e": 3,
                    "c.d.f": 4,
                    "c.d.g.h": 5,
                })
        expect = { "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              }
        result = d_unflatten(data)
        assert result == expect

