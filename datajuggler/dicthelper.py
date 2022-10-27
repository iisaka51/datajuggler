# -*- coding: utf-8 -*-

from __future__ import annotations
import copy

from typing import (
    Any, Dict, Union, Optional, Hashable, Iterable, Type, Sequence,
    Callable, Pattern, Match, Literal, get_args
    )

from collections import defaultdict

from datajuggler.utils import StrCase
from datajuggler.keys import (
     Keylist, Keypath, Default_Keypath_Separator, get_index_from_key
     )
from datajuggler.strings import is_match_string, searchstr
from datajuggler.validator import (
    DictAction, DictActionType, validate_DictAction,
    DictItem, DictItemType, validate_DictItem,
    DictKey, DictKeyType, validate_DictKey,
    )
from datajuggler.validator import TypeValidator as _type

def _dict_updator(
        d: dict,
        new: dict,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) -> Optional[dict]:

    if inplace:
        if id(d) != id(new):
            d.clear()
            d.update(new)
    else:
        if not factory or factory == dict:
            return new
        else:
            return factory(new)

def d_clean(
        obj: dict,
        strings=True,
        collections=True,
        *,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ):
    """Clean the current dict instance removing all empty values:
        None, '', {}, [], ().
    If strings or collections (dict, list, set, tuple) flags are False,
    related empty values will not be deleted.
    """

    def _is_empty(obj, key, strings, collections):
        value = obj.get(key, None)
        if not value:
            del_none = value is None
            del_string = strings and _type.is_str(value)
            del_collection = collections and _type.is_collection(value)
            return any([del_none, del_string, del_collection])

        return False

    new = obj if inplace else factory(obj)

    for key in list(obj.keys()):
        if _is_empty(new, key, strings, collections):
            del new[key]

    return _dict_updator(obj, new, inplace=inplace, factory=factory)

def d_clone(
        obj: dict,
        empty: bool=False,
        memo: Optional[dict]=None,
    ):
    """Return a clone (deepcopy) of the dict. """
    d = copy.deepcopy(obj, memo)
    if empty:
        d.clear()
    return d

def d_compare(
        d1: dict,
        d2: dict,
        *,
        keys: Optional[Union[Hashable, list, Keylist, Keypath]]=None,
        thrown_error: bool=False,
    ):
    """Compare tow dictionary with keys.
    and return  `True` when equal found values.
    otherwise return `False`.
    if not set keys, just compare two dictionaries,
    """

    def compare_values(d1: dict, d2: dict, keys):
        if _type.is_mapping(d1):
            d1_values = get_values(d1, keys)
            if _type.is_dict(d1_values):
                d1_values = list(d1_values.values())
        else:
            d1_values = d1

        if _type.is_mapping(d2):
            d2_values = get_values(d2, keys)
            if _type.is_dict(d2_values):
                d2_values = list(d2_values.values())
        else:
            d2_values = d2
        return d1_values == d2_values

    if not keys:
        keys = get_keys(d1)
        check_key = d1 == d2
    else:
        if _type.is_keylist_or_keypath(keys):
            d1 = get_values(d1, keys)
            d2 = get_values(d2, keys)
            keys = get_keys(d1)
        else:
            keys = [keys] if _type.is_str(keys) else keys

        check_key = True

    check_value = compare_values(d1, d2, keys)

    if check_key and check_value:
        return True
    else:
        if thrown_error:
            raise ValueError(f'{str(d1)} is not equal {str(d2)}.')
        return False

