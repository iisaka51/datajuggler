import re
from typing import (
    Any, Dict, Union, Optional, Hashable, Iterable, Sequence,
    Literal, get_args
)
from collections.abc import Mapping
from collections import OrderedDict
from unicodedata import normalize
from enum import Enum
#
import numpy as np
import pandas as pd
from multimethod import multidispatch, multimethod

__all__ = [
    "urange",
    "uDict",
    "iDict",
    "aDict",
    "StrCase",
    "is_alpha",
    "is_alnum",
    "ordereddict_to_dict",
    "change_dict_keys",
    "omit_values",
    "replace_values",
    "add_df",
    "df_compare",
    "ReplaceFor",
    "ReplaceForType",
    "split_chunks",
    "rename_duplicates",
    "remove_accents",
]

class ReplaceFor(str, Enum):
  KEY = "key"
  VALUE = "value"

ReplaceForType = Literal[ReplaceFor.KEY, ReplaceFor.VALUE]

class urange(object):
    def __init__(self,
        *args: int,
        **kwargs: Any
    ):
        """Return an object that produces a sequence of integes

        range(stop) -> range object
        range(start, stop[, step]) -> range object
        range(start, stop[, func]) -> range object

        from start (inclusive) to stop (exclusive) by step.

          range(i, j) produces i, i+1, i+2, ..., j-1.
          range(i, j, k) produces i, i+k, i+2, ..., j-k.

        start defaults to 0, and stop is omitted!

          range(4) produces 0, 1, 2, 3.

        These are exactly the valid indices for a list of 4 elements.
        When step is given, it specifies the increment (or decrement).

        if set step as callable, pass parameter current value.
        So, you should define as following function.
          def step(val: int)->int:
              # something to do for val
              return val
        """

        if len(args) == 1:
            self._i = 0
            self._end = args[0]
            self._step = kwargs.get('step', 0)
        elif len(args) == 2:
            self._i = args[0]
            self._end = args[1]
            self._step = kwargs.get('step', 0)
        elif len(args) >= 3:
            self._i = args[0]
            self._end = args[1]
            self._step = args[2]
        else:
            self._i = kwargs.get('start', 0)
            self._end = kwargs.get('end')
            self._step = kwargs.get('step', 0)

        self.step_callable = callable(self._step)
        if self._i <= self._end:
            self.ascending = True
            if self._step == 0:
                self._step = 1
            elif not self.step_callable and (self._step < 0):
                raise ValueError(
                      'Step must be postitive value for ascending orders.')
        else:
            self.ascending = False
            if self._step == 0:
                self._step = -1
            elif not self.step_callable and (self._step > 0):
                raise ValueError(
                      'Step must be negative value for descending orders.')

    def __iter__(self):
        return self

    def __next__(self):
        if self.ascending:
            if self._i >= self._end:
                raise StopIteration
        else:
            if self._i <= self._end:
                raise StopIteration

        value = self._i
        if self.step_callable:
            self._i = self._i + self._step(self._i)
        else:
            self._i = self._i + self._step
        return value


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


def is_alpha(word: str)-> bool:
    """ Check word is alphabet.
    Parameters
    ----------
    word: str
        any string

    Returns
    -------
    validate result: bool
        if all characters of word, return ``True`` otherwise return ``False``
    """
    try:
        return word.encode('ascii').isalpha()
    except:
        return False


def is_alnum(word: str)-> bool:
    """ Check word is alphabet and digits.
    :param word: str
        any string

    "returns:  validate result
        if all characters of word, return ``True`` otherwise return ``False``
    """
    try:
        return word.encode('ascii').isalnum()
    except:
        return False

def remove_accents(self, data: Any) -> Any:
    """Return the normal form for a Unicode string
       using canonical decomposition."""

    if isinstance(data, str):
        data = ( normalize("NFD", data)
                 .encode("ascii", "ignore")
                 .decode("ascii") )
    return data

