from enum import Enum
from typing import (
    Any, Dict, Union, Optional, Hashable, Iterable,
    Callable, Pattern, Match, Literal, get_args
)
from collections import OrderedDict
from collections.abc import (
    Mapping, KeysView, ValuesView, ItemsView, Sequence
)
from functools import total_ordering

import re
import uuid
from datetime import datetime, date, time
from decimal import Decimal
from datajuggler.keys import Keylist, Keypath
from datajuggler.checkdigit import validate_checkdigit
from datajuggler.strings import copy_docstring

try:
    from emoji import is_emoji
except ImportError:
    def is_emoji(s: str):
        raise NotImplementedError("You should install 'emoji'.")

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


@total_ordering
class Min(object):
    """
    An object that is less than any other object (except itself).
    Inspired by https://pypi.python.org/pypi/Extremes
    Examples::

        >>> import sys

        >>> Min < -sys.maxint
        True

        >>> Min < None
        True

        >>> Min < ''
        True
    """
    def __lt__(self, other):
        if other is Min:
            return False
        return True

@total_ordering
class Max(object):
    """
    An object that is greater than any other object (except itself).
    Inspired by https://pypi.python.org/pypi/Extremes

    Examples::

        >>> import sys

        >>> Max > Min
        True

        >>> Max > sys.maxint
        True

        >>> Max > 99999999999999999
        True
    """
    def __gt__(self, other):
        if other is Max:
            return False
        return True


class BaseValidator(object):
    @classmethod
    def is_truthy(cls,
            value: Any,
        ) ->bool:
        """Validate that given value is not a falsey value."""
        v =  value and (not isinstance(value, str) or value.strip())
        return True if v else False


class ValueValidator(BaseValidator):
    """ Return whether or not given value is a valid hash.
    currently, support hash are:
    md5, sha1, sha224, sha256, sha512
    """
    Min = Min()
    Max = Max()

    re_uuid = re.compile(
        "^([0-9a-f]{32}){1}$|^([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}){1}$",
        flags=re.IGNORECASE,
    )
    # See Also: https://jex.im/regulex/#!flags=&re=%5E%5B-%2B%5D%3F%5Cd*(%3F%3A(%5B.%2C%20%5D)(%3F%3A%5Cd%7B3%7D%5C1)*%5Cd%7B3%7D)%3F(%3F%3A%5B.%5D%5Cd*)%3F
    re_financial_number = re.compile(
        r'^[-+]?\d*(?:([., ])(?:\d{3}\1)*\d{3})?(?:[.]\d*)?'  )

    re_md5 = re.compile(
        r"^[0-9a-f]{32}$",
        re.IGNORECASE
    )
    re_sha1 = re.compile(
        r"^[0-9a-f]{40}$",
        re.IGNORECASE
    )
    re_sha224 = re.compile(
        r"^[0-9a-f]{56}$",
        re.IGNORECASE
    )
    re_sha256 = re.compile(
        r"^[0-9a-f]{64}$",
        re.IGNORECASE
    )
    re_sha512 = re.compile(
        r"^[0-9a-f]{128}$",
        re.IGNORECASE
    )

    @classmethod
    def is_md5(cls, value):
        v =  ( value and isinstance(value, str)
                 and cls.re_md5.match(value) )
        return True if v else False

    @classmethod
    def is_sha1(cls, value):
        v =  ( value and isinstance(value, str)
                 and cls.re_sha1.match(value) )
        return True if v else False

    @classmethod
    def is_sha224(cls, value):
        v = ( value and isinstance(value, str)
              and cls.re_sha224.match(value) )
        return True if v else False

    @classmethod
    def is_sha256(cls, value):
        v =  ( value and isinstance(value, str)
               and cls.re_sha256.match(value) )
        return True if v else False

    @classmethod
    def is_sha512(cls, value):
        v = ( value and isinstance(value, str)
              and cls.re_sha512.match(value) )
        return True if v else False

    @classmethod
    def is_financial_number(cls, value: Any):
        v =  ( value and isinstance(value, str)
               and cls.re_financial_number.match(value) )
        return True if v else False

    @classmethod
    @copy_docstring(validate_checkdigit)
    def is_valid_checkdigit(cls,
            number: Any,
            num_digits: Optional[int]=None,
            weights: Optional[list]=None,
        ):
        v = validate_checkdigit(number,
                           num_digits=num_digits, weights=weights)
        return True if v else False


    @classmethod
    def is_uuid(cls, value: Any):
        value = str(value) if isinstance(value, uuid.UUID) else value
        v =  ( value and isinstance(value, str)
               and cls.re_uuid.match(value) )
        return True if v else False


    @classmethod
    def is_length(cls,
            value: Any,
            min: Optional[int]=None,
            max: Optional[int]=None,
            thrown_error: bool=False
        ) ->bool:
        """Validate that a the length of given objects
            is within a specified range.
        """

        if (  (min is not None and min < 0)
              or (max is not None and max < 0) ):
            if thrown_error:
                raise AssertionError(
                    '`min` and `max` need to be greater than zero.'
                )
            else:
                return False
        try:
            _len = len(value)
        except TypeError as e:
            if thrown_error:
                raise TypeError(e)
            else:
                return False
        return cls.is_between(_len, min=min, max=max,
                              thrown_error=thrown_error)


    @classmethod
    def is_between(cls,
            value: Any,
            min: Optional[int]=None,
            max: Optional[int]=None,
            thrown_error: bool=False
        ) ->bool:
        """Validate that a number is between minimum and/or maximum value.
        """
        if min is None and max is None:
            if thrown_error:
                raise AssertionError(
                    'At least one of `min` or `max` must be specified.'
                )
            else:
                return False
        if min is None:
            min = cls.Min
        if max is None:
            max = cls.Max
        try:
            min_gt_max = min > max
        except TypeError:
            min_gt_max = max < min
        if min_gt_max:
            raise AssertionError('`min` cannot be more than `max`.')

        return min <= value and max >= value


