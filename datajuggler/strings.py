import re
from typing import (
    Any, Dict, Union, Optional, Hashable, Iterable, Sequence,
    Pattern, Callable,
    Literal, get_args
)

__RE_FLAGS = [ re.UNICODE, ( re.IGNORECASE + re.UNICODE) ]

def searchstr(
        pattern: Pattern,
        string: str,
        ignore_case: bool=False,
    ):
    """ almost same as re.search.
    Scan through string looking for a match to the pattern, returning
    a Match object, or None if no match was found.
    """
    re.search(pattern, string, flags = __RE_FLAGS[ignore_case])

def substr(
        pattern: Pattern,
        repl: Union[str, Callable],
        string: str,
        count=0,
        ignore_case: bool=False,
    )-> str:
    """ almost same as re.sub.
    Return the string obtained by replacing the leftmost
    non-overlapping occurrences of the pattern in string by the
    replacement `repl`.  `repl` can be either a string or a callable;
    if a string, backslash escapes in it are processed.
    If it is a callable, it's passed the Match object and must return
    a replacement string to be used.
    """
    return re.sub(pattern, repl, string,
                  count=count, flags=__RE_FLAGS[ignore_case])

def is_match_string(
        pattern: Union[str, Pattern],
        string: str,
        wild: bool=False,
    ) -> bool:


    if pattern == string:
        return True
    else:
        if not isinstance(string, str):
            return False

        match = re.search(pattern, string, flags = __RE_FLAGS[wild])
        if match:
            return True
        else:
            return False


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


