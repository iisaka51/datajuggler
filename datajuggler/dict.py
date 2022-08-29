import re
from typing import (
    Any, Dict, Union, Optional, Hashable, Iterable, Sequence,
    Literal, get_args
)
from collections.abc import Mapping
from collections import OrderedDict
import json
from enum import Enum
from multimethod import multidispatch

class DictFactory(dict):
    """ Factory class for custom dictionary """

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, dict.__repr__(self))

    def __str__(self):
        return '{}'.format(dict.__repr__(self))

    def __dir__(self):
        return list(self.items())

    def __getstate__(self):
        return {k: v for k, v in self.items()}

    def __setstate__(self, state):
        self.clear()
        self.update(state)

    def update(self, *args, **kwargs):
        for key, val in dict(*args, **kwargs).items():
            self[key] = val

    def get(self, key, default=None):
        if key not in self:
            return default
        return self[key]

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def fromkeys(self,
            seq: Sequence,
            value: Any
        ):
        return type(self)(dict(self).fromkeys(seq, value))

    def fromvalues(self,
            seq: Sequence,
            base: int=1
        ):
        return type(self)({base+x: seq[x] for x in range(len(seq))})

    def fromlists(self,
            keys: Sequence,
            values: Sequence,
        ):
        zipobj = zip(keys, values)
        return type(self)(dict(zipobj))

    def to_json(self, **options):
        return json.dumps(self, **options)

    def from_json(self, stream, *args, **kwargs):
        self.update(json.loads(stream))
        return self

class aDict(DictFactory):
    def __init__(self, *args:Any, **kwargs:Any):
         self.update(*args, **kwargs)

    def __getattr__(self, k):
        try:
            return object.__getattribute__(self, k)
        except AttributeError:
            try:
                return self[k]
            except KeyError:
                raise AttributeError(k)

    def __str__(self):
        return '{}'.format(self.__dict__)

    def __setattr__(self, k, v):
        try:
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                if isinstance(v, Mapping) and not isinstance(v, type(self)):
                    self[k] = self.from_dict(v)
                else:
                    self[k] = v
            except:
                raise AttributeError(k)
        else:
            object.__setattr__(self, k, v)

    def __delattr__(self, k):
        try:
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)
        else:
            object.__delattr__(self, k)

    @property
    def __dict__(self):
        return self.to_dict(self)

    def update(self, *args, **kwargs):
        for key, val in dict(*args, **kwargs).items():
            if isinstance(val, Mapping) and not isinstance(val, type(self)):
                self[key] = self.from_dict(val)
            else:
                self[key] = val

    def copy(self):
        return self.from_dict(self)

    def to_dict(self, obj):
        """ Recursively converts aDict to dict.  """
        holding_obj = dict()

        def convert_loop(obj):
            try:
                return holding_obj[id(obj)]
            except KeyError:
                pass

            holding_obj[id(obj)] = partial = pre_convert(obj)
            return post_convert(partial, obj)

        def pre_convert(obj):
            if isinstance(obj, Mapping):
                return dict()
            elif isinstance(obj, list):
                return type(obj)()
            elif isinstance(obj, tuple):
                type_factory = getattr(obj, "_make", type(obj))
                return type_factory(convert_loop(item) for item in obj)
            else:
                return obj

        def post_convert(partial, obj):
            if isinstance(obj, Mapping):
                partial.update((k, convert_loop(obj[k])) for k in obj.keys())
            elif isinstance(obj, list):
                partial.extend(convert_loop(v) for v in obj)
            elif isinstance(obj, tuple):
                for (value_partial, value) in zip(partial, obj):
                    post_convert(value_partial, value)

            return partial

        return convert_loop(obj)

    @classmethod
    def from_dict(cls, obj, factory=None):
        """ Recursively converts from dict to aDict. """
        factory = factory or cls
        holding_obj = dict()

        def convert_loop(obj):
            try:
                return holding_obj[id(obj)]
            except KeyError:
                pass

            holding_obj[id(obj)] = partial = pre_convert(obj)
            return post_convert(partial, obj)

        def pre_convert(obj):
            if isinstance(obj, Mapping):
                return factory({})
            elif isinstance(obj, list):
                return type(obj)()
            elif isinstance(obj, tuple):
                type_factory = getattr(obj, "_make", type(obj))
                return type_factory(convert_loop(item) for item in obj)
            else:
                return obj

        def post_convert(partial, obj):
            if isinstance(obj, Mapping):
                partial.update((key, convert_loop(obj[key]))
                                for key in obj.keys() )
            elif isinstance(obj, list):
                partial.extend(convert_loop(item) for item in obj)
            elif isinstance(obj, tuple):
                for (item_partial, item) in zip(partial, obj):
                    post_convert(item_partial, item)

            return partial

        return convert_loop(obj)