def d_counts(
        obj: dict,
        pattern: Union[Hashable, Sequence, Pattern],
        *,
        count_for: DictItemType=DictItem.KEY,
        wild: bool=False,
        verbatim: bool=False,
    ) ->Union[int, dict]:
    """Counts of keys or values
       if pass `wild=True`, match substr and ignore_case.
       if pass `verbatim=True`, counts as it is.
    """

    def _counts_of_keys(
            obj: dict,
            keys: Union[Hashable, Sequence],
            wild: bool=False,
            verbatim: bool=False,
        ) ->Union[int, dict]:
        """Counts of keys"""

        if _type.is_str(keys):
            keys = [keys]
            as_int=True
        else:
            as_int=False
        keys = list(keys) if not _type.is_list(keys) else keys

        counts = defaultdict(int)
        all_keys = get_keys(obj)
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

    def _counts_of_values(
            obj: dict,
            value: Any,
            wild: bool=False,
            verbatim: bool=False,
        ) ->Union[int, dict]:
        """Counts of values"""

        def deep_lookup(
                value: Any,
                obj: Union[dict, list, tuple],
                wild: bool=False,
                verbatim: bool=False,
            ):

            if _type.is_mapping(obj):
                for k, v in obj.items():
                    if _type.is_str(v):
                        if is_match_string(value, v, wild):
                            if verbatim:
                                yield (1, v)
                            else:
                                yield (1, value)

                    elif _type.is_mapping(v):
                        for c, v in deep_lookup(value, v,
                                          wild=wild, verbatim=verbatim):
                            yield (c, v)
                    elif _type.is_list_or_tuple(v):
                        for element in v:
                            for c, v in deep_lookup(value, element,
                                             wild=wild, verbatim=verbatim):
                                yield (c, v)
                    elif value == v:
                        yield (1, v)

            elif _type.is_list_or_tuple(obj):
                for element in obj:
                    for c, v in deep_lookup(value, element,
                                     wild=wild, verbatim=verbatim):
                        yield (c, v)

        counts = defaultdict(int)

        for c, v in deep_lookup(value, obj, wild, verbatim=verbatim):
            counts[v] += c

        return dict(counts)


    validate_DictItem(count_for, thrown_error=True)

    if count_for == DictItem.KEY:
        counts = _counts_of_keys(obj, pattern, wild=wild, verbatim=verbatim)
    else:
        counts = _counts_of_values(obj, pattern, wild=wild, verbatim=verbatim)
    return counts

def d_filter(
        predicate: Callable,
        obj: dict,
        *,
        factory: Type[dict]=dict,
    ):
    """ Create a new dictionary with filter items in dictionary by item.
    Predicate function receives key, value arguments
    and should return a bool value.
    If set `factory`, create instance of factory class.
    If set `True` to `inplace`, perform operation in-place.
    """

    new = dict()

    for key, val in obj.items():
        if predicate(key, val):
            new[key] = val

    return _dict_updator(obj, new, factory=factory)


def d_groupby(
        seq: list,
        key: Hashable,
        *,
        factory: Type[dict]=dict,
    ) -> dict:
    """
    A groupby operation involves some combination of splitting the object, applying a function, and combining the results. This can be used to group large amounts of data and compute operations on these groups.
    """
    if not _type.is_list(seq):
        raise ValueError("seq should be a list of dicts.")

    grouped = defaultdict(list)
    for element in seq:
        if not _type.is_mapping(element):
            raise ValueError("element should be a dict.")
        group = element.get(key)
        grouped[group].append(element.copy())

    return factory(grouped)


def d_invert(
        obj: dict,
        flat: bool=False,
        *,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) ->dict:
    """
    Return an inverted dict where values become keys and keys become values.
    Since multiple keys could have the same value, each value will be a list of keys.
    If pass `flat=True` each value will be a single value.
    (use this only if values are unique).
    """

    def _invert_item(
            obj: dict,
            key: Hashable,
            value: Any,
            flat: bool=False,
        ):
        if flat:
            obj.setdefault(value, key)
        else:
            obj.setdefault(value, []).append(key)


    def _invert_list(d, key, value, flat):
        for element in value:
            _invert_item(d, key, element, flat)

    new = factory()
    for key, value in obj.items():
        if _type.is_list_or_tuple(value):
            _invert_list(new, key, value, flat)
        else:
            _invert_item(new, key, value, flat)

    return _dict_updator(obj, new, inplace=inplace, factory=factory)


def d_map(
        func: Callable,
        obj: dict,
        *,
        map_for: Optional[DictItemType]=None,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) ->dict:
    """
    Create a new dictionary with apply function to keys/value of dictionary.
    if pass `map_for=None`  apply function to key and value. (default)
    if pass `map_for="key"`  apply function to key.
    if pass `map_for="value"`  apply function to value.
    If set `factory`, create instance of factory class.
    If set `True` to `inplace`, perform operation in-place.
    """

    new = obj if inplace else factory(obj)

    if not map_for:
        new = dict(map(func, new.items()))
    else:
        validate_DictItem(map_for, thrown_error=True)
        if map_for == DictItem.KEY:
            new = dict(zip(map(func, new.keys()), new.values()))
        else:
            new = dict(zip(new.keys(), map(func, new.values())))

    return _dict_updator(obj, new, inplace=inplace, factory=factory)

