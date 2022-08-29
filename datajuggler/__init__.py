from .dict import (
    aDict, uDict, iDict, ordereddict_to_dict, change_dict_keys,
)
from .utils import (
    StrCase, is_alpha, is_alnum, urange,
    omit_values, replace_values, ReplaceFor, ReplaceForType,
    split_chunks, add_df, df_compare, rename_duplicates, remove_accents,
)

__all__ = [
    "uDict",
    "iDict",
    "aDict",
    "StrCase",
    "urange",
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
