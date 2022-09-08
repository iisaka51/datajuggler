import re
from typing import (
    Any, Dict, Union, Optional, Hashable, Iterable, Sequence,
    Callable, Pattern, Literal, get_args
)
from collections.abc import Mapping
from collections import OrderedDict, defaultdict
import json
import copy
from enum import Enum
from multimethod import multidispatch, multimethod
from .yaml import to_yaml, from_yaml, yaml_initializer
from .toml import to_toml, from_toml
from .strings import is_match_string

class DictItem(str, Enum):
  KEY = "key"
  VALUE = "value"

DictItemType = Literal[DictItem.KEY, DictItem.VALUE]

def validate_DictItem(
        dictitem: DictItemType,
        thrown_error: bool=False,
    ) ->Optional[bool]:
    if dictitem in get_args(DictItemType):
        return True
    else:
        if not thrown_error:
            return False
        else:
            import inspect
            from executing import Source

            callFrame = inspect.currentframe().f_back.f_back
            callNode = Source.executing(callFrame).node
            source = Source.for_frame(callFrame)
            name = source.asttokens().get_text(callNode.args[0])

            raise ValueError("{} must be 'key' or 'value'.".format(name))

class DictFactory(dict):

    yaml_initializer = classmethod(yaml_initializer)
    to_yaml = to_yaml
    from_yaml = from_yaml
    to_toml = to_toml
    from_toml = from_toml

    """ Factory class for custom dictionary """
    def __init__(self,
            *args: Any,
            as_default_dict: bool=False,
            **kwargs: Any
        ):
        if as_default_dict:
            new = self.from_dict(dict(*args, **kwargs), factory=type(self))
            super().__init__(new)
        else:
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

    def copy(self):
        return copy.copy(self)

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

    def to_json(self, obj: Optional[Any]=None, **options) ->str:
        """Generate a new json strings. """
        obj = obj or self
        return json.dumps(obj, **options)

    def from_json(self,
        stream: str,
        inplace: bool=False,
        **options: Any):
        """Create a new dictionary from json strings."""
        if inplace:
            self.update(json.loads(stream, **options))
        else:
            return type(self)(json.loads(stream, **options))

    def to_dict(self, obj: Optional[dict]=None):
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
            factory: Optional[dict]=None,
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
            if isinstance(obj, Mapping) and factory == type(self):
                partial = factory((key, convert_loop(obj[key]))
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

    def __str__(self):
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

    def update(self, *args, **kwargs):
        for key, val in dict(*args, **kwargs).items():
            if isinstance(val, Mapping) and not isinstance(val, type(self)):
                self[key] = self.from_dict(val)
            else:
                self[key] = val



class uDict(DictFactory):
    __hash__ = None

    def __missing__(self, key):
        return None

    def replace_key(self,
            old: Hashable,
            new: Hashable,
            inplace: bool=False
        ):
        """Create the new dictionary wich is chnaged the key of the dictionary)
        If set `True` to `inplace`, perform operation in-place.
        """

        result = self.replace_key_map({old: new}, inplace)
        if not inplace:
            return result

    def replace_key_map(self,
            replace: dict,
            inplace: bool=False
        ):
        """Create the new dictionary which is chnaged the keys using mapping
        dictionary. `replace` expect {old, new}.
        If set `True` to `inplace`, perform operation in-place.
        """

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

    def map_keys(self,
            func: Callable,
            obj: Optional[Mapping]=None,
            factory: Optional[dict]=None,
            inplace: bool=False
        ):
        """ Create a new dictionary with apply function to keys of dictionary.
        if not set `obj`, use self.
        If set `factory`, create instance of factory class.
        If set `True` to `inplace`, perform operation in-place.
        """

        obj = obj or self
        factory = factory or type(self)

        new = dict(zip(map(func, obj.keys()), obj.values()))
        if inplace:
            self.clear()
            self.update(new)
        else:
            return factory(new)

    def map_values(self,
            func: Callable,
            obj: Optional[Mapping]=None,
            factory: Optional[dict]=None,
            inplace: bool=False
        ):
        """ Create a new dictionary with apply function to values of dictionary.
        if not set `obj`, use self.
        If set `factory`, create instance of factory class.
        If set `True` to `inplace`, perform operation in-place.
        """

        obj = obj or self
        factory = factory or type(self)

        new = dict(zip(obj.keys(), map(func, obj.values())))
        if inplace:
            self.clear()
            self.update(new)
        else:
            return factory(new)

    def map_items(self,
            func: Callable,
            obj: Optional[Mapping]=None,
            factory: Optional[dict]=None,
            inplace: bool=False
        ):
        """ Create a new dictionary with apply function to items of dictionary.
        if not set `obj`, use self.
        If set `factory`, create instance of factory class.
        If set `True` to `inplace`, perform operation in-place.
        """

        obj = obj or self
        factory = factory or type(self)

        new = map(func, obj.items())
        if inplace:
            self.clear()
            self.update(new)
        else:
            return factory(new)

    def filter_keys(self,
            predicate: Callable,
            obj: Optional[Mapping]=None,
            factory: Optional[dict]=None,
            inplace: bool=False
        ):
        """ Create a new dictionary with filter items in dictionary by keys.
        if not set `obj`, use self.
        If set `factory`, create instance of factory class.
        If set `True` to `inplace`, perform operation in-place.
        """

        obj = obj or self
        factory = factory or type(self)

        new = factory()

        for k, v in obj.items():
            if predicate(k):
                new[k] = v

        if inplace:
            self.clear()
            self.update(new)
        else:
            return new

    def filter_values(self,
            predicate: Callable,
            obj: Optional[Mapping]=None,
            factory: Optional[dict]=None,
            inplace: bool=False
        ):
        """ Create a new dictionary with filter items in dictionary by values.
        if not set `obj`, use self.
        If set `factory`, create instance of factory class.
        If set `True` to `inplace`, perform operation in-place.
        """

        obj = obj or self
        factory = factory or type(self)

        new = factory()

        for k, v in obj.items():
            if predicate(v):
                new[k] = v

        if inplace:
            self.clear()
            self.update(new)
        else:
            return new

    def filter_items(self,
            predicate: Callable,
            obj: Optional[Mapping]=None,
            factory: Optional[dict]=None,
            inplace: bool=False
        ):
        """ Create a new dictionary with filter items in dictionary by item.
        if not set `obj`, use self.
        If set `factory`, create instance of factory class.
        If set `True` to `inplace`, perform operation in-place.
        """

        obj = obj or self
        factory = factory or type(self)

        new = factory()

        for item in obj.items():
            if predicate(item):
                k, v = item
                new[k] = v

        if inplace:
            self.clear()
            self.update(new)
        else:
            return new

    def get_allkeys(self,
            obj: Optional[dict]=None
        ) -> list:
        """ Get to get all keys from dictionary as a List
            This method is able to process on nested dictionary.
        """

        def get_deeply( obj):
            found_keys = list()

            if isinstance(obj, Mapping):
                for key, val in obj.items():
                    found_keys.append(key)
                    found_keys += get_deeply(val)

            elif isinstance(obj, list) or isinstance(obj, tuple):
                for element in obj:
                    found_keys += get_deeply(element)

            return found_keys

        obj = obj or self
        all_keys = get_deeply(obj)
        return all_keys


    def get_values(self,
            keys: Union[Hashable, Sequence],
            obj: Optional[Union[Mapping, Sequence]] = None,
            wild: bool=False,
            with_keys: bool=False,
            verbatim: bool=False,
        ) -> Union[list, Mapping]:
        """Search the key in the objet(s).
        `obj` : dict, dict[dict], dict[list], list[dict]
        if not set `obj`, use self object.
        return a list of values
        """

        def deep_lookup(
                key: Hashable,
                obj: Union[Mapping, list, tuple],
                wild: bool=False,
                verbatim: bool=False,
            ):
            """Lookup a key in a nested object(s).
            yield a value
            """

            if isinstance(obj, Mapping):
                for k, v in obj.items():
                    if is_match_string(key, k, wild):
                        if verbatim:
                            yield k, v
                        else:
                            yield key, v
                    if isinstance(v, Mapping):
                        for kk, v in deep_lookup(key, v,
                                          wild=wild, verbatim=verbatim):
                            yield (kk, v)
                    elif isinstance(v, list) or isinstance(v, tuple):
                        for element in v:
                            for kk, v in deep_lookup( key, element,
                                             wild=wild, verbatim=verbatim):
                                yield (kk, v)

            elif isinstance(obj, list) or  isinstance(obj, tuple):
                for element in obj:
                    for k, v in deep_lookup(key, element,
                                     wild=wild, verbatim=verbatim):
                        if verbatim:
                            yield (k, v)
                        else:
                            yield (key, v)

        obj = obj or self
        if isinstance(keys, str):
            keys = [keys]
            as_dict = False
        else:
            as_dict = True

        keys = list(keys) if not isinstance(keys, list) else keys

        values = defaultdict(list)
        for key in keys:
            for k, v in deep_lookup(key, obj, wild=wild, verbatim=verbatim):
                values[k].append(v)

        if with_keys or as_dict:
            return values
        else:
            return list(values.values())[0]


    def counts_of_keys(self,
            keys: Union[Hashable, Sequence],
            obj: Optional[Mapping]=None,
            wild: bool=False,
            verbatim: bool=False,
        ) ->Union[int, dict]:

        obj = obj or self
        if isinstance(keys, str):
            keys = [keys]
            as_int=True
        else:
            as_int=False
        keys = list(keys) if not isinstance(keys, list) else keys

        counts = defaultdict(int)
        all_keys = self.get_allkeys(obj)
        for key in keys:
            if wild:
                for k in all_keys:
                    if is_match_string(key, k, wild):
                        if verbatim:
                            counts[k] += 1
                        else:
                            counts[key] += 1
            else:
                counts[key] += all_keys.count(key)

        if as_int:
            return counts[keys[0]]
        else:
            return counts

    def counts_of_values(self,
            value: Any,
            obj: Optional[Mapping]=None,
            wild: bool=False,
            verbatim: bool=False,
        ) ->Union[int, dict]:

        def deep_lookup(
                value: Any,
                obj: Union[Mapping, list, tuple],
                wild: bool=False,
                verbatim: bool=False,
            ):

            if isinstance(obj, Mapping):
                for k, v in obj.items():
                    if isinstance(v, str):
                        if is_match_string(value, v, wild):
                            if verbatim:
                                yield (1, v)
                            else:
                                yield (1, value)

                    elif isinstance(v, Mapping):
                        for c, v in deep_lookup(value, v,
                                          wild=wild, verbatim=verbatim):
                            yield (c, v)
                    elif isinstance(v, list) or isinstance(v, tuple):
                        for element in v:
                            for c, v in deep_lookup(value, element,
                                             wild=wild, verbatim=verbatim):
                                yield (c, v)
                    elif value == v:
                        yield (1, v)

            elif isinstance(obj, list) or  isinstance(obj, tuple):
                for element in obj:
                    for c, v in deep_lookup(value, element,
                                     wild=wild, verbatim=verbatim):
                        yield (c, v)

        obj = obj or self
        counts = defaultdict(int)

        for c, v in deep_lookup(value, obj, wild, verbatim=verbatim):
            counts[v] += c

        return counts


    def compare(self,
            d1: Mapping,
            d2: Optional[Mapping]=None,
            *,
            keys: Optional[Union[Hashable,list]]=None,
            thrown_error: bool=False,
        ):
        """Compare tow dictionary with keys.
           and return  `True` when equal found values.
           otherwise return `False`.
           if not set second dictionary, use self object.
           if not set keys, just compare two dictionaries,
        """

        def compare_dict(d1: Mapping, d2: Mapping, keys):
            keys = keys if isinstance(keys, list) else [keys]
            if isinstance(d1, Mapping):
                d1_values = list(self.get_values(keys, d1).values()).sort()
            else:
                d1_values = d1
            if isinstance(d2, Mapping):
                d2_values = list(self.get_values(keys, d2).values()).sort()
            else:
                d2_values = d2
            return d1_values == d2_values

        d2 = d2 or self
        check = d1 == d2 if not keys else compare_dict(d1, d2, keys)

        if check:
            return True
        else:
            if thrown_error:
                raise ValueError('{} is not equal {}.'
                                 .format(str(d1), str(d2)))
            return False

    def get_items(self,
            loc: Hashable,
            value: Any,
            obj: Optional[Mapping]=None,
            func: Optional[Callable]=None,
            factory: Optional[dict]=None,
        ):
        """ Create new dictionary with new key value pair as d[key]=val.
            If set `True` to `inplace`, perform operation in-place.
            otherwise, not modify the initial dictionary.
        loc
            the location of the value.
            i.e.: { 'a': { 'b1': { 'c1': {'x': 1 },
                                   'c2': {'x': 2 }},
                         { 'b2': { 'c1': {'x': 3 },
                                   'c2': {'x': 4 }} }}}
            if set ['a', 'b1', 'c1',  'x']  as `loc`, val is 1.
            giving the location of the value to be changed in `obj`.
            if set loc as str, convert to list using `loc.split(sep=' ')`.
        value: the value to aplly
        """
        factory = factory or type(self)
        obj = obj or self
        new = factory(obj)
        new = self.update_item(loc, value, new, func=func,
                                  factory=factory, inplace=False, action="get")
        return new

    def del_items(self,
            loc: Union[Hashable, list, tuple],
            obj: Optional[Mapping]=None,
            factory: Optional[dict]=None,
            inplace: bool=False
        ):
        """ Create new dicttionary with the given key(s) removed.
            New dictionary has d[key] deleted for each supplied key.
            If set `True` to `inplace`, perform operation in-place.
            otherwise, not modify the initial dictionary.
        """
        factory = factory or type(self)
        obj = obj or self
        new = factory(obj)

        new = self.update_item(loc, None, new, func=None,
                                  factory=factory, inplace=False, action="del")
        if inplace:
            self.clear()
            self.update(new)
        else:
            return new

    def set_items( self,
            loc: Union[str, Sequence],
            value: Any,
            obj: Optional[Union[Mapping, Sequence]]=None,
            func: Optional[Callable]=None,
            factory: Optional[dict]=None,
            inplace: bool=False,
        ):
        """ Create new dict with new, potentially nested, key value pair
        loc:
            the location of the value.
            i.e.: { 'a': { 'b1': { 'c1': {'x': 1 },
                                   'c2': {'x': 2 }},
                         { 'b2': { 'c1': {'x': 3 },
                                   'c2': {'x': 4 }} }}}
            if set ['a', 'b1', 'c1',  'x']  to loc, val is 1.
            giving the location of the value to be changed in `obj`.
            if set loc as str, convert to list using `str.split(keys)`.
        obj
            dictionary on which to operate
        func:
            the function to apply the object(s)..
        inplace:
            If set `True` to `inplace`, perform operation in-place.
            otherwise, not modify the initial dictionary.
        """

        return self.update_item(loc, value, obj, func=func,
                                  factory=factory, inplace=inplace)

    def update_item(self,
            loc: Union[str, Sequence],
            value: Any,
            obj: Optional[Union[Mapping, Sequence]]=None,
            func: Optional[Callable]=None,
            default: Optional[Any]=None,
            factory: Optional[dict]=None,
            inplace: bool=False,
            action: Literal["get", "del", "set"]="set"
        ):
        """ Create new dictionary Update value from a nested dictionary.
        Paramters
        ---------
        loc
            the location of the value.
            i.e.: { 'a': { 'b1': { 'c1': {'x': 1 },
                                   'c2': {'x': 2 }},
                         { 'b2': { 'c1': {'x': 3 },
                                   'c2': {'x': 4 }} }}}
            if set ['a', 'b1', 'c1',  'x']  as loc,
            giving the location of the value to be changed in d.
            if set loc as str, convert to list using `str.split(keys)`.
        value: the value to aplly
        oonj
            dictionary on which to operate
        func
            function to operate on that value

        If loc is not a key in d,
        update_in creates nested dictionaries to the depth
        specified by the keys, with the innermost value set to func(default).

        If set `True` to `inplace`, perform operation in-place.
        otherwise, not modify the initial dictionary.
        """

        factory = factory or dict
        obj = obj or self
        if isinstance(loc, str):
            loc = loc.split(sep=' ') if loc.find(' ')>0 else [loc]
        else:
            loc = list(loc) if isinstance(loc, tuple) else loc

        iter_key = iter(loc)
        k = next(iter_key)

        new = inner = factory()
        new.update(obj)

        if not func:
            func = lambda x: value

        for key in iter_key:
            if k in obj:
                obj = obj[k]
                wdict = factory()
                wdict.update(obj)
            else:
                obj = wdict = factory()

            inner[k] = inner = wdict
            k = key

        if k in obj:
            inner[k] = func(obj[k])
            if action == "get":
                return inner
            elif action == "del":
                del inner[k]
        else:
            if action != "del":
                inner[k] = func(default)

        if inplace:
            self.clear()
            self.update(new)
        else:
            return new




class iDict(DictFactory):

    def _blocked_attribute(self):
        raise AttributeError( ( "A {} cannot be modified."
                                .format(self.__class__.__name__) ) )

    _blocked_attribute = property(_blocked_attribute)

    __delitem__ = __setitem__ = _blocked_attribute
    pop = popitem = setdefault = clear = update = _blocked_attribute


    def __missing__(self, key):
        return None

    def __getattribute__(self, attribute):
        return dict.__getattribute__(self, attribute)

    def __hash__(self):
        try:
            return self._cached_hash
        except:
            h = self._cached_hash =  hash(frozenset(self.items()))
            return h

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