def d_merge(
        obj: dict,
        others: Union[dict, list, tuple],
        *,
        overwrite: bool=True,
        concat: bool=False,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) ->dict:
    """
    Merge one or more dictionary objects into obj.
    Sub-dictionaries keys will be merged toghether.
    If pass `overwrite=False`, existing values will not be overwritten.
    If pass `concat=True`, list values will be concatenated toghether.
    If set `factory`, create instance of factory class.
    If set `True` to `inplace`, perform operation in-place.
    """

    def _merge_dict(
        obj: dict,
        other: dict,
        overwrite: bool=True,
        concat: bool=False
        ):
        for key, value in other.items():
            _merge_item(obj, key, value, overwrite=overwrite, concat=concat)


    def _merge_item(
        obj: dict,
        key: Hashable,
        value: Any,
        overwrite: bool=True,
        concat: bool=False
        ):

        if key in obj:
            item = obj.get(key, None)
            if _type.is_mapping(item) and _type.is_mapping(value):
                _merge_dict(item, value, overwrite=overwrite, concat=concat)
            elif concat and _type.is_list_or_tuple(item):
                item += value
            elif overwrite:
                obj[key] = value
        else:
            obj[key] = value

    new = obj if inplace else factory(obj)

    others = list(others) if _type.is_tuple(others) else others
    others = [others] if not _type.is_list(others) else others
    for other in others:
        _merge_dict(new, other, overwrite=overwrite, concat=concat)

    return _dict_updator(obj, new, inplace=inplace, factory=factory)

def d_move(
        obj: dict,
        key_src: Union[str, list, dict],
        key_dest: Optional[Union[str, list]]=None,
        *,
        overwrite: bool=True,
        keep_order: bool=False,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) ->dict:
    """Create new dictionary which Move an item from key_src to key_dst.
    It can be used to rename a key.
    If key_dst exists and pass `overwrite=True`, its value will be overwritten.
    if pass `keep_order=True`, keep ordered of dictionary. (may be slow).
    If set `factory`, create instance of factory class.
    If set `True` to `inplace`, perform operation in-place.
    """

    def _move(obj, key_src, key_dest, overwrite, keep_order):
        if key_dest == key_src:
            return
        if key_dest in obj and not overwrite:
            raise KeyError(
                f"Invalid key: '{key_dest}', "
                "key already in dict and 'overwrite' is disabled."
            )

        if keep_order:
            keys = [ key_dest if x == key_src else x for x in obj.keys() ]
            vals = list(obj.values())
            obj.clear()
            obj.update(dict(zip(keys, vals)))
        else:
            obj[key_dest] = obj.pop(key_src)

    new = obj if inplace else factory(obj)

    if _type.is_dict(key_src) and key_dest is None:
        for key_src, key_dest in key_src.items():
            _move(new, key_src, key_dest, overwrite, keep_order)
    else:
        _move(new, key_src, key_dest, overwrite, keep_order)

    return _dict_updator(obj, new, inplace=inplace, factory=factory)


def d_rename(
        obj: dict,
        key: Union[Hashable,dict, list],
        key_new: Optional[Hashable]=None,
        case_name: Optional[str]=None,
        *,
        overwrite: bool=False,
        keep_order: bool=False,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) ->dict:
    """Create the new dictionary which is chnaged the key to key_new.
    if key as dictionary {key: key_new}, change key using mapping dictionary.
    If key_dst exists and pass `overwrite=True`, its value will be overwritten.
    if pass `keep_order=True`, keep ordered of dictionary. (may be slow).
    If set `factory`, create instance of factory class.
    If set `True` to `inplace`, perform operation in-place.
    """

    if case_name:
        c = StrCase()
        if case_name not in c.supported_case:
            supported_case = c.show_supported_case()
            raise ValueError(f'Invalid case_name.\n{supported_case}')

        if ( _type.is_list_or_tuple(key)
            or  _type.is_dict_keys(key) ) and not key_new:
            key = { x: c.convert_case(case_name, x) for x in key }
        elif _type.is_hashable(key) and not key_new:
            key_new = c.convert_case(case_name, key)
    else:
        if _type.is_list(key):
            raise TypeError('Invalid Type. Perhaps you forgot case_name. ')

    return d_move(obj, key, key_new,
                overwrite=overwrite, keep_order=keep_order,
                inplace=inplace, factory=factory)

def d_remove(
        obj: dict,
        keys: Union[list, tuple, Hashable],
        *,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ):
    """Create new dictionary which Remove multiple keys from the dict.
    It is possible to pass a single key or more keys (as list or *args).
    """

    new = obj if inplace else factory(obj)

    keys = [keys] if _type.is_str(keys) else keys
    keys = list(keys) if _type.is_tuple(keys) else keys
    for key in keys:
        new.pop(key)

    return _dict_updator(obj, new, inplace=inplace, factory=factory)

