# -*- coding: utf-8 -*-

# import codecs, sys
#
# sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
# sys.stdin = codecs.getreader('utf_8')(sys.stdin)

import re
import hashlib
import uuid

from datetime import datetime
from collections import OrderedDict, namedtuple
from dataclasses import dataclass
from typing import NamedTuple
import pytest


from datajuggler import Keylist, Keypath
from datajuggler.validator import TypeValidator as _type
from datajuggler.validator import ValueValidator as _value
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

    def test_type_is_uuid(self):
        data = uuid.uuid4()
        assert _type.is_uuid(data) == True
        assert _type.is_uuid('datajuggler') == False

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


    def test_is_made_by_dataclass(self):
        @dataclass
        class User(object):
            id: int
            name: str
        u1 = User(1, "jack")
        assert  _type.is_made_by_dataclass(u1) == True


    def test_is_made_by_namedtuple_case01(self):
        User = namedtuple("user", "id name")
        u1 = User(1, "jack")
        assert  _type.is_made_by_namedtuple(u1) == True

    def test_is_made_by_namedtuple_case02(self):
        class User(NamedTuple):
            id: int
            name: str
        u1 = User(1, "jack")
        assert  _type.is_made_by_namedtuple(u1) == True


    def test_is_made_by_typing_namedtuple_case01(self):
        User = namedtuple("user", "id name")
        u1 = User(1, "jack")
        assert  _type.is_made_by_typing_namedtuple(u1) == False


    def test_is_made_by_typing_namedtuple_case01(self):
        class User(NamedTuple):
            id: int
            name: str
        u1 = User(1, "jack")
        assert  _type.is_made_by_typing_namedtuple(u1) == True

    def test_is_made_by_collections_namedtuple(self):
        User = namedtuple("user", "id name")
        u1 = User(1, "jack")
        assert  _type.is_made_by_collections_namedtuple(u1) == True


    def test_is_made_by_typing_namedtuple_case01(self):
        class User(NamedTuple):
            id: int
            name: str
        u1 = User(1, "jack")
        assert  _type.is_made_by_collections_namedtuple(u1) == False


    def test_is_made_by_pydantic(self):
        pass

    def test_is_md5(self):
        data = 'datajuggler'
        hash_str = hashlib.md5(data.encode()).hexdigest()
        assert _value.is_md5(hash_str) == True
        assert _value.is_md5(data) == False

    def test_is_sha1(self):
        data = 'datajuggler'
        hash_str = hashlib.sha1(data.encode()).hexdigest()
        assert _value.is_sha1(hash_str) == True
        assert _value.is_sha1(data) == False

    def test_is_sha224(self):
        data = 'datajuggler'
        hash_str = hashlib.sha224(data.encode()).hexdigest()
        assert _value.is_sha224(hash_str) == True
        assert _value.is_sha224(data) == False

    def test_is_sha256(self):
        data = 'datajuggler'
        hash_str = hashlib.sha256(data.encode()).hexdigest()
        assert _value.is_sha256(hash_str) == True

    def test_is_sha512(self):
        data = 'datajuggler'
        hash_str = hashlib.sha512(data.encode()).hexdigest()
        assert _value.is_sha512(hash_str) == True
        assert _value.is_sha512(data) == False

    def test_is_between(self):
        assert _value.is_between(10, 2, 10) == True
        assert _value.is_between(10, 2, 20) == True
        assert _value.is_between(10, None, 20) == True
        assert _value.is_between(10, None, None) == False
        assert _value.is_between(10, 1, None) == True
        assert _value.is_between(10, -1, None) == True
        assert _value.is_between(10, 10, None) == True

    def test_is_length_case01(self):
        data = 'datajuggler'
        assert _value.is_length(data, 2, 10) == False
        assert _value.is_length(data, 2, 11) == True
        assert _value.is_length(data, None, 11) == True
        assert _value.is_length(data, None, None) == False
        assert _value.is_length(data, 1, None) == True
        assert _value.is_length(data, -1, None) == False
        assert _value.is_length(data, 11, None) == True

    def test_is_length_case02(self):
        data = list([1,2,3,4,5,6,7,8,9,10,11])
        assert _value.is_length(data, 2, 10) == False
        assert _value.is_length(data, 2, 11) == True
        assert _value.is_length(data, None, 11) == True
        assert _value.is_length(data, None, None) == False
        assert _value.is_length(data, 1, None) == True
        assert _value.is_length(data, -1, None) == False
        assert _value.is_length(data, 11, None) == True

    def test_is_length_case03(self):
        data = range(11)
        assert _value.is_length(data, 2, 10) == False
        assert _value.is_length(data, 2, 11) == True
        assert _value.is_length(data, None, 11) == True
        assert _value.is_length(data, None, None) == False
        assert _value.is_length(data, 1, None) == True
        assert _value.is_length(data, -1, None) == False
        assert _value.is_length(data, 11, None) == True

    def test_value_is_uuid(self):
        data = uuid.uuid4()
        assert _value.is_uuid(data) == True
        assert _value.is_uuid('datajuggler') == False

    def test_value_is_financial_number(self):
        assert _value.is_financial_number('1') == True
        assert _value.is_financial_number('12') == True
        assert _value.is_financial_number('123') == True
        assert _value.is_financial_number('1,234') == True
        assert _value.is_financial_number('-1,234') == True
        assert _value.is_financial_number('-1234') == True
        assert _value.is_financial_number('+1234') == True
        assert _value.is_financial_number('0.12') == True
        assert _value.is_financial_number('.12') == True
        assert _value.is_financial_number('12.') == True

    def test_value_is_valid_checkdigit_case01(self):
        assert _value.is_valid_checkdigit(261009) == True
        assert _value.is_valid_checkdigit(261008) == False
        assert _value.is_valid_checkdigit(26100, 5) == True
        assert _value.is_valid_checkdigit(1100, 5) == True

    def test_value_is_valid_checkdigit_case02(self):
        assert _value.is_valid_checkdigit('261009') == True
        assert _value.is_valid_checkdigit('261008') == False
        assert _value.is_valid_checkdigit('26100', 5) == True
        assert _value.is_valid_checkdigit('1100', 5) == True

    def test_value_is_valid_checkdigit_case03(self):
        assert _value.is_valid_checkdigit(261009,
                                  weights=[6,5,4,3,2]) == True
        assert _value.is_valid_checkdigit('261009',
                                  weights=[6,5,4,3,2]) == True

    def test_value_is_truthy(self):
        assert _value.is_truthy(' ') == False
        assert _value.is_truthy('datajuggler') == True
        assert _value.is_truthy(1) == True
        assert _value.is_truthy(0.2) == True
        assert _value.is_truthy(-1) == True
        assert _value.is_truthy(None) == False
        assert _value.is_truthy(list()) == False
        assert _value.is_truthy(dict()) == False
        assert _value.is_truthy(dict(a=2)) == True
        assert _value.is_truthy(list([1,2,3])) == True

    def test_type_is_truthy(self):
        assert _type.is_truthy(' ') == False
        assert _type.is_truthy('datajuggler') == True
        assert _type.is_truthy(1) == True
        assert _type.is_truthy(0.2) == True
        assert _type.is_truthy(-1) == True
        assert _type.is_truthy(None) == False
        assert _type.is_truthy(list()) == False
        assert _type.is_truthy(dict()) == False
        assert _type.is_truthy(dict(a=2)) == True
        assert _type.is_truthy(list([1,2,3])) == True