def rename_duplicates(
        data: list,
        separator: str = '_',
        format = "{:02}"
    ) -> list:
    """Rename duplicated strings to append a number at the end."""

    counts: Dict[str, int] = {}

    if isinstance(data, list):
        for i, val in enumerate(data):
            if isinstance(val, list):
                new_val = rename_duplicates(val)
                data[i] = new_val
            elif isinstance(val, str):
                cur_count = counts.get(val, 0)
                if cur_count > 0:
                    data[i] = ( "{}{}".format(val, separator)
                                + format.format(cur_count) )
                counts[val] = cur_count + 1
    return data

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


@multidispatch
def replace_values( obj: Any, *arg: Any, **kwargs: Any) ->Any:
    """dispatch function replace_values """
    if obj:
        return obj

@replace_values.register(list, dict)
def _replace_values_multi(
        values: list,
        replace: dict,
        *,
        ignore_case: bool=False,
        inplace: bool=False,
        **kwargs: Any,
    )-> Optional[list]:

        if not inplace:
            values = values.copy()

        flags = [ re.UNICODE, ( re.IGNORECASE + re.UNICODE) ]
        for n in range(len(values)):
            for old, new in replace.items():
                values[n] = re.sub(old, new,  values[n],
                                   flags = flags[ignore_case])
        if not inplace:
            return values

@replace_values.register(dict, dict)
def _replace_values_dict_multi(
        values: dict,
        replace: dict,
        *,
        ignore_case: bool=False,
        inplace: bool=False,
        replace_for: ReplaceForType = ReplaceFor.VALUE
    )-> Optional[list]:
        """replace values of dict
        Parameters
        ----------
        values: dict
           to replace data
        replace: dict
           replace map. { old: new,....}
        replace_for: avaiable 'key', 'value'.
           If replace_for set 'value', replace 'value' of dict.
           If replace_value set 'key', replace 'key' of dict.
           default is 'value'
        """
        if replace_for not in get_args(ReplaceForType):
            raise ValueError("replace_for must be 'key' or 'value'.")

        if replace_for == ReplaceFor.KEY:
            mapper={}
            for key, value in list(values.items()):
                for old, new in replace.items():
                    new_key = replace_values(key, [old], new,
                                             ignore_case=ignore_case)
                    if new == new_key:
                        mapper[key] = new_key

            workdict = values.copy()
            for key, value in list(workdict.items()):
                workdict[mapper.get(key, key)] = workdict.pop(key)

        if replace_for == ReplaceFor.VALUE:
            workdict = values.copy()
            mapper={}
            for key, value in list(workdict.items()):
                for old, new in replace.items():
                    if isinstance(value, str) and ignore_case:
                        new_val = replace_values(value, [old], new,
                                         ignore_case=ignore_case)
                        if new == new_val:
                            mapper[value] = new_val
                    else:
                        if value == old:
                            mapper[value] = new

            for key, value in list(workdict.items()):
                workdict[key] = mapper.get(value, workdict.pop(key))

        if inplace:
            values.update(workdict)
        else:
            return workdict

@replace_values.register(list, list, str)
def _replace_values_single_str(
        values: list,
        replace_from: list,
        replace_to: str,
        *,
        ignore_case: bool=False,
        inplace: bool=False,
        **kwargs: Any,
    )-> Optional[list]:

        if not inplace:
            values = values.copy()

        flags = [ re.UNICODE, ( re.IGNORECASE + re.UNICODE) ]
        for n in range(len(values)):
            for old in replace_from:
                values[n] = re.sub( old, replace_to, values[n],
                                   flags = flags[ignore_case])
        if not inplace:
            return values

@replace_values.register(list, list, Any)
def _replace_values_single_obj(
        values: list,
        replace_from: list,
        replace_to: Any,
        *,
        ignore_case: bool=False,
        inplace: bool=False,
        **kwargs: Any,
    )-> Optional[list]:

        if not inplace:
            values = values.copy()

        for n in range(len(values)):
            for old in replace_from:
                if values[n] ==  old:
                    values[n] = new

        if not inplace:
            return values