def d_nest(
    items: tuple,
    id_key: Union[str, list],
    parent_id_key: Union[str, list],
    children_key: Union[str, list],
    ) -> list:
    """Nest a list of dicts at the given key and return a new nested list
    using the specified keys to establish the correct items hierarchy.
    """

    def _nest_items(nested_items, item, id_key, children_key):
        children_items = nested_items.pop(item[id_key], [])
        item[children_key] = children_items

        for child_item in children_items:
            _nest_items(nested_items, child_item, id_key, children_key)


    if any( [id_key == parent_id_key,
            id_key == children_key,
            parent_id_key == children_key] ):
        raise ValueError("keys should be different.")

    nested_items = d_groupby(items, parent_id_key)
    root_items = nested_items.get(None, [])
    for item in root_items:
        _nest_items(nested_items, item, id_key, children_key)

    return nested_items.get(None)


def d_subset(
        obj: dict,
        keys: Union[str, list, tuple, Hashable],
        *,
        default: Optional[Any]=None,
        use_keypath: bool=False,
        separator: str=Default_Keypath_Separator,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ):
    """
    Return a dict subset for the given keys.
    It is possible to pass a single key or more keys (as list or *args).
    """

    def get_subset(obj, key, val, parents, search_key):
        nonlocal new, use_keypath, separator
        if key == search_key:
            if use_keypath:
                keypath = separator.join(parents)
                new[keypath] = val
            else:
                if not key in new:
                    new[key] = val
                else:
                    raise KeyError(f"Multiple keys founded.'{key}'")

    new = factory()

    keys = [keys] if _type.is_str(keys) else keys
    keys = list(keys) if not _type.is_list(keys) else keys

    for key in keys:
        d_traverse(obj, get_subset, parents=[], search_key=key)

    if len(new) == 0:
        new[key] = default

    return _dict_updator(obj, new, inplace=inplace, factory=factory)

def d_find(
        obj: dict,
        keys: Union[list,Hashable],
        default: Optional[Any]=None,
        first_one: bool=True,
        factory: Type[dict]=dict,
    ) -> Union[Any, dict]:
    """Return the match searching for the given keys.
    if pass `first_one=True`, return first matches.
    If no result found, default value is returned.
    """

    found = defaultdict(list)
    keys = [keys] if _type.is_str(keys) else keys
    keys = list(keys) if not _type.is_list(keys) else keys

    found = factory()
    val = default
    for key in keys:
        if key in obj:
            val =  obj.get(key, default)
            if first_one:
                return val
            else:
                found[key] = val
    return found if not first_one else default

def d_sort(
        obj: dict,
        sort_by: DictItemType=DictItem.KEY,
        reverse: bool=False,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ):
    """Create new dictiionary which is sorted by keys/values.
    `sort_by` accept "key" and "value". default is  "key".
    If pass `reverse=True`, the list will be reversed.
    If pass `inplace=True`, perform operation in-place.
    If set `factory`, create instance of factory class.
    """

    def _items_sorted_by_item_at_index(d, index, reverse):
        return dict(sorted(d.items(), key=lambda item: item[index],
                                      reverse=reverse))

    validate_DictItem(sort_by, thrown_error=True)

    new = obj if inplace else factory(obj)

    if sort_by == DictItem.KEY:
        new = _items_sorted_by_item_at_index(new, 1, reverse)
    else:
        new = _items_sorted_by_item_at_index(new, 0, reverse)

    return _dict_updator(obj, new, inplace=inplace, factory=factory)

