# -*- coding: utf-8 -*-

from __future__ import annotations

import re
from typing import (
    Any, Dict, Union, Optional, Hashable, Iterable, Sequence,
    Callable, Pattern, Type
    )
import copy
import json
from datajuggler.strings import is_match_string, searchstr

from datajuggler.validator import (
    DictAction, DictActionType,
    DictItem, DictItemType,
    DictKey, DictKeyType,
    )
from datajuggler.keys import (
    Keylist, Keypath, Default_Keypath_Separator
    )

from datajuggler import dicthelper as d
from datajuggler import serializer as io
from datajuggler.validator import TypeValidator as _type

class BaseDict(dict):

    """ Factory class for custom dictionary """
    def __init__(self,
            *args: Any,
            **kwargs: Any
        ):
        super().__init__(*args, **kwargs)


    def __repr__(self):
        return f'{self.__class__.__name__}({dict.__repr__(self)})'

    def __str__(self):
        return f'{dict.__repr__(self)}'

    def __getstate__(self):
        return {k: v for k, v in self.items()}

    def __setstate__(self, state):
        self.clear()
        self.update(state)

    def copy(self,
            factory: Optional[Type[dict]]=None,
        ):
        if factory:
            return factory(copy.copy(self))
        else:
            return copy.copy(self)

    def deepcopy(self,
            factory: Optional[Type[dict]]=None,
        ):
        if factory:
            return factory(copy.deepcopy(self))
        else:
            return copy.deepcopy(self)

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
            self.clear()
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

    def to_dict(self, obj: Optional[dict]=None):
        """ Recursively converts BaseDict to dict.  """
        obj = obj if obj or obj == {} else self
        holding_obj = dict()

        def convert_loop(obj):
            try:
                return holding_obj[id(obj)]
            except KeyError:
                pass

            holding_obj[id(obj)] = partial = pre_convert(obj)
            return post_convert(partial, obj)

        def pre_convert(obj):
            if _type.is_dict(obj):
                return dict()
            elif _type.is_list(obj):
                return type(obj)()
            elif _type.is_tuple(obj):
                type_factory = getattr(obj, "_make", type(obj))
                return type_factory(convert_loop(item) for item in obj)
            else:
                return obj

        def post_convert(partial, obj):
            if _type.is_dict(obj):
                partial.update((k, convert_loop(obj[k])) for k in obj.keys())
            elif _type.is_list(obj):
                partial.extend(convert_loop(v) for v in obj)
            elif _type.is_tuple(obj):
                for (value_partial, value) in zip(partial, obj):
                    post_convert(value_partial, value)

            return partial

        return convert_loop(obj)

    def from_dict(self,
            obj: Any,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ):
        """ Recursively converts from dict to BaseDict. """
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
            if _type.is_dict(obj):
                return factory({})
            elif _type.is_list(obj):
                return type(obj)()
            elif _type.is_tuple(obj):
                type_factory = getattr(obj, "_make", type(obj))
                return type_factory(convert_loop(item) for item in obj)
            else:
                return obj

        def post_convert(partial, obj):
            if _type.is_dict(obj) and factory == type(self):
                partial = factory((key, convert_loop(obj[key]))
                                for key in obj.keys() )
            elif _type.is_dict(obj):
                partial.update((key, convert_loop(obj[key]))
                                for key in obj.keys() )
            elif _type.is_list(obj):
                partial.extend(convert_loop(item) for item in obj)
            elif _type.is_tuple(obj):
                for (item_partial, item) in zip(partial, obj):
                    post_convert(item_partial, item)

            return partial

        obj = convert_loop(obj)
        try:
            if inplace:
                self.update(obj)
            else:
                workdict.update(obj)

        except AttributeError:
            pass   # obj is not Mapping

        if not inplace:
            return workdict


