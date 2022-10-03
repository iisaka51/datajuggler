# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Optional, Union, Any, Hashable
import re

Default_Keypath_Separator='.'

def get_index_from_key(key) -> Optional[int]:
    pattern = re.compile(r'\[(?P<INDEX>-?[0-9]*)\]')
    if isinstance(key, int):
        return key
    match = re.search(pattern, key)
    if match:
        index = match.group('INDEX')
        index = int(index) if index != '' else None
    else:
        index = None

    return index

class Keylist(list):
    def __init__(self,
            keylist: list=[],
            separator: str=Default_Keypath_Separator
        ):
        self.separator = separator
        if keylist:
            keylist = self._normalize(keylist)
        super().__init__(keylist)

    def __hash__(self):
        return hash(self.__str__())

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__str__()})'

    def __str__(self):
        return str(list(self))

    def append(self,
            key: Hashable
        ):
        """
        Append key to the end of the keylist.
        """
        self.validate([key])
        super().append(key)

    def find(self,
            val: Union[Any, list, tuple],
        ) -> list:
        """
        Return the list of index that found val in list.
        otherwise return None
        """
        if isinstance(val, (list, tuple)):
            found = [ i for v in val for i, x in enumerate(self) if x == v ]
        else:
            found = [ i for i, x in enumerate(self) if x == val ]

        return found if found else None


    def insert(self,
            index: int,
            key: Hashable
        ):
        """
        Insert object before index.
        """
        self.validate([key])
        super().insert(index, key)

    @staticmethod
    def keylists(
            obj: Any,
            indexes: bool=False,
        ) -> list:
        """keylist is the list of key as keys from dict/list."""

        def _keylist_for_dict(
                obj: dict,
                parent_keys: list,
                indexes: bool=False,
            ) -> list:

            if not isinstance(parent_keys, list):
                parent_keys = list(parent_keys)

            keylist = []
            for key, value in obj.items():
                keys = parent_keys + [key]
                keylist += [keys]
                keylist += _get_keylist(value, keys, indexes)
            return keylist

        def _keylist_for_list(
                obj: list,
                parent_keys: list,
                indexes: bool=False,
            ) ->list:

            if not isinstance(parent_keys, list):
                parent_keys = list(parent_keys)

            keylist = []
            for key, value in enumerate(obj):
                keys = list(parent_keys)
                keys[-1] += f"[{key}]"
                keylist += [keys]
                keylist += _get_keylist(value, keys, indexes)
            return keylist

        def _get_keylist(
                obj: list,
                parent_keys: list,
                indexes: bool=False,
            ) ->list:
            if isinstance(obj, dict):
                return _keylist_for_dict(obj, parent_keys, indexes)
            elif isinstance(obj, list) and indexes:
                return _keylist_for_list(obj, parent_keys, indexes)
            else:
                return []

        return _get_keylist(obj, [], indexes)

    def _normalize(self,
            keylist: list,
            separator: Optional[str]=None,
        )->list:
        separator = separator or self.separator
        trim_index = lambda x: f'[{x}]' if isinstance(x,int) else x
        keylist = [ trim_index(x) for x in keylist ]
        keypath = Keylist.list2path(keylist, separator)
        keylist = keypath.parse_keypath(separator=separator)
        return keylist

    @staticmethod
    def list2path(
            keylists: list,
            separator: str=Default_Keypath_Separator,
        )->Union[list, Keypath]:
        """Convert from keylist to keypath """
        if isinstance(keylists, list) and  not isinstance(keylists[0], list):
           keylists = [keylists]

        trim = lambda x: x.replace(f'{separator}[', '[')
        trim_index = lambda x: f'[{x}]' if isinstance(x,int) else x
        keypaths = [ trim(separator.join(
                          [ trim_index(key) for key in keylist]))
                                      for keylist in keylists  ]
        keypaths = [ Keypath(x, separator) for x in keypaths ]

        if len(keypaths)==1:
            return keypaths[0]
        else:
            return keypaths


    def to_keypath(self,
            keylist: Opyionsl[Union[list, tuple, Keylist]]=None,
            separator: Optional[str]=None,
            as_str: bool=False,
        ) -> Union[Keypath, list]:

        separator = separator or str(self.separator)
        if separator and not isinstance(separator, str):
            raise ValueError('separator must be Hashable or not empty str.')
        keylist = keylist or list(self)
        keypath = Keylist.list2path(keylist, separator)
        if as_str:
            keypath = [ x.value() for x in keypath ]

        if len(keypath) == 1:
            return keypath[0]
        else:
            return keypath

    def update(self,
             keylist: list
        ):
        self.validate(keylist)
        self.__init__(keylist)

    def value(self):
        return list(self)

    def validate(self,
            keylist: Optional[list, tuple, Keylist]=None,
            thrown_error: bool=True,
        ) ->bool:
        keylist = keylist or list(self)
        if not isinstance(keylist, (list, tuple)):
            check =  False
        else:
            check =  all( map(lambda x: x != '' and isinstance(x, Hashable),
                            keylist) )
        if not check and thrown_error:
            raise ValueError('keylist should be list or tuple. '
                             'each element must be Hashable or not empty str.')
        else:
            return check