def d_search(
        obj: dict,
        query: Pattern,
        search_for: DictItemType=DictItem.KEY,
        exact: bool=False,
        separator: str=Default_Keypath_Separator,
        ignore_case: bool=False,
        use_keypath: bool=True,
    ):
    """ Search and return a list of items matching the given query.
    search_for accept 'key', 'value' or others.
    if pass `search_for='all'`, search key and value.
    if pass `ignore_case=True`, match search string with ignore case.
    if pass `use_keypath`, return result with keypath.
    """

    def get_match(
            query: Pattern,
            value: str,
            exact: bool=False,
            ignore_case: bool=False
        ) -> Optional[Match]:
        if exact:
            return query == value
        else:
            if _type.is_str(query) and _type.is_str(value):
                v =  searchstr(query, value, ignore_case=ignore_case)
                return v
            else:
                return None

    def search_item(
            obj: dict,
            key: Hashable,
            value: Any,
            parents: list=[],
            in_keys: bool=False,
            in_values: bool=True,
            exact: bool=False,
            ignore_case: bool=False,
            separator: str=Default_Keypath_Separator,
            use_keypath: bool=True,
        ):

        match_key = in_keys and get_match(query, key, exact, ignore_case)
        match_val = in_values and get_match(query, value, exact, ignore_case)
        if any([match_key, match_val]):
            keypath = Keylist(parents).to_keypath(separator=separator)
            if not use_keypath:
                keypath = str(keypath)
            items[keypath] =  value

    items = defaultdict(str)
    if search_for == DictItem.KEY:
        in_keys = True
        in_values = False
    elif search_for == DictItem.VALUE:
        in_keys = False
        in_values = True
    else:
        in_keys = True
        in_values = True

    d_traverse(obj, search_item,
                  in_keys=in_keys,
                  in_values=in_values,
                  exact=exact,
                  ignore_case=ignore_case,
                  use_keypath=use_keypath)
    return dict(items)

def d_swap(
        obj: dict,
        key1: Hashable,
        key2: Hashable,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) ->Optional[dict]:
    """Swap items values at the given keys."""

    if key1 == key2:
        return obj

    new = obj if inplace else factory(obj)

    val1 = new[key1]
    val1 = val1.copy() if _type.is_mapping(val1) else val1
    val2 = new[key2]
    val2 = val2.copy() if _type.is_mapping(val2) else val2
    new[key1], new[key2] = val2, val1

    return _dict_updator(obj, new, inplace=inplace, factory=factory)

def d_flatten(
        obj: dict,
        separator: str=Default_Keypath_Separator,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) -> dict:
    """Return a new flattened dict using the given separator to join nested dict keys to flatten keypaths."""

    def _flatten_key(
        base_key: Hashable,
        key: Hashable,
        separator: str=Default_Keypath_Separator,
    )-> str:
        if base_key and separator:
            return f"{base_key}{separator}{key}"
        return key

    def _flatten_item(
        obj: dict,
        base_dict: Hashable,
        base_key: Hashable,
        default: Optional[Any]=None,
        separator: str=Default_Keypath_Separator,
    ):
        new_dict = base_dict
        for key in list(obj.keys()):
            new_key = _flatten_key(base_key, key, separator)
            value = obj.get(key, None)
            if _type.is_mapping(value):
                new_value = _flatten_item( value,
                                base_dict=new_dict, base_key=new_key,
                                separator=separator )
                new_dict.update(new_value)
                continue
            if new_key in new_dict:
                raise KeyError(f"Invalid key: '{new_key}', key already in flatten dict.")
            new_dict[new_key] = value
        return new_dict

    new = factory()
    new =  _flatten_item(obj,
                         base_dict=new, base_key="",
                         separator=separator)
    return _dict_updator(obj, new, inplace=inplace, factory=factory)


def d_unflatten(
        obj: dict,
        default: Optional[Any]=None,
        separator: str=Default_Keypath_Separator,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) -> dict:
    """Return a new unflattened dict using the given separator to join nested dict keys to flatten keypaths."""

    def _unflatten_item(key, value, separator):
        keys = key.split(separator)
        if _type.is_mapping(value):
            return (keys, d_unflatten(value, separator=separator))
        return (keys, value)


    new = factory()
    for key in list(obj.keys()):
        value = obj.get(key, default)
        new_keys, new_value = _unflatten_item(key, value, separator)
        new = update_items(new, new_keys, new_value,
                                 inplace=False, factory=factory)

    return _dict_updator(obj, new, inplace=inplace, factory=factory)