class IODict(BaseDict):
    yaml_initializer = classmethod(io.yaml_initializer)

    def __init__(self,
            *args: Any,
            format: Optional[str]=None,
            **kwargs: Any):
        """
        Constructs a new instance.
        """
        # if first argument is data-string, url or filepath try to decode it.
        # use 'format' kwarg to specify the decoder to use, default 'json'.
        if format and format.lower():
            d = IODict._decode_init(format, *args, **kwargs)
            super().__init__(d, **kwargs)
            return
        super().__init__(*args, **kwargs)

    @staticmethod
    def _serializer_init(s, **kwargs):
        pass

    @staticmethod
    def _decode_init(s, **kwargs):
        autodetected_format = io.autodetect_format(s)
        default_format = autodetected_format or "json"
        format = kwargs.pop("format", default_format).lower()
        if format in ["b64", "base64"]:
            kwargs.setdefault("subformat", "json")
        elif format in ["yml", "yaml"]:
            self.yaml_initializer()
        # decode data-string and initialize with dict data.
        return IODict._decode(s, format, **kwargs)

    @staticmethod
    def _decode(s, format, **kwargs):
        try:
            content = io.read_content(s)
            # decode content using the given format
            data = io.decode(content, format, **kwargs)
            if _type.is_dict(data):
                return data
            elif _type.is_list(data):
                # force list to dict
                return {"values": data}
            else:
                raise ValueError(
                    f"Invalid data type: {type(data)}, expected dict or list."
                )
        except Exception as e:
            raise ValueError(f"Invalid data or url or filepath argument: {s}\n{e}")

    @staticmethod
    def _encode(d, format, **kwargs):
        filepath = kwargs.pop("filepath", None)
        s = io.encode(d, format, **kwargs)
        if filepath:
            io.write_file(filepath, s)
        return s

    @classmethod
    def from_base64(cls, s, subformat="json", encoding="utf-8", **kwargs):
        """
        Load and decode Base64 data from url, filepath or data-string.
        Data is decoded according to subformat and encoding.
        Decoder specific options can be passed using kwargs.
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        kwargs["subformat"] = subformat
        kwargs["encoding"] = encoding
        return cls(s, format="base64", **kwargs)

    @classmethod
    def from_csv(cls, s, columns=None, columns_row=True, **kwargs):
        """
        Load and decode CSV data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/csv.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        kwargs["columns"] = columns
        kwargs["columns_row"] = columns_row
        return cls(s, format="csv", **kwargs)

    @classmethod
    def from_ini(cls, s, **kwargs):
        """
        Load and decode INI data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/configparser.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="ini", **kwargs)

    def from_json(self,
            stream,
            inplace:bool=False,
            **options: Any):
        """
        Load and decode JSON data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/json.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        if inplace:
            self.update(json.loads(stream, **options))
        else:
            return type(self)(json.loads(stream, **options))

    @classmethod
    def from_pickle(cls, s, **kwargs):
        """
        Load and decode a pickle encoded in Base64 format data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/pickle.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="pickle", **kwargs)

    @classmethod
    def from_plist(cls, s, **kwargs):
        """
        Load and decode p-list data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/plistlib.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="plist", **kwargs)

    @classmethod
    def from_query_string(cls, s, **kwargs):
        """
        Load and decode query-string from url, filepath or data-string.
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="query_string", **kwargs)

    @classmethod
    def from_toml(cls, s, **kwargs):
        """
        Load and decode TOML data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://pypi.org/project/toml/
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="toml", **kwargs)

    @classmethod
    def from_xml(cls, s, **kwargs):
        """
        Load and decode XML data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://github.com/martinblech/xmltodict
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="xml", **kwargs)

    @classmethod
    def from_yaml(cls, s, **kwargs):
        """
        Load and decode YAML data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://pyyaml.org/wiki/PyYAMLDocumentation
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="yaml", **kwargs)

    def to_base64(self, subformat="json", encoding="utf-8", **kwargs):
        """
        Encode the current dict instance in Base64 format
        using the given subformat and encoding.
        Encoder specific options can be passed using kwargs.
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        kwargs["subformat"] = subformat
        kwargs["encoding"] = encoding
        return self._encode(self.dict(), "base64", **kwargs)

    def to_csv(self, key="values", columns=None, columns_row=True, **kwargs):
        """
        Encode a list of dicts in the current dict instance in CSV format.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/csv.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        kwargs["columns"] = columns
        kwargs["columns_row"] = columns_row
        return self._encode(self.dict()[key], "csv", **kwargs)

    def to_ini(self, **kwargs):
        """
        Encode the current dict instance in INI format.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/configparser.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "ini", **kwargs)

    def to_json(self, **kwargs):
        """
        Encode the current dict instance in JSON format.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/json.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "json", **kwargs)

    def to_pickle(self, **kwargs):
        """
        Encode the current dict instance as pickle (encoded in Base64).
        The pickle protocol used by default is 2.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/pickle.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "pickle", **kwargs)

    def to_plist(self, **kwargs):
        """
        Encode the current dict instance as p-list.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/plistlib.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "plist", **kwargs)

    def to_query_string(self, **kwargs):
        """
        Encode the current dict instance in query-string format.
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "query_string", **kwargs)

    def to_toml(self, **kwargs):
        """
        Encode the current dict instance in TOML format.
        Encoder specific options can be passed using kwargs:
        https://pypi.org/project/toml/
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "toml", **kwargs)

    def to_xml(self, **kwargs):
        """
        Encode the current dict instance in XML format.
        Encoder specific options can be passed using kwargs:
        https://github.com/martinblech/xmltodict
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "xml", **kwargs)

    def to_yaml(self, **kwargs):
        """
        Encode the current dict instance in YAML format.
        Encoder specific options can be passed using kwargs:
        https://pyyaml.org/wiki/PyYAMLDocumentation
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "yaml", **kwargs)