@replace_values.register(str, list, Hashable)
def _replace_values_text(
        values: str,
        replace_from: list,
        replace_to: Hashable,
        *,
        ignore_case: bool=False,
        **kwargs: Any,
    )-> Hashable:

        flags = [ re.UNICODE, ( re.IGNORECASE + re.UNICODE) ]
        for old in replace_from:
            if isinstance(old, str) and isinstance(replace_to, str):
                values = re.sub( old, replace_to, values,
                             flags = flags[ignore_case])
            elif old == origin:
                values = replace_to

        return values


@replace_values.register(Union[int, float], list, Any)
def _replace_values_number(
        values: Union[int, float],
        replace_from: list,
        replace_to: Any,
        **kwargs: Any,
    )-> str:
        if values in replace_from:
            return replace_to
        else:
            return values


@multidispatch
def omit_values( obj: Any, *arg: Any, **kwargs: Any) ->Any:
    """dispatch function replace_values """
    if obj:
        return obj

@omit_values.register(list, list)
def _omit_values_multi(
        values: list,
        omits: list,
        *,
        inplace: bool=False,
        ignore_case: bool=False,
        drop: bool=False
    )-> list:
        if not inplace:
            values = values.copy()

        values =  replace_values(values, omits, '', ignore_case=ignore_case)
        if drop:
            count = values.count('')
            for _ in range(count):
                values.remove('')

        if not inplace:
            return values

@omit_values.register(str, list)
def omit_values_single(
        values: str,
        omits: list,
        *,
        ignore_case: bool=False,
    )-> str:
        return replace_values(values, omits, '', ignore_case=ignore_case)


def add_df(
        values: list,
        columns: list,
        omits: list=[]
    ) ->pd.DataFrame:

        if omits:
            values = self.omit_chars(values,omits)
            columns = self.omit_chars(columns,omits)

        # Since Pandas 1.3.0
        df = pd.DataFrame(values,index=columns)._maybe_depup_names(columns)
        self.df = pd.concat([self.df,df.T])

def df_compare(
        df1: pd.DataFrame,
        df2: pd.DataFrame,
    ) -> int:
    """ Compare DataFrame
    Parameters
    ----------
    df1: pd.DataFrame, df2: pd.DataFrame
        any DataFrame to compare

    Returns
    -------
    validate result: Union[bool,int]
    """

    diff_df = pd.concat([df1,df2]).drop_duplicates(keep=False)
    diffs = len(diff_df)
    return diffs

@multidispatch
def split_chunks( *args: Any, **kwargs: Any ):
    """ dispatch function split_chunks """
    raise TypeError('Invalid Type')

@split_chunks.register
def _split_chunks_list(
        data: list,
        chunk_size: int,
        fill_na: bool=True,
        na_value: Optional[Union[int,str,float]]=None
    ) ->list:
    """Return split into even chunk_size elements for iterable
    Parameters
    ----------
    data: list
        to split itrtable ojects. i.e.: list, tuple, dict, set.
    chunk_size: int
        the size of chunk list.
    fill_na: bool
        subset of a list does not fit in the size of the defined chunk,
        fillers need to be inserted in the place of the empty element holders.
        fillers is able to set `na_value`.
    na_value: int, str, default is `None`.

    Returns
    -------
        splited list
    """

    iterable = iter(data)
    for x in range(0, len(data), chunk_size):
        chunk_data = list()
        for _ in urange(chunk_size):
            try:
                chunk_data.append(next(iterable))
            except StopIteration:
                break

        if fill_na and (len(chunk_data) < chunk_size):
            chunk_data += [ na_value
                            for y in urange(chunk_size-len(chunk_data))]
        yield chunk_data