def d_traverse(
        obj: Union[dict, list, tuple],
        callback: Callable,
        parents: list=[],
        *args: Any,
        **kwargs: Any,
    ):
    """Traverse dict or list and apply callback function.
    callback function will be called as follows.
      `callback(obj, key, value, *args, parents=parents, **kwargs)`
      `callback(obj, index, value, *args, parents=parents, **kwargs)`
    """

    def _traverse_dict(
            obj: dict,
            callback: Callable,
            parents: list=[],
            parents_type: list=[],
            *args: Any,
            **kwargs: Any,
        ):
        for key in list(obj.keys()):
            parents.append(key)
            value = obj.get(key, None)
            callback(obj, key, value, *args, parents=parents, **kwargs)
            d_traverse(value, callback, *args, parents=parents, **kwargs)
            parents.pop()

    def _traverse_list(
            obj: Union[list, tuple],
            callback: Callable,
            parents: list=[],
            parents_type: list=[],
            *args: Any,
            **kwargs: Any,
        ):
        for index, value in list(enumerate(obj)):
            parents.append(f'[{index}]')
            callback(obj, index, value, parents=parents, *args, **kwargs)
            d_traverse(value, callback, *args, parents=parents, **kwargs)
            parents.pop()

    if not _type.is_function(callback):
        raise ValueError("callback argument must be a callable.")
    if _type.is_dict(obj):
        _traverse_dict(obj, callback, *args, parents=parents, **kwargs)
    elif _type.is_list_or_tuple(obj):
        _traverse_list(obj, callback, *args, parents=parents, **kwargs)


def d_unique(
        obj: dict,
    ) -> list:
    """Return unique values from dict. """

    new = dict(obj)
    values = []

    for key in obj.keys():
        value = new.get(key, None)
        if value in values:
            new.pop(key, None)
            continue
        values.append(value)

    return values

def d_using(
        obj: dict,
        *,
        inplace: bool=False,
        factory: Type[dict]=dict,
        **kwargs: Any,
    ) -> dict:
    """
    Create the new dictionary which expand with extra items defined by kwargs.
    If set `factory`, create instance of factory class.
    If set `True` to `inplace`, perform operation in-place.
    """

    new = obj if inplace else factory(obj)
    new.update(kwargs)
    return _dict_updator(obj, new, inplace=inplace, factory=factory)

def d_without(
        obj: dict,
        keys: list,
        *,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) -> dict:
    """
    Create the new dictionary which without the keys named by args.
    If set `factory`, create instance of factory class.
    If set `True` to `inplace`, perform operation in-place.
    """

    new = obj if inplace else factory(obj)
    for key in keys:
        del new[key]
    return _dict_updator(obj, new, inplace=inplace, factory=factory)


def get_parent_item(
        obj: dict,
        keys: list,
    ):
    # TODO:
    pass

def get_item_hierarchy(
        obj: dict,
        keys: list,
    ):
    # TODO:

    def _get_item_keyval(item, key):
        if _type.is_list_or_tuple(item):
            index = key if _type.is_integer(key) else None
            if index is not None:
                return (index, item[index])
            elif _type.is_dict(item):
                return (key, item[key])
            raise KeyError(f"Invalid key: '{key};")

    items = []
    item = obj
    for key in keys:
        try:
            key, val = _get_item_keyval(item, key)
            items.append(item, key, val)
            item = val
        except (IndexError, KeyError):
            items.append((None, None, None))
            break
    return iitems


def get_keys(
        obj: Optional[dict]=None,
        *,
        indexes: bool=False,
        output_as: Optional[DictKey]=None,
        separator: str=Default_Keypath_Separator,
    ) -> list:
    """ Get to get all keys from dictionary as a List
    This method is able to process on nested dictionary.
    if output_as accept "keylist" and "keypath".
    """

    def get_deeply( obj):
        found_keys = list()

        if _type.is_mapping(obj):
            for key, val in obj.items():
                found_keys.append(key)
                found_keys += get_deeply(val)

        elif _type.is_list_or_tuple(obj):
            for element in obj:
                found_keys += get_deeply(element)

        return found_keys


    if not output_as:
        all_keys = get_deeply(obj)
    else:
        validate_DictKey(output_as, thrown_error=True)

        if output_as == DictKey.KEYLIST:
            all_keys = Keylist.keylists(obj, indexes=indexes)
        else:
            all_keys = Keypath.keypaths(obj, indexes=indexes,
                                             separator=separator)

    return all_keys

