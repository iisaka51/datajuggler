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
from .yaml import yaml_initializer, to_yaml, from_yaml

class DictFactory(dict):
    yaml_initializer = classmethod(yaml_initializer)
    to_yaml = to_yaml
    from_yaml = from_yaml

    """ Factory class for custom dictionary """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.yaml_initializer()

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, dict.__repr__(self))

    def __str__(self):
        return '{}'.format(dict.__repr__(self))

    def __getstate__(self):
        return {k: v for k, v in self.items()}

    def __setstate__(self, state):
        self.clear()
        self.update(state)

    def update(self, *args, **kwargs):
        for key, val in dict(*args, **kwargs).items():
            self[key] = val

    def get(self, key: Hashable, default=None):
        if key not in self:
            return default
        return self[key]

    def setdefault(self, key: Hashable, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def fromkeys(self,
            seq: Sequence,
            value: Any,
            inplace: bool=False,
        ) ->Optional[dict]:
        """Create a new dictionary with keys from iterable and values set to value.
           If set `True` to `inplace`, perform operation in-place.
        """
        new = type(self)(dict(self).fromkeys(seq, value))
        if inplace:
            self.update(new)
        else:
            return new

    def fromvalues(self,
            seq: Sequence,
            base: int=1,
            prefix: Optional[str]=None,
            inplace: bool=False,
        ) ->Optional[dict]:
        """Create a new dictionary from list of values.
           keys automaticaly generate as interger.
           `base` is the starting number.
           If set `True` to `inplace`, perform operation in-place.
        """
        if prefix != None:
            new = type(self)({'{}{}'.format(prefix, base+x): seq[x]
                             for x in range(len(seq)) } )
        else:
            new = type(self)({base+x: seq[x] for x in range(len(seq))})
        if inplace:
            self.update(new)
        else:
            return new

    def fromlists(self,
            keys: Sequence,
            values: Sequence,
            inplace: bool=False,
        ) ->Optional[dict]:
        """Create a new dictionary from two list as keys and values.
           Only the number of elements in the shorter of the two lists is processed.
           If set `True` to `inplace`, perform operation in-place.
        """
        zipobj = zip(keys, values)
        new = type(self)(dict(zipobj))
        if inplace:
            self.update(new)
        else:
            return new

    def to_json(self, **options) ->str:
        """Generate a new json strings. """
        return json.dumps(self, **options)

    def from_json(self,
        stream: str,
        inplace: bool=False,
        **options: Any):
        """Create a new dictionary from json strings."""
        if inplace:
            self.update(json.loads(stream, **options))
        else:
            return type(self)(json.loads(stream, **options))

    def to_dict(self, obj: Optional[Any]=None):
        """ Recursively converts DictFactory to dict.  """
        obj = obj or self
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

    def from_dict(self,
            obj: Any,
            factory: Optional[Any]=None,
            inplace: bool=False,
        ):
        """ Recursively converts from dict to DictFactory. """
        factory = factory or type(self)
        holding_obj = dict()
        workdict = type(self)()

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
            if isinstance(obj, iDict):
                partial = iDict((key, convert_loop(obj[key]))
                                for key in obj.keys() )
            elif isinstance(obj, Mapping):
                partial.update((key, convert_loop(obj[key]))
                                for key in obj.keys() )
            elif isinstance(obj, list):
                partial.extend(convert_loop(item) for item in obj)
            elif isinstance(obj, tuple):
                for (item_partial, item) in zip(partial, obj):
                    post_convert(item_partial, item)

            return partial

        obj = convert_loop(obj)
        try:
            if isinstance(self, iDict):
                workdict = iDict((key, convert_loop(obj[key]))
                                 for key in obj.keys() )
            else:
                if inplace:
                    self.update(obj)
                else:
                    workdict.update(obj)

        except AttributeError:
            pass   # obj is not Mapping and/or may be iDict.

        if not inplace:
            return workdict


class aDict(DictFactory):

    def __init__(self,
            *args: Any,
            as_default_dict: bool=False,
            **kwargs: Any
        ):
        if as_default_dict:
            self.update(*args, **kwargs)
        else:
            super().__init__(*args, **kwargs)
        self.yaml_initializer()

    def __str__(self):
        #return '{}'.format(self.__dict__)
        return '{}'.format(self.to_dict(self))

    def __getattr__(self, k):
        try:
            return object.__getattribute__(self, k)
        except AttributeError:
            try:
                return self[k]
            except KeyError:
                raise AttributeError(k)

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

    def __missing__(self, key):
        return None

    def __getattr__(self, attribute):
        if attribute in ('clear', 'update', 'pop', 'popitem', 'setdefault'):
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
        if attribute in ('clear', 'update', 'pop', 'popitem', 'setdefault'):
            raise AttributeError(
                r"{} object has no attribute {}"
                .format(type(self).__name__, attribute) )
        return dict.__getattribute__(self, attribute)

    def __hash__(self):
        return hash(tuple(sorted(self.items())))


    def fromkeys(self,
            seq: Sequence,
            value: Any,
            inplace: bool=False,
        ) ->Optional[dict]:
        """Create a new dictionary with keys from iterable and values set to value.
           If `inplace` parameter set `True`, It will alway be ignored.
        """
        if not inplace:
            return type(self)(dict(self).fromkeys(seq, value))

    def fromvalues(self,
            seq: Sequence,
            base: int=1,
            prefix: Optional[str]=None,
            inplace: bool=False,
        ) ->Optional[dict]:
        """Create a new dictionary from list of values.
           keys automaticaly generate as interger.
           `base` is the number of base.
           If `inplace` parameter set `True`, It will alway be ignored.
        """
        if not inplace:
            if prefix != None:
                new = type(self)({'{}{}'.format(prefix, base+x): seq[x]
                             for x in range(len(seq)) } )
            else:
                new = type(self)({base+x: seq[x] for x in range(len(seq))})
            return new

    def fromlists(self,
            keys: Sequence,
            values: Sequence,
            inplace: bool=False,
        ) ->Optional[dict]:
        """Create a new dictionary from two list as keys and values.
           If `inplace` parameter set `True`, It will alway be ignored.
        """
        if not inplace:
            zipobj = zip(keys, values)
            return type(self)(dict(zipobj))

    def to_json(self,
            **options) ->str:
        """Generate a new json strings.
        """
        return json.dumps(self, **options)

    def from_json(self,
            stream: str,
            inplace: bool=False,
            **options: Any):
        """Create a new dictionary from json strings.
           If `inplace` parameter set `True`, It will alway be ignored.
        """
        if not inplace:
            return type(self)(json.loads(stream, **options))


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


