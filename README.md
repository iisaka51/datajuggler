# DataJuggler

This library provides utility classes and helper functions for data processing.
This is spin-off project from [scrapinghelper](https://github.com/iisaka51/scrapinghelper).


 - class DictFactory
   Factory class for custom dictionary.
 - class aDict
   Allow to access using dot notation for dictionary.
 - class uDict
   Allow to change key for Dict.
 - class iDict
   Immutable Dict. iDict object hashable.
 - class StrCase
   Convert case for object(s).

utilities for string manupulate helper functions.

 -  `is_alpha()` - Check word is alphabet.
 -  `is_alnum()` - Check word is alphabet and digits.
 -  `ordereddict_to_dict()` - convert object from OrderedDict to Dict.
 -  `change_dict_keys()` - Change keys of Dict.
 -  `replace_values()` - Replace objects for object(s).
 -  `omit_values()` - Omit values for object(s).
 -  `add_df()` - Add data into DataFrame.
 -  `df_compare()` - Check DataFrame is equals.
 -  `split_chunks()` - Split iterable object into chunks.
 -  `urange()` - Return an object that produces a sequence of integes.


## class DictFactory

DictFactory is internal base class for custom dictionary.
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
 - `to_json(**options: Any)`
 - `from_json(json_data: str, inplace: bool=False, **options)`
 - `to_yaml(**options: Any)`
 - `from_yaml(stream, *args: Any, inplace: bool=False, **kwargs: Any)`

aDict and uDict, iDict are subclass of DictFactory.

### Common methods.

```python
In [1]: from datajuggler import aDict
   ...:
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...:
   ...: obj = aDict(data)
   ...: assert obj == data

In [2]: expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
   ...: obj = aDict(data)
   ...: assert obj.__str__() == expect

In [3]: expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
   ...:
   ...: obj = aDict(data)
   ...: assert obj.__repr__() == expect

In [4]: expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: obj = aDict(January=1, February=2, March=3, April=4)
   ...: assert obj == expect

In [5]: data = aDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...: expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: assert data == expect

In [6]: data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
   ...: expect = ( "aDict("
   ...:            "{'one': {'two': {'three': {'four': 4}}}}"
   ...:            ")" )
   ...: obj = aDict(data)
   ...: assert obj.__repr__() == expect

In [7]:
```

```python
In [1]: from datajuggler import uDict
   ...:
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...:
   ...: obj = uDict(data)
   ...: assert obj == data

In [2]: expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
   ...: obj = uDict(data)
   ...: assert obj.__str__() == expect

In [3]: expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
   ...:
   ...: obj = uDict(data)
   ...: assert obj.__repr__() == expect

In [4]: expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: result = uDict(January=1, February=2, March=3, April=4)
   ...: assert result == expect

In [5]: data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...: expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: assert data == expect

In [6]: data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
   ...: expect = ( "uDict("
   ...:            "{'one': {'two': {'three': {'four': 4}}}}"
   ...:            ")" )
   ...: obj = uDict(data)
   ...: assert obj.__repr__() == expect

In [7]:
```

```python
In [1]: from datajuggler import iDict
   ...:
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...:
   ...: obj = iDict(data)
   ...: assert obj == data

In [2]: expect = "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
   ...: obj = iDict(data)
   ...: assert obj.__str__() == expect

In [3]: expect = "iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
   ...:
   ...: obj = iDict(data)
   ...: assert obj.__repr__() == expect

In [4]: expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: obj = iDict(January=1, February=2, March=3, April=4)
   ...: assert obj == expect

In [5]: data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...: expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: assert data == expect

In [6]:
```

### fromkeys()

Create a new dictionary with keys from iterable and values set to value.
If set `True` to `inplace`, perform operation in-place.


```python
In [9]: data = [ 'January', 'February', 'March', 'April' ]
   ...: expect = ( "aDict("
   ...:            "{'January': 2, 'February': 2, 'March': 2, 'April': 2}"
   ...:            ")" )
   ...: obj = aDict().fromkeys(data, 2)
   ...: assert obj.__repr__() == expect

In [10]: data = [ 'January', 'February', 'March', 'April' ]
    ...: expect = ( "aDict("
    ...:            "{'January': 2, 'February': 2, 'March': 2, 'April': 2}"
    ...:            ")" )
    ...: obj = aDict()
    ...: obj.fromkeys(data, 2, inplace=True)
    ...: assert obj.__repr__() == expect
```

```python
In [9]: data = [ 'January', 'February', 'March', 'April' ]
   ...: expect = ( "uDict("
   ...:            "{'January': 2, 'February': 2, 'March': 2, 'April': 2}"
   ...:            ")" )
   ...: obj = uDict().fromkeys(data, 2)
   ...: assert obj.__repr__() == expect

In [10]: obj = uDict()
    ...: obj.fromkeys(data, 2, inplace=True)
    ...: assert obj.__repr__() == expect

```

In case of iDict, if set `iplace` parameter, it will not cause an error.
but will always be ignored.

```python
In [4]: data = [ 'January', 'February', 'March', 'April' ]
   ...: expect = ( "iDict("
   ...:            "{'January': 2, 'February': 2, 'March': 2, 'April': 2}"
   ...:            ")" )
   ...: obj = iDict().fromkeys(data, 2)
   ...: assert obj.__repr__() == expect

In [5]: data = [ 'January', 'February', 'March', 'April' ]
   ...: expect = "iDict({})"
   ...: obj = iDict()
   ...: obj.fromkeys(data, 2, inplace=True)
   ...: assert obj.__repr__() == expect

```


### fromvalues()

Create a new dictionary from list of values.
keys automaticaly generate as interger or str.
`base` is the starting number.
if set 'name' to `prefix`, keys will be use 'name01'...
So, set '' to `prefix`, key as str from interger.
If set `True` to `inplace`, perform operation in-place.

```python
In [11]: data = [ 'January', 'February', 'March', 'April' ]
    ...: expect = ( "aDict("
    ...:            "{1: 'January', 2: 'February', 3: 'March', 4: 'April'}"
    ...:            ")" )
    ...: obj = aDict().fromvalues(data)
    ...: assert obj.__repr__() == expect

In [12]: data = [ 'January', 'February', 'March', 'April' ]
    ...: expect = ( "aDict("
    ...:            "{0: 'January', 1: 'February', 2: 'March', 3: 'April'}"
    ...:            ")" )
    ...: obj = aDict().fromvalues(data, base=0)
    ...: assert obj.__repr__() == expect

In [13]: data = [ 'January', 'February', 'March', 'April' ]
    ...: expect = ( "aDict("
    ...:            "{1: 'January', 2: 'February', 3: 'March', 4: 'April'}"
    ...:            ")" )
    ...: obj = aDict()
    ...: obj.fromvalues(data, base=1, inplace=True)
    ...: assert obj.__repr__() == expect

In [14]: data = [ 'January', 'February', 'March', 'April' ]
    ...:
    ...: expect = ( "aDict("
    ...:            "{'1': 'January', '2': 'February', "
    ...:             "'3': 'March', '4': 'April'})" )
    ...:
    ...: obj = aDict().fromvalues(data, prefix='')
    ...: assert obj.__repr__() == expect

In [15]: expect = ( "aDict("
    ...:            "{'month_1': 'January', 'month_2': 'February', "
    ...:             "'month_3': 'March', 'month_4': 'April'})" )
    ...:
    ...: obj = aDict().fromvalues(data, prefix='month_')
    ...: assert obj.__repr__() == expect

In [16]:
```


```python
In [11]: data = [ 'January', 'February', 'March', 'April' ]
    ...: expect = ( "uDict("
    ...:            "{1: 'January', 2: 'February', 3: 'March', 4: 'April'}"
    ...:            ")" )
    ...: obj = uDict().fromvalues(data)
    ...: assert obj.__repr__() == expect

In [12]: obj = uDict()
    ...: obj.fromvalues(data, base=1, inplace=True)
    ...: assert obj.__repr__() == expect

In [13]: expect = ( "uDict("
    ...:            "{0: 'January', 1: 'February', 2: 'March', 3: 'April'}"
    ...:            ")" )
    ...: obj = uDict().fromvalues(data, base=0)
    ...: assert obj.__repr__() == expect

In [14]: data = [ 'January', 'February', 'March', 'April' ]
    ...:
    ...: expect = ( "uDict("
    ...:            "{'1': 'January', '2': 'February', "
    ...:             "'3': 'March', '4': 'April'})" )
    ...:
    ...: obj = uDict().fromvalues(data, prefix='')
    ...: assert obj.__repr__() == expect

In [15]: expect = ( "uDict("
    ...:            "{'month_1': 'January', 'month_2': 'February', "
    ...:             "'month_3': 'March', 'month_4': 'April'})" )
    ...:
    ...: obj = uDict().fromvalues(data, prefix='month_')
    ...: assert obj.__repr__() == expect

In [16]:
```

In case of iDict, if set `iplace` parameter, it will not cause an error.
but will always be ignored.

```python
In [11]: data = [ 'January', 'February', 'March', 'April' ]
    ...: expect = ( "iDict("
    ...:            "{1: 'January', 2: 'February', 3: 'March', 4: 'April'}"
    ...:            ")" )
    ...: obj = iDict().fromvalues(data)
    ...: assert obj.__repr__() == expect

In [12]: data = [ 'January', 'February', 'March', 'April' ]
    ...: expect = ( "iDict("
    ...:            "{0: 'January', 1: 'February', 2: 'March', 3: 'April'}"
    ...:            ")" )
    ...: obj = iDict().fromvalues(data, base=0)
    ...: assert obj.__repr__() == expect

In [13]: data = [ 'January', 'February', 'March', 'April' ]
    ...: expect = "iDict({})"
    ...: obj = iDict()
    ...: obj.fromvalues(data, base=1, inplace=True)
    ...: assert obj.__repr__() == expect

In [14]: data = [ 'January', 'February', 'March', 'April' ]
    ...:
    ...: expect = ( "iDict("
    ...:            "{'1': 'January', '2': 'February', "
    ...:             "'3': 'March', '4': 'April'})" )
    ...:
    ...: obj = iDict().fromvalues(data, prefix='')
    ...: assert obj.__repr__() == expect

In [15]: expect = ( "iDict("
    ...:            "{'month_1': 'January', 'month_2': 'February', "
    ...:             "'month_3': 'March', 'month_4': 'April'})" )
    ...:
    ...: obj = iDict().fromvalues(data, prefix='month_')
    ...: assert obj.__repr__() == expect

In [16]:
```


### fromlists()

Create a new dictionary from two list as keys and values.
Only the number of elements in the shorter of the two lists is processed.
If set `True` to `inplace`, perform operation in-place.


```python
In [14]: keys = [ 'January', 'February', 'March', 'April' ]
    ...: values = [ 1, 2, 3, 4 ]
    ...: expect = ( "aDict("
    ...:            "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
    ...:            ")" )
    ...: obj = aDict().fromlists(keys, values)
    ...: assert obj.__repr__() == expect

In [15]: keys = [ 'January', 'February', 'March', 'April' ]
    ...: values = [ 1, 2, 3, 4 ]
    ...: expect = ( "aDict("
    ...:            "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
    ...:            ")" )
    ...: obj = aDict()
    ...: obj.fromlists(keys, values, inplace=True)
    ...: assert obj.__repr__() == expect

In [16]: keys = [ 'January', 'February' ]
    ...: values = [ 1, 2, 3, 4 ]
    ...: expect = "aDict({'January': 1, 'February': 2})"
    ...: obj = aDict().fromlists(keys, values)
    ...: assert obj.__repr__() == expect

In [17]: keys = [ 'January', 'February', 'March', 'April' ]
    ...: values = [ 1, 2 ]
    ...: expect = "aDict({'January': 1, 'February': 2})"
    ...: obj = aDict().fromlists(keys, values)
    ...: assert obj.__repr__() == expect
```


```python
In [14]: keys = [ 'January', 'February', 'March', 'April' ]
    ...: values = [ 1, 2, 3, 4 ]
    ...: expect = ( "uDict("
    ...:            "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
    ...:            ")" )
    ...: obj = uDict().fromlists(keys, values)
    ...: assert obj.__repr__() == expect

In [15]: obj = uDict()
    ...: obj.fromlists(keys, values, inplace=True)
    ...: assert obj.__repr__() == expect

In [16]: keys = [ 'January', 'February' ]
    ...: values = [ 1, 2, 3, 4 ]
    ...: expect = "uDict({'January': 1, 'February': 2})"
    ...: obj = uDict().fromlists(keys, values)
    ...: assert obj.__repr__() == expect

In [17]: keys = [ 'January', 'February', 'March', 'April' ]
    ...: values = [ 1, 2 ]
    ...: expect = "uDict({'January': 1, 'February': 2})"
    ...: obj = uDict().fromlists(keys, values)
    ...: assert obj.__repr__() == expect

```

In case of iDict, if set `iplace` parameter, it will not cause an error.
but will always be ignored.

```python
In [1]: from datajuggler import iDict
   ...:
   ...: keys = [ 'January', 'February', 'March', 'April' ]
   ...: values = [ 1, 2, 3, 4 ]
   ...: expect = ( "iDict("
   ...:            "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
   ...:            ")" )
   ...: obj = iDict().fromlists(keys, values)
   ...: assert obj.__repr__() == expect

In [2]: keys = [ 'January', 'February', 'March', 'April' ]
   ...: values = [ 1, 2, 3, 4 ]
   ...: expect = "iDict({})"
   ...: obj = iDict()
   ...: obj.fromlists(keys, values, inplace=True)
   ...: assert obj.__repr__() == expect

In [3]: keys = [ 'January', 'February' ]
   ...: values = [ 1, 2, 3, 4 ]
   ...: expect = "iDict({'January': 1, 'February': 2})"
   ...: obj = iDict().fromlists(keys, values)
   ...: assert obj.__repr__() == expect

In [4]: keys = [ 'January', 'February', 'March', 'April' ]
   ...: values = [ 1, 2 ]
   ...: expect = "iDict({'January': 1, 'February': 2})"
   ...: obj = iDict().fromlists(keys, values)
   ...: assert obj.__repr__() == expect

```

## Serialization

### JSON

to_json() and from_json().
If set `True` to `inplace`, perform operation in-place.


```python
In [6]: data = {"console": "Nintendo Switch",
   ...:         "games": ["The Legend of Zelda", "Mario Golf"]}
   ...: json_data = ( '{"console": "Nintendo Switch", '
   ...:            '"games": ["The Legend of Zelda", "Mario Golf"]}' )
   ...: obj = aDict(data)
   ...: assert obj.to_json() == json_data
```

If set `True` to `inplace`, perform operation in-place.


```python
In [7]: expect = ( "aDict({'console': 'Nintendo Switch', "
   ...:            "'games': ['The Legend of Zelda', 'Mario Golf']})" )
   ...: obj = aDict().from_json(json_data)
   ...: assert obj.__repr__() == expect

In [8]: obj = aDict()
   ...: obj.from_json(json_data, inplace=True)
   ...: assert obj.__repr__() == expect

```


```python
In [5]: from datajuggler import uDict
   ...:
   ...: data = {"console": "Nintendo Switch",
   ...:         "games": ["The Legend of Zelda", "Mario Golf"]}
   ...: json_data = ( '{"console": "Nintendo Switch", '
   ...:            '"games": ["The Legend of Zelda", "Mario Golf"]}' )
   ...: repr  = ( "uDict({'console': 'Nintendo Switch', "
   ...:            "'games': ['The Legend of Zelda', 'Mario Golf']})" )

In [6]: obj = uDict(data)
   ...: assert obj.to_json() == json_data

In [7]: new = uDict().from_json(json_data)
   ...: assert new.__repr__() == repr

In [8]: obj = uDict()
   ...: obj.from_json(json_data, inplace=True)
   ...: assert obj.__repr__() == repr

```

if set `iplace` parameter, it will not cause an error.
but will always be ignored.

```python
In [1]: from datajuggler import iDict
   ...:
   ...: data = {"console": "Nintendo Switch",
   ...:         "games": ["The Legend of Zelda", "Mario Golf"]}
   ...: json_data = ( '{"console": "Nintendo Switch", '
   ...:               '"games": ["The Legend of Zelda", "Mario Golf"]}' )
   ...: obj = iDict(data)
   ...: assert obj.to_json() == json_data

In [2]: expect = ( "iDict({'console': 'Nintendo Switch', "
   ...:            "'games': ['The Legend of Zelda', 'Mario Golf']})" )
   ...: result = iDict().from_json(json_data)
   ...: assert result.__repr__() == expect

In [3]: expect = "iDict({})"
   ...: obj = iDict()
   ...: obj.from_json(json_data, inplace=True)
   ...: assert obj.__repr__() == expect

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




```python
In [1]: from datajuggler import iDict
   ...: import yaml
   ...:
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = "{April: 4, February: 2, January: 1, March: 3}\n"
   ...:
   ...: obj = iDict(data)
   ...: result = yaml.safe_dump(obj, default_flow_style=True)
   ...: assert result == expect

In [2]: expect = "{January: 1, February: 2, March: 3, April: 4}\n"
   ...: obj = iDict(data)
   ...: result = yaml.safe_dump(obj, default_flow_style=True,sort_keys=False)
   ...: assert result == expect

In [3]: expect = "{April: 4, February: 2, January: 1, March: 3}\n"
   ...: obj = iDict(data)
   ...: result = obj.to_yaml(default_flow_style=True)
   ...: assert result == expect

In [4]: expect = "{January: 1, February: 2, March: 3, April: 4}\n"
   ...: obj = iDict(data)
   ...: result = obj.to_yaml(default_flow_style=True,sort_keys=False)
   ...: assert result == expect

In [5]: expect = ( "!datajuggler.iDict "
   ...:            "{April: 4, February: 2, January: 1, March: 3}\n" )
   ...: obj = iDict(data)
   ...: result = yaml.dump(obj, default_flow_style=True)
   ...: assert result == expect

In [6]: expect = ( "!datajuggler.iDict "
   ...:            "{January: 1, February: 2, March: 3, April: 4}\n" )
   ...: obj = iDict(data)
   ...: result = yaml.dump(obj, default_flow_style=True,sort_keys=False)
   ...: assert result == expect

In [7]: expect = ( "!datajuggler.iDict "
   ...:            "{April: 4, February: 2, January: 1, March: 3}\n" )
   ...: obj = iDict(data)
   ...: result = obj.to_yaml(Dumper=yaml.Dumper,  default_flow_style=True)
   ...: assert result == expect

In [8]: expect = ( "!datajuggler.iDict "
   ...:            "{January: 1, February: 2, March: 3, April: 4}\n" )
   ...: obj = iDict(data)
   ...: result = obj.to_yaml(Dumper=yaml.Dumper,
   ...:                      default_flow_style=True, sort_keys=False)
   ...: assert result == expect

In [9]: data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
   ...: expect = "{one: {two: {three: {four: 4}}}}\n"
   ...: obj = iDict(data)
   ...: result = obj.to_yaml(default_flow_style=True,sort_keys=False)
   ...: assert result  == expect

In [10]: expect = ( "!datajuggler.iDict "
    ...:            "{one: {two: {three: {four: 4}}}}\n" )
    ...: obj = iDict(data)
    ...: result = obj.to_yaml(Dumper=yaml.Dumper,
    ...:                      default_flow_style=True, sort_keys=False)
    ...: assert result  == expect

In [11]: yaml_str = ( "!datajuggler.iDict "
    ...:              "{April: 4, February: 2, January: 1, March: 3}\n" )
    ...: expect = ( "iDict("
    ...:            "{'April': 4, 'February': 2, 'January': 1, 'March': 3}"
    ...:            ")" )
    ...: obj = iDict()
    ...: result = obj.from_yaml(yaml_str)
    ...: assert result.__repr__() == expect

In [12]: yaml_str = ( "!python/object:datajuggler.iDict "
    ...:              "{April: 4, February: 2, January: 1, March: 3}\n" )
    ...: obj = iDict()
    ...: result = obj.from_yaml(yaml_str)
    ...: assert result.__repr__() == expect

In [13]: yaml_str = ( "!datajuggler.iDict "
    ...:              "{January: 1, February: 2, March: 3, April: 4}\n"
    ...:             ")" )
    ...: obj = iDict()
    ...: expect = ( "iDict("
    ...:            "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
    ...:            ")" )
    ...: result = obj.from_yaml(yaml_str)
    ...: assert result.__repr__() == expect

In [14]: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
    ...: yaml_str = ( "!python/object:datajuggler.iDict "
    ...:              "{January: 1, February: 2, March: 3, April: 4}\n" )
    ...: expect = ( "iDict("
    ...:            "{'January': 1, 'February': 2, 'March': 3, 'April': 4}"
    ...:            ")" )
    ...: obj = iDict()
    ...: result = obj.from_yaml(yaml_str)
    ...: assert result.__repr__() == expect

In [15]: yaml_str = ( "!datajuggler.iDict "
    ...:              "{April: 4, February: 2, January: 1, March: 3}\n" )
    ...: expect = "iDict({})"
    ...: obj = iDict()
    ...: _ = obj.from_yaml(yaml_str)
    ...: assert obj.__repr__() == expect

In [16]: yaml_str = ( "!python/object:datajuggler.iDict "
    ...:              "{January: 1, February: 2, March: 3, April: 4}\n" )
    ...: expect = "iDict({})"
    ...: obj = iDict()
    ...: _ = obj.from_yaml(yaml_str)
    ...: assert obj.__repr__() == expect

In [17]: yaml_str = ( "!datajuggler.iDict "
    ...:              "{April: 4, February: 2, January: 1, March: 3}\n" )
    ...: expect = "iDict({})"
    ...: obj = iDict()
    ...: obj.from_yaml(yaml_str, inplace=True)
    ...: assert obj.__repr__() == expect

In [18]: yaml_str = ( "!python/object:datajuggler.iDict "
    ...:              "{January: 1, February: 2, March: 3, April: 4}\n" )
    ...: expect = "iDict({})"
    ...: obj = iDict()
    ...: obj.from_yaml(yaml_str, inplace=True)
    ...: assert obj.__repr__() == expect

In [19]:
```
if pass `as_default_dict=True` to custructor,
use aDict, uDict, iDict insted of dict.

```python
In [1]: from datajuggler import aDict, iDict, uDict

In [2]: aDict({1: 1, 2: 2, 3: {3: '3'}})
Out[2]: aDict({1: 1, 2: 2, 3: {3: '3'}})

In [3]: aDict({1: 1, 2: 2, 3: {3: '3'}}, as_default_dict=True)
Out[3]: aDict({1: 1, 2: 2, 3: aDict({3: '3'})})

In [4]: uDict({1: 1, 2: 2, 3: {3: '3'}})
Out[4]: uDict({1: 1, 2: 2, 3: {3: '3'}})

In [5]: uDict({1: 1, 2: 2, 3: {3: '3'}}, as_default_dict=True)
Out[5]: uDict({1: 1, 2: 2, 3: uDict({3: '3'})})

In [6]: iDict({1: 1, 2: 2, 3: {3: '3'}})
Out[6]: iDict({1: 1, 2: 2, 3: {3: '3'}})

In [7]: iDict({1: 1, 2: 2, 3: {3: '3'}}, as_default_dict=True)
Out[7]: iDict({1: 1, 2: 2, 3: iDict({3: '3'})})

In [8]:

```



## class aDict
Allow to access using dot notation for dictionary.
This class inspired [munch](https://github.com/Infinidat/munch).
aDict is subclass of DictFactory.


```python
In [1]: from datajuggler import aDict
   ...:
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = 2
   ...: obj = aDict(data)
   ...: assert obj.February == expect

In [2]: data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
   ...: expect = { 'two': { 'three': { 'four': 4 }}}
   ...: obj = aDict(data)
   ...: assert obj.one == expect

In [3]: data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
   ...: expect = "{'one': {'two': {'three': {'four': 4}}}}"
   ...: obj = aDict(data)
   ...: try:
   ...:     result = obj.one.two
   ...: except AttributeError as e:
   ...:     print('Error')
   ...:     assert str(e) == "'dict' object has no attribute 'two'"
   ...:
Error

In [4]: data = {'one': aDict({'two': aDict({'three': aDict({'four': 4 })})})}
   ...: expect = ( "aDict({'one': "
   ...:              "aDict({'two': "
   ...:                "aDict({'three': "
   ...:                  "aDict({'four': 4})})})})" )
   ...: obj = aDict(data)
   ...: assert obj.__repr__() == expect

In [5]: data = {'one': aDict({'two': aDict({'three': aDict({'four': 4 })})})}
   ...: expect = 4
   ...: obj = aDict(data)
   ...: assert obj.one.two.three.four == expect

In [6]:
```

## class uDict
uDict is utilized dictionary.
uDict has followings  methods.

 - `replace_key(old, new, inplace=False)`
 - `replace_key_map(replace: Mapping, inplace=False)`
 - `map_keys( func, obj: Mapping, factory=None, inplace=False)`
 - `map_values( func, obj: Mapping, factory=None, inplace=False)`
 - `map_items( func, obj: Mapping, factory=None, inplace=Fals=Falsee)`
 - `filter_keys( func, obj: Mapping, factory=None, inplace=False)`
 - `filter_values( func, obj: Mapping, factory=None, inplace=False)`
 - `filter_items( func, obj: Mapping, factory=None, inplace=False)`
 - `map_keys(func, obj: Mapping, factory=None, inplace=False)`
 - `map_values(func, obj: Mapping, factory=None, inplace=False)`
 - `map_items(func, obj: Mapping, factory=None, inplace=False)`
 - `filter_keys(func, obj: Mapping, factory=None, inplace=False)`
 - `filter_values(func, obj: Mapping, factory=None, inplace=False)`
 - `filter_items(func, obj: Mapping, factory=None, inplace=False)`
 - `get_allkeys(obj: Mapping)`
 - `get_values(keys, obj: Mapping, wild=False, with_keys=False, verbatim=Flase)`
 - `counts_of_keys(keys, obj: Mapping, wild=False, verbatim=False)`
 - `counts_of_values(keys, obj: Mapping, wild=False, verbatim=False)`
 - `get_items(loc, value, obj: Mapping, func=None, factory=None)`
 - `del_items(loc, obj: Mapping, factory=None, inplace=False)`
 - `set_items(loc, value, obj: Mapping, func=None, factory=None, inplace=False)`
 - `compare(d1: Mapping, d2: Mapping, keys=None, thrown_error=False)`


### replace_key()

Create the new dictionary with changed keys.
If set `True` to `inplace`, perform operation in-place.

```python
In [1]: from datajuggler import uDict
   ...:
   ...: data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...: expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4 }
   ...:
   ...: saved = data.copy()
   ...: result = data.replace_key('April', 'Apr')
   ...: assert ( result == expect
   ...:          and data == saved )