def get_values(
        obj: Union[dict, Sequence],
        keys: Union[Hashable, Keylist, Keypath],
    ) -> Any:
    """Get the value of key in the objet(s).
    `obj` : dict, dict[dict], dict[list], list[dict]
    return value, list, dict.
    """

    def deep_lookup(
            key: Hashable,
            obj: Union[dict, list, tuple],
        ):
        """Lookup a key in a nested object(s).
        yield a value
        """

        if _type.is_mapping(obj):
            for k, v in obj.items():
                if key == k:
                    yield k, v
                if _type.is_mapping(v):
                    for kk, v in deep_lookup(key, v):
                        yield (kk, v)
                elif _type.is_list_or_tuple(v):
                    for element in v:
                        for kk, v in deep_lookup( key, element):
                            yield (kk, v)

        elif _type.is_list_or_tuple(obj):
            index = get_index_from_key(key)
            if _type.is_not_none(index):
                yield (index, obj[index] )
            else:
                for element in obj:
                    for k, v in deep_lookup(key, element):
                        yield (k, v)

    as_dict = False
    if _type.is_keypath(keys):
        keys = keys.to_keylist().value()
    elif _type.is_keylist(keys):
        keys = keys.value()
    elif _type.is_tuple(keys):
        keys = [keys]
    elif _type.is_str(keys):
        keys = [keys]
    elif not _type.is_list_not_empty(keys):
        keys = list(keys)
        as_dict = True

    values = defaultdict(list)
    v = obj
    k = None
    for key in keys:
        for k, v in deep_lookup(key, v):
            values[k].append(v)

    if as_dict:
        return values
    else:
        return values[k][-1] if k is not None else None

def get_items(
        obj: dict,
        loc: Union[Hashable, Keylist, Keypath],
        value: Any,
        *,
        func: Optional[Callable]=None,
        factory: Type[dict]=dict,
    ):
    """
    Create new dictionary with new key value pair as d[key]=val.
    If set `True` to `inplace`, perform operation in-place.
    otherwise, not modify the initial dictionary.
    obj
        dictionary on which to operate
    loc
        the location of the value. str and keypath, keylist.
        i.e.: { 'a': { 'b1': { 'c1': {'x': 1 },
                               'c2': {'x': 2 }},
                     { 'b2': { 'c1': {'x': 3 },
                               'c2': {'x': 4 }} }}}
        if set Keylist('a', 'b1', 'c1',  'x') to `loc`, val is 1.
        if set Keypath('a.b1.c1.x')  to `loc`, val is 1.
        giving the location of the value to be changed in `obj`.
    value: the value to aplly
    """

    new = factory(obj)

    new = update_items(new, loc, value, func=func,
                        action=DictAction.GET,
                        inplace=False, factory=factory)
    return new

def pop_items(
        obj: dict,
        loc: Union[Hashable, Keylist, Keypath],
        value: Any,
        *,
        func: Optional[Callable]=None,
        factory: Type[dict]=dict,
    ):
    """ Create new dictionary with new key value pair as d[key]=val.
        If set `True` to `inplace`, perform operation in-place.
        otherwise, not modify the initial dictionary.
    obj
        dictionary on which to operate
    loc
        the location of the value. str and keypath, keylist.
        i.e.: { 'a': { 'b1': { 'c1': {'x': 1 },
                               'c2': {'x': 2 }},
                     { 'b2': { 'c1': {'x': 3 },
                               'c2': {'x': 4 }} }}}
        if set Keylist('a', 'b1', 'c1',  'x') to `loc`, val is 1.
        if set Keypath('a.b1.c1.x')  to `loc`, val is 1.
        giving the location of the value to be changed in `obj`.
        if set loc as str and has `.keypath_separator`,
        convert keypath to str using
        `str.split(keys, sep=separator)`.
    value: the value to aplly
    """
    item = update_items(obj, loc, value, func=func,
                        action=DictAction.POP,
                        inplace=True, factory=factory)
    return item

def del_items(
        obj: dict,
        loc: Union[Hashable, Keylist, Keypath],
        *,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ):
    """ Create new dicttionary with the given key(s) removed.
        New dictionary has d[key] deleted for each supplied key.
        If set `True` to `inplace`, perform operation in-place.
        otherwise, not modify the initial dictionary.
    obj
        dictionary on which to operate
    loc
        the location of the value. str and keypath, keylist.
        i.e.: { 'a': { 'b1': { 'c1': {'x': 1 },
                               'c2': {'x': 2 }},
                     { 'b2': { 'c1': {'x': 3 },
                               'c2': {'x': 4 }} }}}
        if set Keylist('a', 'b1', 'c1',  'x') to `loc`, val is 1.
        if set Keypath('a.b1.c1.x')  to `loc`, val is 1.
        giving the location of the value to be changed in `obj`.
    value: the value to aplly
    func:
        the function to apply the object(s)..
    inplace:
        If set `True` to `inplace`, perform operation in-place.
        otherwise, not modify the initial dictionary.
    """

    obj = obj if inplace else factory(obj)

    new = update_items(obj, loc, None, func=None,
                        action=DictAction.DEL,
                        inplace=False, factory=factory)

    return _dict_updator(obj, new, inplace=inplace, factory=factory)