@split_chunks.register
def _split_chunks_tuple(
        data: tuple,
        chunk_size: int,
        fill_na: bool=True,
        na_value: Optional[Union[int,str,float]]=None
    ) ->list:
    """Return split into even chunk_size elements for iterable
    Parameters
    ----------
    data: tuple
        to split itrtable ojects. i.e.: list, tuple, dict, set.
    chunk_size: int
        the size of chunk list.
    fill_na: bool
        subset of a list does not fit in the size of the defined chunk,
        fillers need to be inserted in the place of the empty element holders.
        fillers is able to set `na_value`.
    na_value: int, str, default is `None`.

    Returns
    -------
        splited list
    """

    iterable = iter(data)
    for x in range(0, len(data), chunk_size):
        chunk_data = list()
        for _ in urange(chunk_size):
            try:
                chunk_data.append(next(iterable))
            except StopIteration:
                break

        if fill_na and (len(chunk_data) < chunk_size):
            chunk_data += [ na_value
                            for y in range(chunk_size-len(chunk_data))]
        yield tuple(chunk_data)


@split_chunks.register
def _split_chunks_dict(
        data: dict,
        chunk_size: int,
        *args: Any,
        **kwargs: Any,
    ) ->list:
    """Return split into even chunk_size elements for iterable
    Parameters
    ----------
    data: dict
        to split dict ojects.
    chunk_size: int
        the size of chunk list.
    na_value: int, str, default is `None`.

    Returns
    -------
        splited list
    """

    iterable = iter(data)
    for x in range(0, len(data), chunk_size):
        chunk_data = dict()
        for _ in urange(chunk_size):
            try:
                key = next(iterable)
                chunk_data[key] = data[key]
            except StopIteration:
                break

        yield chunk_data

@split_chunks.register
def _split_chunks_str(
        data: str,
        chunk_size: int,
        *args: Any,
        **kwargs: Any,
    ) ->list:
    """Return split into even chunk_size elements for iterable
    Parameters
    ----------
    data: str
        to split dict ojects.
    chunk_size: int
        the size of chunk list.
    na_value: int, str, default is `None`.

    Returns
    -------
        splited str list
    """

    iterable = iter(data)
    for x in range(0, len(data), chunk_size):
        chunk_data = ""
        for _ in urange(chunk_size):
            try:
                 chunk_data += next(iterable).replace('\n', '')
            except StopIteration:
                break

        yield chunk_data


