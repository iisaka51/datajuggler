from enum import Enum
from typing import (
    Any, Dict, Union, Optional, Hashable, Iterable,
    Callable, Pattern, Match, Literal, get_args
)
from collections import OrderedDict
from collections.abc import (
    Mapping, KeysView, ValuesView, ItemsView, Sequence
)

import re
from datetime import datetime
from decimal import Decimal
from datajuggler.keys import Keylist, Keypath

try:
    from emoji import is_emoji
except ImportError:
    def is_emoji(s: str):
        raise NotImplementedError('You should install emoji.')

class DictKey(str, Enum):
    KEYLIST = "keylist"
    KEYPATH = "keypath"

DictKeyType = Literal[DictKey.KEYLIST, DictKey.KEYPATH]

class DictItem(str, Enum):
    KEY = "key"
    VALUE = "value"

DictItemType = Literal[DictItem.KEY, DictItem.VALUE]

class DictAction(str, Enum):
    SET = "set"
    GET = "get"
    DEL = "del"
    POP = "pop"

DictActionType = Literal[
    DictAction.SET,
    DictAction.GET,
    DictAction.DEL,
    DictAction.POP,
]

def validate_DictKey(
        dictkey: DictKeyType,
        *,
        thrown_error: bool=False,
    ) ->Optional[bool]:
    if dictkey in get_args(DictKeyType):
        return True
    else:
        if not thrown_error:
            return False
        else:
            available_args = [x.value for x in get_args(DictKeyType)]
            raise ValueError(f"DictKey must be '{available_args}'.")

def validate_DictItem(
        dictitem: DictItemType,
        *,
        thrown_error: bool=False,
    ) ->Optional[bool]:
    if dictitem in get_args(DictItemType):
        return True
    else:
        if not thrown_error:
            return False
        else:
            available_args = [x.value for x in get_args(DictItemType)]
            raise ValueError(f"DictItem must be '{available_args}'.")

def validate_DictAction(
        dictaction: DictActionType,
        *,
        thrown_error: bool=False,
    ) ->Optional[bool]:
    if dictaction in get_args(DictActionType):
        return True
    else:
        if not thrown_error:
            return False
        else:
            available_args = [x.value for x in get_args(DictActionType)]
            raise ValueError(f"DictAction must be '{available_args}'.")