def set_items(
        obj: Union[dict, Sequence],
        loc: Union[Hashable, Keylist, Keypath],
        value: Any,
        func: Optional[Callable]=None,
        factory: Type[dict]=dict,
    ):
    """ Create new dict with new, potentially nested, key value pair
    obj
        dictionary on which to operate
    loc:
        the location of the value. str and keypath, keylist.
        i.e.: { 'a': { 'b1': { 'c1': {'x': 1 },
                               'c2': {'x': 2 }},
                     { 'b2': { 'c1': {'x': 3 },
                               'c2': {'x': 4 }} }}}
        if set Keylist('a', 'b1', 'c1',  'x') to `loc`, val is 1.
        if set Keypath('a.b1.c1.x')  to `loc`, val is 1.
        giving the location of the value to be changed in `obj`.
        if set loc as str and has `.keypath_separator`,
    value: the value to aplly
    func:
        the function to apply the object(s)..
    inplace:
        If set `True` to `inplace`, perform operation in-place.
        otherwise, not modify the initial dictionary.
    """

    new = update_items(obj, loc, value, func=func,
                         factory=factory, inplace=False)
    return _dict_updator(obj, new, inplace=True, factory=factory)


def update_items(
        obj: Union[dict, Sequence],
        loc: Union[Hashable, Keylist, Keypath],
        value: Optional[Any]=None,
        *,
        default: Optional[Any]=None,
        func: Optional[Callable]=None,
        action: DictActionType=DictAction.SET,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ):
    """ Create new dictionary Update value from a nested dictionary.
    Paramters
    ---------
    loc
        the location of the value. str and keypath, keylist.
        i.e.: { 'a': { 'b1': { 'c1': {'x': 1 },
                               'c2': {'x': 2 }},
                     { 'b2': { 'c1': {'x': 3 },
                               'c2': {'x': 4 }} }}}
        if set ['a', 'b1', 'c1',  'x']  as loc,
        giving the location of the value to be changed in d.
        if set loc as str and has `.keypath_separator`,
        convert keypath to str using
        `str.split(keys, sep=separator)`.
    value: the value to aplly
    obj
        dictionary on which to operate
    func
        function to operate on that value

    If loc is not a key in d,
    update_in creates nested dictionaries to the depth
    specified by the keys, with the innermost value set to func(default).

    If set `True` to `inplace`, perform operation in-place.
    otherwise, not modify the initial dictionary.
    """

    validate_DictAction(action, thrown_error=True)

    if _type.is_keylist(loc):
        loc = loc.value()
    elif _type.is_keypath(loc):
        loc = loc.to_keylist().value()
    elif _type.is_str_not_empty(loc):
        loc = Keypath(loc).to_keylist().value()
    if _type.is_tuple(loc):
        loc = list(loc)

    iter_key = iter(loc)
    k = next(iter_key)

    new = inner = factory()
    new.update(obj)

    if _type.is_not_none(value):
        func = func if func else lambda x: value
    else:
        func = func if func else lambda x: x

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
        if action == DictAction.GET:
            item = factory(inner)
            return item
        elif action == DictAction.DEL:
            del inner[k]
        elif action == DictAction.POP:
            item = factory(inner)
            del inner[k]
            _dict_updator(obj, new, inplace=True, factory=factory)
            return item
    else:
        if action not in ( DictAction.DEL, DictAction.POP ):
            inner[k] = func(default)

    return _dict_updator(obj, new, inplace=inplace, factory=factory)


def keylists(
        obj: Any,
        indexes: bool=False,
    ) -> list:
    """keylist is the list of key as keys from dict/list."""

    return Keylist.keylists(obj, indexes)


def keypaths(
        obj: dict,
        indexes: bool=False,
        separator: str=Default_Keypath_Separator,
    ) -> str:
    """
    Keypath is the string for  attribute-sytle access to value.
    (dot-notation by default).
    """
    return Keypath.keypaths(obj, indexes, separator=separator)


__all__ = [
    "d_counts",
    "d_compare",
    "d_groupby",
    "d_invert",
    "d_find",
    "d_filter",
    "d_flatten",
    "d_unflatten",
    "d_map",
    "d_merge",
    "d_move",
    "d_remove",
    "d_rename",
    "d_nest",
    "d_search",
    "d_sort",
    "d_subset",
    "d_swap",
    "d_traverse",
    "d_unique",
    "keylists",
    "keypaths",
    "get_keys",
    "get_values",
    "get_items",
    "pop_items",
    "del_items",
    "set_items",
    "update_items",
]

