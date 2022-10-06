[![](https://img.shields.io/pypi/pyversions/datajuggler.svg?color=blue&logo=python&logoColor=white)](https://www.python.org/)
[![](https://img.shields.io/pypi/v/datajuggler.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/datajuggler/)
[![](https://pepy.tech/badge/datajuggler/month)](https://pepy.tech/project/datajuggler)
[![](https://img.shields.io/github/stars/iisaka51/datajuggler?logo=github)](https://github.com/iisaka51/datajuggler/)
[![](https://img.shields.io/pypi/l/datajuggler.svg?color=blue)](https://github.com/iisaka51/datajuggler/blob/master/LICENSE.txt)

# DataJuggler

This library provides utility classes and helper functions for data processing.
This is spin-off project from [scrapinghelper](https://github.com/iisaka51/scrapinghelper).
This project is inspired by follow greate projects.

 - [python-benedict](https://github.com/fabiocaccamo/python-benedict)
 - [munch](https://github.com/Infinidat/munch)
 - [adict](https://github.com/mewwts/addict).


## Features

 - 100% backward-compatible, you can safely wrap existing dictionaries and list.
 - Keypath list-index support (also negative) using the standard [n] suffix.
 - aDict support dot-notation access to value of dictionaries.
 - aDict support immutable and hashable of dictiinary.
 - uDict support Keylist and Keypath which are pointing to valaues of dictionaries.
 - uDict and many helper functions parse methods to retrieve data as needed.
 - iList support immutable and hashable of list.
 - iList support hold attributes using aDict.

## classes

 - class BaseDict
   Factory class for custom dictionary.
 - class IODict
   Factory class for IO serializable dictionary.
 - class aDict
   Allow to access using dot notation for dictionary.
 - class Keypath and Keylist
   type and manage for keypath and Keylist
 - class uDict
   Allow to access using keypath and keylist.
 - class iList
   Allow hashable and immutable list. when call freeze().
 - class StrCase
   Convert case for object(s).
 - class TypeValidator
   drop in replace for isinstance() for convinient.

utilities for string manupulate helper functions.

 -  `replace_values()` - Replace objects for object(s).
 -  `omit_values()` - Omit values for object(s).
 -  `rename_duplicates()` - Rename duplicated strings to append a number at the end.
 -  `split_chunks()` - Split iterable object into chunks.
 -  `urange()` - Return an object that produces a sequence of integes.

if pandas installed, follows functions are enabled.
otherwise raise NotImplementedError when function call it.

 -  `add_df()` - Add data into DataFrame.
 -  `df_compare()` - Check DataFrame is equals.

## Installation

 - Run `pip install datajuggler`

## Getting Start

### aDict

aDict allow to access using dot notation for values of dictionary.
and support freeze/unfreeze object.

```python
In [1]: from datajuggler import aDict, uDict, iList

In [2]: data = { 'one': { 'two': { 'three': { 'four': 4 }}}}

In [3]: a = aDict(data)

In [4]: a.one.two.three.four
Out[4]: 4

In [5]: a.one.two.three.four = 3

In [6]: a.one.two.three.four
Out[6]: 3

In [7]: a.freeze()

In [8]: hash(a)
Out[8]: 2318099281826460897

In [9]: try:
   ...:     a.one.two.three.four=10
   ...: except AttributeError as e:
   ...:     print(e)
   ...:
aDict frozen object cannot be modified.

In [10]: a.unfreeze()

In [11]: a.one.two.three.four = 10

In [12]: try:
    ...:     hash(a)
    ...: except AttributeError as e:
    ...:     print(e)
    ...:
unhashable not frozen object.

In [13]:
```

### uDict

uDict is utilized class support keylist and keypath accessing to values.

```python
In [1]: from datajuggler import uDict, Keypath, Keylist

In [2]: data = { "a": 1,
   ...:              "b": { "c": { "x": 2, "y": 3, },
   ...:                     "d": { "x": 4, "y": 5, },
   ...:                     "e": [ { "x": 1, "y": -1, "z": [1, 2, 3], },
   ...:                            { "x": 2, "y": -2, "z": [2, 3, 4], },
   ...:                            { "x": 3, "y": -3, "z": [3, 4, 5], },
   ...:                          ],
   ...:                   },
   ...:           }

In [3]: d = uDict(data)

In [4]: d['a']
Out[4]: 1

In [5]: d['b', 'c']
Out[5]: uDict({'x': 2, 'y': 3})

In [6]: d[Keylist(['b', 'e[1]', 'z[2]'])]
Out[6]: 4

In [7]: d[Keypath('b.e[1].z[2]')]
Out[7]: 4

In [8]:
```

### iList

iList is universal object with list and aDict.

```python
In [1]: from datajuggler import iList

In [2]: l = iList()
   ...: assert l == []

In [3]: l = iList([1,2,3])
   ...: assert l == [1,2,3]

In [4]: l = iList()
   ...: try:
   ...:     l[0] = 1
   ...: except IndexError as e:
   ...:     print(e)
   ...:
list assignment index out of range

In [5]: l = iList([1])
   ...: l[0] = 10

In [6]: l1 = iList([1,2,3,4,5])
   ...: l2 = iList([1,2,3,4,5])

In [7]: assert l1 == l2

In [8]: l1 = iList([1,2,3,4,5])
   ...: l2 = list([1,2,3,4,5])

In [9]: assert l1 == l2

In [10]: l1 = iList([5,4,3,2,1])
    ...: l2 = list([1,2,3,4,5])
    ...: assert l1 != l2

In [11]: l1 = iList([1, 2, 3])

In [12]: try:
    ...:     hash(l1)
    ...: except AttributeError as e:
    ...:     print(e)
    ...:
unhashable not frozen object.

In [13]: l1.freeze()

In [14]: hash(l1)
Out[14]: 7029740037309777799

In [15]: try:
    ...:     l1[0] = 10
    ...: except AttributeError as e:
    ...:     print(e)
    ...:
iList frozen object cannot be modified.

In [16]: l1.unfreeze()

In [17]: l1[0] = 10

In [18]: l = iList([1,2,3])

In [19]: l.Hello='Python'

In [20]: l.Hello
Out[20]: 'Python'

In [21]: l == [1,2,3]
Out[21]: True

In [22]: l.get_attrs()
Out[22]: {'Hello': 'Python'}

In [23]:
```

## class BaseDict

BaseDict is internal base class for custom dictionary.
this class has follows methods.

 - `update(*args, **kwargs)`
 - `get(key: Hashable, default=None))`
 - `setdefault(key: Hashable, default=None)`
 - `fromkeys(sequence, inplace:bool=False)`
 - `fromvalues(sequence, base: int=1,
               prefix: Optional[str]=None,inplace:bool=False)`
 - `fromlists(keys: Sequence, values: Sequence, inplace:bool=False)`
 - `to_dict(obj: Any)`
 - `from_dict(obj: Any, factory=None, inplace: bool=False)`



### fromkeys()

Create a new dictionary with keys from iterable and values set to value.
If set `True` to `inplace`, perform operation in-place.


```python
In [1]: from datajuggler import aDict,uDict

In [2]: data = [ 'January', 'February', 'March', 'April' ]

In [3]: aDict().fromkeys(data, 2)
Out[3]: aDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})

In [4]: uDict().fromkeys(data, 2)
Out[4]: uDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})

In [5]:

```

### fromvalues()

Create a new dictionary from list of values.
keys automaticaly generate as interger or str.
`base` is the starting number.
if set 'name' to `prefix`, keys will be use 'name01'...
So, set '' to `prefix`, key as str from interger.
If set `True` to `inplace`, perform operation in-place.

```python
In [1]: from datajuggler import aDict,uDict

In [2]: data = [ 'January', 'February', 'March', 'April' ]

In [3]: aDict().fromvalues(data)
Out[3]: aDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})

In [4]: uDict().fromvalues(data)
Out[4]: uDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})

In [6]: aDict().fromvalues(data, base=0)
Out[6]: aDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})

In [7]: aDict().fromvalues(data, base=100)
Out[7]: aDict({100: 'January', 101: 'February', 102: 'March', 103: 'April'})

In [8]: aDict().fromvalues(data, prefix='key_')
Out[8]: aDict({'key_1': 'January', 'key_2': 'February', 'key_3': 'March', 'key_4': 'April'})

In [9]: aDict().fromvalues(data, prefix='')
Out[9]: aDict({'1': 'January', '2': 'February', '3': 'March', '4': 'April'})

In [10]:
```


### fromlists()

Create a new dictionary from two list as keys and values.
Only the number of elements in the shorter of the two lists is processed.
If set `True` to `inplace`, perform operation in-place.


```python
In [1]: from datajuggler import aDict,uDict

In [2]: keys = [ 'January', 'February', 'March', 'April' ]

In [3]: values = [ 1, 2, 3, 4 ]

In [4]: aDict().fromlists(keys, values)
Out[4]: aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})

In [5]: uDict().fromlists(keys, values)
Out[5]: uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})

In [6]:
```


## class IODict

this class support serialize method. Base64, INI, JSON, YAML, TOML, XML.

if not installed PyYAML and/or toml and call from_yaml(), from_tomo(),
will raise NotImpelementedError.

aDict and uDict are subclass of IODict.

 - `from_base64(cls, s, subformat="json", encoding="utf-8", **kwargs)`
 - `from_csv(cls, s, columns=None, columns_row=True, **kwargs)`
 - `from_ini(cls, s, **kwargs)`
 - `from_json(self, s, **kwargs)`
 - `from_pickle(cls, s, **kwargs)`
 - `from_plist(cls, s, **kwargs)`
 - `from_query_string(cls, s, **kwargs)`
 - `from_toml(cls, s, **kwargs)`
 - `from_xml(cls, s, **kwargs)`
 - `from_yaml(cls, s, **kwargs)`

## Serialization

Provides serializer are follows.

 - `Base64Serializer`
 - `CSVSerializer`
 - `INISerializer`
 - `JSONSerializer`
 - `PickleSerializer`
 - `PListSerializer`
 - `QueryStringSerializer``
 - `TOMLSerializer`
 - `XMLSerializer`
 - `YAMLSerializer`

```python
from datajuggler import serializer as io

data = {"console": "Nintendo Switch",
        "games": ["The Legend of Zelda", "Mario Golf"]}

s = io.JSONSerializer()
s.encode(data)
```

and provide helper functions.

 - `get_format_by_path(path)`
 - `get_serializer_by_format(format)`
 - `get_serializers_extensions()`
 - `autodetect_format(s)`
 - `validate_file(s)`
 - `is_url(s)`
 - `is_dsn(s)`
 - `read_contents(s)`
 - `read_database(s)`
 - `read_url(url, **options)`
 - `read_file(filepath, encording="utf-8", **options)`
 - `write_file(filepath, content, encording="utf-8", **options)`

### read_contents()

read contets from filepath.
if requests module installed and filepath is starts with 'http://' or 'https://', read coontes from URL.
if dataset momdule installed and filepath is starts with
'sqlite://' or 'mysql://', 'postgresql://' read contents form DATABASE.

```python
In [1]: from datajuggler import serializer as io

In [2]: io.read_contents('sqlite:///users.sqlite#users')
Out[5]:
[{'id': 1, 'name': 'Jack Bauer', 'age': 55, 'belongs': 'CTU'},
 {'id': 2, 'name': "Chloe O'Brian", 'age': 0, 'belongs': 'CTU'},
 {'id': 3, 'name': 'Anthony Tony', 'age': 29, 'belongs': 'CTU'},
 {'id': 4, 'name': 'David Gilmour', 'age': 75, 'belongs': 'Pink Floyd'},
 {'id': 5, 'name': 'Ann Wilson', 'age': 71, 'belongs': 'Heart'},
 {'id': 6, 'name': 'Nacy Wilson', 'age': 67, 'belongs': 'Heart'}]

In [3]: from datajuggler import uDict

In [4]: d = uDict('sqlite:///users.sqlite#users')

In [5]: d
Out[5]: uDict({'values': [{'id': 1, 'name': 'Jack Bauer', 'age': 55, 'belongs': 'CTU'}, {'id': 2, 'name': "Chloe O'Brian", 'age': 0, 'belongs': 'CTU'}, {'id': 3, 'name': 'Anthony Tony', 'age': 29, 'belongs': 'CTU'}, {'id': 4, 'name': 'David Gilmour', 'age': 75, 'belongs': 'Pink Floyd'}, {'id': 5, 'name': 'Ann Wilson', 'age': 71, 'belongs': 'Heart'}, {'id': 6, 'name': 'Nacy Wilson', 'age': 67, 'belongs': 'Heart'}]})

In [6]:
```

### JSON

#### to_json() and from_json().

```python
In [1]: from datajuggler import aDict,uDict

In [2]: data = {"console": "Nintendo Switch",
   ...:         "games": ["The Legend of Zelda", "Mario Golf"]}
   ...:

In [3]: aDict(data).to_json()
Out[3]: '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'

In [4]: uDict(data).to_json()
Out[4]: '{"console": "Nintendo Switch", "games": ["The Legend of Zelda", "Mario Golf"]}'

In [5]:
```

### YAML

if PyYAML is installed, enable `to_yaml()` and `from_yaml()` method.
otherwise raise NotImplementedError.

```python
In [1]: from datajuggler import aDict
   ...: import yaml
   ...:
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = "{April: 4, February: 2, January: 1, March: 3}\n"
   ...:
   ...: obj = aDict(data)
   ...: result = yaml.safe_dump(obj, default_flow_style=True)
   ...: assert result == expect

In [2]: expect = "{January: 1, February: 2, March: 3, April: 4}\n"
   ...: obj = aDict(data)
   ...: result = yaml.safe_dump(obj, default_flow_style=True,sort_keys=False)
   ...: assert result == expect

In [3]: expect = "{April: 4, February: 2, January: 1, March: 3}\n"
   ...: obj = aDict(data)
   ...: result = obj.to_yaml(default_flow_style=True)
   ...: assert result == expect

In [4]: expect = "{January: 1, February: 2, March: 3, April: 4}\n"
   ...: obj = aDict(data)
   ...: result = obj.to_yaml(default_flow_style=True,sort_keys=False)
   ...: assert result == expect

In [5]: expect = ( "!datajuggler.aDict "
   ...:            "{April: 4, February: 2, January: 1, March: 3}\n" )
   ...: obj = aDict(data)
   ...: result = yaml.dump(obj, default_flow_style=True)
   ...: assert result == expect

In [6]: expect = ( "!datajuggler.aDict "
   ...:            "{January: 1, February: 2, March: 3, April: 4}\n" )
   ...: obj = aDict(data)
   ...: result = yaml.dump(obj, default_flow_style=True,sort_keys=False)
   ...: assert result == expect

In [7]: expect = ( "!datajuggler.aDict "
   ...:            "{April: 4, February: 2, January: 1, March: 3}\n" )
   ...: obj = aDict(data)
   ...: result = obj.to_yaml(Dumper=yaml.Dumper,  default_flow_style=True)
   ...: assert result == expect

In [8]: expect = ( "!datajuggler.aDict "
   ...:            "{January: 1, February: 2, March: 3, April: 4}\n" )
   ...: obj = aDict(data)
   ...: result = obj.to_yaml(Dumper=yaml.Dumper,
   ...:                      default_flow_style=True, sort_keys=False)
   ...: assert result == expect

In [9]: data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
   ...: expect = "{one: {two: {three: {four: 4}}}}\n"
   ...: obj = aDict(data)
   ...: result = obj.to_yaml(default_flow_style=True,sort_keys=False)
   ...: assert result  == expect

In [10]: expect = ( "!datajuggler.aDict "
    ...:            "{one: {two: {three: {four: 4}}}}\n" )
    ...: obj = aDict(data)
    ...: result = obj.to_yaml(Dumper=yaml.Dumper,
    ...:                      default_flow_style=True, sort_keys=False)
    ...: assert result  == expect

In [11]: yaml_str = ( "!datajuggler.aDict "
    ...:              "{April: 4, February: 2, January: 1, March: 3}\n" )
    ...: expect = ( "aDict("
    ...:            "{'April': 4, 'February': 2, 'January': 1, 'March': 3}"
    ...:            ")" )
    ...: obj = aDict()
    ...: result = obj.from_yaml(yaml_str)
    ...: assert result.__repr__() == expect

In [12]: yaml_str = ( "!python/object:datajuggler.aDict "
    ...:              "{April: 4, February: 2, January: 1, March: 3}\n" )
    ...: expect = ( "aDict("
    ...:            "{'April': 4, 'February': 2, 'January': 1, 'March': 3}"
    ...:            ")" )
    ...: obj = aDict()
    ...: result = obj.from_yaml(yaml_str)
    ...: assert result.__repr__() == expect

In [13]: yaml_str = ( "!datajuggler.aDict "
    ...:              "{January: 1, February: 2, March: 3, April: 4}\n" )
    ...: expect = ( "aDict("
    ...:            "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
    ...:            ")" )
    ...: obj = aDict()
    ...: result = obj.from_yaml(yaml_str)
    ...: assert result.__repr__() == expect

In [14]: yaml_str = ( "!python/object:datajuggler.aDict "
    ...:              "{January: 1, February: 2, March: 3, April: 4}\n" )
    ...: expect = ( "aDict("
    ...:            "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
    ...:            ")" )
    ...: obj = aDict()
    ...: result = obj.from_yaml(yaml_str)
    ...: assert result.__repr__() == expect

In [15]: yaml_str = ( "!datajuggler.aDict "
    ...:              "{April: 4, February: 2, January: 1, March: 3}\n" )
    ...: expect = "aDict({})"
    ...: obj = aDict()
    ...: _ = obj.from_yaml(yaml_str)
    ...: assert obj.__repr__() == expect

In [16]: yaml_str = ( "!python/object:datajuggler.aDict "
    ...:              "{January: 1, February: 2, March: 3, April: 4}\n" )
    ...: expect = "aDict({})"
    ...: obj = aDict()
    ...: _ = obj.from_yaml(yaml_str)
    ...: assert obj.__repr__() == expect

In [17]: yaml_str = ( "!datajuggler.aDict "
    ...:              "{April: 4, February: 2, January: 1, March: 3}\n" )
    ...: expect = ( "aDict("
    ...:            "{'April': 4, 'February': 2, 'January': 1, 'March': 3}"
    ...:            ")" )
    ...: obj = aDict()
    ...: obj.from_yaml(yaml_str, inplace=True)
    ...: assert obj.__repr__() == expect

In [18]: yaml_str = ( "!python/object:datajuggler.aDict "
    ...:              "{January: 1, February: 2, March: 3, April: 4}\n" )
    ...: expect = ( "aDict("
    ...:            "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
    ...:            ")" )
    ...: obj = aDict()
    ...: obj.from_yaml(yaml_str, inplace=True)
    ...: assert obj.__repr__() == expect

In [19]:
```


```python
In [1]: from datajuggler import uDict
   ...: import yaml
   ...:
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = "{April: 4, February: 2, January: 1, March: 3}\n"
   ...:
   ...: obj = uDict(data)
   ...: result = yaml.safe_dump(obj, default_flow_style=True)
   ...: assert result == expect

In [2]: expect = "{January: 1, February: 2, March: 3, April: 4}\n"
   ...: obj = uDict(data)
   ...: result = yaml.safe_dump(obj, default_flow_style=True,sort_keys=False)
   ...: assert result == expect

In [3]: expect = "{April: 4, February: 2, January: 1, March: 3}\n"
   ...: obj = uDict(data)
   ...: result = obj.to_yaml(default_flow_style=True)
   ...: assert result == expect

In [4]: expect = "{January: 1, February: 2, March: 3, April: 4}\n"
   ...: obj = uDict(data)
   ...: result = obj.to_yaml(default_flow_style=True,sort_keys=False)
   ...: assert result == expect

In [5]: expect = ( "!datajuggler.uDict "
   ...:            "{April: 4, February: 2, January: 1, March: 3}\n" )
   ...: obj = uDict(data)
   ...: result = yaml.dump(obj, default_flow_style=True)
   ...: assert result == expect

In [6]: expect = ( "!datajuggler.uDict "
   ...:            "{January: 1, February: 2, March: 3, April: 4}\n" )
   ...: obj = uDict(data)
   ...: result = yaml.dump(obj,default_flow_style=True,sort_keys=False)
   ...: assert result == expect

In [7]: expect = ( "!datajuggler.uDict "
   ...:            "{April: 4, February: 2, January: 1, March: 3}\n" )
   ...: obj = uDict(data)
   ...: result = obj.to_yaml(Dumper=yaml.Dumper,  default_flow_style=True)
   ...: assert result == expect

In [8]: expect = ( "!datajuggler.uDict "
   ...:            "{January: 1, February: 2, March: 3, April: 4}\n" )
   ...: obj = uDict(data)
   ...: result = obj.to_yaml(Dumper=yaml.Dumper,
   ...:                      default_flow_style=True, sort_keys=False)
   ...: assert result == expect

In [9]: data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
   ...: expect = "{one: {two: {three: {four: 4}}}}\n"
   ...:
   ...: obj = uDict(data)
   ...: result = obj.to_yaml(default_flow_style=True,sort_keys=False)
   ...: assert result  == expect

In [10]: expect = ( "!datajuggler.uDict "
    ...:            "{one: {two: {three: {four: 4}}}}\n" )
    ...: obj = uDict(data)
    ...: result = obj.to_yaml(Dumper=yaml.Dumper,
    ...:                      default_flow_style=True, sort_keys=False)
    ...: assert result  == expect

In [11]: yaml_str = ( "!datajuggler.uDict "
    ...:              "{April: 4, February: 2, January: 1, March: 3}\n" )
    ...: expect = ( "uDict("
    ...:            "{'April': 4, 'February': 2, 'January': 1, 'March': 3}"
    ...:            ")" )
    ...: obj = uDict()
    ...: result = obj.from_yaml(yaml_str)
    ...: assert result.__repr__() == expect

In [12]: yaml_str = ( "!python/object:datajuggler.uDict "
    ...:              "{April: 4, February: 2, January: 1, March: 3}\n" )
    ...: expect = ( "uDict("
    ...:            "{'April': 4, 'February': 2, 'January': 1, 'March': 3}"
    ...:            ")" )
    ...: obj = uDict()
    ...: result = obj.from_yaml(yaml_str)
    ...: assert result.__repr__() == expect

In [13]: yaml_str = ( "!datajuggler.uDict "
    ...:              "{January: 1, February: 2, March: 3, April: 4}\n" )
    ...: expect = ( "uDict("
    ...:            "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
    ...:            ")" )
    ...: obj = uDict()
    ...: result = obj.from_yaml(yaml_str)
    ...: assert result.__repr__() == expect

In [14]: yaml_str = ( "!python/object:datajuggler.uDict "
    ...:              "{January: 1, February: 2, March: 3, April: 4}\n" )
    ...: expect = ( "uDict("
    ...:            "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
    ...:            ")" )
    ...: obj = uDict()
    ...: result = obj.from_yaml(yaml_str)
    ...: assert result.__repr__() == expect

In [15]: yaml_str = ( "!datajuggler.uDict "
    ...:              "{April: 4, February: 2, January: 1, March: 3}\n" )
    ...: expect = "uDict({})"
    ...: obj = uDict()
    ...: _ = obj.from_yaml(yaml_str)
    ...: assert obj.__repr__() == expect

In [16]: yaml_str = ( "!python/object:datajuggler.uDict "
    ...:              "{January: 1, February: 2, March: 3, April: 4}\n" )
    ...: expect = "uDict({})"
    ...: obj = uDict()
    ...: _ = obj.from_yaml(yaml_str)
    ...: assert obj.__repr__() == expect

In [17]: yaml_str = ( "!datajuggler.uDict "
    ...:              "{April: 4, February: 2, January: 1, March: 3}\n" )
    ...: expect = ( "uDict("
    ...:            "{'April': 4, 'February': 2, 'January': 1, 'March': 3}"
    ...:            ")" )
    ...: obj = uDict()
    ...: obj.from_yaml(yaml_str, inplace=True)
    ...: assert obj.__repr__() == expect

In [18]: yaml_str = ( "!python/object:datajuggler.uDict "
    ...:              "{January: 1, February: 2, March: 3, April: 4}\n" )
    ...: expect = ( "uDict("
    ...:            "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
    ...:            ")" )
    ...: obj = uDict()
    ...: obj.from_yaml(yaml_str, inplace=True)
    ...: assert obj.__repr__() == expect

In [19]:
```



### TOML

if toml is installed or using Python 3.11 or later, enable `to_toml()` and `from_toml()` method.
otherwise raise NotImplementedError.

```python
In [1]: from datajuggler import aDict,  uDict
   ...:
   ...: data = {'target': {'ip': 'xx.xx.xx.xx',
   ...:   'os': {'os': 'win 10', 'Arch': 'x64'},
   ...:   'ports': {'ports': ['1', '2'], '1': {'service': 'xxx', 'ver': '5.9'}}}
   ...: }
   ...:
   ...: toml_str = ( '[target]\nip = "xx.xx.xx.xx"\n\n'
   ...:              '[target.os]\nos = "win 10"\nArch = "x64"\n\n'
   ...:              '[target.ports]\nports = [ "1", "2",]\n\n'
   ...:              '[target.ports.1]\nservice = "xxx"\nver = "5.9"\n' )
   ...:
   ...: result = aDict(data).to_toml()
   ...: assert result == toml_str

In [2]: result = aDict().to_toml(data)
   ...: assert result == toml_str

In [3]: obj = aDict()
   ...: result = obj.from_toml(toml_str)
   ...: assert result == data

In [4]: obj = aDict()
   ...: obj.from_toml(toml_str, inplace=True)
   ...: assert obj == data

In [5]: result = uDict(data).to_toml()
   ...: assert result == toml_str

In [6]: result = uDict().to_toml(data)
   ...: assert result == toml_str

In [7]: obj = uDict()
   ...: result = obj.from_toml(toml_str)
   ...: assert result == data

In [8]: obj = uDict()
   ...: obj.from_toml(toml_str, inplace=True)
   ...: assert obj == data

```

## class aDict

Allow to access using dot notation for dictionary.
This class is inspired by [munch](https://github.com/Infinidat/munch).
aDict is subclass of BaseDict.

This class is inspired by [munch](https://github.com/Infinidat/munch) and [adict](https://github.com/mewwts/addict).

```python
In [1]: from datajuggler import aDict

In [2]: d = aDict()

In [3]: d.python = 'great'

In [4]: d
Out[4]: aDict({'python': 'great'})

In [5]: d['python']
Out[5]: 'great'

In [6]: data = {'one': {'two': {'three': {'four': 4 }}}}

In [7]: d = aDict(data)

In [8]: d
Out[8]: aDict({'one': aDict({'two': aDict({'three': aDict({'four': 4})})})})

In [9]: d.one.two.three.four
Out[9]: 4

In [10]:
```

aDict support hashable and immutable dictionary.

 - `freeze()` - freeze object for immutable.
 - `unfreeze()` - unfreeze object

built-in function `hash()` acceptfrozen object.
So, frozen aDict object is able to set as key to dictionary.

```python
In [1]: from datajuggler import aDict

In [2]: d = aDict({'one': {'two': {'three': {'four': 4 }}}})

In [3]: d
Out[3]: aDict({'one': aDict({'two': aDict({'three': aDict({'four': 4})})})})

In [4]: d.one.two.three.four = 1

In [5]: d.freeze()

In [6]: try:
   ...:     d.one.two.three.four = 2
   ...: except AttributeError as e:
   ...:     print(e)
   ...:
aDict frozen object cannot be modified.

In [7]: d.unfreeze()

In [8]: d.one.two.three.four = 2

In [9]:
```


## class Keypath and Keylist

This is utility class for uDict and manage for keypath and Keylist

```python
    { 'a': { 'b1': { 'c1': {'x': 1 },
                     'c2': {'x': 2 }},
           { 'b2': { 'c1': {'x': 3 },
                     'c2': {'x': 4 }} }}}
```
Keylist(['a','b1', 'c1', 'x']) point to value `1`.
Keypath(['a.b1.c1.x']) point to value `1`.

The following keylists is evaluated as the same value.

 - Keylist(['a', 'b', 1, 'c', 1, 'x']
 - Keylist(['a', 'b[1]', 'c[1]', 'x']

### methods for Keylist class

 - `keylistss(d: dict)`
 - `to_keypath(d: dict)`
 - `list2path(keylist)`
 - `value()`
 - `validate(keylist)`

### methods for Keypath class
 - `keypaths(d: dict)`
 - `to_keylist(keypath)`
 - `path2list(keypath)`
 - `value()`
 - `validate(keypath)`

### keylists()

keylists() suppport list of key as keys.

 - `keylists(obj, indexes=False)`

```python
In [1]: from datajuggler import keylists
   ...:
   ...: data = { "a": 1,
   ...:          "b": { "c": { "x": 2, "y": 3, },
   ...:                 "d": { "x": 4, "y": 5, },
   ...:               },
   ...:         }
   ...:
   ...: expect = [ ["a"],
   ...:            ["b"],
   ...:            ["b", "c"],
   ...:            ["b", "c", "x"],
   ...:            ["b", "c", "y"],
   ...:            ["b", "d"],
   ...:            ["b", "d", "x"],
   ...:            ["b", "d", "y"],
   ...:        ]
   ...: result = keylists(data)
   ...: assert result == expect

In [2]: data = { 1: { 1: 1, },
   ...:          2: { 2: 1, },
   ...:          3: { None: 1, },
   ...:        }
   ...: expect = [[1], [1, 1], [2], [2, 2], [3], [3, None]]
   ...: result = keylists(data)
   ...: assert result == expect

   ...:                        { "x": 2, "y": -2, "z": [2, 3, 4], },
   ...:                        { "x": 3, "y": -3, "z": [3, 4, 5], },
   ...:                      ],
   ...:               },
   ...:        }
   ...: expect = [
   ...:     ["a"],
   ...:     ["b"],
   ...:     ["b", "c"],
   ...:     ["b", "c", "x"],
   ...:     ["b", "c", "y"],
   ...:     ["b", "d"],
   ...:     ["b", "d", "x"],
   ...:     ["b", "d", "y"],
   ...:     ["b", "e"],
   ...:     ["b", "e[0]"],
   ...:     ["b", "e[0]", "x"],
   ...:     ["b", "e[0]", "y"],
   ...:     ["b", "e[0]", "z"],
   ...:     ["b", "e[0]", "z[0]"],
   ...:     ["b", "e[0]", "z[1]"],
   ...:     ["b", "e[0]", "z[2]"],
   ...:     ["b", "e[1]"],
   ...:     ["b", "e[1]", "x"],
   ...:     ["b", "e[1]", "y"],
   ...:     ["b", "e[1]", "z"],
   ...:     ["b", "e[1]", "z[0]"],
   ...:     ["b", "e[1]", "z[1]"],
   ...:     ["b", "e[1]", "z[2]"],
   ...:     ["b", "e[2]"],
   ...:     ["b", "e[2]", "x"],
   ...:     ["b", "e[2]", "y"],
   ...:     ["b", "e[2]", "z"],
   ...:     ["b", "e[2]", "z[0]"],
   ...:     ["b", "e[2]", "z[1]"],
   ...:     ["b", "e[2]", "z[2]"],
   ...: ]
   ...: result  = keylists(data, indexes=True)
   ...: result.sort()
   ...: assert result == expect

In [4]: data = { "a": { "b": [
   ...:                    [1, 2],
   ...:                    [3, 4, 5],
   ...:                    [ { "x": 1, "y": -1, }, ],
   ...:                  ],
   ...:               },
   ...:        }
   ...: expect = [ ["a"],
   ...:            ["a", "b"],
   ...:            ["a", "b[0]"],
   ...:            ["a", "b[0][0]"],
   ...:            ["a", "b[0][1]"],
   ...:            ["a", "b[1]"],
   ...:            ["a", "b[1][0]"],
   ...:            ["a", "b[1][1]"],
   ...:            ["a", "b[1][2]"],
   ...:            ["a", "b[2]"],
   ...:            ["a", "b[2][0]"],
   ...:            ["a", "b[2][0]", "x"],
   ...:            ["a", "b[2][0]", "y"],
   ...:         ]
   ...: result = keylists(data, indexes=True)
   ...: result.sort()
   ...: assert result == expect

In [5]: data = { "a": 1,
   ...:          "b": { "c": { "x": 2, "y": 3, },
   ...:                 "d": { "x": 4, "y": 5, },
   ...:                 "e": [ { "x": 1, "y": -1, "z": [1, 2, 3], },
   ...:                        { "x": 2, "y": -2, "z": [2, 3, 4], },
   ...:                        { "x": 3, "y": -3, "z": [3, 4, 5], },
   ...:                      ],
   ...:               },
   ...:       }
   ...: expect = [ ["a"],
   ...:            ["b"],
   ...:            ["b", "c"],
   ...:            ["b", "c", "x"],
   ...:            ["b", "c", "y"],
   ...:            ["b", "d"],
   ...:            ["b", "d", "x"],
   ...:            ["b", "d", "y"],
   ...:            ["b", "e"],
   ...:        ]
   ...: result = keylists(data, indexes=False)
   ...: result.sort()
   ...: assert result == expect

In [6]:
```

### keypaths()

Keypath support attribute-styple access to value (dot-notation by default).

 - `keypaths(obj, separator, indexes=False)`

```python
In [1]: from datajuggler import keypaths
   ...:
   ...: data = { "a": 1,
   ...:          "b": { "c": { "x": 2, "y": 3 },
   ...:                 "d": { "x": 4, "y": 5 },
   ...:          },
   ...: }
   ...: expect = [ "a",
   ...:            "b",
   ...:            "b.c",
   ...:            "b.c.x",
   ...:            "b.c.y",
   ...:            "b.d",
   ...:            "b.d.x",
   ...:            "b.d.y",
   ...:       ]
   ...:
   ...: result = keypaths(data)
   ...: assert result == expect

In [2]: data = { "a": 1,
   ...:          "b": { "c": { "x": 2, "y": 3 },
   ...:          "d": { "x": 4, "y": 5 },
   ...:     },
   ...: }
   ...: expect = [ "a",
   ...:            "b",
   ...:            "b c",
   ...:            "b c x",
   ...:            "b c y",
   ...:            "b d",
   ...:            "b d x",
   ...:            "b d y",
   ...:       ]
   ...: result = keypaths(data, separator=" ")
   ...: assert result == expect

In [3]: data = { 1: { 1: 1 }, 2: { 2: 1 }, 3: { 3: 1 } }
   ...: expect = ['1', '1.1', '2', '2.2', '3', '3.3']
   ...: result = keypaths(data)
   ...: assert result == expect

In [4]: data = { "a": 1,
   ...:          "b": { "c": { "x": 2, "y": 3, },
   ...:                 "d": { "x": 4, "y": 5, },
   ...:                 "e": [ { "x": 1, "y": -1, "z": [1, 2, 3], },
   ...:                        { "x": 2, "y": -2, "z": [2, 3, 4], },
   ...:                        { "x": 3, "y": -3, "z": [3, 4, 5], },
   ...:                 ],
   ...:             },
   ...:         }
   ...: expect = [ "a",
   ...:            "b",
   ...:            "b.c", "b.c.x", "b.c.y", "b.d", "b.d.x", "b.d.y", "b.e",
   ...:            "b.e[0]", "b.e[0].x", "b.e[0].y", "b.e[0].z",
   ...:            "b.e[0].z[0]", "b.e[0].z[1]", "b.e[0].z[2]",
   ...:            "b.e[1]", "b.e[1].x", "b.e[1].y", "b.e[1].z",
   ...:            "b.e[1].z[0]", "b.e[1].z[1]", "b.e[1].z[2]",
   ...:            "b.e[2]", "b.e[2].x", "b.e[2].y", "b.e[2].z",
   ...:            "b.e[2].z[0]", "b.e[2].z[1]", "b.e[2].z[2]",
   ...:     ]
   ...:
   ...: result = keypaths(data, indexes=True)
   ...: assert result == expect

In [5]: data = { "a": 1,
   ...:          "b": {
   ...:             "c": { "x": 2, "y": 3, },
   ...:             "d": { "x": 4, "y": 5, },
   ...:             "e": [ { "x": 1, "y": -1, "z": [1, 2, 3], },
   ...:                    { "x": 2, "y": -2, "z": [2, 3, 4], },
   ...:                    { "x": 3, "y": -3, "z": [3, 4, 5], },
   ...:                  ],
   ...:             },
   ...:         }
   ...: expect = [ "a",
   ...:            "b",
   ...:            "b.c",
   ...:            "b.c.x",
   ...:            "b.c.y",
   ...:            "b.d",
   ...:            "b.d.x",
   ...:            "b.d.y",
   ...:            "b.e",
   ...:        ]
   ...: result = keypaths(data, indexes=False)
   ...: assert result == expect

In [6]: data  = { "a": { "b": [ [1, 2],
   ...:                         [3, 4, 5],
   ...:                         [ { "x": 1, "y": -1, }, ],
   ...:                   ],
   ...:             },
   ...:      }
   ...: expect = [ "a",
   ...:            "a.b",
   ...:            "a.b[0]",
   ...:            "a.b[0][0]",
   ...:            "a.b[0][1]",
   ...:            "a.b[1]",
   ...:            "a.b[1][0]",
   ...:            "a.b[1][1]",
   ...:            "a.b[1][2]",
   ...:            "a.b[2]",
   ...:            "a.b[2][0]",
   ...:            "a.b[2][0].x",
   ...:            "a.b[2][0].y",
   ...: ]
   ...: result = keypaths(data, indexes=True)
   ...: assert result == expect

In [7]:
```

### list2path() and path2list()
Convert from/to keylists and keypaths.

```python
In [1]: from datajuggler import Keylist, Keypath
   ...:
   ...: data = ['x', 'y', 'z']
   ...: expect = ['x.y.z']
   ...:
   ...: result = Keylist.list2path(data)
   ...: assert result == expect

In [2]: expect = ['x_y_z']
   ...: result = Keylist.list2path(data, separator='_')
   ...: assert result == expect

In [3]: data = [['x', 'y', 'z'], ['a', 'b', 'c']]
   ...: expect = ['x.y.z', 'a.b.c']
   ...: result = Keylist.list2path(data)
   ...: assert result == expect

In [4]: data = 'x.y.z'
   ...: expect = ['x', 'y', 'z']
   ...: result = Keypath.path2list(data)
   ...: assert result == expect

In [5]: data = 'x_y_z'
   ...: expect = ['x', 'y', 'z']
   ...: result = Keypath.path2list(data, separator='_')
   ...: assert result == expect

In [6]: data = ['x.y.z', 'a.b.c']
   ...: expect = [['x', 'y', 'z'], ['a', 'b', 'c']]
   ...: result = Keypath.path2list(data)
   ...: assert result == expect

In [7]:
```

## class uDict
uDict is utilized dictionary which is subclass of IODict.
This class is inspired by [python-benedict](https://github.com/fabiocaccamo/python-benedict).
uDict support keypath and keylist.

uDict has following  methods.

 - `clean(d1: dict, strings=True, collections=True,
          inplace=False, factory=dict)`
 - `clone(d1: dict, empty=False, memo=None)`
 - `compare(d1: dict, d2: dict, keys=None, thrown_error=False)`
 - `counts(pattern, d=None, count_for"key", wild=False, verbatim=False)`
 - `filter(predicate, d=None, factory=dict)`
 - `get_keys(d=None, output_as=None)`
 - `get_values(keys, d=None)`
 - `groupby(seq, key, factory=dict)`
 - `invert(d=None, flat=False, inplace=False, factory=dict)`
 - `keylists(d=None, indexes=False)`
 - `keypaths(d=None, indexes=False, separator=".")`
 - `map(func, d=None, map_for=None, inplace=False, factory=dict)`
 - `merge(other, d=None, overwrite=False, inplace=False, factory=dict)`
 - `move(key_src, key_dest, d=None, overwrite=False, inplace=False, factory=dict)`
 - `nest(items, key, patrent_key, children_key)`
 - `rename(key, key_new, d=None, case_name=None, overwrite=False,
           inplace=False, factory=dict)`
 - `remove(keys, d=None, inplace=False, factory=dict)`
 - `subset(keys, d=None, default=None, use_keypath=False,
           separator=".", inplace=False, factory=dict)`
 - `find(keys, d=None, default=None, first_one=True, factory=dict)`
 - `search(query, d=None, search_for="key", exact=False, ignore_case=False)`
 - `sort(d=None, sort_by="key", reverse=False, inplace=False, factory=dict)`
 - `swap(key1, key2, d=None, inplace=False, factory=dict)`
 - `flatten(d=None, separator=".", inplace=False, factory=dict)`
 - `unflatten(d=None, default=None, separator=".", inplace=False, factory=dict)`
 - `traverse(callback, d=None, parents=[], *args, **kwargs)`
 - `unique(d=None)`
 - `get_items(loc, value, d=None, func=None,
                   separator='.',inplace=False,  factory=dict)`
 - `pop_items(loc, value, d=None, func=None,
                   separator='.',inplace=False,  factory=dict)`
 - `del_items(loc, value, d=None, func=None,
                   separator='.',inplace=False,  factory=dict)`
 - `set_items(loc, value, d=None, func=None,
                   separator='.',inplace=False,  factory=dict)`

helper functions are defined in datajuggler.dicthelper for normal dict objects.

 - `d_clean()`
 - `d_clone()`
 - `d_compare()`
 - `d_counts()`
 - `d_filter()`
 - `d_groupby()`
  - d_invert()`
 - `d_map()`
 - `d_merge()`
 - `d_move()`
 - `d_rename()`
 - `d_remove()`
 - `d_nest()`
 - `d_subset()`
 - `d_find()`
 - `d_sort()`
 - `d_search()`
 - `d_swap()`
 - `d_flatten()`
 - `d_unflatten()`
 - `d_traverse()`
 - `d_unique()`
 - `get_keys()`
 - `get_values()`
 - `get_items()`
 - `pop_items()`
 - `del_items()`
 - `set_items()`

### clean() and d_clean()

```python
def clean(self,
        obj: Optional[dict]=None,
        strings=True,
        collections=True,
        inplace: bool=False,
        factory: Optional[Type[dict]]=None,
    ):
```

```python
def d_clean(
        obj: dict,
        strings=True,
        collections=True,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ):
```

Clean the current dict instance removing all empty values:

    None, '', {}, [], ().

If strings or collections (dict, list, set, tuple) flags are False,
related empty values will not be deleted.


```python
In [1]: from datajuggler import aDict
   ...: from datajuggler.dicthelper import d_clean
   ...:
   ...: data = {
   ...:     "a": {},
   ...:     "b": {"x": 1},
   ...:     "c": [],
   ...:     "d": [0, 1],
   ...:     "e": 0.0,
   ...:     "f": "",
   ...:     "g": None,
   ...:     "h": "0",
   ...: }
   ...:
   ...: expect = {
   ...:     "b": {"x": 1},
   ...:     "d": [0, 1],
   ...:     "e": 0.0,
   ...:     "h": "0",
   ...: }
   ...:
   ...: result = d_clean(data)
   ...: assert result == expect

In [2]: expect = {
   ...:     "a": {},
   ...:     "b": {"x": 1},
   ...:     "c": [],
   ...:     "d": [0, 1],
   ...:     "e": 0.0,
   ...:     "h": "0",
   ...: }
   ...:
   ...: result = d_clean(data, collections=False)
   ...: assert result == expect

In [3]: expect = {
   ...:     "b": {"x": 1},
   ...:     "d": [0, 1],
   ...:     "e": 0.0,
   ...:     "f": "",
   ...:     "h": "0",
   ...: }
   ...:
   ...: result = d_clean(data, strings=False)
   ...: assert result == expect

In [4]: expect = aDict({
   ...:             "b": {"x": 1},
   ...:             "d": [0, 1],
   ...:             "e": 0.0,
   ...:             "h": "0",
   ...:          })
   ...:
   ...: result = d_clean(data, factory=aDict)
   ...: assert result == expect

In [5]: expect = {
   ...:     "b": {"x": 1},
   ...:     "d": [0, 1],
   ...:     "e": 0.0,
   ...:     "h": "0",
   ...: }
   ...:
   ...: d_clean(data, inplace=True)
   ...: assert data == expect

In [6]:
```

### clone() and d_clone()

```python
def clone(self,
        obj: Optional[dict]=None,
        empty: bool=False,
        memo: Optional[dict]=None,
        factory: Optional[Type[dict]]=None,
    ):
```

```python
def d_clone(
        obj: dict,
        empty: bool=False,
        memo: Optional[dict]=None,
    ):
```

Return a clone (deepcopy) of the dict.

```python
In [1]: from datajuggler.dicthelper import d_clone
   ...:
   ...: data = { "a": { "b": { "c": 1, }, }, }
   ...:
   ...: result = d_clone(data)
   ...: assert isinstance(result, dict) == True
   ...: assert result == data

In [2]: result["a"]["b"]["c"] = 2
   ...:
   ...: assert result["a"]["b"]["c"] == 2
   ...: assert data["a"]["b"]["c"] == 1

In [3]: data = { "a": { "b": { "c": 1, }, }, }
   ...: result = d_clone(data, empty=True)
   ...: assert isinstance(result, dict) == True
   ...: assert result == {}

In [4]:
```

### compare() and d_compare()

```python
def compare(self,
    d1: dict,
    d2: Optional[dict]=None,
    *,
    keys: Optional[Union[Hashable,list]]=None,
    keylist: bool=False,
    keypath: bool=False,
    thrown_error: bool=False,
    ):
```

```pythob
def d_compare(
        d1: dict,
        d2: dict,
        *,
        keys: Optional[Union[Hashable,list, Keylist, Keypath]]=None,
        keylist: bool=False,
        keypath: bool=False,
        thrown_error: bool=False,
    ):
```

Compare tow dictionary with keys and return `True` when equal found values.
otherwise return `False`.

if not set second dictionary, use self object.
if not set keys, just compare two dictionaries,
if pass `thrown_error=True`, raise ValueError when not equal found values.
if passs `keylist=True`, keylist accept for key.
if passs `keypath=True`, keypath accept for key.

```python
In [1]: from datajuggler import aDict, Keylist, Keypath
   ...: from datajuggler.dicthelper import d_compare
   ...:
   ...: d1 = {}
   ...: d2 = {}
   ...: result = d_compare(d1, d2)
   ...: assert result == True

In [2]: d1 = {1: 1}
   ...: d2 = {1: 1}
   ...: result = d_compare(d1, d2)
   ...: assert result == True

In [3]: d1 = {'1': 'one'}
   ...: d2 = {'1': 'one'}
   ...: result = d_compare(d1, d2)
   ...: assert result == True

In [4]: d1 = {'1': 'one'}
   ...: d2 = {'1':  2}
   ...: result = d_compare(d1, d2)
   ...: assert result == False

In [5]: d1 = { "a": 1, "b": [1,2,3] }
   ...: d2 = { "a": 1, "b": [1,2,3] }
   ...: result = d_compare(d1, d2)
   ...: assert result == True

In [6]: d1 = { "a": 1,
   ...:        "b": 2,
   ...:        "c": {
   ...:             "d": {
   ...:                 "e": 3,
   ...:                 "f": 4,
   ...:                 "g": { "h": 5, },
   ...:             }
   ...:          },
   ...:       }
   ...: d2 = { "a": 1,
   ...:        "b": 2,
   ...:        "c": {
   ...:             "d": {
   ...:                 "e": 3,
   ...:                 "f": 4,
   ...:                 "g": { "h": 5, },
   ...:             }
   ...:          },
   ...:       }
   ...: result = d_compare(d1, d2)
   ...: assert result == True

In [7]: d1 = { "a": 1,
   ...:        "b": 2,
   ...:        "c": {
   ...:             "d": {
   ...:                 "e": 3,
   ...:                 "f": 4,
   ...:                 "g": { "h": 5, },
   ...:             }
   ...:          },
   ...:       }
   ...: d2 = { "a": 1,
   ...:        "b": 2,
   ...:        "c": {
   ...:             "d": {
   ...:                 "e": 13,
   ...:                 "f": 14,
   ...:                 "g": { "h": 5, },
   ...:             }
   ...:          },
   ...:       }
   ...: result = d_compare(d1, d2, keys='b')
   ...: assert result == True

In [8]: d1 = { "a": 1,
   ...:        "b": 2,
   ...:        "c": {
   ...:             "d": {
   ...:                 "e": 3,
   ...:                 "f": 4,
   ...:                 "g": { "h": 5, },
   ...:             }
   ...:          },
   ...:       }
   ...: d2 = { "a": 1,
   ...:        "b": 2,
   ...:        "c": {
   ...:             "d": {
   ...:                 "e": 13,
   ...:                 "f": 14,
   ...:                 "g": { "h": 5, },
   ...:             }
   ...:          },
   ...:       }
   ...: result = d_compare(d1, d2, keys='d')
   ...: assert result == False

In [9]: d1 = { "a": 1,
   ...:        "b": 2,
   ...:        "c": {
   ...:             "d": {
   ...:                 "e": 3,
   ...:                 "f": 4,
   ...:                 "g": { "h": 5, },
   ...:             }
   ...:          },
   ...:       }
   ...: d2 = { "a": 1,
   ...:        "b": 2,
   ...:        "c": {
   ...:             "d": {
   ...:                 "e": 13,
   ...:                 "f": 14,
   ...:                 "g": { "h": 5, },
   ...:             }
   ...:          },
   ...:       }
   ...: result = d_compare(d1, d2, keys=Keylist(['c', 'd', 'g']))
   ...: assert result == True

In [10]: d1 = { "a": 1,
    ...:        "b": 2,
    ...:        "c": {
    ...:             "d": {
    ...:                 "e": 3,
    ...:                 "f": 4,
    ...:                 "g": { "h": 5, },
    ...:             }
    ...:          },
    ...:       }
    ...: d2 = { "a": 1,
    ...:        "b": 2,
    ...:        "c": {
    ...:             "d": {
    ...:                 "e": 13,
    ...:                 "f": 14,
    ...:                 "g": { "h": 5, },
    ...:             }
    ...:          },
    ...:       }
    ...: result = d_compare(d1, d2, keys=Keypath('c.d.g'))
    ...: assert result == True

In [11]:
```

### counts() and d_counts()

```python
def counts(self,
        pattern: Union[Pattern, Hashable, Sequence],
        obj: Optional[dict]=None,
        count_for: DictItemType=DictItem.KEY,
        wild: bool=False,
        verbatim: bool=False,
    ) ->Union[int, dict]:
```

```python
def d_counts(
        obj: dict,
        pattern: Union[Hashable, Pattern, Sequence],
        count_for: DictItemType=DictItem.KEY,
        wild: bool=False,
        verbatim: bool=False,
    ) ->Union[int, dict]:
```
Counts of keys or values.
`count_for` accept "key" and "value".
if pass `wild=True`, match substr and ignore_case.
if pass `verbatim=True`, counts as it is.


```python
In [1]: from datajuggler.dicthelper import d_counts
   ...:
   ...: data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
   ...:                           {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
   ...: d_counts(data, 'aA')
Out[1]: 2

In [2]: d_counts(data, 'aA', count_for='key')
Out[2]: 2

In [3]: d_counts(data, 'aa', count_for='key')
Out[3]: 0

In [4]: d_counts(data, 'aa', count_for='key', wild=True)
Out[4]: 2

In [5]: d_counts(data, ['aA', 'b'])
Out[5]: defaultdict(int, {'aA': 2, 'b': 2})

In [6]: d_counts(data, ['aA', 'b'], wild=True)
Out[6]: defaultdict(int, {'aA': 2, 'b': 2})

In [7]: d_counts(data, ['a', 'b'], wild=True, verbatim=True)
Out[7]: defaultdict(int, {'aA': 2, 'b': 2})

In [8]: d_counts(data, 'v11', count_for='value')
Out[8]: {'v11': 1}

In [9]: d_counts(data, 'v1', count_for='value', wild=True)
Out[9]: {'v1': 3}

In [10]: d_counts(data, 'v1', count_for='value', wild=True, verbatim=True)
Out[10]: {'v11': 1, 'v12': 1, 'v13': 1}

In [11]: data = {'x': {'y': {'z': [{'aA': 100, 'b': 101, 'c': 103},
    ...:                           {'aA': 100, 'b': 101, 'c': 103}]} }}
    ...: d_counts(data, 100, count_for='value')
Out[11]: {100: 2}

In [12]:
```

### filter() and d_filter()

```python
def filter(self,
        predicate: Callable,
        obj: Optional[dict]=None,
        factory: Optional[Type[dict]]=None,
    ):
```

```python
def d_filter(
        predicate: Callable,
        obj: dict,
        factory: Type[dict]=dict,
    ):
```

Create a new dictionary with filter items in dictionary by item.

Predicate function receives key, value arguments
and should return a bool value.
If set `factory`, create instance of factory class.
If set `True` to `inplace`, perform operation in-place.

```python
In [1]: from datajuggler import uDict,  aDict
   ...: from datajuggler.dicthelper import d_filter
   ...:
   ...:
   ...: is_janfeb = lambda x, y: x.endswith('ary')
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...:
   ...: d_filter(is_janfeb, data)
Out[1]: {'January': 1, 'February': 2}

In [2]: d_filter(is_janfeb, data, factory=uDict)
Out[2]: uDict({'January': 1, 'February': 2})

In [3]: is_even = lambda x, y: y % 2 == 0
   ...: d_filter(is_even, data)
Out[3]: {'February': 2, 'April': 4}

In [4]:
```

### groupby() and d_groupby()

```python
def groupby( self,
        seq: list,
        key: Hashable,
        factory: Optional[Type[dict]]=None,
    ) -> dict:
```

```python
def d_groupby(
        seq: list,
        key: Hashable,
        factory: Type[dict]=dict,
    ) -> dict:
```

A groupby operation involves some combination of splitting the object, applying a function, and combining the results. This can be used to group large amounts of data and compute operations on these groups.

```python
In [1]: from datajuggler import uDict,  aDict
   ...: from datajuggler.dicthelper import d_groupby
   ...:
   ...: data = [
   ...:     {"id": 1, "name": "John"},
   ...:     {"id": 2, "name": "Paul"},
   ...:     {"id": 3, "name": "David"},
   ...:     {"id": 4, "name": "Freddie"},
   ...:     {"id": 3, "name": "Jack"},
   ...:     {"id": 1, "name": "Eddie"},
   ...:     {"id": 3, "name": "Bob"},
   ...:     {"id": 4, "name": "Maichael"},
   ...:     {"id": 1, "name": "Edward"},
   ...: ]
   ...: expect = ( "{1: [{'id': 1, 'name': 'John'}, "
   ...:                 "{'id': 1, 'name': 'Eddie'}, "
   ...:                 "{'id': 1, 'name': 'Edward'}], "
   ...:             "2: [{'id': 2, 'name': 'Paul'}], "
   ...:             "3: [{'id': 3, 'name': 'David'}, "
   ...:                 "{'id': 3, 'name': 'Jack'}, "
   ...:                 "{'id': 3, 'name': 'Bob'}], "
   ...:             "4: [{'id': 4, 'name': 'Freddie'}, "
   ...:                 "{'id': 4, 'name': 'Maichael'}]}" )
   ...: result = d_groupby(data, "id")
   ...: assert result.__repr__() == expect

```

### invert() and d_invert()

```python
def invert( self,
        obj: Optional[dict]=None,
        flat: bool=False,
        inplace: bool=False,
        factory: Optional[Type[dict]]=None,
    ) ->dict:
```


```python
def d_invert(
        obj: dict,
        flat: bool=False,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) ->dict:
```

Return an inverted dict where values become keys and keys become values.
Since multiple keys could have the same value, each value will be a list of keys.
If pass `flat=True` each value will be a single value.
(use this only if values are unique).

```python
In [1]: from datajuggler import aDict
   ...: from datajuggler.dicthelper import d_invert
   ...:
   ...:
   ...: data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
   ...: expect = {1: ['a'], 2: ['b'], 3: ['c'], 4: ['d'], 5: ['e']}
   ...: result = d_invert(data)
   ...: assert result == expect

In [2]: data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
   ...: expect = {1: ['a'], 2: ['b'], 3: ['c'], 4: ['d'], 5: ['e']}
   ...: d_invert(data, inplace=True)
   ...: assert data == expect

In [3]: data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
   ...: expect = aDict({1: ['a'], 2: ['b'], 3: ['c'], 4: ['d'], 5: ['e']})
   ...: result = d_invert(data, factory=aDict)
   ...: assert result == expect

In [4]: data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
   ...: expect = { 1: "a", 2: "b", 3: "c", 4: "d", 5: "e"}
   ...: result = d_invert(data, flat=True)
   ...: assert result == expect

In [5]: data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
   ...: expect = { 1: "a", 2: "b", 3: "c", 4: "d", 5: "e"}
   ...: d_invert(data, flat=True, inplace=True)
   ...: assert data == expect

In [6]: data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
   ...: expect = aDict({ 1: "a", 2: "b", 3: "c", 4: "d", 5: "e"})
   ...: result = d_invert(data, flat=True, factory=aDict)
   ...: assert result == expect

In [7]:
```

### map() and d_map()

```python
def map(self,
        func: Callable,
        obj: Optional[dict]=None,
        map_for: Optional[DictItemType]=None,
        inplace: bool=False,
        factory: Optional[Type[dict]]=None,
    ) ->dict:
```

```python
def d_map(
        func: Callable,
        obj: dict,
        map_for: Optional[DictItemType]=None,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) ->dict:
```
Create a new dictionary with apply function to keys/value of dictionary.
if pass `map_for=None`  apply function to key and value. (default)
if pass `map_for="key"`  apply function to key.
if pass `map_for="value"`  apply function to value.
If set `factory`, create instance of factory class.
If set `True` to `inplace`, perform operation in-place.

```python
In [1]: from datajuggler import uDict,  aDict
   ...: from datajuggler.dicthelper import d_map
   ...:
   ...:
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = { 1: 'January', 2: 'February', 3: 'March', 4: 'April' }
   ...: result = d_map(reversed, data)
   ...: assert result == expect

In [2]: expect = uDict({ 1: 'January', 2: 'February', 3: 'March', 4: 'April' })
   ...: result = d_map(reversed, data, factory=uDict)
   ...: assert result == expect
   ...:

In [3]: expect = { 1: 'January', 2: 'February', 3: 'March', 4: 'April' }
   ...: result = d_map(reversed, data, inplace=True)
   ...: assert data == expect

In [4]: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = uDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
   ...: result = d_map(str.upper, data, map_for="key")
   ...: assert result == expect

In [5]: data = { 'Jack': [10, 11, 12], 'John': [8, 15, 3] }
   ...: expect = { 'Jack': 33, 'John': 26 }
   ...: result = d_map(sum, data, map_for="value")
   ...: assert result == expect

In [6]:
```

### merge() and d_merger()

```python
def merge(self,
        others: list,
        obj: Optional[dict]=None,
        overwrite: bool=True,
        concat: bool=False,
        inplace: bool=False,
        factory: Optional[Type[dict]]=None,
    ) ->dict:
```

```python
def d_merge(
        obj: dict,
        others: Union[dict, list, tuple],
        overwrite: bool=True,
        concat: bool=False,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) ->dict:
```

Merge one or more dictionary objects into obj.
Sub-dictionaries keys will be merged toghether.
If pass `overwrite=False`, existing values will not be overwritten.
If pass `concat=True`, list values will be concatenated toghether.
If set `factory`, create instance of factory class.
If set `True` to `inplace`, perform operation in-place.

```python
In [1]: from datajuggler import aDict
   ...: from datajuggler.dicthelper import d_merge
   ...:
   ...:
   ...: d1 = { "a": 1, "b": 1, }
   ...: d2 = { "b": 2, "c": 3, }
   ...: expect = { "a": 1, "b": 2, "c": 3, }
   ...: d_merge(d1, d2)
Out[1]: {'a': 1, 'b': 2, 'c': 3}

In [2]: d_merge(d1, d2, factory=aDict)
Out[2]: aDict({'a': 1, 'b': 2, 'c': 3})

In [3]: d_merge(d1, d2, inplace=True)

In [4]: d1
Out[4]: {'a': 1, 'b': 2, 'c': 3}

In [5]: d1 = {
   ...:     "a": [0, 1, 2],
   ...:     "b": [5, 6, 7],
   ...:     "c": [],
   ...:     "d": [],
   ...: }
   ...: d2 = {
   ...:     "a": [3, 4, 5],
   ...:     "b": [8, 9, 0],
   ...:     "c": [-1],
   ...: }
   ...: expect = {
   ...:     "a": [3, 4, 5],
   ...:     "b": [8, 9, 0],
   ...:     "c": [-1],
   ...:     "d": [],
   ...: }

In [6]: d_merge(d1, d2)
Out[6]: {'a': [3, 4, 5], 'b': [8, 9, 0], 'c': [-1], 'd': []}

In [7]: d_merge(d1, d2, concat=True)
Out[7]: {'a': [0, 1, 2, 3, 4, 5], 'b': [5, 6, 7, 8, 9, 0], 'c': [-1], 'd': []}

In [8]: d1 = { "a": 1, "b": 1, }
   ...: d2 = { "b": 2, "c": 3, "d": 3, }
   ...: d3 = { "d": 5, "e": 5, }
   ...: d4 = { "d": 4, "f": 6, }

In [9]: d_merge(d1, [d2, d3, d4])
Out[9]: {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}

In [10]: d_merge(d1, (d2, d3, d4))
Out[10]: {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}

In [11]: d1 = {
    ...:     "a": 1,
    ...:     "b": {
    ...:         "c": { "x": 2, "y": 3, },
    ...:         "d": { "x": 4, "y": 5, },
    ...:         "e": { "x": 6, "y": 7, },
    ...:     },
    ...: }
    ...: d2 = {
    ...:     "a": 0,
    ...:     "b": {
    ...:         "c": 1,
    ...:         "d": { "y": 1, "z": 2, },
    ...:         "e": {
    ...:             "f": { "x": 2, "y": 3, },
    ...:             "g": { "x": 4, "y": 5, },
    ...:         },
    ...:     },
    ...: }

In [12]: d_merge(d1, d2)
Out[12]:
{'a': 0,
 'b': {'c': 1,
  'd': {'x': 4, 'y': 1, 'z': 2},
  'e': {'x': 6, 'y': 7, 'f': {'x': 2, 'y': 3}, 'g': {'x': 4, 'y': 5}}}}

In [13]:  d_merge(d1, d2, overwrite=False)
Out[13]:
{'a': 1,
 'b': {'c': 1,
  'd': {'x': 4, 'y': 1, 'z': 2},
  'e': {'x': 6, 'y': 7, 'f': {'x': 2, 'y': 3}, 'g': {'x': 4, 'y': 5}}}}

In [14]:
```

### move() and d_move()

```python
def move(self,
        key_src: Union[str, list],
        key_dest: Union[str, list],
        obj: Optional[dict]=None,
        *,
        keep_order: bool=False,
        overwrite: bool=True,
        inplace: bool=False,
        factory: Optional[Type[dict]]=None,
    ) ->dict:
```

```python
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
```

Create new dictionary which Move an item from key_src to key_dst.
It can be used to rename a key.
If key_dst exists and pass `overwrite=True`, its value will be overwritten.
if pass `keep_order=True`, keep ordered of dictionary. (may be slow).
If set `factory`, create instance of factory class.
If set `True` to `inplace`, perform operation in-place.

```python
In [1]: from datajuggler import aDict
   ...: from datajuggler.dicthelper import d_move
   ...:
   ...: data = {
   ...:     "a": { "x": 1, "y": 1, },
   ...:     "b": { "x": 2, "y": 2, },
   ...:     "c": { "x": 3, "y": 3, },
   ...: }

In [2]: d_move(data, "a", "a")
Out[2]: {'a': {'x': 1, 'y': 1}, 'b': {'x': 2, 'y': 2}, 'c': {'x': 3, 'y': 3}}

In [3]: d_move(data, "a", "d")
Out[3]: {'b': {'x': 2, 'y': 2}, 'c': {'x': 3, 'y': 3}, 'd': {'x': 1, 'y': 1}}

In [4]: d_move(data, "a", "d", overwrite=False)
Out[4]: {'b': {'x': 2, 'y': 2}, 'c': {'x': 3, 'y': 3}, 'd': {'x': 1, 'y': 1}}

In [5]: d_move(data, "a", "d", keep_order=True)
Out[5]: {'d': {'x': 1, 'y': 1}, 'b': {'x': 2, 'y': 2}, 'c': {'x': 3, 'y': 3}}

In [6]: d_move(data, "a", "d", factory=aDict)
Out[6]: aDict({'b': {'x': 2, 'y': 2}, 'c': {'x': 3, 'y': 3}, 'd': {'x': 1, 'y': 1}})

In [7]: d_move(data, "a", "d", inplace=True)

In [8]: data
Out[8]: {'b': {'x': 2, 'y': 2}, 'c': {'x': 3, 'y': 3}, 'd': {'x': 1, 'y': 1}}

In [9]:
```


### rename() and d_rename()

```python
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
```

```python
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
```

Create the new dictionary which is chnaged the key to key_new.
if key as dictionary {key: key_new}, change key using mapping dictionary.
If key_dst exists and pass `overwrite=True`, its value will be overwritten.
if pass `keep_order=True`, keep ordered of dictionary. (may be slow).
If set `factory`, create instance of factory class.
If set `True` to `inplace`, perform operation in-place.

```python
In [1]: from datajuggler import  aDict
   ...: from datajuggler.dicthelper import d_rename
   ...:
   ...: data = { "a": 1, "b": 2, "c": 3, "d": None, }

In [2]: d_rename(data, "a", "a")
Out[2]: {'a': 1, 'b': 2, 'c': 3, 'd': None}

In [3]: d_rename(data, "a", "A")
Out[3]: {'b': 2, 'c': 3, 'd': None, 'A': 1}

In [4]: d_rename(data, "a", "A", keep_order=True)
Out[4]: {'A': 1, 'b': 2, 'c': 3, 'd': None}

In [5]: try:
   ...:     result = d_rename(data, "a", "b")
   ...: except KeyError as e:
   ...:     print(e)
   ...:
"Invalid key: 'b', key already in dict and 'overwrite' is disabled."

In [6]: d_rename(data, "a", "b", overwrite=True)
Out[6]: {'b': 1, 'c': 3, 'd': None}

In [7]: d_rename(data, {'a': 'A', 'b': 'B'})
Out[7]: {'c': 3, 'd': None, 'A': 1, 'B': 2}

In [8]: d_rename(data, "b", "B", inplace=True)

In [9]: data
Out[9]: {'a': 1, 'c': 3, 'd': None, 'B': 2}

In [10]: data = { "First Name": 'jack', 'Last Name': 'bauwer' }

In [11]: d_rename(data, "First Name", case_name='snake')
Out[11]: {'Last Name': 'bauwer', 'first_name': 'jack'}

In [12]: keys = list(data.keys())
    ...: d_rename(data, keys, case_name='snake')
Out[12]: {'first_name': 'jack', 'last_name': 'bauwer'}

In [13]: d_rename(data, keys, case_name='camel')
Out[13]: {'firstName': 'jack', 'lastName': 'bauwer'}

In [14]:
```


### remove() and d_remove()

```python
def remove(self,
        keys: Union[list, Hashable],
        obj: Optional[dict]=None,
        *,
        inplace: bool=False,
        factory: Optional[Type[dict]]=None,
    ):
```

```python
def d_remove(
        obj: dict,
        keys: Union[list, tuple, Hashable],
        *,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ):
```

Create new dictionary which Remove multiple keys from the dict.
It is possible to pass a single key or more keys (as list or *args).

```python
In [1]: from datajuggler import aDict
   ...: from datajuggler.dicthelper import d_remove
   ...:
   ...: data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, }

In [2]: d_remove(data, "c")
Out[2]: {'a': 1, 'b': 2, 'd': 4, 'e': 5}

In [3]: d_remove(data, ["c", "d", "e"])
Out[3]: {'a': 1, 'b': 2}

In [4]: d_remove(data, ("c", "d", "e"))
Out[4]: {'a': 1, 'b': 2}

In [5]: d_remove(data, "c", factory=aDict)
Out[5]: aDict({'a': 1, 'b': 2, 'd': 4, 'e': 5})

In [6]: d_remove(data, "c", inplace=True)

In [7]: data
Out[7]: {'a': 1, 'b': 2, 'd': 4, 'e': 5}

In [8]:
```

### nest() and d_nest()


```python
def d_nest(
    items: tuple,
    id_key: Union[str, list],
    parent_id_key: Union[str, list],
    children_key: Union[str, list],
    ) -> list:
```

Nest a list of dicts at the given key and return a new nested list
using the specified keys to establish the correct items hierarchy.

```python
In [1]: from datajuggler.dicthelper import d_nest
   ...:
   ...: data = [
   ...:     {"id": 1, "parent_id": None, "name": "John"},
   ...:     {"id": 2, "parent_id": 1, "name": "Frank"},
   ...:     {"id": 3, "parent_id": 2, "name": "Tony"},
   ...:     {"id": 4, "parent_id": 3, "name": "Jimmy"},
   ...:     {"id": 5, "parent_id": 1, "name": "Sam"},
   ...:     {"id": 6, "parent_id": 3, "name": "Charles"},
   ...:     {"id": 7, "parent_id": 2, "name": "Bob"},
   ...:     {"id": 8, "parent_id": 3, "name": "Paul"},
   ...:     {"id": 9, "parent_id": None, "name": "Michael"},
   ...: ]

In [2]: d_nest(data, "id", "parent_id", "children")
Out[2]:
[{'id': 1,
  'parent_id': None,
  'name': 'John',
  'children': [{'id': 2,
    'parent_id': 1,
    'name': 'Frank',
    'children': [{'id': 3,
      'parent_id': 2,
      'name': 'Tony',
      'children': [{'id': 4, 'parent_id': 3, 'name': 'Jimmy', 'children': []},
       {'id': 6, 'parent_id': 3, 'name': 'Charles', 'children': []},
       {'id': 8, 'parent_id': 3, 'name': 'Paul', 'children': []}]},
     {'id': 7, 'parent_id': 2, 'name': 'Bob', 'children': []}]},
   {'id': 5, 'parent_id': 1, 'name': 'Sam', 'children': []}]},
 {'id': 9, 'parent_id': None, 'name': 'Michael', 'children': []}]

In [3]: try:
   ...:     result = d_nest(data, "id", "id", "children")
   ...: except ValueError as e:
   ...:     print(e)
   ...:
keys should be different.

In [4]: try:
   ...:     result = d_nest(data, "id", "parent_id", "id")
   ...: except ValueError as e:
   ...:     print(e)
   ...:
keys should be different.

In [5]: try:
   ...:     d_nest(data, "id", "parent_id", "parent_id")
   ...: except ValueError as e:
   ...:     print(e)
   ...:
keys should be different.

In [6]: data = [
   ...:     [{"id": 1, "parent_id": None, "name": "John"}],
   ...:     [{"id": 2, "parent_id": 1, "name": "Frank"}],
   ...: ]

In [7]: try:
   ...:     d_nest(data, "id", "parent_id", "children")
   ...: except ValueError as e:
   ...:     print(e)
   ...:
element should be a dict.

In [8]:
```


### subset() and d_subset()

```python
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
```

Return a dict subset for the given keys.
It is possible to pass a single key or more keys (as list or *args).


```python
In [1]: from datajuggler import aDict
   ...: from datajuggler.dicthelper import d_subset
   ...:
   ...:
   ...: data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

In [2]: d_subset(data, 'b')
Out[2]: {'b': 2}

In [3]: d_subset(data, ['b', 'd'])
Out[3]: {'b': 2, 'd': 4}

In [4]: d_subset(data, ('b', 'd'))
Out[4]: {'b': 2, 'd': 4}

In [5]: d_subset(data, ('b', 'd'), factory=aDict)
Out[5]: aDict({'b': 2, 'd': 4})

In [6]: d_subset(data, ('b', 'd'), inplace=True)

In [7]: data
Out[7]: {'b': 2, 'd': 4}

In [8]: data = { "a": 1,
   ...:          "b": { "c": { "x": 2, "y": 3 },
   ...:                 "d": { "x": 4, "y": 5 },
   ...:          },
   ...: }

In [9]: d_subset(data, keys='z', default={})
Out[9]: {'z': {}}

In [10]: try:
    ...:     d_subset(data, keys='x', default={})
    ...: except KeyError as e:
    ...:     print(e)
    ...:
"Multiple keys founded.'x'"

In [11]: d_subset(data, keys='x', default={}, use_keypath=True)
Out[11]: {'b.c.x': 2, 'b.d.x': 4}

In [12]: d_subset(data, keys='c')
Out[12]: {'c': {'x': 2, 'y': 3}}

In [13]: d_subset(data, keys=['c', 'd'])
Out[13]: {'c': {'x': 2, 'y': 3}, 'd': {'x': 4, 'y': 5}}

In [14]: d_subset(data, keys=['c', 'd'], use_keypath=True)
Out[14]: {'b.c': {'x': 2, 'y': 3}, 'b.d': {'x': 4, 'y': 5}}

In [15]: d_subset(data, keys=['c', 'd'],use_keypath=True, separator=' ')
Out[15]: {'b c': {'x': 2, 'y': 3}, 'b d': {'x': 4, 'y': 5}}

In [16]:
```

### find() and d_find()

```python
def d_find(
        obj: dict,
        keys: Union[list,Hashable],
        default: Optional[Any]=None,
        first_one: bool=True,
        factory: Type[dict]=dict,
    ) -> Union[Any, dict]:
```
Return the match searching for the given keys.
if pass `first_one=True`, return first matches.
If no result found, default value is returned.


```python
In [1]: from datajuggler.dicthelper import d_find
   ...:
   ...: data = { "a": 1, "b": 2, "c": 3, "d": None, }

In [2]: d_find(data, "b", 0)
Out[2]: 2

In [3]: d_find(data, "e", 0)
Out[3]: 0

In [4]: d_find(data, ["x", "y", "b", "z"], 5)
Out[4]: 2

In [5]: d_find(data, ["a", "x", "b", "y"], 5)
Out[5]: 1

In [6]: d_find(data, ["x", "y", "z"], 5)
Out[6]: 5

In [7]: d_find(data, ["x", "y", "z"], "missing")
Out[7]: 'missing'

In [8]: d_find(data, ["x", "y", "z"])

In [9]: d_find(data, ["a", "b", "c"], first_one=True)
Out[9]: 1

In [10]: d_find(data, ["a", "b", "c"], first_one=False)
Out[10]: {'a': 1, 'b': 2, 'c': 3}

In [11]:
```


### sort() and d_sort()

```python
def d_sort(
        obj: dict,
        sort_by: DictItemType=DictItem.KEY,
        reverse: bool=False,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ):
```

Create new dictiionary which is sorted by keys/values.
`sort_by` accept "key" and "value". default is  "key".
If pass `reverse=True`,  the list will be reversed.
If set `factory`, create instance of factory class.
If set `True` to `inplace`, perform operation in-place.

```python
In [1]: from datajuggler import aDict
   ...: from datajuggler.dicthelper import d_sort
   ...:
   ...: data = {
   ...:     "a": 8,
   ...:     "c": 6,
   ...:     "e": 4,
   ...:     "g": 2,
   ...:     "b": 7,
   ...:     "d": 5,
   ...:     "f": 3,
   ...:     "h": 1,
   ...: }

In [2]: d_sort(data)
Out[2]: {'h': 1, 'g': 2, 'f': 3, 'e': 4, 'd': 5, 'c': 6, 'b': 7, 'a': 8}

In [3]: d_sort(data, reverse=True)
Out[3]: {'a': 8, 'b': 7, 'c': 6, 'd': 5, 'e': 4, 'f': 3, 'g': 2, 'h': 1}

In [4]: d_sort(data, sort_by="value")
Out[4]: {'a': 8, 'b': 7, 'c': 6, 'd': 5, 'e': 4, 'f': 3, 'g': 2, 'h': 1}

In [5]: d_sort(data, factory=aDict)
Out[5]: aDict({'h': 1, 'g': 2, 'f': 3, 'e': 4, 'd': 5, 'c': 6, 'b': 7, 'a': 8})

In [6]: d_sort(data, inplace=True)

In [7]: data
Out[7]: {'h': 1, 'g': 2, 'f': 3, 'e': 4, 'd': 5, 'c': 6, 'b': 7, 'a': 8}

In [8]:
```


### search() and d_search()

```python
def d_search(
        obj: dict,
        query: Pattern,
        search_for: DictItemType=DictItem.KEY,
        exact: bool=False,
        ignore_case: bool=False,
        use_keypath: bool=True,
    ):
```

Search and return a list of items matching the given query.

```python
In [1]: from datajuggler.dicthelper import d_search
   ...:
   ...: data =  {
   ...:     "a": "January",
   ...:     "b": "january!",
   ...:     "c": {
   ...:         "d": True,
   ...:         "e": " january february ",
   ...:         "f": {
   ...:             "g": ['January', 'February', 'March', 'April' ],
   ...:             "january": 12345,
   ...:             "February": True,
   ...:         },
   ...:     },
   ...:     "x": "Peter Piper picked a peck of pickled peppers.",
   ...:     "y": { "x": { "y": 5, "z": 6, }, },
   ...:     "January February": "march",
   ...: }

In [2]: d_search(data, "jarnuary", search_for="value")
Out[2]: {}

In [3]: d_search(data, "january", search_for="value", ignore_case=True)
Out[3]: {'a': 'January', 'b': 'january!', 'c.f.g.0': 'January'}

In [4]: d_search(data, "january", search_for="value", exact=True)
Out[4]: {}

In [5]: d_search(data, "january", search_for="value", ignore_case=True)
Out[5]:
{Keypath("a"): 'January',
 Keypath("b"): 'january!',
 Keypath("c.f.g[0]"): 'January'}

In [6]: d_search(data, "january", search_for="value",
   ...:          ignore_case=True, use_keypath=False)
Out[6]: {'a': 'January', 'b': 'january!', 'c.f.g[0]': 'January'}

In [7]:
```

### swap() and d_swap()

```python
def d_swap(
        obj: dict,
        key1: Hashable,
        key2: Hashable,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) ->Optional[dict]:
```

Swap items values at the given keys.


```python
In [1]: from datajuggler import aDict
   ...: from datajuggler.dicthelper import d_swap
   ...:
   ...: data = { "a": 1, "b": 2, "c": 3, "d": None, }

In [2]: d_swap(data, "a", "b")
Out[2]: {'a': 2, 'b': 1, 'c': 3, 'd': None}

In [3]: d_swap(data, "a", "a")
Out[3]: {'a': 1, 'b': 2, 'c': 3, 'd': None}

In [4]: d_swap(data, "a", "b", factory=aDict)
Out[4]: aDict({'a': 2, 'b': 1, 'c': 3, 'd': None})

In [5]: d_swap(data, "a", "b", inplace=True)

In [6]: data
Out[6]: {'a': 2, 'b': 1, 'c': 3, 'd': None}

In [7]:
```

### flatten() and d_flatten()

```python
def d_flatten(
        obj: dict,
        separator: str=Default_Keypath_Separator,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) -> dict:
```

Return a new flattened dict using the given separator to join nested

```python
In [1]: from datajuggler import aDict
   ...: from datajuggler.dicthelper import d_flatten, d_unflatten
   ...:
   ...: data = { "a": 1,
   ...:          "b": 2,
   ...:          "c": {
   ...:             "d": {
   ...:                 "e": 3,
   ...:                 "f": 4,
   ...:                  "g": { "h": 5, },
   ...:             }
   ...:          },
   ...:       }

In [2]: d_flatten(data)
Out[2]: {'a': 1, 'b': 2, 'c.d.e': 3, 'c.d.f': 4, 'c.d.g.h': 5}

In [3]: d_flatten(data, separator="_")
Out[3]: {'a': 1, 'b': 2, 'c_d_e': 3, 'c_d_f': 4, 'c_d_g_h': 5}

In [4]: d_flatten(data, factory=aDict)
Out[4]: aDict({'a': 1, 'b': 2, 'c.d.e': 3, 'c.d.f': 4, 'c.d.g.h': 5})

In [5]: d_flatten(data, inplace=True)

In [6]: data
Out[6]: {'a': 1, 'b': 2, 'c.d.e': 3, 'c.d.f': 4, 'c.d.g.h': 5}

In [7]:
```

### unflatten() and d_unflatten()

```python

def d_unflatten(
        obj: dict,
        default: Optional[Any]=None,
        separator: str=Default_Keypath_Separator,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ) -> dict:
```

Return a new unflattened dict using the given separator to join nested dict keys to flatten keypaths.


```python
In [1]: from datajuggler import aDict
   ...: from datajuggler.dicthelper import d_flatten, d_unflatten
   ...:
   ...: data = {
   ...:     "a": 1,
   ...:     "b": 2,
   ...:     "c.d.e": 3,
   ...:     "c.d.f": 4,
   ...:     "c.d.g.h": 5,
   ...: }

In [2]: d_unflatten(data)
Out[2]: {'a': 1, 'b': 2, 'c': {'d': {'e': 3, 'f': 4, 'g': {'h': 5}}}}

In [3]: data = {
   ...:     "a": 1,
   ...:     "b": 2,
   ...:     "c_d_e": 3,
   ...:     "c_d_f": 4,
   ...:     "c_d_g_h": 5,
   ...: }

In [4]: d_unflatten(data, separator="_")
Out[4]: {'a': 1, 'b': 2, 'c': {'d': {'e': 3, 'f': 4, 'g': {'h': 5}}}}

In [5]: d_unflatten(data, separator="_", inplace=True)

In [6]: data
Out[6]: {'a': 1, 'b': 2, 'c': {'d': {'e': 3, 'f': 4, 'g': {'h': 5}}}}

In [7]:
```

### traverse() and d_traverse()

```python
ef d_traverse(
        obj: Union[dict, list, tuple],
        callback: Callable,
        parents: list=[],
        *args: Any,
        **kwargs: Any,
    ):
```
Traverse dict or list and apply callback function.
callback function will be called as follows.

  - `callback(obj, key, value, parents=parents, *args,  **kwargs)`
  - `callback(obj, index, value, parents=parents, *args,  **kwargs)`

`parantes` can pass to Keylist().

  - Keylist(parents)`

```python
In [1]: from datajuggler.dicthelper import d_traverse
   ...:
   ...:
   ...: data = { "a": { "x": 2, "y": 3, "z": { "ok": 5, }, },
   ...:          "b": { "x": 7, "y": 11, "z": { "ok": 13, }, },
   ...:          "c": { "x": 17, "y": 19, "z": { "ok": 23, }, },
   ...:        }

In [2]: def func(obj, key, val, *args, **kwargs):
   ...:     if not isinstance(val, dict):
   ...:         obj[key] = val + 1
   ...:
   ...: d_traverse(data, func)

In [3]: data
Out[3]:
{'a': {'x': 3, 'y': 4, 'z': {'ok': 6}},
 'b': {'x': 8, 'y': 12, 'z': {'ok': 14}},
 'c': {'x': 18, 'y': 20, 'z': {'ok': 24}}}

In [4]: paths=[]
   ...: def func(obj, key, val, parents, *args, **kwargs):
   ...:     global paths
   ...:     if not isinstance(val, dict):
   ...:         obj[key] = val + 1
   ...:         paths.append(Keylist(parents).to_keypath())
   ...:
   ...: d_traverse(data, func)

In [5]: data
Out[5]:
{'a': {'x': 4, 'y': 5, 'z': {'ok': 7}},
 'b': {'x': 9, 'y': 13, 'z': {'ok': 15}},
 'c': {'x': 19, 'y': 21, 'z': {'ok': 25}}}

In [6]: data = [ 100, [200, [300, 310], 210], 110]
   ...:
   ...: def func(obj, index, val, parents, *args, **kwargs):
   ...:     if not isinstance(val, list):
   ...:         obj[index] = val + 1000
   ...:
   ...: d_traverse(data, func)

In [7]: data
Out[7]: [1100, [1200, [1300, 1310], 1210], 1110]

In [8]: paths = []
   ...: def func(obj, index, val, parents, *args, **kwargs):
   ...:     global paths
   ...:     index_paths = [ str(x) for x in parents ]
   ...:     paths.append( ' '.join(index_paths))
   ...:
   ...: d_traverse(data, func)

In [9]: data
Out[9]: [1100, [1200, [1300, 1310], 1210], 1110]

In [10]: data = [ 100, [200, [300, 310], 210], 110]

In [11]: paths = []
    ...: def func(obj, index, val, parents, *args, **kwargs):
    ...:     global paths
    ...:     index_paths = [ str(x) for x in parents ]
    ...:     paths.append( ' '.join(index_paths))
    ...:
    ...: d_traverse(data, func)

In [12]: data
Out[12]: [100, [200, [300, 310], 210], 110]

In [13]: data = { "a": { "x": [ 100, 200], "y": 3, "z": { "ok": 5, }, },
    ...:          "b": { "x": [ 110, 210], "y": 11, "z": { "ok": 13, }, },
    ...:          "c": { "x": [ 120, 220], "y": 19, "z": { "ok": 13, }, },
    ...:        }
    ...:
    ...: paths = []
    ...: def func(obj, key, val, parents, *args, **kwargs):
    ...:     global paths
    ...:     if not isinstance(val, dict) and not isinstance(val, list):
    ...:         obj[key] = val + 1
    ...:
    ...: d_traverse(data, func)

In [14]: data
Out[14]:
{'a': {'x': [101, 201], 'y': 4, 'z': {'ok': 6}},
 'b': {'x': [111, 211], 'y': 12, 'z': {'ok': 14}},
 'c': {'x': [121, 221], 'y': 20, 'z': {'ok': 14}}}

In [15]: aths = []
    ...: def func(obj, key, val, parents, *args, **kwargs):
    ...:     global paths
    ...:     if not isinstance(val, dict) and  not isinstance(val, list):
    ...:         obj[key] = val + 1
    ...:         index_paths = [ str(x) for x in parents ]
    ...:         paths.append( ' '.join(index_paths))
    ...:
    ...: d_traverse(data, func)

In [16]: data
Out[16]:
{'a': {'x': [102, 202], 'y': 5, 'z': {'ok': 7}},
 'b': {'x': [112, 212], 'y': 13, 'z': {'ok': 15}},
 'c': {'x': [122, 222], 'y': 21, 'z': {'ok': 15}}}

In [17]:
```


### unique() and d_unique()

```python
def d_unique(
        obj: dict,
    ) -> list:
```

Return unique values from dict.

```python
In [1]: from datajuggler.dicthelper import  d_unique
   ...:
   ...: data = { "a": { "x": 1, "y": 1, },
   ...:          "b": { "x": 2, "y": 2, },
   ...:          "c": { "x": 1, "y": 1, },
   ...:          "d": { "x": 1, },
   ...:          "e": { "x": 1, "y": 1, "z": 1, },
   ...:          "f": { "x": 2, "y": 2, },
   ...: }

In [2]: d_unique(data)
Out[2]: [{'x': 1, 'y': 1}, {'x': 2, 'y': 2}, {'x': 1}, {'x': 1, 'y': 1, 'z': 1}]

In [3]:
```

### get_keys()

```python
def get_keys(
        obj: Optional[dict]=None,
        indexes: bool=False,
        *,
        output_as: Optional[DictKey]=None,
        separator: str=Default_Keypath_Separator,
    ) -> list:
```
Get all keys from dictionary as a List
This function is able to process on nested dictionary.
`output_as` accept "keylist" and "keypath".

```python
In [1]: from datajuggler.dicthelper import get_keys

In [2]: data = { "a": 1,
   ...:                  "b": { "c": { "x": 2, "y": 3, },
   ...:                         "d": { "x": 4, "y": 5, },
   ...:                       },
   ...:                 }

In [3]: get_keys(data)
Out[3]: ['a', 'b', 'c', 'x', 'y', 'd', 'x', 'y']

In [4]: get_keys(data, output_as="keylist")
Out[4]:
[['a'],
 ['b'],
 ['b', 'c'],
 ['b', 'c', 'x'],
 ['b', 'c', 'y'],
 ['b', 'd'],
 ['b', 'd', 'x'],
 ['b', 'd', 'y']]

In [5]: get_keys(data, output_as="keypath")
Out[5]: ['a', 'b', 'b.c', 'b.c.x', 'b.c.y', 'b.d', 'b.d.x', 'b.d.y']

In [6]: get_keys(data, output_as="keypath", separator='_')
Out[6]: ['a', 'b', 'b_c', 'b_c_x', 'b_c_y', 'b_d', 'b_d_x', 'b_d_y']

In [7]:
```

### get_values()

```python
def get_values(
        obj: Union[dict, Sequence],
        keys: Union[Hashable, Keylist, Keypath],
    ) -> Any:
```

Get the value of key in the objet(s).
`obj` : dict, dict[dict], dict[list], list[dict]
return value, list, dict.


```python
In [1]: from datajuggler import uDict, Keypath, Keylist
   ...: from datajuggler.dicthelper import get_values

In [2]: data = { "a": 1,
   ...:          "b": { "c": { "x": 2, "y": 3, },
   ...:                 "d": { "x": 4, "y": 5, },
   ...:                 "e": [ { "x": 1, "y": -1, "z": [1, 2, 3], },
   ...:                        { "x": 2, "y": -2, "z": [2, 3, 4], },
   ...:                        { "x": 3, "y": -3, "z": [3, 4, 5], },
   ...:                      ],
   ...:               },
   ...:       }
   ...:

In [3]: get_values(data, 'a')
Out[3]: 1

In [4]: get_values(data, ('b', 'c'))
Out[4]: {'x': 2, 'y': 3}

In [5]: get_values(data, Keylist(['b', 'c']))
Out[5]: {'x': 2, 'y': 3}

In [6]: get_values(data, Keylist(['b', 'e[1]', 'z[2]']))
Out[6]: 4

In [7]: get_values(data, Keypath('b.c'))
Out[7]: {'x': 2, 'y': 3}

In [8]: get_values(data, Keypath('b.e[1].z[2]'))
Out[8]: 4

In [9]: d = uDict(data)

In [10]: d['a']
Out[10]: 1

In [11]: d[('b', 'c')]
Out[11]: uDict({'x': 2, 'y': 3})

In [12]: d[Keylist(['b', 'c'])]
Out[12]: uDict({'x': 2, 'y': 3})

In [13]: d[Keylist(['b', 'e[1]', 'z[2]'])]
Out[13]: 4

In [14]: d[Keypath('b.c')]
Out[14]: uDict({'x': 2, 'y': 3})

In [15]: d[Keypath('b.e[1].z[2]')]
Out[15]: 4

In [16]:
```


### keylists()
```python
def keylists(
        obj: Any,
        indexes: bool=False,
    ) -> list:
```

keylist is the list of key as keys from dict/list.

this function is just calling Keylist.keylists()

### keypaths()

```python
def keypaths(
        obj: dict,
        indexes: bool=False,
        separator: str=Default_Keypath_Separator,
    ) -> str:
```
Keypath is the string for  attribute-sytle access to value.
(dot-notation by default).

this function is just calling Keypath.keypaths()




### get_items()

```python
def get_items(
        obj: dict,
        loc: Hashable,
        value: Any,
        func: Optional[Callable]=None,
        *,
        separator: str=Default_Keypath_Separator,
        factory: Type[dict]=dict,
    ):
```
Create new dictionary with new key value pair as d[key]=val.
If set `True` to `inplace`, perform operation in-place.
otherwise, not modify the initial dictionary.

```python
In [1]: from datajuggler import uDict, Keypath, Keylist
   ...: from datajuggler.dicthelper import get_items

In [2]: get_items({}, 'a', 1)
Out[2]: {'a': 1}

In [3]: data = { 'a': 1, 'b': 2}
   ...: get_items(data, 'a', 3)
Out[3]: {'a': 3, 'b': 2}

In [4]: data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
   ...:                        {'c': 22, 'd': 22 }] }
   ...:
   ...: get_items(data, 'b', 2)
Out[4]: {'a': 1, 'b': 2}

In [5]: data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
   ...:                        {'c': 22, 'd': 22 }] }
   ...:
   ...: get_items(data, 'c', 4)
Out[5]: {'a': 1, 'b': [{'c': 11, 'd': 12}, {'c': 22, 'd': 22}], 'c': 4}

In [6]: data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
   ...:                        {'c': 22, 'd': 22 }] }
   ...:
   ...: get_items(data, ('b','c'), 4)
Out[6]: {'a': 1, 'b': {'c': 4}}

In [7]: data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
   ...:                        {'c': 22, 'd': 22 }] }
   ...:
   ...: get_items(data, Keylist('b','c'), 4)
Out[7]: {'a': 1, 'b': 4}

In [8]: data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
   ...:                        {'c': 22, 'd': 22 }] }
   ...:
   ...: get_items(data, Keypath('b.c'), 4)
Out[8]: {'a': 1, 'b': {'c': 4}}

In [9]: d = uDict(data)

In [10]: d
Out[10]: uDict({'a': 1, 'b': [{'c': 11, 'd': 12}, {'c': 22, 'd': 22}]})

In [11]: d.get_items('a', 3)
Out[11]: uDict({'a': 3, 'b': [{'c': 11, 'd': 12}, {'c': 22, 'd': 22}]})

In [12]: d.get_items('c', 4)
Out[12]: uDict({'a': 1, 'b': [{'c': 11, 'd': 12}, {'c': 22, 'd': 22}], 'c': 4})

In [13]: d.get_items('b', 2)
Out[13]: uDict({'a': 1, 'b': 2})

In [14]: d.get_items(('b','c'), 4)
Out[14]: uDict({'a': 1, 'b': uDict({'c': 4})})

In [15]: d.get_items(Keylist('b','c'), 4)
Out[15]: uDict({'a': 1, 'b': 4})

In [16]: d.get_items(Keypath('b.c'), 4)
Out[16]: uDict({'a': 1, 'b': uDict({'c': 4})})

In [17]:
```

###  pop_items()

```python
ef pop_items(
        obj: dict,
        loc: Hashable,
        value: Optional[Any]=None,
        func: Optional[Callable]=None,
        *,
        separator: str=Default_Keypath_Separator,
        factory: Type[dict]=dict,
    ):
```
Create new dictionary with new key value pair as d[key]=val.
If set `True` to `inplace`, perform operation in-place.
otherwise, not modify the initial dictionary.


### del_items()

```python
def del_items(
        obj: dict,
        loc: Union[Hashable, list, tuple],
        *.
        separator: str=Default_Keypath_Separator,
        inplace: bool=False,
        factory: Type[dict]=dict,
    ):
```
Create new dicttionary with the given key(s) removed.
New dictionary has d[key] deleted for each supplied key.
If set `True` to `inplace`, perform operation in-place.
otherwise, not modify the initial dictionary.

### set_items()

```python
def set_items(
        obj: Union[dict, Sequence],
        loc: Union[str, Sequence],
        value: Any,
        func: Optional[Callable]=None,
        separator: str=Default_Keypath_Separator,
        factory: Type[dict]=dict,
    ):
```

Create new dict with new, potentially nested, key value pair.


## class iList

`iList` class support immutable and hashable for list.

 - `freeze()` change status of object in frozen.
 - `unfreeze()` unfreeze for object.

if call `freeze()`, following method will raise AttiributeError.

 - `__hash__()`
 - `__radd__()`
 - `__rand__()`
 - `__ior__()`
 - `__isub__()`
 - `__setitem__()`
 - `__reversed__()`
 - `append()`
 - `reverse()`
 - `clear()`
 - `expand()`
 - `pop()`
 - `remove()`
 - `sort()`

and add new helper mehtods.

 - `copy(freeze: bool=False)`
 - `clone(empty: bool=False)`
 - `find(val)`
 - `without(items)`
 - `replace(old, new)`




### copy()

```python
    def copy(self, freeze: bool=False):
```
Creaate the new list that is copied this list.
this method could not copy self.attrs..
if pass `freeze=True`, return frozen list object.

```python
In [1]: from datajuggler import iList

In [2]: l1 = iList([1,2,3])
   ...: l1.Hello = 'Python'
   ...: l2 = l1.copy()
   ...: assert l2 == l1

In [3]: l2.get_attrs()
Out[3]: {}

In [4]: l1 = iList([1])
   ...: l2 = l1.copy(freeze=True)
   ...: hash(l2)
Out[4]: -4714387948668998104

In [5]:
```


### clone()

```python
    def clone(self, empty: bool=False):
```
Creaate the new list that is cloned this list.
this method copy self.attrs.
if pass `empty=True`, keep self.attrs but list will be cleared.

```python
In [5]: l1 = iList([1,2,3])
   ...: l1.Hello = 'Python'
   ...: l2 = l1.clone()
   ...: assert l2 == l1

In [6]: l2.get_attrs()
Out[6]: {'Hello': 'Python'}

In [7]: l3 = l1.clone(empty=True)

In [8]: l3
Out[8]: iList([])

In [9]: l3.get_attrs()
Out[9]: {'Hello': 'Python'}

In [10]:
```

### without()

```python
   def without(self, *items):
```

Create new list without items and return iterable.

```python
In [13]: l1 = iList([1,2,3,4,5,6,7,8,9])

In [14]: l1.without([2,4,6,8])
Out[14]: [1, 3, 5, 7, 9]

In [15]: l1
Out[15]: iList([1, 2, 3, 4, 5, 6, 7, 8, 9])

In [16]:
```

### find()

```python
    def find(self,
            val: Union[Any, list, tuple],
        ) -> list:
```
Return the list of index that found val in list.
otherwise return None

```python
In [2]: l1 = iList([1,2,3,4,5,6,7,8,9])

In [3]: l1.find(2)
Out[3]: [1]

In [4]: l1.find([2,4,6,8])
Out[4]: [1, 3, 5, 7]

In [5]:
```

### replace()

```python
    def replace(self,
            old: Any,
            new: Any,
            func: Optional[Callable]=None,
        ) ->list:
```

Return a new list that has new instead of old.
if old is not found, it will raise an ItemNotFountError.
callback function will be called as follows.

 - `func(index, old, new)`

```python
In [1]: from datajuggler import iList

In [2]: l1 = iList([1,2,3,1,2,3])

In [3]: l1.replace(3, 5)
Out[3]: [1, 2, 5, 1, 2, 5]

In [4]: def func(index, old, new):
   ...:     if index > 3:
   ...:         return new
   ...:     else:
   ...:         return old
   ...:

In [5]: l1 = iList([1,2,3,1,2,3])

In [6]: l1.replace(3, 5, func)
Out[6]: [1, 2, 3, 1, 2, 5]

In [7]:
```


## class TypeValidator

TypeValidator class has following classmethods.
using TypeValidator not necessary including typing module.

 - `is_bool(cls, obj: Any)`
 - `is_collection(cls, obj: Any)`
 - `is_callable(cls, obj: Any)`
 - `is_datetime(cls, obj: Any)`
 - `is_decimal(cls, obj: Any)`
 - `is_dict(cls, obj: Any)`
 - `is_dict_or_other(cls, obj: Any, other: Any)`
 - `is_dict_and_not_other(cls, obj: Any, other: Any)`
 - `is_dict_keys(cls, obj: Any)`
 - `is_dict_values(cls, obj: Any)`
 - `is_dict_items(cls, obj: Any)`
 - `is_dict_or_list(cls, obj: Any)`
 - `is_dict_or_list_or_tuple(cls, obj: Any)`
 - `is_float(cls, obj: Any)`
 - `is_function(cls, obj: Any)`
 - `is_hashable(cls, obj: Any)`
 - `is_integer(cls, obj: Any)`
 - `is_integer_or_float(cls, obj: Any)`
 - `is_iterable(cls, obj: Any)`
 - `is_json_serializable(cls, obj: Any)`
 - `is_keylist(cls, obj: Any)`
 - `is_keypath(cls, obj: Any)`
 - `is_keylist_or_keypath(cls, obj: Any)`
 - `is_list(cls, obj: Any)`
 - `is_list_not_empty(cls, obj: Any)`
 - `is_list_or_tuple(cls, obj: Any)`
 - `is_list_of_keylists(cls, obj: Any)`
 - `is_list_of_keypaths(cls, obj: Any)`
 - `is_mapping(cls, obj: Any)`
 - `is_match(cls, obj: Any)`
 - `is_none(cls, obj: Any)`
 - `is_not_none(cls, obj: Any)`
 - `is_pattern(cls, obj: Any)`
 - `is_regex(cls, obj: Any)`
 - `is_same_as(cls, obj: Any, other: Any)`
 - `is_sequence(cls, obj: Any)`
 - `is_set(cls, obj: Any)`
 - `is_set_not_empty(cls, obj: Any)`
 - `is_str(cls, obj: Any)`
 - `is_str_not_empty(cls, obj: Any)`
 - `is_tuple(cls, obj: Any)`
 - `is_tuple_not_empty(cls, obj: Any)`
 - `is_uuid(cls, obj: Any)`
 - `is_str_alnum(cls, obj: Any)`
 - `is_str_alpha(cls, obj: Any)`
 - `is_str_financial_number(cls, obj: Any)`
 - `is_str_emoji(cls, obj: Any)`

Using TypeValidator class no need to include typing module compare with objects.

i.e.:
```python
In [1]: from datajuggler.validator import TypeValidator as _type

In [2]: data = { "a": 1,
   ...:                  "b": { "c": { "x": 2, "y": 3, },
   ...:                         "d": { "x": 4, "y": 5, },
   ...:                       },
   ...:                 }

In [3]: keys = data.keys()

In [4]: keys
Out[4]: dict_keys(['a', 'b'])

In [5]: _type.is_dict_keys(keys)
Out[5]: True

In [6]:
```


## class StrCase

`strCase` class support convert case.

 - `convert_case(case)`
 - `show_supported_case()`

```python
In [1]: from datajuggler import StrCase

In [2]: c = StrCase()

In [3]: c.show_supported_case()
Out[3]:
{'case': 'sample',
 'snake': 'convert_case',
 'kebab': 'convert-case',
 'camel': 'convertCase',
 'pascal': 'ConvertCase',
 'const': 'CONVERT_CASE',
 'sentence': 'Convert case',
 'title': 'Convert Case',
 'lower': 'convert case',
 'upper': 'CONVERT CASE'}

In [5]: c.convert_case('The sky is the limits')
Out[4]: 'the_sky_is_the_limits'

In [5]: c.convert_case('sentence', 'The sky is the limits')
Out[5]: 'The sky is the limits'

In [6]: c.convert_case('const', 'The sky is the limits')
Out[6]: 'THE_SKY_IS_THE_LIMITS'

In [7]: c.convert_case('camel', ['Good Morning','Thank you'])
Out[7]: ['goodMorning', 'thankYou']

In [8]:
```

`StrCase` class accept str, list, dict objects for inputs.

```python
In [8]: data = "The sky is the limit"
   ...: expect = 'the-sky-is-the-limit'
   ...: s = StrCase(data)
   ...: assert s.convert_case('kebab') == expect

In [9]: data = "The sky is the limit"
   ...: expect = 'theSkyIsTheLimit'
   ...: s = StrCase(data)
   ...: assert s.convert_case(case='camel') == expect

In [10]: data = ["Good luck", "The sky is the limit" ]
    ...: expect = ["good_luck", "the_sky_is_the_limit"]
    ...: s = StrCase(data)
    ...: assert s.convert_case() == expect

In [11]: data = {1: "Good luck", 2: "The sky is the limit" }
    ...: expect = {1: "good_luck", 2: "the_sky_is_the_limit" }
    ...: s = StrCase(data)
    ...: assert s.convert_case() == expect

In [12]: data = {"Good luck": 1, "The sky is the limit": 2 }
    ...: expect = {"good_luck": 1, "the_sky_is_the_limit": 2 }
    ...: s = StrCase(data)
    ...: assert s.convert_case(replace_for='key') == expect

In [13]:
```

`StrCase` class support nested objects.

```python
In [13]: data = ["Good luck", "The sky is the limit",
    ...:         {1: "Good luck", 2: "The sky is the limit" } ]
    ...: expect = ["good_luck", "the_sky_is_the_limit",
    ...:         {1: "good_luck", 2: "the_sky_is_the_limit" } ]
    ...: s = StrCase(data)
    ...: assert s.convert_case() == expect

In [14]:
```

### split_chunks()

Return split into even chunk_size elements.

```python
In [1]: from datajuggler import split_chunks
   ...:
   ...: data = [11,12,13,14, 21,22,23, 31,32,33]
   ...: expect = [[11,12,13, 14], [21,22,23,31], [32,33, None, None ]]
   ...: result = list(split_chunks(data,4))
   ...: assert result == expect

In [2]: data = [11,12,13,14, 21,22,23, 31,32,33]
   ...: expect = [[11,12,13, 14], [21,22,23,31], [32,33] ]
   ...: result = list(split_chunks(data,4, fill_na=False))
   ...: assert result == expect

In [3]: data = [11,12,13,14, 21,22,23,31,32,33]
   ...: expect = [[11,12,13, 14], [21,22,23,31], [32,33, -1, -1] ]
   ...: result = list(split_chunks(data,4, na_value=-1))
   ...: assert result == expect

In [4]:
```

if pass tuple as input. return list of tuple for chunk data.

```python
In [4]: data = (11,12,13,21,22,23,31,32,33)
   ...: expect = [(11,12,13), (21,22,23), (31,32,33)]
   ...: result = list(split_chunks(data,3))
   ...: assert result == expect

In [5]:
```

if pass dict objects as input. return list of dict for chunk data.
`fill_na` and `na_value` is always ignored.

```python
In [5]: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = [{ 'January': 1, 'February': 2, 'March': 3},
   ...:           { 'April': 4 } ]
   ...: result = list(split_chunks(data,3))
   ...: assert result == expect

In [6]: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = [{ 'January': 1, 'February': 2, 'March': 3},
   ...:           { 'April': 4 } ]
   ...: result = list(split_chunks(data,3, fill_na=True))
   ...: assert result == expect

In [7]: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = [{ 'January': 1, 'February': 2, 'March': 3},
   ...:           { 'April': 4 } ]
   ...: result = list(split_chunks(data,3, na_value=None))

In [8]:
```

if pass str objects as input. return list of str for chunk data.
`fill_na` and `na_value` is always ignored.

```python
In [8]: data = "Peter Piper picked a peck of pickled peppers."
   ...: expect = [ "Peter Piper picked a",
   ...:            " peck of pickled pep",
   ...:            "pers." ]
   ...: result = list(split_chunks(data,20))
   ...: assert result == expect

In [9]: data = "Peter Piper picked a peck of pickled peppers."
   ...: expect = [ "Peter Piper picked a",
   ...:            " peck of pickled pep",
   ...:            "pers." ]
   ...: result = list(split_chunks(data,20, fill_na=True, na_value=None))
   ...: assert result == expect

In [10]:
```

### urange()

`urange()` is almost same as `range()`

```
In [1]: from datajuggler import urange
   ...:
   ...: expect = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   ...: result = list(urange(10))
   ...: assert result == expect

In [2]: expect = [1, 2, 3, 4, 5, 6, 7, 8, 9]
   ...: result = list(urange(1, 10))
   ...: assert result == expect

In [3]: expect = [1, 3, 5, 7, 9]
   ...: result = list(urange(1, 10, 2))
   ...: assert result == expect

In [4]: expect = [10, 8, 6, 4, 2]
   ...: result = list(urange(10, 1, -2))
   ...: assert result == expect

In [5]: expect = [10, 9, 8, 7, 6, 5, 4, 3, 2]
   ...: result = list(urange(10, 1))
   ...: assert result == expect

In [6]:
```

`urange()` support callable as step.

```python
In [6]: def  gen_step(val):
   ...:     return (val * 3)
   ...:
   ...: expect = [1, 4, 16]
   ...: result = list(urange(1, 20, gen_step))
   ...: assert result == expect

In [7]:
```

### rename_duplicate()

Rename duplicate string for list or values of dict.

```python
In [1]: from datajuggler import rename_duplicates
   ...:
   ...: data = ["Apple", "Apple", "Banana", "Maple" ]
   ...: expect = ["Apple", "Apple_01", "Banana", "Maple" ]
   ...: result = rename_duplicates(data)
   ...: assert result == expect

In [2]: data = ["Apple", "Apple", "Banana", "Maple" ]
   ...: expect = ["Apple", "Apple__01", "Banana", "Maple" ]
   ...: result = rename_duplicates(data, separator='__')
   ...: assert result == expect

In [3]: data = ["Apple", "Apple", "Banana", "Maple" ]
   ...: expect = ["Apple", "Apple_001", "Banana", "Maple" ]
   ...: result = rename_duplicates(data, format="{:03}")
   ...: assert result == expect

In [4]: data = ["Apple", ["Apple", "Apple", "Banana", "Maple" ]]
   ...: expect = ["Apple", ["Apple", "Apple_01", "Banana", "Maple" ]]
   ...: result = rename_duplicates(data)
   ...: assert result == expect

In [5]:
```

### df_compare()

```python
In [1]: from datajuggler import df_compare
   ...:
   ...: d1 = pd.DataFrame([ ['Kyoto', 35.0117,135.452],
   ...:                     ['Osaka', 34.4138,135.3808]],
   ...:                   columns=['cityName', 'latitude', 'longitude'])
   ...: d2 = pd.DataFrame([ ['Kyoto', 35.0117,135.452],
   ...:                     ['Osaka', 34.4138,135.3808]],
   ...:                   columns=['cityName', 'latitude', 'longitude'])
   ...: assert ( df_compare(d1, d2) == 0 )

In [2]: d1 = pd.DataFrame([ ['26100', 35.0117,135.452],
   ...:                     ['27100', 34.4138,135.3808]],
   ...:                   columns=['cityCode', 'latitude', 'longitude'])
   ...: d2 = pd.DataFrame([ ['Kyoto', 35.0117,135.452],
   ...:                     ['Osaka', 34.4138,135.3808]],
   ...:                   columns=['cityName', 'latitude', 'longitude'])
   ...: assert ( df_compare(d1, d2) != 0 )

In [3]:
```

### omit_values()

Omit values from objects.

```python
In [1]: from datajuggler import omit_values
   ...:
   ...: data = ['January', 'February', 'March', 'April' ]
   ...: omits = ['February', 'April']
   ...: expect = ['January', '', 'March', '' ]
   ...: result = omit_values(data, omits)
   ...: assert result == expect

In [2]: data = ['January', 'February', 'March', 'April' ]
   ...: omits = ['february', 'april']
   ...: expect = ['January', '', 'March', '' ]
   ...: result = omit_values(data, omits, ignore_case=True)
   ...: assert result == expect

In [3]: data = ['January', 'February', 'March', 'April' ]
   ...: omits = ['February', 'April']
   ...: expect = ['January', 'March' ]
   ...: result = omit_values(data, omits, drop=True)
   ...: assert result == expect

In [4]: data = "JanuaryFebruaryMarchApril"
   ...: omits = ['February', 'April']
   ...: expect = "JanuaryMarch"
   ...: result = omit_values(data, omits)
   ...: assert result == expect

In [5]:
```

### replace_values()

Replace values for objects.
mutltidispatch functions as follows.

 - replace_values( data: str, old, new, ignore_case)
 - replace_values( values: list, replace: dict, *,
        ignore_case: bool=False, inplace: bool=False, **kwargs: Any )
 - replace_values( values: dict, replace: dict, *,
        ignore_case: bool=False, inplace: bool=False,
        replace_for: ReplaceForType = ReplaceFor.VALUE )
    ReplaceFor.KEY and ReplaceFor.VALUE are defined 'key' and 'value'.
 - replace_values( values: list, replace_from: list, replace_to: str, *,
        ignore_case: bool=False, inplace: bool=False, **kwargs: Any)
 - replace_values( values: str, replace_from: list, replace_to: Hashable, *,
        ignore_case: bool=False, **kwargs: Any)

 - replace_values( values: str, replace: dict, *,
        ignore_case: bool=False, **kwargs: Any)

```python
In [1]: from datajuggler import replace_values
   ...:
   ...: data = "JanuaryFebruaryMarchApril"
   ...: old = [ 'March', 'April' ]
   ...: replace_to = ""
   ...: expect = "JanuaryFebruary"
   ...: result = replace_values( data, old, replace_to )
   ...: assert result == expect

In [2]: data = "JanuaryFebruaryMarchApril"
   ...: replace = { 'March': '3', 'April': '4' }
   ...: expect = "JanuaryFebruary34"
   ...: result = replace_values( data, replace )
   ...: assert result == expect
   ...:

In [3]: data = "JanuaryFebruaryMarchApril"
   ...: replace = { 'March': 3, 'April': 4 }
   ...: expect = "JanuaryFebruary34"
   ...: result = replace_values( data, replace )
   ...: assert result == expect

In [4]: data = ['January', 'February', 'March', 'April' ]
   ...: replace = { 'March': '3', 'April': '4' }
   ...: expect = ['January', 'February', '3', '4' ]
   ...: result = replace_values( data, replace )
   ...: assert result == expect

In [5]: def convert_func(matchobj):
   ...:     map = {'January': '1',
   ...:            'February': '2' }
   ...:     return map[matchobj.group(0)]
   ...:
   ...: data = ['January', 'February', 'March', 'April',
   ...:         'May', 'June', 'July', 'August',
   ...:         'September', 'October', 'November', 'December']
   ...:
   ...: replace = { '.*ary': convert_func, '.*ber': 'BER' }
   ...:
   ...: expect = ['1', '2', 'March', 'April',
   ...:         'May', 'June', 'July', 'August',
   ...:         'BER', 'BER', 'BER', 'BER']
   ...: result = replace_values( data, replace)
   ...: assert result == expect

In [6]: data = ['January', 'February', 'March', 'April']
   ...: replace = {'march': '3', 'april': '4' }
   ...:
   ...: expect = ['January', 'February', '3', '4' ]
   ...: result = replace_values( data, replace, ignore_case=True)
   ...: assert result == expect

In [7]: data = ['January', 'February', 'March', 'April']
   ...: replace = {'march': '3', 'april': '4' }
   ...: expect = ['January', 'February', '3', '4' ]
   ...: replace_values( data, replace, ignore_case=True, inplace=True)
   ...: assert data == expect

In [8]: data = { 1: 'January', 2: 'February', 3: 'March', 4: 'April' }
   ...: replace = { 'March': 3, 'April': 4 }
   ...: expect = { 1: 'January', 2: 'February', 3: 3, 4: 4 }
   ...: result = replace_values( data, replace )
   ...: assert result == expect

In [9]: data = { 1: 'January', 2: 'February', 3: 'March', 4: 'April' }
   ...: replace = { 'March': 3, 'April': 4 }
   ...: expect = { 1: 'January', 2: 'February', 3: 3, 4: 4 }
   ...: result = replace_values( data, replace, replace_for='value' )
   ...: assert result == expect

In [10]: data = { 1: 'January', 2: 'February', 3: 'March', 4: 'April' }
    ...: replace = { 'march': 3, 'april': 4 }
    ...: expect = { 1: 'January', 2: 'February', 3: 3, 4: 4 }
    ...: result = replace_values( data, replace, ignore_case=True )
    ...: assert result == expect

In [11]: data = { 1: 'January', 2: 'February', 3: 'March', 4: 'April' }
    ...: replace = { 'march': 3, 'april': 4 }
    ...: expect = { 1: 'January', 2: 'February', 3: 3, 4: 4 }
    ...: replace_values( data, replace, ignore_case=True, inplace=True )
    ...: assert data == expect

In [12]: data = { 1: 'one', 2: 'two', 3: 'three', 4: 'four' }
    ...: replace = {1: 'one',  2: 'two', 3: 'three'}
    ...: expect = { 'one': 'one', 'two': 'two', 'three': 'three', 4: 'four' }
    ...: result = replace_values( data, replace, replace_for='key')
    ...: assert result == expect

In [13]: data = { 1: 'one', 2: 'two', 3: 'three', 4: 'four' }
    ...: replace = {'one': 1, 'two': [2, 'two'], 'three': { 3: 'three'}}
    ...: expect = { 1: 1, 2: [2, 'two'] , 3: {3: 'three'}, 4: 'four' }
    ...: result = replace_values( data, replace )
    ...: assert result == expect

In [14]:
```

## KNOWN PROBLEMS

datajuggler is not support followings issues.

 - out-of-core processing.

if you want to processing  huge datasets. you shoud combine [datatables](https://github.com/h2oai/datatable).