class TypeValidator(BaseValidator):
    regex = re.compile("").__class__

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
    def is_date(cls, obj: Any):
        return isinstance(obj, date)

    @classmethod
    def is_time(cls, obj: Any):
        return isinstance(obj, time)

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
    def is_json_serializable_datajuggler(cls, obj: Any):
        json_types = (type(None), bool, dict, float, int, list, str, tuple,
                      Decimal, datetime, date, time,
                     )
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
        return obj != '' and isinstance(obj, str)

    @classmethod
    def is_tuple(cls, obj: Any):
        return isinstance(obj, tuple)

    @classmethod
    def is_tuple_not_empty(cls, obj: Any):
        return obj != () and isinstance(obj, tuple)

    @classmethod
    def is_uuid(cls, obj: Any):
        return obj and isinstance(obj, uuid.UUID)

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
    def is_str_emoji(cls, obj: Any):
        return obj and isinstance(obj, str) and is_emoji(obj)

    @classmethod
    def is_bytes(cls, obj: Any):
        return isinstance(obj, bytes)

    @classmethod
    def is_bytes_not_empty(cls, obj: Any):
        return obj != '' and isinstance(obj, bytes)


    @classmethod
    def is_made_by_pydantic(cls, obj: Any):
        try:
            return "<class 'pydantic.main.BaseModel'>" in [
                      str(c) for c in obj.__class__.__mro__ ]
        except:
            return False

    @classmethod
    def is_made_by_dataclass(cls, obj: Any):
        if hasattr(obj, '__dataclass_fields__'):
            return True
        else:
            return False

    @classmethod
    def is_made_by_namedtuple(cls, obj: Any):
        """Return True, if collections.namedtuple or typing.NamedTuple,
           otherwise, return False.
        """
        if ( isinstance(obj, tuple)
             and hasattr(obj, '_fields')
             and hasattr(obj, '_field_defaults')
             and hasattr(obj, '_make')
             and hasattr(obj, '_asdict') ):
            return True
        else:
            return False

    @classmethod
    def is_made_by_typing_namedtuple(cls, obj: Any):
        if isinstance(obj, tuple) and hasattr(obj, '__orig_bases__'):
            return True
        else:
            return False

    @classmethod
    def is_made_by_collections_namedtuple(cls, obj: Any):
        """Return True, if collections.namedtuple or typing.NamedTuple,
           otherwise, return False.
        """
        if ( cls.is_made_by_namedtuple(obj)
             and not hasattr(obj, '__orig_bases__') ):
            return True
        else:
            return False
