# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Hashable
import snoop

Default_Keypath_Separator='.'

class Keylist(list):
    keylist: Optional[Union[list, tuple, Keylist]]=None

    def __new__(cls, keylist, separator=Default_Keypath_Separator):
        self = super().__new__(cls, keylist)
        self.separator = separator
        if not self.validate(keylist):
            raise ValueError('keylist should be list or tuple. each element must be Hashable or not empty str.')
        self.keylist = keylist
        return self

    def __hash__(self):
        try:
            return self._cached_hash
        except:
            h = self._cached_hash =  hash(str(self.keylist))
            return h

    def __repr__(self):
        return ( f'Keylist("{self.keylist}")' )

    def __str__(self):
        return f'{self.keypath}'


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

    @staticmethod
    def list2path(
            keylists: list,
            separator: str=Default_Keypath_Separator,
        )->str:
        """Convert from keylist to keypath """
        if isinstance(keylists, list) and  not isinstance(keylists[0], list):
           keylists = [keylists]

        keypaths = [ separator.join([f"{key}" for key in keylist])
                                      for keylist in keylists ]
        return keypaths


    def to_keypath(self,
            keylist: Opyionsl[Union[list, tuple, Keylist]]=None,
            separator: Optional[str]=None
        ) -> Keypath:
        separator = separator or str(self.separator)
        if not ( isinstance(separator, str) and separator != '' ):
            raise ValueError('separator must be Hashable or not empty str.')
        keylist = keylist or self.keylist
        keypath = [ separator.join([f"{key}" for key in keylist]) ]
        keypath = keypath[0].replace('.[', '[')
        return Keypath(keypath)

    def value(self):
        return self.keylist

    def validate(self, keylist: Optional[list, tuple, Keylist]=None):
        keylist = keylist or self.keylist
        if not isinstance(keylist, list):
            return False
        return all( map(lambda x: x != '' and isinstance(x, Hashable),
                        keylist) )

class Keypath(str):
    keypath: Optional[Union[str, Keypath]]=None

    def __new__(cls, keypath, separator=Default_Keypath_Separator):
        self = super().__new__(cls, keypath)
        if not ( isinstance(separator, str) and separator != ''):
            raise ValueError('separator must be Hashable or not empty str.')
        self.separator = separator
        self.keypath = self.validate(keypath)
        return self

    def __repr__(self):
        return ( f'Keypath("{self.keypath}")')

    def __str__(self):
        return f'{self.keypath}'

    def __hash__(self):
        try:
            return self._cached_hash
        except:
            h = self._cached_hash =  hash(self.keypath)
            return h

    @staticmethod
    def keypaths(
            obj: dict,
            indexes: bool=False,
            separator: str=Default_Keypath_Separator,
        ) -> str:
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
        keylist = [x.split(sep=separator) if x.find(separator)>0 else x
                   for x in keypaths ]
        if len(keylist) == 1:
            return keylist[0]
        else:
            return keylist


    def to_keylist(self,
            keypaths: Optional[Union[str,list,tuple]]=None,
        ):
        keypaths = keypaths or self.keypath
        keypaths = [keypaths] if isinstance(keypaths, str) else keypaths
        keylist = [ x.split(sep=str(self.separator))
                    if self.validate(x) else x
                    for x in keypaths ]
        if len(keylist) == 1:
            return keylist[0]
        else:
            return keylist

    def validate(self, keypath:str):
        if isinstance(keypath, str) and keypath != '':
            return keypath
        else:
            return None

    def value(self):
        return self.keypath

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
                return keys
            return [key]

        def _split_keys_and_indexes(keypath, separator):
            """ Splits keys and indexes using the given separator:
            i.e.: 'item[0].subitem[1]' -> ['item', 0, 'subitem', 1].
            """
            if isinstance(keypath, str):
                keys1 = _split_keys(keypath, separator)
                keys2 = []
                for key in keys1:
                    keys2 += _split_key_indexes(key)
                return keys2
            return [keypath]

        keypath = keypath or self.keypath
        separator = separator or self.separator
        if isinstance(keypath, list):
            keys = []
            for key in keypath:
                keys += self.parse_keypath(key, separator)
            return keys

        return


__all__ = [
    "Keylist",
    "Keypath",
    "Default_Keypath_Separator",
]