class StrCase(object):

    def __init__(self, *args: Any):
        self.depth = 0
        self.__NULL_VALUES = {"", None, np.nan, pd.NA}

        self.supported_case = iDict({
            "snake": {
                'sample': 'convert_case',
                'separaator': '_',
                'splitor': self.split_strip_string,
                'convertor': lambda x: "_".join(x).lower() },
            "kebab": {
                'sample': 'convert-case',
                'separaator': '-',
                'splitor': self.split_strip_string,
                'convertor': lambda x: "-".join(x).lower() },
            "camel": {
                'sample': 'convertCase',
                'separaator': '',
                'splitor': self.split_strip_string,
                'convertor': lambda x: x[0].lower() + "".join(w.capitalize() for w in x[1:]) },
            "pascal": {
                'sample': 'ConvertCase',
                'separaator': '',
                'splitor': self.split_strip_string,
                'convertor': lambda x:  "".join(w.capitalize() for w in x) },
            "const": {
                'sample': 'CONVERT_CASE',
                'separaator': '_',
                'splitor': self.split_strip_string,
                'convertor':  lambda x: "_".join(x).upper() },
            "sentence": {
                'sample': 'Convert case',
                'splitor': self.split_string,
                'convertor':  lambda x: " ".join(x).capitalize() },
            "title": {
                'sample': 'Convert Case',
                'separaator': ' ',
                'splitor': self.split_string,
                'convertor':  lambda x: " ".join(w.capitalize() for w in x) },
            "lower": {
                'sample': 'convert case',
                'separaator': ' ',
                'splitor': self.split_string,
                'convertor':  lambda x:  " ".join(x).lower() },
            "upper": {
                'sample': 'CONVERT CASE',
                'separaator': ' ',
                'splitor': self.split_string,
                 'convertor': lambda x: " ".join(x).upper() },
        })

        if len(args) == 0:
            self.__origin = None
        elif len(args) == 1:
            self.__origin = self.validate(args[0])
        else:
            raise TypeError(
                'Expected at most 1 arguments, got {}.'.format(len(args)))

    def validate(self,
            val: Union[str, list, dict]
        )-> Union[str, list, dict]:

        if ( isinstance(val, str)
             or isinstance(val, list)
             or isinstance(val, dict)
             ):
            return val
        else:
            raise TypeError( 'Expected str or list, dict objects, got {}.'
                             .format(type(val)) )

    @property
    def origin(self):
        return self.__origin

    @origin.setter
    def origin(self, val):
        self.__origin = self.validate(val)

    def show_supported_case(self, verbose=False):
        header = { "case":  "sample" }
        case_sample = dict(header,
           **{ case: "{}".format(self.supported_case[case]['sample'])
               for case in self.supported_case.keys() } )
        if verbose:
            print(case_sample)
        return case_sample

    @classmethod
    def split_strip_string(cls, string: str) -> list:
        """Split the string into separate words and strip punctuation."""
        string = re.sub(r"[!()*+\,\-./:;<=>?[\]^_{|}~]", " ", string)
        string = re.sub(r"[\'\"\`]", "", string)

        return re.sub(
            r"([A-Z][a-z]+)",
            r" \1", re.sub(r"([A-Z]+|[0-9]+|\W+)",
            r" \1",
            string)
        ).split()

    @classmethod
    def split_string(cls, string: str) -> list:
        """Split the string into separate words."""
        string = re.sub(r"[\-_]", " ", string)

        return re.sub(
            r"([A-Z][a-z]+)",
            r" \1",
            re.sub(r"([A-Z]+)",
            r"\1", string)
        ).split()

    def __convert_case_str(self,
            case: str,
            data: str,
        )-> str:

        if data != '':
            if case in self.supported_case:
                words = self.supported_case[ case ]['splitor'](data)
                data = self.supported_case[ case ]['convertor'](words)
            else:
                raise ValueError(
                    'Invalid casename, '
                    'check class.show_supported_case().' )

        return data

    def __convert_case_dict(self,
            case: str,
            data: dict,
            replace_for: ReplaceForType
           ) -> dict:

        self.depth += 1
        if replace_for == ReplaceFor.KEY:
            convdict = { self.convert_case(case, x, replace_for ):y
                         for x, y in data.items() }
        elif replace_for == ReplaceFor.VALUE:
            convdict = { x:self.convert_case(case, y, replace_for )
                         for x, y in data.items() }
        self.depth -= 1
        return convdict

    def convert_case(self,
            case: str='snake',
            data: Optional[Union[list,str, dict]] = None,
            replace_for: ReplaceForType = ReplaceFor.VALUE
        ) -> str:
        """Convert case style for obj.

        Parameters
        ----------
        case: str
            Preferred case type, i.e.:  (default: 'snake')
            check `.show_supported_case()`

        obj: Any
            convert case for data

        Returns:
        --------
        converted data: str
        """

        if replace_for not in get_args(ReplaceForType):
            raise ValueError("replace_for must be 'key' or 'value'.")

        if data is None:
            if self.depth == 0:
                if self.__origin:
                    data = self.__origin
                else:
                    raise ValueError('Expected at most 1 objets')
            else:
                return data

        if isinstance(data, str):
            return self.__convert_case_str(case, data)
        elif isinstance(data, list):
            self.depth += 1
            convobj = [ self.convert_case(case, x, replace_for)
                        for x in data ]
            self.depth -= 1
            return convobj
        elif isinstance(data, dict):
            return self.__convert_case_dict(case, data, replace_for)
        else:
            return data

    def __str__(self) -> str:
        return str(self.origin)

    def __repr__(self) -> str:
        if isinstance(self.__origin, str):
            return 'StrCase("{}")'.format(self.__origin)
        else:
            return 'StrCase({})'.format(self.__origin)
