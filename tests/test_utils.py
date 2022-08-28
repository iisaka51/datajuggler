import sys
import time
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import (
    StrCase, is_alpha, is_alnum, omit_values, replace_values,
    add_df, df_compare, change_dict_keys, uDict, iDict, aDict,
    split_chunks, urange, rename_duplicates,
)
from pprint import pprint
from pathlib import Path
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

    def test_show_supported_case(self):
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

    def test_conver_case_str(self):
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
        result = s.convert_case(data=data)
        assert result == expect['snake']
        for case in expect.keys():
            result = s.convert_case(case, data)
            assert result == expect[case]

    def test_conver_case_list(self):
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

    def test_conver_case_dict(self):
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

    def test_conver_case_nullval(self):
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

    def test_conver_case_nest(self):
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

    def test_is_alpha_alphabet(self):
        assert ( is_alpha('iisaka')
                 == True )

    def test_is_alpha_alphabet_with_number(self):
        assert ( is_alpha('iisaka51')
                 == False )

    def test_is_alpha_alphabet_with_symbol(self):
        assert ( is_alpha('@iisaka51')
                 == is_alpha('Goichi (iisaka) Yukawa')
                 == False )

    def test_is_alpha_kanji(self):
        assert ( is_alpha('京都市')
                 == False )

    def test_is_alpha_kanji_num(self):
        assert ( is_alpha('１２３')
                 == False )

    def test_is_alnum_alphabet(self):
        assert ( is_alnum('iisaka')
                 == True )

    def test_is_alnum_alphabet_with_number(self):
        assert ( is_alnum('iisaka51')
                 == True )

    def test_is_alnum_alphabet_with_symbol(self):
        assert ( is_alnum('@iisaka51')
                 == is_alnum('Goichi (iisaka) Yukawa')
                 == False )

    def test_is_alnum_kanji(self):
        assert ( is_alnum('京都市')
                 == False )

    def test_is_alnum_kanji_num(self):
        assert ( is_alpha('１２３')
                 == False )

    def test_df_compare(self):
        d1 = pd.DataFrame([ ['Kyoto', 35.0117,135.452],
                            ['Osaka', 34.4138,135.3808]],
                          columns=['cityName', 'latitude', 'longitude'])
        d2 = pd.DataFrame([ ['Kyoto', 35.0117,135.452],
                            ['Osaka', 34.4138,135.3808]],
                          columns=['cityName', 'latitude', 'longitude'])
        assert ( df_compare(d1, d2) == 0 )

    def test_df_compare_diff_count_non_zero(self):
        d1 = pd.DataFrame([ ['26100', 35.0117,135.452],
                            ['27100', 34.4138,135.3808]],
                          columns=['cityCode', 'latitude', 'longitude'])
        d2 = pd.DataFrame([ ['Kyoto', 35.0117,135.452],
                            ['Osaka', 34.4138,135.3808]],
                          columns=['cityName', 'latitude', 'longitude'])
        assert ( df_compare(d1, d2) != 0 )

    def test_omit_values(self):
        data = ['January', 'February', 'March', 'April' ]
        omits = ['February', 'April']
        expect = ['January', '', 'March', '' ]
        result = omit_values(data, omits)
        assert result == expect

    def test_omit_values_ignore_case(self):
        data = ['January', 'February', 'March', 'April' ]
        omits = ['february', 'april']
        expect = ['January', '', 'March', '' ]
        result = omit_values(data, omits, ignore_case=True)
        assert result == expect

    def test_omit_values_with_drop(self):
        data = ['January', 'February', 'March', 'April' ]
        omits = ['February', 'April']
        expect = ['January', 'March' ]
        result = omit_values(data, omits, drop=True)
        assert result == expect

    def test_omit_values_asstr(self):
        data = "JanuaryFebruaryMarchApril"
        omits = ['February', 'April']
        expect = "JanuaryMarch"
        result = omit_values(data, omits)
        assert result == expect

    def test_replace_values_list(self):
        data = ['January', 'February', 'March', 'April' ]
        replace = { 'February': 'february', 'April': 'april' }
        expect = ['January', 'february', 'March', 'april' ]
        result = replace_values( data, replace)
        assert result == expect

    def convert_func(self, matchobj):
        map = {'January': '1',
               'February': '2' }
        return map[matchobj.group(0)]

    def test_replace_values_with_regexp(self):
        data = ['January', 'February', 'March', 'April',
                'May', 'June', 'July', 'August',
                'September', 'October', 'November', 'December']

        replace = { '.*ary': self.convert_func, '.*ber': 'BER' }

        expect = ['1', '2', 'March', 'April',
                'May', 'June', 'July', 'August',
                'BER', 'BER', 'BER', 'BER']
        result = replace_values( data, replace)
        assert result == expect

    def test_replace_values_ignore_case(self):
        data = ['January', 'February', 'March', 'April',
                'May', 'June', 'July', 'August',
                'September', 'October', 'November', 'December']

        replace = {'april': '4', 'september': '9' }

        expect = ['January', 'February', 'March', '4',
                'May', 'June', 'July', 'August',
                '9', 'October', 'November', 'December']
        result = replace_values( data, replace, ignore_case=True)
        assert result == expect

    def test_replace_values_list_inplace(self):
        data = ['January', 'February', 'March', 'April',
                'May', 'June', 'July', 'August',
                'September', 'October', 'November', 'December']

        replace = {'April': 'april', 'September': 'september' }

        expect = ['January', 'February', 'March', 'april',
                  'May', 'June', 'July', 'August',
                  'september', 'October', 'November', 'December']
        replace_values( data, replace, inplace=True)
        assert data == expect

    def test_replace_values_dict_val_default(self):
        data = { 1: 'January', 2: 'February', 3: 'March', 4: 'April',
                 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'September', 10: 'October', 11: 'November', 12: 'December'}

        replace = {'April': 'april', 'September': 'september' }

        expect = { 1: 'January', 2: 'February', 3: 'March', 4: 'april',
                 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'september', 10: 'October', 11: 'November', 12: 'December'}

        result = replace_values( data, replace )
        assert result == expect

    def test_replace_values_dict_val_explicit(self):
        data = { 1: 'January', 2: 'February', 3: 'March', 4: 'April',
                 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'September', 10: 'October', 11: 'November', 12: 'December'}

        replace = {'April': 'april', 'September': 'september' }

        expect = { 1: 'January', 2: 'February', 3: 'March', 4: 'april',
                 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'september', 10: 'October', 11: 'November', 12: 'December'}

        result = replace_values( data, replace, replace_for='value' )
        assert result == expect

    def test_replace_values_dict_val_ignore_case(self):
        data = { 1: 'January', 2: 'February', 3: 'March', 4: 'April',
                 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'September', 10: 'October', 11: 'November', 12: 'December'}

        replace = {'APRIL': 'april', 'SEPTEMBER': 'september' }

        expect = { 1: 'January', 2: 'February', 3: 'March', 4: 'april',
                 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'september', 10: 'October', 11: 'November', 12: 'December'}

        result = replace_values( data, replace, ignore_case=True )
        assert result == expect

    def test_replace_values_dict_inplace(self):
        data = { 1: 'January', 2: 'February', 3: 'March', 4: 'April',
                 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

        replace = {'April': 'april', 'September': 'september' }

        expect = { 1: 'January', 2: 'February', 3: 'March', 4: 'april',
                 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                 9: 'september', 10: 'October', 11: 'November', 12: 'December'}

        replace_values( data, replace, inplace=True )
        assert data == expect

    def test_replace_values_dict_keys(self):
        data = { 1: 'one', 2: 'two', 3: 'three', 4: 'four' }

        replace = {1: 'one',  2: 'two', 3: 'three'}

        expect = { 'one': 'one', 'two': 'two', 'three': 'three', 4: 'four' }

        result = replace_values( data, replace, replace_for='key')
        assert result == expect

    def test_replace_values_dict_val_obj(self):
        data = { 1: 'one', 2: 'two', 3: 'three', 4: 'four' }

        replace = {'one': 1, 'two': [2, 'two'], 'three': { 3: 'three'}}

        expect = { 1: 1, 2: [2, 'two'] , 3: {3: 'three'}, 4: 'four' }

        result = replace_values( data, replace )
        assert result == expect


    def test_change_dict_keys_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4,
                 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        replace = {'April': 4, 'September': 9 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 4: 4,
                   'May': 5, 'June': 6, 'July': 7, 'August': 8,
                 9: 9, 'October': 10, 'November': 11, 'December': 12}
        result = change_dict_keys(data, replace)
        assert result == expect

    def test_change_dict_keys_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4,
                 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        replace = {'April': 4, 'September': 9 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 4: 4,
                   'May': 5, 'June': 6, 'July': 7, 'August': 8,
                 9: 9, 'October': 10, 'November': 11, 'December': 12}
        change_dict_keys(data, replace, inplace=True)
        assert data == expect

    def test_change_dict_keys_case03(self):
        data = { 1: 'January', 2: 'February', 3: 'March', 4: 'April',
                 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        replace = {4: 'Apr', 7: 'Jul' }
        expect = { 1: 'January', 2: 'February', 3: 'March', 'Apr': 'April',
                 5: 'May', 6: 'June', 'Jul': 'July', 8: 'August',
                 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        result = change_dict_keys(data, replace)
        assert result == expect

    def test_change_dict_keys_case04(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4,
                 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4,
                   'May': 5, 'June': 6, 'July': 7, 'August': 8,
                 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        result = change_dict_keys(data, 'April', 'Apr')
        assert result == expect

    def test_change_dict_keys_case05(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4,
                 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4,
                   'May': 5, 'June': 6, 'July': 7, 'August': 8,
                 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        change_dict_keys(data, 'April', 'Apr', inplace=True)
        assert data == expect

    def test_adict_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        result = aDict(data)
        assert result == data

    def test_adict_case02(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = 2
        result = aDict(data)
        assert result.February == expect

    def test_adict_case03(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = 4
        result = aDict(data)
        assert result.one.two.three.four == expect

    def test_adict_case04(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = "{'one': {'two': {'three': {'four': 4}}}}"
        result = aDict(data)
        assert result.__str__() == expect

    def test_adict_case05(self):
        data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
        expect = "aDict({'one': aDict({'two': aDict({'three': aDict({'four': 4})})})})"
        result = aDict(data)
        assert result.__repr__() == expect

    def test_udict_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        result = uDict(data)
        assert result == data

    def test_udict_case02(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        assert data == expect

    def test_udict_case03(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4 }
        saved = data.copy()
        result = data.replace_key('April', 'Apr')
        assert ( result == expect
                 and data == saved )

    def test_udict_case04(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        replace = {'January': 'Jan', 'February': 'Feb' }
        expect = { 'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4 }
        saved = data.copy()
        result = data.replace_key_map(replace)
        assert ( result == expect
                 and data == saved )

    def test_udict_case05(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        replace = {'January': 'Jan', 'February': 'Feb' }
        expect = { 'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4 }
        saved = data.copy()
        data.replace_key_map(replace, inplace=True)
        assert ( data == expect
                 and data != saved )

    def test_udict_case06(self):
        data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(TypeError) as e:
            result = dict({data: 1})
        assert str(e.value) == "unhashable type: 'uDict'"

    def test_udict_case07(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = uDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})
        result = uDict().fromvalues(data)
        assert result == expect

    def test_udict_case08(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = uDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})
        result = uDict().fromvalues(data, base=0)
        assert result == expect

    def test_udict_case09(self):
        keys = [ 1, 2, 3, 4 ]
        values = [ 'January', 'February', 'March', 'April' ]
        expect = uDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})
        result = uDict().fromlists(keys, values)
        assert result == expect

    def test_udict_case10(self):
        values = [ 'January', 'February', 'March', 'April' ]
        keys = range(1, len(values)+1)
        expect = uDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})
        result = uDict().fromlists(keys, values)
        assert result == expect

    def test_udict_case11(self):
        keys = [ 1, 2, ]
        values = [ 'January', 'February', 'March', 'April' ]
        expect = uDict({1: 'January', 2: 'February' })
        result = uDict().fromlists(keys, values)
        assert result == expect

    def test_udict_case12(self):
        keys = [ 1, 2, 3, 4 ]
        values = [ 'January', 'February' ]
        expect = uDict({1: 'January', 2: 'February' })
        result = uDict().fromlists(keys, values)
        assert result == expect

    def test_udict_case13(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
        result = uDict(data)
        assert result.__str__() == expect

    def test_udict_case14(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        result = uDict(data)
        assert result.__repr__() == expect

    def test_idict_case01(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        result = iDict(data)
        assert result == data

    def test_idict_case02(self):
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        result = iDict(January=1, February=2, March=3, April=4)
        assert result == expect

    def test_idict_case03(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        assert data == expect

    def test_idict_case04(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(TypeError) as e:
            data['January'] = 'Jan'
        assert str(e.value) == 'iDict object does not support item assignment'

    def test_idict_case05(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(AttributeError) as e:
            result  = data.pop(0)
        assert str(e.value) == 'iDict object has no attribute pop'

    def test_idict_case06(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(AttributeError) as e:
            data.clear()
        assert str(e.value) == 'iDict object has no attribute clear'

    def test_idict_case07(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(AttributeError) as e:
            data.update({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        assert str(e.value) == 'iDict object has no attribute update'

    def test_idict_case08(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        with pytest.raises(AttributeError) as e:
            data.setdefault('March', 3)
        assert str(e.value) == 'iDict object has no attribute setdefault'

    def test_idict_case09(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        assert hasattr(data, '__hash__') == True

    def test_idict_case10(self):
        data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
        result = dict({data: 1})
        assert  result[data]  == 1

    def test_idict_case11(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = iDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})
        result = iDict().fromvalues(data)
        assert result == expect

    def test_idict_case12(self):
        data = [ 'January', 'February', 'March', 'April' ]
        expect = iDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})
        result = iDict().fromvalues(data, base=0)
        assert result == expect

    def test_idict_case13(self):
        keys = [ 1, 2, 3, 4 ]
        values = [ 'January', 'February', 'March', 'April' ]
        expect = iDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})
        result = iDict().fromlists(keys, values)
        assert result == expect

    def test_idict_case14(self):
        values = [ 'January', 'February', 'March', 'April' ]
        keys = range(1, len(values)+1)
        expect = iDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})
        result = iDict().fromlists(keys, values)
        assert result == expect

    def test_idict_case15(self):
        keys = [ 1, 2, ]
        values = [ 'January', 'February', 'March', 'April' ]
        expect = iDict({1: 'January', 2: 'February' })
        result = iDict().fromlists(keys, values)
        assert result == expect

    def test_idict_case16(self):
        keys = [ 1, 2, 3, 4 ]
        values = [ 'January', 'February' ]
        expect = iDict({1: 'January', 2: 'February' })
        result = iDict().fromlists(keys, values)
        assert result == expect

    def test_idict_case17(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
        result = iDict(data)
        assert result.__str__() == expect

    def test_idict_case18(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = "iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
        result = iDict(data)
        assert result.__repr__() == expect

    def test_split_chunks_case01(self):
        data = [11,12,13,21,22,23,31,32,33]
        expect = [[11,12,13], [21,22,23], [31,32,33]]
        result = list(split_chunks(data,3))
        assert result == expect

    def test_split_chunks_case02(self):
        data = [11,12,13,14, 21,22,23,31,32,33]
        expect = [[11,12,13, 14], [21,22,23,31], [32,33, None, None ]]
        result = list(split_chunks(data,4))
        assert result == expect

    def test_split_chunks_case03(self):
        data = [11,12,13,14, 21,22,23,31,32,33]
        expect = [[11,12,13, 14], [21,22,23,31], [32,33, None, None ]]
        result = list(split_chunks(data,4))
        assert result == expect

    def test_split_chunks_case04(self):
        data = [11,12,13,14, 21,22,23,31,32,33]
        expect = [[11,12,13, 14], [21,22,23,31], [32,33] ]
        result = list(split_chunks(data,4, fill_na=False))
        assert result == expect

    def test_split_chunks_case05(self):
        data = [11,12,13,14, 21,22,23,31,32,33]
        expect = [[11,12,13, 14], [21,22,23,31], [32,33, -1, -1] ]
        result = list(split_chunks(data,4, na_value=-1))
        assert result == expect

    def test_split_chunks_case06(self):
        data = [11,12,13,14, 21,22,23,31,32,33]
        expect = [[11,12,13, 14], [21,22,23,31], [32,33, 0, 0] ]
        result = list(split_chunks(data,4, na_value=0))
        assert result == expect

    def test_split_chunks_case07(self):
        data = [11,12,13,14, 21,22,23,31,32,33]
        expect = [ [11,12,13,14], [21,22,23,31], [32, 33] ]
        result = list(split_chunks(data,4, fill_na=False, na_value=0))
        assert result == expect

    def test_split_chunks_case08(self):
        data = (11,12,13,21,22,23,31,32,33)
        expect = [(11,12,13), (21,22,23), (31,32,33)]
        result = list(split_chunks(data,3))
        assert result == expect

    def test_split_chunks_case09(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4,
                 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        expect = [{ 'January': 1, 'February': 2, 'March': 3},
                  { 'April': 4, 'May': 5, 'June': 6},
                  { 'July': 7, 'August': 8, 'September': 9},
                  { 'October': 10, 'November': 11, 'December': 12} ]
        result = list(split_chunks(data,3))
        assert result == expect

    def test_split_chunks_case10(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = [{ 'January': 1, 'February': 2, 'March': 3},
                  { 'April': 4 } ]
        result = list(split_chunks(data,3))
        assert result == expect

    def test_split_chunks_case11(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = [{ 'January': 1, 'February': 2, 'March': 3},
                  { 'April': 4 } ]
        result = list(split_chunks(data,3, fill_na=True))
        assert result == expect

    def test_split_chunks_case12(self):
        data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
        expect = [{ 'January': 1, 'February': 2, 'March': 3},
                  { 'April': 4 } ]
        result = list(split_chunks(data,3, na_value=None))
        assert result == expect

    def test_split_chunks_case13(self):
        data = "Peter Piper picked a peck of pickled peppers."
        expect = ["Peter Pipe",
                  "r picked a",
                  " peck of p",
                  "ickled pep",
                  "pers."]
        result = list(split_chunks(data,10))
        assert result == expect

    def test_split_chunks_case14(self):
        data = "Peter Piper picked a peck of pickled peppers."
        expect = [ "Peter Piper picked a",
                   " peck of pickled pep",
                   "pers." ]
        result = list(split_chunks(data,20))
        assert result == expect

    def test_split_chunks_case15(self):
        data = "Peter Piper picked a peck of pickled peppers."
        expect = [ "Peter Piper picked a",
                   " peck of pickled pep",
                   "pers." ]
        result = list(split_chunks(data,20, fill_na=True, na_value=None))
        assert result == expect

    def test_urange_case01(self):
        expect = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = list(urange(10))
        assert result == expect

    def test_urange_case02(self):
        expect = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = list(urange(1, 10))
        assert result == expect

    def test_urange_case03(self):
        expect = [1, 3, 5, 7, 9]
        result = list(urange(1, 10, 2))
        assert result == expect

    def test_urange_case04(self):
        expect = [10, 8, 6, 4, 2]
        result = list(urange(10, 1, -2))
        assert result == expect

    def test_urange_case05(self):
        expect = [10, 9, 8, 7, 6, 5, 4, 3, 2]
        result = list(urange(10, 1))
        assert result == expect

    def test_urange_case06(self):
        expect = [10, 8, 6, 4, 2]
        with pytest.raises(ValueError) as e:
            result = list(urange(10, 1, 1))
        assert ( str(e.value)
                 == "Step must be negative value for descending orders." )

    def test_urange_case07(self):
        expect = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        with pytest.raises(ValueError) as e:
            result = list(urange(1, 10, -1))
        assert ( str(e.value)
                 == "Step must be postitive value for ascending orders." )

    def test_urange_case08(self):
        expect = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = list(urange(end=10))
        assert result == expect

    def test_urange_case09(self):
        expect = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = list(urange(end=10, start=1))
        assert result == expect

    def test_urange_case10(self):
        expect = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = list(urange(end=10, start=1, step=1))
        assert result == expect

    def test_urange_case11(self):
        expect = [10, 8, 6, 4, 2]
        with pytest.raises(ValueError) as e:
            result = list(urange(start=10, end=1, step=1))
        assert ( str(e.value)
                 == "Step must be negative value for descending orders." )

    def test_urange_case12(self):
        expect = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        with pytest.raises(ValueError) as e:
            result = list(urange(start=1, end=10, step=-1))
        assert ( str(e.value)
                 == "Step must be postitive value for ascending orders." )

    def test_urange_case13(self):
        def  gen_step(val):
             return (val * 3)

        expect = [1, 4, 16]
        result = list(urange(1, 20, gen_step))
        assert result == expect

    def test_urange_case14(self):
        def  gen_step(val):
             return (val * 3)

        expect = [1, 4, 16]
        result = list(urange(start=1, end=20, step=gen_step))
        assert result == expect

    def test_urange_case15(self):
        def  gen_step(val):
             return (val * 3)

        expect = [1, 4, 16]
        result = list(urange(1, 20, step=gen_step))
        assert result == expect

    def test_rename_duplicates_case01(self):
        data = ["Apple", "Apple", "Banana", "Maple" ]
        expect = ["Apple", "Apple_01", "Banana", "Maple" ]
        result = rename_duplicates(data)
        assert result == expect

    def test_rename_duplicates_case02(self):
        data = ["Apple", "Apple", "Banana", "Maple" ]
        expect = ["Apple", "Apple__01", "Banana", "Maple" ]
        result = rename_duplicates(data, separator='__')
        assert result == expect

    def test_rename_duplicates_case03(self):
        data = ["Apple", "Apple", "Banana", "Maple" ]
        expect = ["Apple", "Apple_001", "Banana", "Maple" ]
        result = rename_duplicates(data, format="{:03}")
        assert result == expect

    def test_rename_duplicates_case04(self):
        data = ["Apple", ["Apple", "Apple", "Banana", "Maple" ]]
        expect = ["Apple", ["Apple", "Apple_01", "Banana", "Maple" ]]
        result = rename_duplicates(data)
        assert result == expect

    def test_rename_duplicates_case05(self):
        data = ["Apple", ["Apple", "Apple", "Banana", "Maple" ], "Apple"]
        expect = ["Apple", ["Apple", "Apple_01", "Banana", "Maple" ], "Apple_01"]
        result = rename_duplicates(data)
        assert result == expect

    def test_rename_duplicates_case06(self):
        data = ["Apple", {1: "Apple", 2: "Apple", 3: "Banana", 4: "Maple" }]
        expect = ["Apple", {1: "Apple", 2: "Apple", 3: "Banana", 4: "Maple" }]
        result = rename_duplicates(data)
        assert result == expect