class Keypath(str):
    keypath: Optional[Union[str, Keypath]]=None

    def __new__(cls,
            keypath: Optional[str]='',
            separator=Default_Keypath_Separator
        ):
        self = super().__new__(cls, keypath)
        if not ( isinstance(separator, str) and separator != ''):
            raise ValueError('separator must be Hashable or not empty str.')
        self.separator = separator
        keypath and self.validate(keypath)
        return self


    def __hash__(self):
        return hash(self.__str__())

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.__str__()}")'

    @staticmethod
    def has_keypath_separator(keypath,
            separator: str=Default_Keypath_Separator,
        ) ->bool:
        if ( keypath and isinstance(separator, str)
             and keypath.find(separator) >= 0 ):
            return True
        else:
            return False

    @staticmethod
    def keypaths(
            obj: dict,
            indexes: bool=False,
            separator: str=Default_Keypath_Separator,
        ) -> Union[Keypath, list]:
        """
        Keypath is the string for  attribute-sytle access to value.
        (dot-notation by default).
        """
        separator = separator or Default_Keypath_Separator
        if not isinstance(separator, str):
            raise ValueError("separator must be a (non-empty) string.")

        key_lists = Keylist.keylists(obj, indexes=indexes)
        key_paths = [ separator.join([f"{key}" for key in key_list])
                                               for key_list in key_lists ]
        key_paths.sort()
        return key_paths

    @staticmethod
    def path2list(
            keypaths: Union[str, list],
            separator: str=Default_Keypath_Separator
        )->list:
        """Convert from keypath to keylist """

        keypaths = [keypaths] if isinstance(keypaths, str) else keypaths
        keylist = [ Keypath.parse_keypath(x,separator=separator)
                    for x in keypaths ]

        if len(keylist)==1:
            return keylist[0]
        else:
            return keylist


    def to_keylist(self,
            keypaths: Optional[Union[str,list,tuple]]=None,
            separator: OPtional[str]=None,
            as_list: bool=False,
        ) ->Union[Keylist, list]:

        separator = separator or self.separator
        keypaths = keypaths or self
        keypaths = [keypaths] if isinstance(keypaths, (str, Keypath)) else keypaths
        keylist = [ self.parse_keypath(x,separator=separator)
                    for x in keypaths ]

        if not as_list:
            keylist = [ Keylist(x,separator) for x in keylist ]

        if len(keylist) == 1:
            return keylist[0]
        else:
            return keylist

    def validate(self,
            keypath:str,
            separator: Optional[str]=None,
            thrown_error: bool=True,
        ) ->bool:
        if keypath and isinstance(keypath, (str, Keypath)):
            return True
        else:
            if thrown_error:
                raise ValueError('keypath should be str and not empty.')
            else:
                return False

    def value(self):
        return str(self)

    def parse_keypath(self,
            keypath: Optional[str]=None,
            separator: Optional[str]=None
        ):
        separator = separator or self.separator
        RE_KEY_INDEX = r"(?:\[[\'\"]*(\-?[\d]+)[\'\"]*\]){1}$"

        def _split_keys(keypath, separator):
            """ Splits keys using the given separator:
            i.e.: 'item.subitem[1]' -> ['item', 'subitem[1]'].
            """
            if separator:
                return keypath.split(separator)
            return [keypath]

        def _split_key_indexes(key):
            """ Splits key indexes:
            i.e.: 'item[0][1]' -> ['item', 0, 1].
            """
            if "[" in key and key.endswith("]"):
                keys = []
                while True:
                    matches = re.findall(RE_KEY_INDEX, key)
                    if matches:
                        key = re.sub(RE_KEY_INDEX, "", key)
                        index = int(matches[0])
                        keys.insert(0, index)
                        continue
                    keys.insert(0, key)
                    break
                try:
                    keys.remove('') # may be int as key of dictionary.
                except ValueError:
                    pass
                return keys
            return [key]

        def _split_keys_and_indexes(keypath, separator):
            """ Splits keys and indexes using the given separator:
            i.e.: 'item[0].subitem[1]' -> ['item', [0], 'subitem', [1]].
            """
            if isinstance(keypath, str):
                keys1 = _split_keys(keypath, separator)
                keys2 = []
                for key in keys1:
                    keys2 += _split_key_indexes(key)
                return keys2
            return [keypath]

        separator = separator or self.separator
        keypath = keypath or Keypath(self, separator)
        if isinstance(keypath, list):
            keys = []
            for key in keypath:
                keys += self.parse_keypath(key, separator)
            return keys
        else:
            return _split_keys_and_indexes(keypath, separator)

__all__ = [
    "Keylist",
    "Keypath",
    "Default_Keypath_Separator",
]