class aDict(IODict):

    def __init__(__self,
            *args: Any,
            format: Optional[str]=None,
            **kwargs: Any
        ):
        object.__setattr__(__self, '__parent', kwargs.pop('__parent', None))
        object.__setattr__(__self, '__key', kwargs.pop('__key', None))
        object.__setattr__(__self, '__frozen', False)
        if format:
            args = super()._decode_init(format, *args, **kwargs)

        for arg in args:
            if not arg:
                continue
            elif _type.is_dict(arg):
                for key, val in arg.items():
                    __self[key] = __self._hook(val)
            elif _type.is_tuple(arg)  and (not _type.is_tuple(arg[0])):
                __self[arg[0]] = __self._hook(arg[1])
            else:
                for key, val in iter(arg):
                    __self[key] = __self._hook(val)

        for key, val in kwargs.items():
            __self[key] = __self._hook(val)

    def _check_frozen(self,
            thrown_error: bool=False,
            msg: str='frozen object cannot be modified.',
            ):
        if object.__getattribute__(self, '__frozen'):
            if thrown_error:
                raise AttributeError( f"{self.__class__.__name__} {msg}" )
            else:
                return True
        else:
            return False

    def __setattr__(self, name, value):
        if hasattr(self.__class__, name):
            raise AttributeError("'aDict' object attribute "
                                 "'{0}' is read-only".format(name))
        else:
            self[name] = value

    def __setitem__(self, name, value):
        if self._check_frozen(thrown_error=False):
            if name not in super().keys():
                raise KeyError(name)
            else:
                raise AttributeError("'aDict' object attribute "
                                 "'{0}' is read-only".format(name))

        super().__setitem__(name, value)
        try:
            p = object.__getattribute__(self, '__parent')
            key = object.__getattribute__(self, '__key')
        except AttributeError:
            p = None
            key = None
        if p is not None:
            p[key] = self
            object.__delattr__(self, '__parent')
            object.__delattr__(self, '__key')


    def __add__(self, other):
        if not self.keys():
            return other
        else:
            self_type = type(self).__name__
            other_type = type(other).__name__
            msg = "unsupported operand type(s) for +: '{}' and '{}'"
            raise TypeError(msg.format(self_type, other_type))

    @classmethod
    def _hook(cls, item):
        if _type.is_dict(item):
            return cls(item)
        elif _type.is_list_or_tuple(item):
            return type(item)(cls._hook(elem) for elem in item)
        return item

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __missing__(self, name):
        if object.__getattribute__(self, '__frozen'):
            raise KeyError(name)
        return self.__class__(__parent=self, __key=name)

    def __delattr__(self, name):
        self._check_frozen(thrown_error=True)
        del self[name]

    def __hash__(self):
        if self._check_frozen(thrown_error=False):
            return hash(frozenset(self.items()))
        else:
            raise AttributeError('unhashable not frozen object.')

    def __deepcopy__(self, memo):
        other = self.__class__()
        memo[id(self)] = other
        for key, value in self.items():
            other[copy.deepcopy(key, memo)] = copy.deepcopy(value, memo)
        return other

    def update(self, *args, **kwargs):
        self._check_frozen(thrown_error=True)
        other = {}
        if args:
            if len(args) > 1:
                raise TypeError()
            other.update(args[0])
        other.update(kwargs)
        for k, v in other.items():
            if ((k not in self) or
                (not _type.is_dict(self[k])) or
                (not _type.is_dict(v))):
                self[k] = v
            else:
                self[k].update(v)

    def __getnewargs__(self):
        return tuple(self.items())

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self._check_frozen(thrown_error=True)
        self.update(state)

    def __or__(self, other):
        # if not _type.is_dict(other):
        #    return NotImplemented
        # new = copy.copy(self)
        # new.update(other)
        # return new
        return d.d_merge(self, other,
                         overwrite=True, concat=True,
                         inplace=False, factory=type(self))

    def __ror__(self, other):
        # if not _type.is_dict(other):
        #     return NotImplemented
        # new = copy.copy(other)
        # new.update(self)
        # return new
        return d.d_merge(other, self,
                         overwrite=True, concat=True,
                         inplace=False, factory=type(self))

    def __ior__(self, other):
        self._check_frozen(thrown_error=True)
        self.update(other)
        return self

    def __str__(self):
        return f'{self.to_dict(self)}'

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
                if _type.is_dict_and_not_other(dict, self):
                    self[k] = self.from_dict(v)
                else:
                    self[k] = v
            except:
                if not self._check_frozen(thrown_error=False):
                    raise AttributeError(k)
        else:
            object.__setattr__(self, k, v)

    def __delattr__(self, k):
        self._check_frozen(thrown_error=True)
        try:
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)
        else:
            object.__delattr__(self, k)

    def copy(self):
        return copy.copy(self)

    def clear(self):
        self._check_frozen(thrown_error=True)
        return super().clear()

    def pop(self, key, value):
        self._check_frozen(thrown_error=True)
        return super().pop(key, value)

    def popitem(self, key, value):
        self._check_frozen(thrown_error=True)
        return super().pop(key, value)

    def setdefault(self, key, default=None):
        self._check_frozen(thrown_error=True)
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def freeze(self, shouldFreeze=True):
        object.__setattr__(self, '__frozen', shouldFreeze)
        for key, val in self.items():
            if _type.is_same_as(val, self):
                val.freeze(shouldFreeze)

    def unfreeze(self):
        self.freeze(False)

    def update(self, *args, **kwargs):
        self._check_frozen(thrown_error=True)
        for key, val in dict(*args, **kwargs).items():
            if _type.is_dict_and_not_other(dict, self):
                self[key] = self.from_dict(val)
            else:
                self[key] = val