```

### replace_key_map()

Create the new dictionary with changed keys using map dictionary..
If set `True` to `inplace`, perform operation in-place.

```python

In [2]: data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...: replace = {'January': 'Jan', 'February': 'Feb' }
   ...: expect = { 'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4 }
   ...: saved = data.copy()
   ...: result = data.replace_key_map(replace)
   ...: assert ( result == expect
   ...:          and data == saved )

In [3]: data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...: replace = {'January': 'Jan', 'February': 'Feb' }
   ...: expect = { 'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4 }
   ...: saved = data.copy()
   ...: data.replace_key_map(replace, inplace=True)
   ...: assert ( data == expect
   ...:          and data != saved )
```

### map_keys()
Create a new dictionary with apply function to keys of dictionary.
if not set `obj`, use self.
If set `factory`, create instance of factory class.
If set `True` to `inplace`, perform operation in-place.

```python
In [1]: from datajuggler import aDict, uDict, iDict
   ...:
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = uDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
   ...: obj = uDict(data)
   ...: saved = obj.copy()
   ...: result = obj.map_keys(str.upper)
   ...: assert ( result == expect and data == saved )

In [2]: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = uDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
   ...: result = uDict().map_keys(str.upper, data)
   ...: assert result == expect

In [3]: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = iDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
   ...: result = uDict().map_keys(str.upper, data, factory=iDict)
   ...: assert result == expect

In [4]: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = uDict({ 'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4 })
   ...: obj = uDict(data)
   ...: obj.map_keys(str.upper, inplace=True)
   ...: assert ( obj == expect )
```

### map_values()
Create a new dictionary with apply function to values of dictionary.
if not set `obj`, use self.
If set `factory`, create instance of factory class.
If set `True` to `inplace`, perform operation in-place.


```python
In [5]: data = { 'Jack': [10, 11, 12], 'John': [8, 15, 3] }
   ...: expect = { 'Jack': 33, 'John': 26 }
   ...: obj = uDict(data)
   ...: saved = obj.copy()
   ...: result = obj.map_values(sum)
   ...: assert ( result == expect and data == saved )

In [6]: data = { 'Jack': [10, 11, 12], 'John': [8, 15, 3] }
   ...: expect = { 'Jack': 33, 'John': 26 }
   ...: obj = uDict(data)
   ...: saved = obj.copy()
   ...: obj.map_values(sum, inplace=True)
   ...: assert ( obj == expect )
```

### map_items()
Create a new dictionary with apply function to items of dictionary.
if not set `obj`, use self.
If set `factory`, create instance of factory class.
If set `True` to `inplace`, perform operation in-place.

```python
In [7]: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = uDict({ 1: 'January', 2: 'February', 3: 'March', 4: 'April' })
   ...: obj = uDict(data)
   ...: saved = obj.copy()
   ...: result = obj.map_items(reversed)
   ...: assert ( result == expect and obj == saved )

In [8]: result = uDict().map_items(reversed, data)
   ...: assert result == expect

In [9]: expect = aDict({ 1: 'January', 2: 'February', 3: 'March', 4: 'April' })
   ...: result = uDict().map_items(reversed, data, factory=aDict)
   ...: assert result == expect

```

### filter_keys()
Create a new dictionary with filter items in dictionary by keys.
if not set `obj`, use self.
If set `factory`, create instance of factory class.
If set `True` to `inplace`, perform operation in-place.

```python
In [10]: is_janfeb = lambda x: x.endswith('ary')
    ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
    ...: expect = uDict({ 'January': 1, 'February': 2 })
    ...:
    ...: obj = uDict(data)
    ...: saved = obj.copy()
    ...: result = obj.filter_keys(is_janfeb)
    ...: assert ( result == expect and obj == saved )

In [11]: obj = uDict(data)
    ...: obj.filter_keys(is_janfeb, inplace=True)
    ...: assert obj == expect

In [12]: result = uDict().filter_keys(is_janfeb, data)
    ...: assert result == expect

In [13]: expect = aDict({ 'January': 1, 'February': 2 })
    ...: result = uDict().filter_keys(is_janfeb, data, factory=aDict)
    ...: assert result == expect
```

### filter_values()
Create a new dictionary with filter items in dictionary by values.
if not set `obj`, use self.
If set `factory`, create instance of factory class.
If set `True` to `inplace`, perform operation in-place.

```python
In [14]: is_even = lambda x: x % 2 == 0
    ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
    ...: expect = uDict({ 'February': 2, 'April': 4 })
    ...:
    ...: obj = uDict(data)
    ...: saved = obj.copy()
    ...: result = obj.filter_values(is_even)
    ...: assert ( result == expect and obj == saved )

In [15]: obj = uDict(data)
    ...: obj.filter_values(is_even, inplace=True)
    ...: assert obj == expect

In [16]: result = uDict().filter_values(is_even, data)
    ...: assert result == expect

In [17]: expect = aDict({ 'February': 2, 'April': 4 })
    ...: result = uDict().filter_values(is_even, data, factory=aDict)
    ...: assert result == expect

In [18]:
```

### filter_items()
Create a new dictionary with filter items in dictionary by item.
if not set `obj`, use self.
If set `factory`, create instance of factory class.
If set `True` to `inplace`, perform operation in-place.

```python
In [1]: from datajuggler import uDict, iDict, aDict
   ...:
   ...: def is_valid(item):
   ...:     k, v = item
   ...:     return k.endswith('ary') and v % 2 == 0
   ...:
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = uDict({ 'February': 2 })
   ...:
   ...: obj = uDict(data)
   ...: saved = obj.copy()
   ...: result = obj.filter_items(is_valid)
   ...: assert ( result == expect and obj == saved )

In [2]: obj = uDict(data)
   ...: obj.filter_items(is_valid, inplace=True)
   ...: assert obj == expect

In [3]: is_even = lambda x: x % 2 == 0
   ...: expect = uDict({ 'February': 2 })
   ...: result = uDict().filter_items(is_valid, data)
   ...: assert result == expect

In [4]: is_even = lambda x: x % 2 == 0
   ...: expect = aDict({ 'February': 2 })
   ...: result = uDict().filter_items(is_valid, data, factory=aDict)
   ...: assert result == expect

In [5]: result.February
Out[5]: 2

In [6]:
```

### get_allkeys()
Get to get all keys from dictionary as a List
This method is able to process on nested dictionary.

```python
In [1]: from datajuggler import uDict, iDict, aDict
   ...:
   ...: data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
   ...: expect = ['x', 'y', 'z', 'a', 'b', 'c']
   ...:
   ...: result = uDict().get_allkeys(data)
   ...: assert result == expect

In [2]: result = uDict(data).get_allkeys()
   ...: assert result == expect

In [3]: data = {'x': {'y': {'z': [{'a': 'v11', 'b': 'v12', 'c': 'v13'},
   ...:                           {'a': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
   ...: expect =  ['x', 'y', 'z', 'a', 'b', 'c', 'a', 'b', 'c']
   ...:
   ...: result = uDict(data).get_allkeys()
   ...: assert result == expect

In [4]:
```

### get_values()
Search the key in the objet(s).
if not set `obj`, use self object.
return a list of values.
if pass `with_keys=True`, return dict with key, values pair.
if pass `wild=True` match strings substr and ignorecase.


```python
In [1]: from datajuggler import uDict, iDict, aDict
   ...:
   ...: data = {'x': {'y': {'z': [{'a': 'v11', 'b': 'v12', 'c': 'v13'},
   ...:                           {'a': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
   ...: expect = ['v11', 'v21']
   ...: result = uDict().get_values('a', data)
   ...: assert result == expect

In [2]: expect = ['v11', 'v21']
   ...: result = uDict(data).get_values('a')
   ...: assert result == expect

In [3]: expect = {'a': ['v11', 'v21']}
   ...: result = uDict().get_values('a', data, with_keys=True)
   ...: assert result == expect

In [4]: data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
   ...:                           {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
   ...: expect = ['v11', 'v21']
   ...: result = uDict().get_values('a', data, wild=True)
   ...: assert result == expect

In [5]: expect = ['v11', 'v21']
   ...: result = uDict().get_values('aa', data, wild=True)
   ...: assert result == expect

In [6]: expect = {'aA': ['v11', 'v21'], 'b': ['v12', 'v22']}
   ...: result = uDict(data).get_values(['aA', 'b'])
   ...: assert result == expect

In [7]: expect = {'a': ['v11', 'v21'], 'b': ['v12', 'v22']}
   ...: result = uDict(data).get_values(('a', 'b'), wild=True)
   ...: assert result == expect

In [8]: expect = {'aA': ['v11', 'v21'], 'b': ['v12', 'v22']}
   ...: result = uDict(data).get_values(('a', 'b'), wild=True, verbatim=True)
   ...: assert result == expect

In [9]:
```

### counts_of_keys()

Count of keys.

```python
In [1]: from datajuggler import uDict, iDict, aDict
   ...:
   ...: data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
   ...:                           {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
   ...: count = uDict(data).counts_of_keys('aA')
   ...: assert count == 2

In [2]: count = uDict().counts_of_keys('aA', data)
   ...: assert count == 2
   ...:

In [3]: count = uDict(data).counts_of_keys('aa')
   ...: assert count == 0
   ...:

In [4]: count = uDict(data).counts_of_keys('aa', wild=True)
   ...: assert count == 2

In [5]: count = uDict(data).counts_of_keys('a', wild=True)
   ...: assert count == 2

In [6]: expect = {'aA': 2, 'b': 2}
   ...: count = uDict().counts_of_keys(['aA', 'b'], data)
   ...: assert count == expect

In [7]: expect = {'a': 2, 'b': 2}
   ...: count = uDict().counts_of_keys(['a', 'b'], data, wild=True)
   ...: assert count == expect

In [8]: expect = {'aA': 2, 'b': 2}
   ...: count = uDict().counts_of_keys(['a', 'b'], data,
   ...:                 wild=True, verbatim=True)
   ...: assert count == expect

In [9]:
```

### counts_of_values()

Counts of values.

```python
In [1]: from datajuggler import uDict, iDict, aDict
   ...:
   ...: data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
   ...:                           {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
   ...: expect = {'v11': 1}
   ...: count = uDict(data).counts_of_values('v11')
   ...: assert count == expect

In [2]: data = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
   ...:                           {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
   ...: expect = {'v11': 1}
   ...: count = uDict().counts_of_values('v11', data)
   ...: assert count == expect

In [3]: expect = {'v1': 3}
   ...: count = uDict().counts_of_values('v1', data, wild=True)
   ...: assert count == expect

In [4]: expect = {'v11': 1, 'v12': 1, 'v13': 1}
   ...: count = uDict().counts_of_values('v1', data, wild=True, verbatim=True)
   ...:
   ...: assert count == expect

In [5]: data = {'x': {'y': {'z': [{'aA': 100, 'b': 101, 'c': 103},
   ...:                           {'aA': 100, 'b': 101, 'c': 103}]} }}
   ...: expect = {100: 2}
   ...: count = uDict(data).counts_of_values(100)
   ...: assert count == expect

In [6]:
```


### get_items()

 `get_items(loc, value, obj: Mapping, func=None, factory=None)`

Create new dictionary with new key value pair as d[key]=val.
If set `True` to `inplace`, perform operation in-place.
otherwise, not modify the initial dictionary.

`loc` is  the location of the value.

i.e.: { 'a': { 'b1': { 'c1': {'x': 1 },
                       'c2': {'x': 2 }},
             { 'b2': { 'c1': {'x': 3 },
                       'c2': {'x': 4 }} }}}

if set ['a', 'b1', 'c1',  'x']  to `loc`, val is 1.
giving the location of the value to be changed in `obj`.
if set loc as str, convert to list using `loc.split(sep=' ')`.
value: the value to aplly


```python
In [1]: from datajuggler import uDict, iDict, aDict
   ...:
   ...: data = { 'a': 1, 'b': 2}
   ...: expect = {'a': 3, 'b': 2}
   ...:
   ...: result = uDict(data).get_items('a', 3)
   ...: assert result == expect

In [2]: result = uDict().get_items('a', 3, data)
   ...: assert result == expect

In [3]: expect = {'a': 1, 'b': 2, 'c': 3}
   ...: result = uDict(data).get_items('c', 3)
   ...: assert result == expect

In [4]: data = {}
   ...: expect = {'a': 1}
   ...: result = uDict(data).get_items('a', 1)
   ...: assert result == expect

In [5]: data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
   ...:                        {'c': 22, 'd': 22 }] }
   ...: expect = {'a': 1, 'b': 2}
   ...: result = uDict(data).get_items('b', 2)
   ...: assert result == expect

In [6]: data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
   ...:                        {'c': 22, 'd': 22 }] }
   ...: expect = {'a': 1, 'b': [{'c': 11, 'd': 12},
   ...:                         {'c': 22, 'd': 22}], 'c': 33}
   ...: result = uDict(data).get_items('c', 33)
   ...: assert result == expect

In [7]: data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
   ...: expect = {'a': 'v11', 'b': 'v2', 'c': 'v3'}
   ...: result = uDict(data).get_items('x y z a', 'v11')
   ...: assert result == expect

In [8]:
```

### del_items()

 - `del_items(loc, obj: Mapping, factory=None, inplace=False)

Create new dicttionary with the given key(s) removed.
New dictionary has d[key] deleted for each supplied key.
If set `True` to `inplace`, perform operation in-place.
otherwise, not modify the initial dictionary.

loc:
    the location of the value.
    i.e.: { 'a': { 'b1': { 'c1': {'x': 1 },
                           'c2': {'x': 2 }},
                 { 'b2': { 'c1': {'x': 3 },
                           'c2': {'x': 4 }} }}}
    if set ['a', 'b1', 'c1',  'x']  to loc, val is 1.
    giving the location of the value to be changed in `obj`.
    if set loc as str, convert to list using `loc.split(sep=' ')`.
obj
    dictionary on which to operate
inplace:
    If set `True` to `inplace`, perform operation in-place.
    otherwise, not modify the initial dictionary.


```python
In [1]: from datajuggler import uDict, iDict, aDict
   ...:
   ...: data = { 'a': 1, 'b': 2}
   ...: expect = {'b': 2}
   ...:
   ...: result = uDict(data).del_items('a')
   ...: assert result == expect

In [2]: result = uDict().del_items('a', data)
   ...: assert result == expect

In [3]: expect = {'a': 1, 'b': 2}
   ...: result = uDict(data).del_items('c')
   ...: assert result == expect

In [4]: expect = {'b': 2}
   ...: obj = uDict(data)
   ...: obj.del_items('a', inplace=True)
   ...: assert obj == expect

In [5]: expect = "aDict({'b': 2})"
   ...: result = uDict(data).del_items('a', factory=aDict)
   ...: assert result.__repr__() == expect

In [6]: data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
   ...: expect = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
   ...: result = uDict(data).del_items('a')
   ...: assert result == expect

In [7]: data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
   ...: expect = {'x': {'y': {'z': {'b': 'v2', 'c': 'v3'}}}}
   ...: result = uDict(data).del_items('x y z a')
   ...: assert result == expect

In [8]:
```

### set_items()

 - `set_items(loc, value, obj: Mapping, func=None, factory=None, inplace=False)`

Create new dict with new, potentially nested, key value pair
loc:
    the location of the value.
    i.e.: { 'a': { 'b1': { 'c1': {'x': 1 },
                           'c2': {'x': 2 }},
                 { 'b2': { 'c1': {'x': 3 },
                           'c2': {'x': 4 }} }}}
    if set ['a', 'b1', 'c1',  'x']  to loc, val is 1.
    giving the location of the value to be changed in `obj`.
    if set loc as str, convert to list using `loc.split(sep=' ')`.
obj
    dictionary on which to operate
func:
    the function to apply the object(s)..
inplace:
    If set `True` to `inplace`, perform operation in-place.
    otherwise, not modify the initial dictionary.


```python
In [1]: from datajuggler import uDict, iDict, aDict
   ...:
   ...: data = { 'a': 1, 'b': 2}
   ...: expect = { 'a': 2, 'b': 2}
   ...:
   ...: result = uDict(data).set_items('a',2 )
   ...: assert result == expect

In [2]: obj = uDict(data)
   ...: obj.set_items('a',2, inplace=True)
   ...: assert obj == expect

In [3]: data = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
   ...:                        {'c': 22, 'd': 22 }] }
   ...: expect = {'a': 1, 'b': 2}
   ...: result = uDict(data).set_items('b', 2)
   ...: assert result == expect

In [4]: expect = { 'a': 1, 'b': [{'c': 11, 'd': 12 },
   ...:                        {'c': 22, 'd': 22 }], 'c': 3 }
   ...: result = uDict(data).set_items('c', 3)
   ...: assert result == expect

In [5]: data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
   ...: expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
   ...: obj = uDict(data)
   ...: obj['x']['y']['z']['a']='v11'
   ...: assert obj == expect

In [6]: data = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
   ...: expect = {'x': {'y': {'z': {'a': 'v11', 'b': 'v2', 'c': 'v3'}}}}
   ...: result = uDict(data).set_items('x y z a', 'v11')
   ...: assert result == expect

In [7]:
```

### compare()

 - `compare(d1: Mapping, d2: Mapping, keys=None, thrown_error=False)`

Compare tow dictionary with keys and return `True` when equal found values.
otherwise return `False`.
if not set second dictionary, use self object.
if not set keys, just compare two dictionaries,
if pass `thrown_error=True`, raise ValueError when not equal found values.

```python
In [1]: from datajuggler import uDict, iDict, aDict
   ...:
   ...: d1 = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
   ...:                         {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
   ...: d2 = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
   ...:                         {'aA': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
   ...:
   ...: result = uDict().compare(d1, d2)
   ...: assert result == True

In [2]: result = uDict(d1).compare(d2)
   ...: assert result == True

In [3]: result = uDict().compare(d1, d2, keys='aA')
   ...: assert result == True

In [4]: d1 = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
   ...:                         {'aB': 'v21', 'b': 'v22', 'c': 'v23'}]} }}
   ...: d2 = {'x': {'y': {'z': [{'aA': 'v11', 'b': 'v12', 'c': 'v13'},
   ...:                         {'aB': 'd21', 'b': 'd22', 'c': 'd23'}]} }}
   ...: result = uDict().compare(d1, d2, keys=['aA', 'b'])
   ...: assert result == True

In [5]: d1 = {'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}}
   ...: d2 = {'x': {'y': {'z': {'a': 'v10', 'b': 'v2', 'c': 'v3'}}}}
   ...: expect = "{'x': {'y': {'z': {'a': 'v1', 'b': 'v2', 'c': 'v3'}}}} is no
   ...: t equal {'x': {'y': {'z': {'a': 'v10', 'b': 'v2', 'c': 'v3'}}}}."
   ...: try:
   ...:     result = uDict().compare(d1, d2, thrown_error=True)
   ...: except ValueError as e:
   ...:     print('Error')
   ...:     assert str(e) == expect
   ...:
Error

In [6]:
```


### class iDict

Immutable Dict. iDict is hashable object.

if set `iplace` parameter, it will not cause an error.
but will always be ignored.

```python
In [1]: from datajuggler import iDict
   ...:
   ...: data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...:
   ...: assert hasattr(data, '__hash__') == True

In [2]: obj = dict({data: 1})
   ...: assert  obj[data]  == 1

In [3]: obj
Out[3]: {iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4}): 1}

In [4]: try:
   ...:     data['January'] = 'Jan'
   ...: except TypeError as e:
   ...:     print('Error')
   ...:     assert str(e) == 'iDict object does not support item assignment'
   ...:
Error

In [5]: try:
   ...:     result  = data.pop(0)
   ...: except AttributeError as e:
   ...:     print('Error')
   ...:     assert str(e) == 'iDict object has no attribute pop'
   ...:
Error

In [6]: try:
   ...:     data.clear()
   ...: except AttributeError as e:
   ...:     print('Error')
   ...:     assert str(e) == 'iDict object has no attribute clear'
   ...:
Error

In [7]: try:
   ...:     data.update({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: )
   ...: except AttributeError as e:
   ...:     print('Error')
   ...:     assert str(e) == 'iDict object has no attribute update'
   ...:
Error

In [8]: try:
   ...:     data.setdefault('March', 3)
   ...: except AttributeError as e:
   ...:     print('Error')
   ...:     assert str(e) == 'iDict object has no attribute setdefault'
   ...:
Error

In [9]:
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

In [4]: c.convert_case('sentence', 'The sky is the limits')
Out[4]: 'The sky is the limits'

In [5]: c.convert_case('The sky is the limits')
Out[5]: 'the_sky_is_the_limits'

In [6]: c.convert_case('const', 'The sky is the limits')
Out[6]: 'THE_SKY_IS_THE_LIMITS'

In [7]: c.convert_case('camel', ['Good Morning','Thank you'])
Out[7]: ['goodMorning', 'thankYou']

In [8]:
```

`StrCase` class support str, list, dict.

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


### ordereddict_to_dict()

Convert objects from OrderedDict to Dict.

```python
In [1]: from collections import OrderedDict
   ...: from datajuggler import ordereddict_to_dict
   ...:
   ...: data = OrderedDict([('month', 'January'), ('day', 13 )])
   ...: expect = dict({'month': 'January', 'day': 13})
   ...: result = ordereddict_to_dict(data)
   ...: assert result == expect

In [2]: data = OrderedDict([('month', 'January'), ('day', 13 ),
   ...:                     ('time', OrderedDict([('hours', 7), ('minutes', 30
   ...: )]))])
   ...: expect = dict({'month': 'January', 'day': 13,
   ...:                'time': {'hours': 7, 'minutes': 30}})
   ...: result = ordereddict_to_dict(data)
   ...: assert result == expect

In [3]:
```

### chnage_dict_keys()

Change keys for dict objects.
if you want to change nested object, you should try `replace_values()`.
and uDict object has `replace_key()` and `replace_key_map()` method.

```python
In [1]: from datajuggler import change_dict_keys
   ...:
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: replace = { 'March': 3, 'April': 4 }
   ...: expect = { 'January': 1, 'February': 2, 3: 3, 4: 4 }
   ...: result = change_dict_keys(data, replace)
   ...: assert result == expect

In [2]: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: replace = { 'March': 3, 'April': 4 }
   ...: expect = { 'January': 1, 'February': 2, 3: 3, 4: 4 }
   ...: change_dict_keys(data, replace, inplace=True)
   ...: assert data == expect
   ...:

In [3]: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4 }
   ...: result = change_dict_keys(data, 'April', 'Apr')
   ...: assert result == expect

In [4]: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4 }
   ...: change_dict_keys(data, 'April', 'Apr', inplace=True)
   ...: assert data == expect

In [5]:
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

### is_alpha() and is_alnum()

```python
assert is_alpha('iisaka') == True
assert is_alpha('iisaka51') == False
assert is_alpha('@iisaka51') == False
assert is_alpha('Goichi (iisaka) Yukawa') == False
assert is_alpha('京都市') == False
assert is_alpha('１２３') == False

assert is_alnum('iisaka') == True
assert is_alnum('iisaka51') == True
assert is_alnum('@iisaka51') == False
assert is_alnum('Goichi (iisaka) Yukawa') == False

assert ( is_alnum('京都市') == False )
assert ( is_alnum('１２３') == False )
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

