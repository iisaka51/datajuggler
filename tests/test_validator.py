# -*- coding: utf-8 -*-

# import codecs, sys
#
# sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
# sys.stdin = codecs.getreader('utf_8')(sys.stdin)

import re

from datetime import datetime
from collections import OrderedDict
import pytest


from datajuggler import Keylist, Keypath
from datajuggler.validator import TypeValidator as _type
from datajuggler.validator import (
    validate_DictItem, validate_DictAction
)

class TestClass:
    def test_validate_DictItem(self):
        assert validate_DictItem("key") == True
        assert validate_DictItem("value") == True
        assert validate_DictItem("item") == False
        with pytest.raises(ValueError) as e:
            validate_DictItem("item", thrown_error=True)
        assert str(e.value) == "DictItem must be '['key', 'value']'."

    def test_validate_DictAction(self):
        assert validate_DictAction("get") == True
        assert validate_DictAction("set") == True
        assert validate_DictAction("del") == True
        assert validate_DictAction("pop") == True
        assert validate_DictAction("remove") == False
        with pytest.raises(ValueError) as e:
            validate_DictAction("remove", thrown_error=True)
        assert str(e.value) == "DictAction must be '['set', 'get', 'del', 'pop']'."

    def test_is_bool(self):
        assert _type.is_bool(True) == True
        assert _type.is_bool(False) == True
        assert _type.is_bool(1) == False
        assert _type.is_bool(0) == False

    def test_is_collection(self):
        data = dict()
        assert _type.is_collection(data) == True
        data = list()
        assert _type.is_collection(data) == True
        data = set()
        assert _type.is_collection(data) == True
        data = tuple()
        assert _type.is_collection(data) == True

    def test_is_callable(self):
        assert _type.is_callable(sum) == True

    def test_is_datetime(self):
        data = datetime.now()
        assert _type.is_datetime(data) == True

    def test_is_decimal(self):
        pass

    def test_is_dict(self):
        data = dict()
        assert _type.is_dict(data) == True

    def test_is_dict_keys(self):
        data = dict(a=1, b=2, c=3).keys()
        assert _type.is_dict_keys(data) == True

    def test_is_dict_values(self):
        data = dict(a=1, b=2, c=3).values()
        assert _type.is_dict_values(data) == True

    def test_is_dict_items(self):
        data = dict(a=1, b=2, c=3).items()
        assert _type.is_dict_items(data) == True

    def test_is_dict_or_list(self):
        data = list()
        assert _type.is_list(data) == True

    def test_is_dict_or_list_or_tuple(self):
        data = dict()
        assert _type.is_dict_or_list_or_tuple(data) == True
        data = list()
        assert _type.is_dict_or_list_or_tuple(data) == True
        data = tuple()
        assert _type.is_dict_or_list_or_tuple(data) == True
        data = str()
        assert _type.is_dict_or_list_or_tuple(data) == False

    def test_is_float(self):
        data = 3.141592
        assert _type.is_float(data) == True

    def test_is_function(self):
        assert _type.is_function(sum) == True

    def test_is_hashable(self):
        data = str()
        assert _type.is_hashable(data) == True
        data = list()
        assert _type.is_hashable(data) == False

    def test_is_integer(self):
        data = 1
        assert _type.is_integer(data) == True
        data = 3.141592
        assert _type.is_integer(data) == False

    def test_is_iterable(self):
        data = dict(a=1, b=2, c=3).keys()
        assert _type.is_iterable(data) == True

    def test_is_json_serializable(self):
        pass

    def test_is_keylist(self):
        data = Keylist(['a'])
        assert _type.is_keylist(data) == True
        data = list()
        assert _type.is_keylist(data) == False
        data = str()
        assert _type.is_keylist(data) == False

    def test_is_keypath(self):
        data = Keypath('a')
        assert _type.is_keypath(data) == True
        data = Keypath('a.b.c')
        assert _type.is_keypath(data) == True
        data = 'a.b.c'
        assert _type.is_keypath(data) == False
        data = list()
        assert _type.is_keypath(data) == False
        data = str()
        assert _type.is_keypath(data) == False

    def test_is_list(self):
        data = list()
        assert _type.is_list(data) == True
        data = tuple()
        assert _type.is_list(data) == False

    def test_is_list_or_tuple(self):
        data = list()
        assert _type.is_list_or_tuple(data) == True
        data = tuple()
        assert _type.is_list_or_tuple(data) == True
        data = str()
        assert _type.is_list_or_tuple(data) == False

    def test_is_list_of_keylists(self):
        data = [Keylist(['a'])]
        assert _type.is_list_of_keylists(data) == True
        data = Keylist(['a'])
        assert _type.is_list_of_keylists(data) == False
        data = []
        assert _type.is_list_of_keylists(data) == False

    def test_is_list_of_keypaths(self):
        data = [Keypath('a')]
        assert _type.is_list_of_keypaths(data) == True
        data = Keypath('a')
        assert _type.is_list_of_keypaths(data) == False
        data = []
        assert _type.is_list_of_keypaths(data) == False

    def test_is_list_of_ordereddict(self):
        data = [OrderedDict()]
        assert _type.is_list_of_ordereddict(data) == True
        data = OrderedDict()
        assert _type.is_list_of_ordereddict(data) == False
        data = []
        assert _type.is_list_of_ordereddict(data) == False

    def test_is_mapping(self):
        pass

    def test_is_match(self):
        pattern =  re.compile(r'([^01-9]+)?')
        result = re.search(pattern, '1234')
        assert _type.is_match(result) == True

    def test_is_none(self):
        data = None
        assert _type.is_none(data) == True

    def test_is_not_none(self):
        data = True
        assert _type.is_not_none(data) == True

    def test_is_pattern(self):
        pattern =  re.compile(r'([^01-9]+)?')
        assert _type.is_pattern(pattern) == True

    def test_is_regex(self):
        pattern =  re.compile(r'([^01-9]+)?')
        assert _type.is_regex(pattern) == True

    def test_is_same_as(self):
        d1 = dict(a=1,b=2, c=3)
        d2 = dict(a=1,b=2, c=3)
        assert _type.is_same_as(d1, d2) == True

    def test_is_sequence(self):
        pass

    def test_is_str(self):
        data = str()
        assert _type.is_str(data) == True
        data = 2
        assert _type.is_str(data) == False
        data = str()
        assert _type.is_str_not_empty(data) == False
        data = 'python'
        assert _type.is_str_not_empty(data) == True

    def test_is_tuple(self):
        data = tuple()
        assert _type.is_tuple(data) == True
        data = list()
        assert _type.is_tuple(data) == False
        data = tuple()
        assert _type.is_tuple_not_empty(data) == False
        data = (1,2,3)
        assert _type.is_tuple_not_empty(data) == True

    def test_is_uuid(self):
        pass

    def test_is_str_alpha_case01(self):
        assert ( _type.is_str_alpha('iisaka')
                 == True )

    def test_is_str_alpha_case02(self):
        assert ( _type.is_str_alpha('iisaka51')
                 == False )

    def test_is_str_alpha_case03(self):
        assert ( _type.is_str_alpha('@iisaka51')
                 == False )

    def test_is_str_alpha_case04(self):
        assert ( _type.is_str_alpha('Goichi (iisaka) Yukawa')
                 == False )

    def test_is_str_alpha_case05(self):
        assert ( _type.is_str_alpha('京都市')
                 == False )

    def test_is_str_alpha_case06(self):
        assert ( _type.is_str_alpha('１２３')
                 == False )

    def test_is_str_alnum_case01(self):
        assert ( _type.is_str_alnum('iisaka')
                 == True )

    def test_is_str_alnum_case02(self):
        assert ( _type.is_str_alnum('iisaka51')
                 == True )

    def test_is_str_alnum_case03(self):
        assert ( _type.is_str_alnum('@iisaka51')
                 == False )

    def test_is_str_alnum_case04(self):
        assert ( _type.is_str_alnum('Goichi (iisaka) Yukawa')
                 == False )

    def test_is_str_alnum_case05(self):
        assert ( _type.is_str_alnum('京都市')
                 == False )

    def test_is_str_alnum_case06(self):
        assert ( _type.is_str_alnum('１２３')
                 == False )