class uDict(IODict):
    __hash__ = None
    _keypath_separator=Default_Keypath_Separator

    def __init__(self,
            *args: Any,
            separator: str=Default_Keypath_Separator,
            **kwargs: Any
        ):
        if separator:
            self._keypath_separator = separator
        super().__init__(*args, **kwargs)

    def __is_keypath_or_keylist(self, x):
        return ( self._keypath_separator is not None
                 and _type.is_keylist_or_keypath(x) )

    def __is_keylist(self, x):
        return ( self._keypath_separator is not None
                 and _type.is_keylist(x) )

    def __is_keypath(self, x):
        return ( self._keypath_separator is not None
                 and _type.is_keypath(x) )

    @property
    def keypath_separator(self):
        return self._keypath_separator

    @keypath_separator.setter
    def keypath_separator(self, val):
        if _type.is_str_not_empty(val):
            self._separator = val
        else:
            raise ValueError('separator must be not empty str.')


    def __missing__(self, key):
        return None

    def __contains__(self,
            key: Union[str, Keylist, Keypath],
        ):
        if self.__is_keypath(key):
            allkeys = self.get_keys(as_keypath=True)
            return key in allkeys
        elif self.__is_keylist(key):
            allkeys = self.get_keys(as_keylist=True)
            return key in allkeys
        elif _type.is_str(key):
            allkeys = self.get_keys()
            return key in allkeys

        return super().__contains__(key)

    def __delitem__(self,
            key: Union[str, Keylist, Keypath],
        ):
        if self.__is_keypath_or_keylist(key):
            self.del_items(key)
            return
        super().__delitem__(key)

    def __getitem__(self,
            key: Union[str, list, tuple, Keylist, Keypath],
        ):
        if self.__is_keypath_or_keylist(key):
            return self.get_items(key)
        return super().__getitem__(key)

    def __setitem__(self,
            key: Union[str, Keylist, Keypath],
            val: Any,
        ):
        if self.__is_keypath_or_keylist(key):
            return self.set_items(key, val)
        super().__setitem__(key, val)

    def __or__(self, other):
        return d.d_merge(self, other,
                         overwrite=True, concat=True,
                         inplace=False, factory=type(self))

    def __ror__(self, other):
        return d.d_merge(other, self,
                         overwrite=True, concat=True,
                         inplace=False, factory=type(self))

    def __ior__(self, other):
        self.update(other)
        return self


    def get(self,
            key: Union[str, Keylist, Keypath],
            default=None,
        ):
        if self.__is_keypath_or_keylist(key):
            return self.get_items(key, default)
        return super().get(key, default)

    def pop(self,
            key: Union[str, Keylist, Keypath],
            *args: Any,
        ):
        if self.__is_keypath_or_keylist(key):
            return self.pop_items(key)
        if args:
            return args[0]
        raise KeyError(f"Invalid keys: '{keys}'")

    def set(self,
            key: Union[str, Keylist, Keypath],
            val: Any,
        ):
        self[key] = val

    def setdefault(self,
            key: Union[str, Keylist, Keypath],
            default=None,
        ):
        if key not in self:
            self[key] = default
            return default
        return self[key]


    @staticmethod
    def _get_docstring(obj, attr: Optional[str]=None):
        if attr:
            doc = f"{obj.__doc__}\nIf {attr} is omitted, self is used."
        else:
            doc = f"{obj.__doc__}"
        return doc

    def clean(self,
            obj: Optional[dict]=None,
            strings=True,
            collections=True,
            *,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ):
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        new =  d.d_clean(obj, strings, collections,
                                       inplace=False, factory=dict)
        if inplace:
            self.clear()
            self.update(new)
        else:
            return factory(new)

    clean.__doc__ = _get_docstring(d.d_clean, 'obj')

    def clone(self,
            obj: Optional[dict]=None,
            empty: bool=False,
            memo: Optional[dict]=None,
            factory: Optional[Type[dict]]=None,
        ):
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        new = d.d_clone(obj, empty, memo)
        return factory(new)

    clone.__doc__ = _get_docstring(d.d_clone, 'obj')

    def compare(self,
        d1: dict,
        d2: Optional[dict]=None,
        *,
        keys: Optional[Union[Hashable,list]]=None,
        keylist: bool=False,
        keypath: bool=False,
        thrown_error: bool=False,
        ):
        d2 = d2 or self
        return d.d_compare(d1, d2, keys=keys,
                         keylist=keylist, keypath=keypath,
                         thrown_error=thrown_error)

    compare.__doc__ = _get_docstring(d.d_compare, 'd2')

    def counts(self,
            pattern: Union[Pattern, Hashable, Sequence],
            obj: Optional[dict]=None,
            *,
            count_for: DictItemType=DictItem.KEY,
            wild: bool=False,
            verbatim: bool=False,
        ) ->Union[int, dict]:

        obj = obj if obj or obj == {} else self
        return d.d_counts(obj, pattern, count_for=count_for,
                        wild=wild, verbatim=verbatim)

    counts.__doc__ = _get_docstring(d.d_counts, 'obj')


    def filter(self,
            predicate: Callable,
            obj: Optional[dict]=None,
            *,
            factory: Optional[Type[dict]]=None,
        ):
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        new = factory()

        return d.d_filter(predicate, obj, factory=factory)

    filter.__doc__ = _get_docstring(d.d_filter, 'obj')

    def groupby( self,
            seq: list,
            key: Hashable,
            *,
            factory: Optional[Type[dict]]=None,
        ) -> dict:
        factory = factory or type(self)
        return d.d_groupby(seq, key, factory)

    groupby.__doc__ = _get_docstring(d.d_groupby)

    def invert( self,
            obj: Optional[dict]=None,
            flat: bool=False,
            *,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ) ->dict:
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        return d.d_invert(obj, flat=flat,
                               inplace=inplace, factory=factory)

    invert.__doc__ = _get_docstring(d.d_invert, 'obj')

    def map(self,
            func: Callable,
            obj: Optional[dict]=None,
            *,
            map_for: Optional[DictItemType]=None,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ) ->dict:

        obj = obj if obj or obj == {} else self
        factory = factory or type(self)

        return d.d_map(func, obj, map_for=map_for,
                       inplace=inplace, factory=factory)

    map.__doc__ = _get_docstring(d.d_map, 'obj')

    def merge(self,
            others: list,
            obj: Optional[dict]=None,
            *,
            overwrite: bool=True,
            concat: bool=False,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ) ->dict:

        obj = obj if obj or obj == {} else self
        factory = factory or type(self)

        return d.d_merge(obj, others,
                         overwrite=overwrite, concat=concat,
                         inplace=inplace, factory=factory)

    merge.__doc__ = _get_docstring(d.d_merge, 'obj')

    def move(self,
            key_src: Union[str, list],
            key_dest: Union[str, list],
            obj: Optional[dict]=None,
            *,
            overwrite: bool=True,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ) ->dict:
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        new = d.d_move(obj, key_src, key_dest,
                        overwrite=overwrite,
                        inplace=False, factory=dict)
        return d._dict_updator(obj, new, inplace=inplace, factory=factory)

    move.__doc__ = _get_docstring(d.d_move, 'obj')


    def nest(self,
        items: tuple,
        id_key: Union[str, list],
        parent_id_key: Union[str, list],
        children_key: Union[str, list],
        )->list:

       return d.d_nest(items, id_key, parent_id_key, children_key)

    nest.__doc__ = _get_docstring(d.d_nest)


    def remove(self,
            keys: Union[list, Hashable],
            obj: Optional[dict]=None,
            *,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ):
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        return d.d_remove(obj, keys,
                      inplace=inplace, factory=factory)

    remove.__doc__ = _get_docstring(d.d_remove, 'obj')

    def rename(self,
            key: Union[Hashable,dict],
            key_new: Optional[Hashable]=None,
            obj: Optional[dict]=None,
            case_name: Optional[str]=None,
            *,
            overwrite: bool=False,
            keep_order: bool=False,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ) ->dict:
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        new = d.d_rename(obj, key, key_new,
                        case_name=case_name, overwrite=overwrite,
                        inplace=False, factory=dict)
        return d._dict_updator(obj, new, inplace=inplace, factory=factory)


    rename.__doc__ = _get_docstring(d.d_rename, 'obj')


    def get_keys(self,
            obj: Optional[dict]=None,
            *,
            output_for: Optional[DictKeyType]=None,
            separator: str=Default_Keypath_Separator,
        ) -> list:
        obj = obj if obj or obj == {} else self
        return d.get_keys(obj, output_for=output_for,
                               separator=separator)

    get_keys.__doc__ = _get_docstring(d.get_keys, 'obj')

    def get_values(self,
            keys: Union[Hashable, Sequence],
            obj: Optional[Union[dict, Sequence]] = None,
            *,
            wild: bool=False,
            with_keys: bool=False,
            verbatim: bool=False,
        ) -> Union[list, dict]:
        obj = obj if obj or obj == {} else self
        return d.get_values(obj, keys,
                        wild=wild, with_keys=with_keys, verbatim=verbatim)

    get_values.__doc__ = _get_docstring(d.get_values, 'obj')

    def get_items(self,
            loc: Hashable,
            value: Optional[Any]=None,
            obj: Optional[dict]=None,
            func: Optional[Callable]=None,
            *,
            separator: Optional[str]=None,
            factory: Optional[Type[dict]]=None,
        ):
        separator = separator or self.keypath_separator
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        new = factory(obj)
        new = d.get_items(new, loc, value, func=func,
                          separator=separator, factory=factory)
        return new

    get_items.__doc__ = _get_docstring(d.get_items, 'obj')

    def pop_items(self,
            loc: Hashable,
            value: Optional[Any]=None,
            obj: Optional[dict]=None,
            func: Optional[Callable]=None,
            *,
            separator: Optional[str]=None,
            factory: Optional[Type[dict]]=None,
        ):
        separator = separator or self.keypath_separator
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        item = d.pop_items(obj, loc, value, func=func,
                          separator=separator, factory=factory)
        return item

    pop_items.__doc__ = _get_docstring(d.pop_items, 'obj')

    def del_items(self,
            loc: Union[Hashable, list, tuple],
            obj: Optional[dict]=None,
            *,
            separator: Optional[str]=None,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ):
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        separator = separator or self.keypath_separator

        return d.del_items(obj, loc, separator=separator,
                                inplace=inplace, factory=factory)

    del_items.__doc__ = _get_docstring(d.del_items, 'obj')

    def set_items( self,
            loc: Union[str, Sequence],
            value: Any,
            obj: Optional[Union[dict, Sequence]]=None,
            func: Optional[Callable]=None,
            *,
            separator: Optional[str]=None,
            factory: Optional[Type[dict]]=None,
        ):
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        separator = separator or self.keypath_separator

        d.set_items(obj, loc, value, func=func,
                          separator=separator, factory=factory)

    set_items.__doc__ = _get_docstring(d.set_items, 'obj')

    def find( self,
            keys: Union[list,Hashable],
            default: Optional[Any]=None,
            obj: Optional[dict]=None,
            *,
            first_one: bool=True
        ):
        obj = obj if obj or obj == {} else self
        return d.d_find(obj, keys, default, first_one)


    find.__doc__ = _get_docstring(d.d_find, 'obj')

    def flatten( self,
            obj: Optional[dict]=None,
            *,
            separator: str=Default_Keypath_Separator,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ) -> dict:
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        new =  d.d_flatten(obj, separator, inplace=False, factory=factory)
        return d._dict_updator(obj, new, inplace=inplace, factory=factory)

    flatten.__doc__ = _get_docstring(d.d_flatten, 'obj')

    def unflatten( self,
            obj: Optional[dict]=None,
            default: Optional[Any]=None,
            *,
            separator: str=Default_Keypath_Separator,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ) -> dict:
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        new =  d.d_unflatten(obj, default, separator,
                                  inplace=False, factory=factory)
        return d._dict_updator(obj, new, inplace=inplace, factory=factory)

    unflatten.__doc__ = _get_docstring(d.d_unflatten, 'obj')


    def keylists( self,
            obj: Optional[dict]=None,
            indexes: bool=False,
        ) -> list:
        obj = obj if obj or obj == {} else self
        keylists = []
        for k in d.keylists(obj, indexes):
            keylists.append(Keylist(k, separator=self.keypath_separator))
        return keylists


    keylists.__doc__ = _get_docstring(d.keylists, 'obj')

    def keypaths( self,
            obj: Optional[dict]=None,
            indexes: bool=False,
            *,
            separator: Optional[str]=None,
        ) -> list:
        obj = obj if obj or obj == {} else self
        separator = separator or self.keypath_separator
        kps = []
        for kp in d.keypaths(obj, indexes=indexes, separator=separator):
            kps.append(Keypath(kp, separator=separator))
        return kps

    keypaths.__doc__ = _get_docstring(d.keypaths, 'obj')

    def search( self,
            query: Pattern,
            obj: Optional[dict]=None,
            *,
            search_for: DictItemType=DictItem.KEY,
            exact: bool=False,
            ignore_case: bool=False
        ):
        obj = obj if obj or obj == {} else self
        return d.d_search(obj, query,
                          search_for=search_for,
                          exact=exact,
                          ignore_case=ignore_case)

    search.__doc__ = _get_docstring(d.d_search, 'obj')

    def sort( self,
            obj: Optional[dict]=None,
            *,
            sort_by: DictItemType=DictItem.KEY,
            reverse: bool=False,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ):
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        return d.d_sort(obj, sort_by, reverse=reverse,
                           inplace=inplace, factory=factory)
    sort.__doc__ = _get_docstring(d.d_sort, 'obj')


    def subset( self,
            keys: Union[str, list, tuple, Hashable],
            default: Optional[Any]=None,
            obj: Optional[dict]=None,
            *,
            use_keypath: bool=False,
            separator: Optional[str]=None,
            inplace: bool=False,
            factory: Optional[Type[dict]]=None,
        ):
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        separator = separator or self.keypath_separator
        return d.d_subset(obj, keys, default=default,
                        use_keypath=use_keypath,
                        separator=separator,
                        inplace=inplace, factory=factory)

    subset.__doc__ = _get_docstring(d.d_subset, 'obj')

    def swap( self,
            key1: Hashable,
            key2: Hashable,
            obj: Optional[dict]=None,
            *,
            inplace: bool=False,
            factory: Optional[dict]=None
        ) ->Optional[dict]:
        obj = obj if obj or obj == {} else self
        factory = factory or type(self)
        return d.d_swap(obj, key1, key2,
                        inplace=inplace, factory=factory)

    swap.__doc__ = _get_docstring(d.d_swap, 'obj')


    def traverse( self,
            callback: Callable,
            obj: Optional[Union[dict, list, tuple]]=None,
            parents: list=[],
            *args: Any,
            **kwargs: Any,
        ):
        obj = obj if obj or obj == {} else self
        return d.d_traverse(obj, callback, parents, *args, **kwargs)

    traverse.__doc__ = _get_docstring(d.d_traverse, 'obj')


    def unique( self,
            obj: Optional[dict]=None,
        ) -> list:
        obj = obj if obj or obj == {} else self
        return d.d_unique(obj)

    unique.__doc__ = _get_docstring(d.d_unique, 'obj')