class uDict(DictFactory):
    __hash__ = None

    def __missing__(self, key):
        return None

    def replace_key(self, old, new, inplace=False):
        result = self.replace_key_map({old: new}, inplace)
        if not inplace:
            return result

    def replace_key_map(self, replace, inplace=False):
        if not inplace:
            work_dict = self.copy()
        else:
            work_dict = self

        for key in list(self.keys()):
            work_dict[replace.get(key, key)] = work_dict.pop(key)

        if inplace:
            self.update(work_dict)
        else:
            return work_dict

class iDict(DictFactory):
    def __init__(self, *args:Any, **kwargs:Any):
         super().__init__(*args, **kwargs)

    def __missing__(self, key):
        return None

    def __getattr__(self, attribute):
        if attribute in ('clear', 'update', 'pop', 'popitem',
                         'setdefault', 'from_json'):
            raise AttributeError(
                r"{} object has no attribute {}"
                .format(type(self).__name__, attribute) )

    def __setitem__(self, key, value):
        raise TypeError(
            r"{} object does not support item assignment"
            .format(type(self).__name__) )

    def __delitem__(self, key):
        raise TypeError(
            r"{} object does not support item deletion"
            .format(type(self).__name__) )

    def __getattribute__(self, attribute):
        if attribute in ('clear', 'update', 'pop', 'popitem',
                         'setdefault', 'from_json'):
            raise AttributeError(
                r"{} object has no attribute {}"
                .format(type(self).__name__, attribute) )
        return dict.__getattribute__(self, attribute)

    def __hash__(self):
        return hash(tuple(sorted(self.items())))


@multidispatch
def ordereddict_to_dict( obj: Any) -> dict:
    raise TypeError("Unsupported type.")

@ordereddict_to_dict.register(str)
def _ordereddict_to_dict(obj: str):
    return obj

@ordereddict_to_dict.register(Union[int, float])
def _ordereddict_to_dict(obj: Union[int, float]) ->Union[int, float]:
    return obj

@ordereddict_to_dict.register(dict)
def _ordereddict_to_dict(obj: dict) ->dict:
    return {k: ordereddict_to_dict(v) for k, v in obj.items()}

@ordereddict_to_dict.register(OrderedDict)
def _ordereddict_to_dict(obj: OrderedDict) ->dict:
    return dict(obj)

@ordereddict_to_dict.register(Union[list, tuple])
def _ordereddict_to_dict(obj: Union[list, tuple]) ->list:
    return [ordereddict_to_dict(e) for e in obj]

@multidispatch
def change_dict_keys( *args: Any, **kwargs: Any):
    raise TypeError("Invaid Type.")

@change_dict_keys.register(dict, Hashable, Hashable)
def _change_dict_keys_single(
    data: dict,
    old: Hashable,
    new: Hashable,
    inplace: bool=False,
    ) -> dict:
    """Change dict key.
    Parameters
    ----------
    data: dict
         old dict
    old: Hashable
         old key
    new: Hashable
         new key
    inplace: bool
        Whether to perform the operation in place on the data. default False.
    Returns
    -------
    new dict: dict
    """

    if not inplace:
        data = data.copy()

    workdict = {}
    replace={old:new}
    for key in list(data.keys()):
        data[replace.get(key,key)] = data.pop(key)

    if not inplace:
        return data

@change_dict_keys.register(dict, dict)
def _change_dict_keys_multi(
        data: dict,
        replace: dict,
        inplace: bool=False,
    ) -> dict:
    """Change dict key using dict.
    Parameters
    ----------
    d: dict
         old dict
    replace: dict {old_key: new_key,...}
        replace keymap as dict.
    inplace: bool
        Whether to perform the operation in place on the data. default False.
    Returns
    -------
    new dict: dict
    """

    if not inplace:
        data = data.copy()

    for key in list(data.keys()):
        data[replace.get(key, key)] = data.pop(key)

    if not inplace:
        return data


