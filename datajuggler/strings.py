# -*- coding: utf-8 -*-

import re
from typing import Any, Union, Pattern, Match, Callable, Optional


__RE_FLAGS = [ re.UNICODE, ( re.IGNORECASE + re.UNICODE) ]

# See Also: https://stackoverflow.com/questions/30069846/how-to-find-out-chinese-or-japanese-character-in-a-string-in-python

cjk_ranges = [
  {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
  {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
  {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
  {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
  {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
  {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
  {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
  {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
  {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
  {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
  {"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
  {"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
  {"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]

def is_cjk(char):
  return any([ range["from"] <= ord(char) <= range["to"]
               for range in cjk_ranges ])


def cjk_substrings(string):
      i = 0
      while i<len(string):
        if is_cjk(string[i]):
          start = i
          while is_cjk(string[i]): i += 1
          yield string[start:i]
        i += 1


def searchstr(
        pattern: Pattern,
        string: str,
        wild: bool=False,
        ignore_case: bool=False,
    ) -> Match:
    """ almost same as re.search.
    Scan through string looking for a match to the pattern, returning
    a Match object, or None if no match was found.
    """
    if wild:
        return re.search(pattern, string, flags = __RE_FLAGS[ignore_case])
    else:
        return re.match(pattern, string, flags = __RE_FLAGS[ignore_case])

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
        if not ( isinstance(string, str)
                 and isinstance(pattern, (str, Pattern))):
            return False

        match = re.search(pattern, string, flags = __RE_FLAGS[wild])
        if match:
            return True
        else:
            return False


def remove_accents(data: Any) -> Any:
    """Return the normal form for a Unicode string
       using canonical decomposition."""

    if isinstance(data, str):
        data = ( normalize("NFD", data)
                 .encode("ascii", "ignore")
                 .decode("ascii") )
    return data

def remove_character(
        string: str,
        punctuations_list: Optional[list]=None
    ) ->str:
    if not stop_words_list:
        return string
    else:
        return "".join([letter for letter in string.lower() if letter not in punctuations_list])

def remove_words(
        string: str,
        stop_words_list: Optional[list]=None
    ) ->str:
    if not stop_words_list:
        return string
    else:
        return " ".join([word for word in give_string.split(" ") if word not in stopwords_list])


def copy_docstring(copy_func: Callable) -> Callable:
    """Copying the docstring of function onto another function by name

    Example:
        copy_docstring(self.copy_func)(self.func)
        or
        used as @copy_docstring(copy_func)

    See Also: https://stackoverflow.com/questions/68901049/
    """
    def wrapper(func: Callable) -> Callable:
        save_doc = func.__doc__ or ''
        func.__doc__ = copy_func.__doc__ + save_doc
        return func
    return wrapper
