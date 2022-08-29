import sys
import time
import pytest

sys.path.insert(0,"../datajuggler")

from datajuggler import (
    is_alpha, is_alnum, omit_values, replace_values,
    add_df, df_compare, change_dict_keys,
    split_chunks, urange, rename_duplicates,
)
import pandas as pd

class TestClass:
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