class TypeValidator(object):
    regex = re.compile("").__class__
    re_uuid = re.compile(
        "^([0-9a-f]{32}){1}$|^([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}){1}$",
        flags=re.IGNORECASE,
    )
    re_financial_number = re.compile(r"(?=\d+,\d+).*")


    @classmethod
    def is_bool(cls, obj: Any):
        return isinstance(obj, type(True))

    @classmethod
    def is_collection(cls, obj: Any):
        return isinstance(obj, (dict, set, list, tuple))

    @classmethod
    def is_callable(cls, obj: Any):
        return isinstance(obj, Callable)

    @classmethod
    def is_datetime(cls, obj: Any):
        return isinstance(obj, datetime)

    @classmethod
    def is_decimal(cls, obj: Any):
        return isinstance(obj, Decimal)

    @classmethod
    def is_dict(cls, obj: Any):
        return isinstance(obj, dict)

    @classmethod
    def is_dict_or_other(cls, obj: Any, other: Any):
        return isinstance(obj, (dict, type(other)))

    @classmethod
    def is_dict_and_not_other(cls, obj: Any, other: Any):
        return ( isinstance(obj, dict)
                 and not isinstance(obj, type(other)))

    @classmethod
    def is_dict_keys(cls, obj: Any):
        return isinstance(obj, KeysView)

    @classmethod
    def is_dict_values(cls, obj: Any):
        return isinstance(obj, ValuesView)

    @classmethod
    def is_dict_items(cls, obj: Any):
        return isinstance(obj, ItemsView)

    @classmethod
    def is_dict_or_list(cls, obj: Any):
        return isinstance(obj, (dict, list))

    @classmethod
    def is_dict_or_list_or_tuple(cls, obj: Any):
        return isinstance(obj, (dict, list, tuple))

    @classmethod
    def is_float(cls, obj: Any):
        return isinstance(obj, float)

    @classmethod
    def is_function(cls, obj: Any):
        return callable(obj)

    @classmethod
    def is_hashable(cls, obj: Any):
        return isinstance(obj, Hashable)

    @classmethod
    def is_integer(cls, obj: Any):
        return isinstance(obj, int)

    def is_integer_or_float(cls, obj: Any):
        return isinstance(obj, (int, float))

    @classmethod
    def is_iterable(cls, obj: Any):
        return isinstance(obj, Iterable)

    @classmethod
    def is_json_serializable(cls, obj: Any):
        json_types = (type(None), bool, dict, float, int, list, str, tuple)
        return isinstance(obj, json_types)

    @classmethod
    def is_keylist(cls, obj: Any):
        return isinstance(obj, Keylist)

    @classmethod
    def is_keypath(cls, obj: Any):
        return isinstance(obj, Keypath)

    @classmethod
    def is_keylist_or_keypath(cls, obj: Any):
        return isinstance(obj, (Keylist, Keypath))

    @classmethod
    def is_list(cls, obj: Any):
        return isinstance(obj, list)

    @classmethod
    def is_list_not_empty(cls, obj: Any):
        return obj and isinstance(obj, list)

    @classmethod
    def is_list_or_tuple(cls, obj: Any):
        return isinstance(obj, (list, tuple))

    @classmethod
    def is_list_of_keylists(cls, obj: Any):
        return ( isinstance(obj, list)
                 and len(obj) >= 1
                 and all(map(lambda x: isinstance(x, Keylist), obj)) )

    @classmethod
    def is_list_of_keypaths(cls, obj: Any):
        return ( isinstance(obj, list)
                 and len(obj) >= 1
                 and all(map(lambda x: isinstance(x, Keypath), obj)) )
    @classmethod
    def is_list_of_ordereddict(cls, obj: Any):
        return ( isinstance(obj, list)
                 and len(obj) >= 1
                 and all(map(lambda x: isinstance(x, OrderedDict), obj)) )

    @classmethod
    def is_mapping(cls, obj: Any):
        return isinstance(obj, Mapping)

    @classmethod
    def is_match(cls, obj: Any):
        return isinstance(obj, Match)

    @classmethod
    def is_none(cls, obj: Any):
        return obj is None

    @classmethod
    def is_not_none(cls, obj: Any):
        return obj is not None

    @classmethod
    def is_pattern(cls, obj: Any):
        return isinstance(obj, Pattern)

    @classmethod
    def is_regex(cls, obj: Any):
        return isinstance(obj, cls.regex)

    @classmethod
    def is_same_as(cls, obj: Any, other: Any):
        return isinstance(obj, type(other))

    @classmethod
    def is_sequence(cls, obj: Any):
        return isinstance(obj, Sequence)

    @classmethod
    def is_set(cls, obj: Any):
        return isinstance(obj, set)

    @classmethod
    def is_set_not_empty(cls, obj: Any):
        return obj and isinstance(obj, set)

    @classmethod
    def is_slice(cls, obj: Any):
        return isinstance(obj, slice)

    @classmethod
    def is_str(cls, obj: Any):
        return isinstance(obj, str)

    @classmethod
    def is_str_not_empty(cls, obj: Any):
        return obj and isinstance(obj, str)

    @classmethod
    def is_tuple(cls, obj: Any):
        return isinstance(obj, tuple)

    @classmethod
    def is_tuple_not_empty(cls, obj: Any):
        return obj and isinstance(obj, tuple)

    @classmethod
    def is_uuid(cls, obj: Any):
        return obj and isinstance(obj, str) and cls.re_uuid.match(obj)

    @classmethod
    def is_str_alnum(cls, obj: Any):
        def is_alnum(obj):
            try:
                return isinstance(obj, str) and obj.encode('ascii').isalnum()
            except:
                False
        return True if is_alnum(obj) else False

    @classmethod
    def is_str_alpha(cls, obj: Any):
        def is_alpha(obj):
            try:
                return isinstance(obj, str) and obj.encode('ascii').isalpha()
            except:
                False
        return True if is_alpha(obj) else False

    @classmethod
    def is_str_financial_number(cls, obj: Any):
        return obj and isinstance(obj, str) and cls.re_financial_number.match(obj)

    @classmethod
    def is_str_emoji(cls, obj: Any):
        return obj and isinstance(obj, str) and is_emoji(obj)

