# -*- coding: utf-8 -*-

import re
from typing import Any, Dict, Union, Optional, Hashable
from collections.abc import Mapping
from functools import partial
from unicodedata import normalize
#
from multimethod import multidispatch, multimethod
from datajuggler.validator import (
    DictItem, DictItemType, validate_DictItem, validate_DictItem
)

from datajuggler.strings import substr
from datajuggler.validator import TypeValidator as _type

try:
    import pandas as pd
    import numpy as np
    pd_NA = pd.NA
    np_NA = np.nan

    def add_df(
            values: list,
            columns: list,
            omits: list=[]
        ) ->pd.DataFrame:
        """Add values to dataframe"""

        if not pandas_installed:
            raise NotImplementedError("'pandas' module is not installed.")

        if omits:
            values = omit_values(values,omits)
            columns = omit_values(columns,omits)

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

        if not pandas_installed:
            raise NotImplementedError("'pandas' module is not installed.")

        diff_df = pd.concat([df1,df2]).drop_duplicates(keep=False)
        diffs = len(diff_df)
        return diffs

        pandas_installed = True

except ImportError:
    pd_NA = None
    np_NA = None
    pandas_installed = False

    def add_df(
            values: list,
            columns: list,
            omits: list=[]
        ):
        """Add values to dataframe"""
        raise NotImplementedError("'pandas' module is not installed.")

    def df_compare(
            df1,
            df2,
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
        raise NotImplementedError("'pandas' module is not installed.")


class StrCase(object):

    def __init__(self, *args: Any):
        self.depth = 0
        self.__NULL_VALUES = {"", None, np_NA, pd_NA}

        self.supported_case = {
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
        }

        if len(args) == 0:
            self.__origin = None
        elif len(args) == 1:
            self.__origin = self.__validate(args[0])
        else:
            raise TypeError(
                'Expected at most 1 arguments, got {}.'.format(len(args)))

    def __validate(self,
            val: Union[str, list, dict]
        )-> Union[str, list, dict]:

        if _type.is_str(val) or _type.is_list(val) or _type.is_dict(val):
            return val
        else:
            raise TypeError( 'Expected str or list, dict objects, got {}.'
                             .format(type(val)) )

    @property
    def origin(self):
        return self.__origin

    @origin.setter
    def origin(self, val):
        self.__origin = self.__validate(val)

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
            replace_for: DictItemType
           ) -> dict:

        self.depth += 1
        if replace_for == DictItem.KEY:
            convdict = { self.convert_case(case, x, replace_for ):y
                         for x, y in data.items() }
        elif replace_for == DictItem.VALUE:
            convdict = { x:self.convert_case(case, y, replace_for )
                         for x, y in data.items() }
        self.depth -= 1
        return convdict

    def convert_case(self,
            case: str='snake',
            data: Optional[Union[list,str, dict]] = None,
            replace_for: DictItemType = DictItem.VALUE
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

        validate_DictItem(replace_for, thrown_error=True)

        if data is None:
            if self.depth == 0:
                if self.__origin:
                    data = self.__origin
                else:
                    raise ValueError('Expected at most 1 objets')
            else:
                return data

        if _type.is_str(data):
            return self.__convert_case_str(case, data)
        elif _type.is_list(data):
            self.depth += 1
            convobj = [ self.convert_case(case, x, replace_for)
                        for x in data ]
            self.depth -= 1
            return convobj
        elif _type.is_dict(data):
            return self.__convert_case_dict(case, data, replace_for)
        else:
            return data

    def __str__(self) -> str:
        return str(self.origin)

    def __repr__(self) -> str:
        if _type.is_str(self.__origin):
            return 'StrCase("{}")'.format(self.__origin)
        else:
            return 'StrCase({})'.format(self.__origin)

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

def rename_duplicates(
        data: list,
        separator: str = '_',
        format = "{:02}"
    ) -> list:
    """Rename duplicated strings to append a number at the end."""

    counts: Dict[str, int] = {}

    if _type.is_list(data):
        for i, val in enumerate(data):
            if _type.is_list(val):
                new_val = rename_duplicates(val)
                data[i] = new_val
            elif _type.is_str(val):
                cur_count = counts.get(val, 0)
                if cur_count > 0:
                    data[i] = ( "{}{}".format(val, separator)
                                + format.format(cur_count) )
                counts[val] = cur_count + 1
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

   for n in range(len(values)):
       for old, new in replace.items():
           values[n] = substr(old, new,  values[n], ignore_case=ignore_case)
   if not inplace:
       return values

@replace_values.register(dict, dict)
def _replace_values_dict_multi(
        values: dict,
        replace: dict,
        *,
        ignore_case: bool=False,
        inplace: bool=False,
        replace_for: DictItemType = DictItem.VALUE
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

    def replace_val(value, replace, ignore_case):
       for old, new in replace.items():
           if ignore_case :
               if value.lower() == old.lower():
                   return new
               else:
                   value
           else:
               if value == old:
                   return new
               else:
                   value
       return value

    validate_DictItem(replace_for, thrown_error=True)

    mapper={}
    if replace_for == DictItem.KEY:
       keys = [ replace_val(x, replace, ignore_case)
                for x in values.keys() ]
       vals = list(values.values())
    elif replace_for == DictItem.VALUE:
       keys = list(values.keys())
       vals = [replace_val(x, replace, ignore_case)
               for x in values.values() ]
    else:
       return None

    workdict = dict(zip(keys, vals))

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

   for n in range(len(values)):
       for old in replace_from:
           values[n] = substr( old, replace_to, values[n],
                                    ignore_case=ignore_case)
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
           if _type.is_str(values[n]) and ignore_case:
               new = replace_values(values[n], [old], replace_to)
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

   for old in replace_from:
       if _type.is_str(old):
           if not _type.is_str(replace_to):
               replace_to = str(replace_to)
           values = substr(old, replace_to, values, ignore_case=ignore_case)
       else:
           if values == old:
               values = replace_to

   return values

@replace_values.register(str, dict)
def _replace_values_text_multi(
        values: str,
        replace: dict,
        *,
        ignore_case: bool=False,
        **kwargs: Any,
    )-> Hashable:

   for old, replace_to in replace.items():
       if _type.is_str(old):
           if not _type.is_str(replace_to):
               replace_to = str(replace_to)
           values = substr(old, replace_to, values,
                                ignore_case =ignore_case)
       else:
           if values == old:
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


def parse_slice(expr: str):
    """ Parse slice expression and return tupele. """
    def to_piece(s):
        try:
            return s and int(s) or None
        except:
            return None
    pieces = list(map(to_piece, expr.split(':')))
    if len(pieces) == 1:
        return slice(pieces[0], pieces[0] + 1)
    else:
        return slice(*pieces)
