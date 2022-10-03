# -*- coding: utf-8 -*-

import pytest

from datajuggler import aDict, uDict

class TestClass:

    def test_udict_flatten_case01(self):
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
        expect = uDict({
            "a": 1,
            "b": 2,
            "c.d.e": 3,
            "c.d.f": 4,
            "c.d.g.h": 5,
        })
        result = uDict().flatten(data)
        assert result == expect

        obj = uDict(data)
        result = obj.flatten()
        assert result == expect

    def test_udict_flatten_case02(self):
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
        expect = uDict({
            "a": 1,
            "b": 2,
            "c_d_e": 3,
            "c_d_f": 4,
            "c_d_g_h": 5,
        })
        result = uDict(data).flatten(separator="_")
        assert result == expect

    def test_udict_flatten_case03(self):
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
        expect = uDict({
                "a": 1,
                "b": 2,
                "c.d.e": 3,
                "c.d.f": 4,
                "c.d.g.h": 5,
            })
        obj = uDict(data)
        obj.flatten(inplace=True)
        assert obj == expect

    def test_udict_flatten_case04(self):
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
        result = uDict(data).flatten(factory=aDict)
        assert result == expect

    def test_udict_unflatten_case01_1(self):
        data = {
            "a": 1,
            "b": 2,
            "c.d.e": 3,
            "c.d.f": 4,
            "c.d.g.h": 5,
        }
        expect = uDict({ "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              })
        result = uDict().unflatten(data)
        assert result == expect

    def test_udict_unflatten_case01_2(self):
        data = {
            "a": 1,
            "b": 2,
            "c.d.e": 3,
            "c.d.f": 4,
            "c.d.g.h": 5,
        }
        expect = uDict({ "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              })
        obj = uDict(data)
        result = obj.unflatten()
        assert result == expect

    def test_udict_unflatten_case02(self):
        data = {
            "a": 1,
            "b": 2,
            "c_d_e": 3,
            "c_d_f": 4,
            "c_d_g_h": 5,
        }
        expect = uDict({ "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              })
        result = uDict().unflatten(data, separator="_")
        assert result == expect

    def test_udict_unflatten_case03(self):
        data = {
                "a": 1,
                "b": 2,
                "c.d.e": 3,
                "c.d.f": 4,
                "c.d.g.h": 5,
            }
        expect = uDict({ "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              })
        obj = uDict(data)
        obj.unflatten(inplace=True)
        assert obj == expect

    def test_udict_unflatten_case04(self):
        data = aDict({
                    "a": 1,
                    "b": 2,
                    "c.d.e": 3,
                    "c.d.f": 4,
                    "c.d.g.h": 5,
                })
        expect = uDict({ "a": 1,
                 "b": 2,
                 "c": {
                    "d": {
                        "e": 3,
                        "f": 4,
                         "g": { "h": 5, },
                    }
                 },
              })
        result = uDict(data).unflatten()
        assert result == expect

