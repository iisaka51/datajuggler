import sys
import time
import pytest

from datajuggler import StrCase
import numpy as np
import pandas as pd

class TestClass:
    def test_strcase_case01(self):
        data = "The sky is the limit"
        expect = 'StrCase("The sky is the limit")'
        s = StrCase(data)
        assert s.__repr__() == expect

    def test_strcase_case02(self):
        data = "The sky is the limit"
        expect = data
        s = StrCase(data)
        assert s.__str__() == expect

    def test_strcase_case03(self):
        data = "The sky is the limit"
        expect = "THE sky is the limit"
        s = StrCase(data)
        assert s.origin.replace('The', 'THE') == expect

    def test_strcase_case04(self):
        data = 1
        expect = "Expected str or list, dict objects, got <class 'int'>."
        with pytest.raises(TypeError) as e:
            s = StrCase(data)
        assert str(e.value) == expect

    def test_strcase_case05(self):
        data = ["Good luck", "The sky is the limit"]
        expect = "Expected at most 1 arguments, got 2."
        with pytest.raises(TypeError) as e:
            s = StrCase(*data)
        assert str(e.value) == expect

    def test_strcase_case06(self):
        data = "The sky is the limit"
        expect = 'StrCase("The sky is the limit")'
        s = StrCase()
        s.origin = data
        assert s.__repr__() == expect

    def test_strcase_case07(self):
        data = 1
        expect = "Expected str or list, dict objects, got <class 'int'>."
        s = StrCase()
        with pytest.raises(TypeError) as e:
            s.origin = data
        assert str(e.value) == expect

    def test_strcase_case08(self):
        data = ["Good luck", "The sky is the limit"]
        expect = "StrCase(['Good luck', 'The sky is the limit'])"
        s = StrCase(data)
        assert s.__repr__() == expect

    def test_strcase_case09(self):
        data = ["Good luck", "The sky is the limit"]
        expect = "['Good luck', 'The sky is the limit']"
        s = StrCase(data)
        assert s.__str__() == expect

    def test_strcase_case10(self):
        data = ["Good luck", "The sky is the limit"]
        expect = "Good luck"
        s = StrCase(data)
        assert s.origin[0] == expect

    def test_strcase_case11(self):
        data = "The sky is the limit"
        expect = "the_sky_is_the_limit"
        s = StrCase(data)
        assert s.convert_case('snake') == expect

    def test_strcase_case12(self):
        data = ["Good luck", "The sky is the limit"]
        expect = ["good_luck", "the_sky_is_the_limit"]
        s = StrCase(data)
        assert s.convert_case('snake') == expect

    def test_strcase_case13(self):
        data = "The sky is the limit"
        expect = 'the_sky_is_the_limit'
        s = StrCase(data)
        assert s.convert_case() == expect

    def test_strcase_case14(self):
        data = "The sky is the limit"
        expect = 'the-sky-is-the-limit'
        s = StrCase(data)
        assert s.convert_case('kebab') == expect

    def test_strcase_case15(self):
        data = "The sky is the limit"
        expect = 'theSkyIsTheLimit'
        s = StrCase(data)
        assert s.convert_case(case='camel') == expect

    def test_strcase_case16(self):
        data = ["Good luck", "The sky is the limit" ]
        expect = ["good_luck", "the_sky_is_the_limit"]
        s = StrCase(data)
        assert s.convert_case() == expect

    def test_strcase_case17(self):
        data = {1: "Good luck", 2: "The sky is the limit" }
        expect = {1: "good_luck", 2: "the_sky_is_the_limit" }
        s = StrCase(data)
        assert s.convert_case() == expect

    def test_strcase_case18(self):
        data = {"Good luck": 1, "The sky is the limit": 2 }
        expect = {"good_luck": 1, "the_sky_is_the_limit": 2 }
        s = StrCase(data)
        assert s.convert_case(replace_for='key') == expect

    def test_strcase_case19(self):
        data = ["Good luck", "The sky is the limit",
                {1: "Good luck", 2: "The sky is the limit" } ]
        expect = ["good_luck", "the_sky_is_the_limit",
                {1: "good_luck", 2: "the_sky_is_the_limit" } ]
        s = StrCase(data)
        assert s.convert_case() == expect

    def test_strcase_case20(self):
        data = ["Good luck", None,
                {1: "Good luck", 2: None } ]
        expect = ["good_luck", None,
                {1: "good_luck", 2: None } ]
        s = StrCase(data)
        assert s.convert_case() == expect

    def test_strcase_case21(self):
        data = "Hello"
        expect = "Hello Python"
        s = StrCase(data)
        assert s.origin + " Python" == expect

    def test_strcase_case22(self):
        data = ["Hello"]
        expect = ["Hello", "Python"]
        s = StrCase(data)
        assert s.origin + ["Python"] == expect

    def test_strcase_case23(self):
        expect = {'case': 'sample',
                 'snake': 'convert_case',
                 'kebab': 'convert-case',
                 'camel': 'convertCase',
                 'pascal': 'ConvertCase',
                 'const': 'CONVERT_CASE',
                 'sentence': 'Convert case',
                 'title': 'Convert Case',
                 'lower': 'convert case',
                 'upper': 'CONVERT CASE'}
        s = StrCase()
        result = s.show_supported_case()
        assert result == expect

    def test_strcase_case24(self):
        data = 'convert case'
        expect = { 'snake': 'convert_case',
                 'kebab': 'convert-case',
                 'camel': 'convertCase',
                 'pascal': 'ConvertCase',
                 'const': 'CONVERT_CASE',
                 'sentence': 'Convert case',
                 'title': 'Convert Case',
                 'lower': 'convert case',
                 'upper': 'CONVERT CASE'}
        s = StrCase()
        for case in expect.keys():
            result = s.convert_case(case, data)
            assert result == expect[case]

    def test_strcase_case25(self):
        data = ['convert case', 'Convert Case']
        expect = { 'snake': ['convert_case','convert_case'],
                   'kebab': ['convert-case','convert-case'],
                   'camel': ['convertCase','convertCase'],
                   'pascal': ['ConvertCase','ConvertCase'],
                   'const': ['CONVERT_CASE','CONVERT_CASE'],
                   'sentence': ['Convert case','Convert case'],
                   'title': ['Convert Case','Convert Case'],
                   'lower': ['convert case','convert case'],
                   'upper': ['CONVERT CASE', 'CONVERT CASE']}
        s = StrCase()
        for case in expect.keys():
            result = s.convert_case(case, data)
            print(case)
            assert result == expect[case]

    def test_strcase_case26(self):
        data = {1: 'convert case', 2: 'Convert Case' }
        expect = { 'snake': {1: 'convert_case', 2: 'convert_case'},
                   'kebab': {1: 'convert-case', 2: 'convert-case'},
                   'camel': {1: 'convertCase', 2: 'convertCase'},
                   'pascal': {1: 'ConvertCase', 2: 'ConvertCase'},
                   'const': {1: 'CONVERT_CASE', 2: 'CONVERT_CASE'},
                   'sentence': {1: 'Convert case', 2: 'Convert case'},
                   'title': {1: 'Convert Case', 2: 'Convert Case'},
                   'lower': {1: 'convert case', 2: 'convert case'},
                   'upper': {1: 'CONVERT CASE', 2: 'CONVERT CASE'} }
        s = StrCase()
        for case in expect.keys():
            result = s.convert_case(case, data)
            print(case)
            assert result == expect[case]

    def test_strcase_case27(self):
        data = ['', None, np.nan, pd.NA]
        expect = { 'snake': ['', None, np.nan, pd.NA],
                   'kebab': ['', None, np.nan, pd.NA],
                   'camel': ['', None, np.nan, pd.NA],
                   'pascal': ['', None, np.nan, pd.NA],
                   'const': ['', None, np.nan, pd.NA],
                   'sentence': ['', None, np.nan, pd.NA],
                   'title': ['', None, np.nan, pd.NA],
                   'lower': ['', None, np.nan, pd.NA],
                   'upper': ['', None, np.nan, pd.NA]}
        s = StrCase()
        for case in expect.keys():
            result = s.convert_case(case, data)
            assert result == expect[case]

    def test_strcase_case28(self):
        data = [10, 10.0, ['convert case'],
                ('convert case'), {'test': "convert case" } ]
        expect = { 'snake': [10, 10.0,
             ['convert_case'], ('convert_case'), {'test': "convert_case" }],
                 'kebab': [10, 10.0,
             ['convert-case'], ('convert-case'), {'test': "convert-case" }],
                 'camel': [10, 10.0,
             ['convertCase'], ('convertCase'), {'test': "convertCase" }],
                 'pascal': [10, 10.0,
             ['ConvertCase'], ('ConvertCase'), {'test': "ConvertCase" }],
                 'const': [10, 10.0,
             ['CONVERT_CASE'], ('CONVERT_CASE'), {'test': "CONVERT_CASE" }],
                 'sentence': [10, 10.0,
             ['Convert case'], ('Convert case'), {'test': "Convert case" }],
                 'title': [10, 10.0,
             ['Convert Case'], ('Convert Case'), {'test': "Convert Case" }],
                 'lower': [10, 10.0,
             ['convert case'], ('convert case'), {'test': "convert case" }],
                 'upper': [10, 10.0,
             ['CONVERT CASE'], ('CONVERT CASE'), {'test': "CONVERT CASE" }] }
        s = StrCase()

        for case in expect.keys():
            result = s.convert_case(case, data)
            assert result == expect[case]