class iList(list):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, '_attrs', aDict())

    @property
    def attrs(self):
        return self._attrs

    def get_attrs(self, name: Optional[str]=None, default=None):
        if not name:
            return self._attrs.to_dict()
        else:
            return self._attrs.get(name, default)

    def _check_frozen(self,
            thrown_error: bool=False,
            msg: str='frozen object cannot be modified.',
            ):
        if self._attrs._check_frozen(thrown_error=False):
            if thrown_error:
                raise AttributeError( f"{self.__class__.__name__} {msg}" )
            else:
                return True
        else:
            return False

    def __add__(self, other): # self + other
        """
        Create new list that is Concatenate this list with another list.
        """
        self._check_frozen(thrown_error=True)
        return super().__add__(other)

    def __radd__(self, other): # self + other
        """
        Concatenate this list with another list
        """
        self._check_frozen(thrown_error=True)
        return super().__add__(other)

    def __iadd__(self, other):  # self += other
        """
        Concatenate this list with another list in-placed.
        """
        self._check_frozen(thrown_error=True)
        return super().__iadd__(other)

    def __imul__(self, other):  # self *= other
        """
        Return value*self.
        """
        self._check_frozen(thrown_error=True)
        return super().__imul__(other)

    def __and__(self, other):  # self & other
        self._check_frozen(thrown_error=True)
        return list(set(self).intersection(other))

    def __rand__(self, other):  # self & other
        self._check_frozen(thrown_error=True)
        return list(set(other).intersection(self))

    def __or__(self, other):  # self | other
        new = list(set([*self, *other]))
        return new

    def __xor__(self, other):  # self ^ other
        new = list(set(self).symmetric_difference(set(other)))
        return new

    def __sub__(self, other): # self - other
        return list(set(self).difference(other))

    def __rsub__(self, other): # self - other
        return list(set(other).difference(self))

    def __setitem__(self, index, val):
        self._check_frozen(thrown_error=True)
        return super().__setitem__(index, val)

    def __setattr__(self, name, val):
        self._check_frozen(thrown_error=True)
        self._attrs[name] = val

    def __getattr__(self, item):
        if item in self._attrs:
            return self._attrs[item]
        else:
            self.__missing__(item)

    def __missing__(self, name):
        raise KeyError(f'{name} not found.')

    def __delattr__(self, name):
        self._check_frozen(thrown_error=True)
        del self._attrs[name]

    def __hash__(self):
        if self._check_frozen(thrown_error=False):
            return hash(frozenset(self.__repr__()))
        else:
            raise AttributeError('unhashable not frozen object.')

    def __reversed__(self):
        """ Create new list revesesed items.  """
        for element in self[::-1]:
            yield element

    def __repr__(self, verbose: bool=False):
        str_value = str(list(self))
        return f'{self.__class__.__name__}({str_value})'

    def append(self, other):
        """
        Append object to the end of the list.
        """
        self._check_frozen(thrown_error=True)
        super().append(other)

    def reverse(self):
        """ Reverse *IN PLACE* """
        self._check_frozen(thrown_error=True)
        super().reverse()

    def clear(self):
        """
        Remove all items from list.
        """
        self._check_frozen(thrown_error=True)
        super().clear()

    def copy(self, freeze: bool=False):
        """
        Creaate the new list that is copied this list.
        this method could not copy self.attrs..
        if pass `freeze=True`, return frozen list object.
        """

        new = type(self)([x for x in self])
        new.freeze(freeze)
        return new

    def clone(self, empty: bool=False):
        """
        Creaate the new list that is cloned this list.
        this method copy self.attrs.
        if pass `empty=True`, keep self.attrs but list will be cleared.
        """

        if empty:
            new = type(self)([])
        else:
            new = type(self)([x for x in self])

        new.attrs.from_dict(self.attrs.to_dict(), inplace=True)
        new.attrs.freeze(self.attrs._check_frozen(thrown_error=False))
        return new

    def extend(self, obj: Iterable):
        """
        Extend list by appending elements from the iterable.
        """
        self._check_frozen(thrown_error=True)
        super().extend(obj)

    def insert(self, index: inte, obj: Iterable):
        """
        Insert object before index
        """
        self._check_frozen(thrown_error=True)
        super().insert(index, obj)

    def pop(self, index: int=-1):
        """
        Remove and return item at index (default last).
        Raises IndexError if list is empty or index is out of range.
        """
        self._check_frozen(thrown_error=True)
        return super().pop(index)

    def remove(self, val: Any):
        """
        Remove first occurrence of value.
        Raises ValueError if the value is not present.
        """
        self._check_frozen(thrown_error=True)
        return super().remove(val)

    def without(self, *items):
        """ Create new list without items and return iterable.  """
        return list(set(self).difference(*items))

    def find(self,
            val: Union[Any, list, tuple],
        ) -> list:
        """
        Return the list of index that found val in list.
        otherwise return None
        """
        if _type.is_list_or_tuple(val):
            found = [ i for v in val for i, x in enumerate(self) if x == v ]
        else:
            found = [ i for i, x in enumerate(self) if x == val ]

        return found if found else None

    def replace(self,
            old: Any,
            new: Any,
            func: Optional[Callable]=None,
        ) ->list:
        """
        Return a new list that has new instead of old.
        if old is not found, it will raise an ItemNotFountError.
        callback function will be called as follows.
            `func(index, old, new)`
        """
        indexes = self.find(old)
        if indexes is None:
            raise ValueError(f'Item {old} not found in list.')

        func = func if func else lambda x, y, z: new
        new_list = list(self)
        for i in indexes:
            new_list[i] = func(i, old, new)

        return new_list

    def sort(self, key: Optional[Callable]=None, reverse: bool=False):
        """
        Sort the list in ascending order and return None.
        The sort is in-place (i.e. the list itself is modified)
        and stable (i.e. the order of two equal elements is maintained).
        If a key function is given,
        apply it once to each list item and sort them,
        ascending or descending, according to their function values.
        The reverse flag can be set to sort in descending order.
        """
        self._check_frozen(thrown_error=True)
        super().sort(key=key, reverse=reverse)

    def freeze(self, shouldFreeze=True):
        self._attrs.freeze(shouldFreeze)

    def unfreeze(self):
        self._attrs.unfreeze()