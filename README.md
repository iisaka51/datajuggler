# DataJuggler

This library provides utility classes and helper functions for data processing.
This is spin-off project from [scrapinghelper](https://github.com/iisaka51/scrapinghelper).


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

## class aDict
Allow to access using dot notation for dictionary.
This class inspired [munch](https://github.com/Infinidat/munch).

 - `fromkeys(sequence, inplace:bool=False)`
 - `fromvalues(sequence, inplace:bool=False)`
 - `fromlists(keys, values, inplace:bool=False)`
 - `to_json(**options)`
 - `from_json(json_data: str, inplace: bool=False, **options)`
 - `to_yaml(**options)`
 - `from_yaml(stream, *args, inplace: bool=False, **kwargs)`


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

### fromvalues()

Create a new dictionary from list of values.
keys automaticaly generate as interger.
`base` is the starting number.
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


## class uDict
Support change keys for dict.

 - `fromkeys(sequence, inplace:bool=False)
 - `fromvalues(sequence, inplace:bool=False)
 - `fromlists(keys, values, inplace:bool=False)
 - `to_json(**options)
 - `from_json(json_data: str, inplace: bool=False, **options),
 - `to_yaml(**options)`
 - `from_yaml(stream, *args, inplace: bool=False, **kwargs)`

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

### fromkeys()

Create a new dictionary with keys from iterable and values set to value.
If set `True` to `inplace`, perform operation in-place.

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

### fromvalues()

Create a new dictionary from list of values.
keys automaticaly generate as interger.
`base` is the starting number.
If set `True` to `inplace`, perform operation in-place.

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

```

### fromlists()

Create a new dictionary from two list as keys and values.
Only the number of elements in the shorter of the two lists is processed.
If set `True` to `inplace`, perform operation in-place.

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

### JSON

to_json() and from_json().
If set `True` to `inplace`, perform operation in-place.


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

### YAML

if PyYAML is installed, enable `to_yaml()` and `from_yaml()` method.

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

### class iDict

Immutable Dict. iDict is hashable object.

 - `fromkeys(sequence, inplace:bool=False)
 - `fromvalues(sequence, inplace:bool=False)
 - `fromlists(keys, values, inplace:bool=False)
 - `to_json(**options)
 - `from_json(json_data: str, inplace: bool=False, **options),
 - `to_yaml(**options)`
 - `from_yaml(stream, *args, inplace: bool=False, **kwargs)`

if set `iplace` parameter, it will not cause an error.
but will always be ignored.

```python
In [1]: from datajuggler import iDict
   ...:
   ...: data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: result = iDict(data)
   ...: assert result == data

In [2]: expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: result = iDict(January=1, February=2, March=3, April=4)
   ...: assert result == expect

In [3]: data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...: expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
   ...: assert data == expect

In [4]: data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...: try:
   ...:     data['January'] = 'Jan'
   ...: except TypeError as e:
   ...:     assert str(e) == 'iDict object does not support item assignment'
   ...:     print(e)
   ...:
iDict object does not support item assignment

In [5]: data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...: try:
   ...:     result  = data.pop(0)
   ...: except AttributeError as e:
   ...:     assert str(e) == 'iDict object has no attribute pop'
   ...:     print(e)
   ...:
iDict object has no attribute pop

In [6]: data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...: try:
   ...:     data.clear()
   ...: except AttributeError as e:
   ...:     assert str(e) == 'iDict object has no attribute clear'
   ...:     print(e)
   ...:
iDict object has no attribute clear

In [7]: data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...: try:
   ...:     data.update({ 'January': 1, 'February': 2, 'March': 3, 'April': 4
   ...: })
   ...: except AttributeError as e:
   ...:     assert str(e) == 'iDict object has no attribute update'
   ...:     print(e)
   ...:
iDict object has no attribute update

In [8]: data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
   ...: try:
   ...:     data.setdefault('March', 3)
   ...: except AttributeError as e:
   ...:     assert str(e) == 'iDict object has no attribute setdefault'
   ...:     print(e)
   ...:
iDict object has no attribute setdefault
```

iDict object is hashable.

```python
In [1]: from datajuggler import iDict
   ...:
   ...: data = iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})
   ...: assert hasattr(data, '__hash__') == True

In [2]: data = iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})
   ...: result = dict({data: 1})
   ...: assert  result[data]  == 1

In [3]: result
Out[3]: {iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4}): 1}

In [4]: type(result)
Out[4]: dict

```

### fromkeys()

Create a new dictionary with keys from iterable and values set to value.
if set `iplace` parameter, it will not cause an error.
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
keys automaticaly generate as interger.
`base` is the starting number.
if set `iplace` parameter, it will not cause an error.
but will always be ignored.

```python
In [6]: data = [ 'January', 'February', 'March', 'April' ]
   ...: expect = ( "iDict("
   ...:            "{1: 'January', 2: 'February', 3: 'March', 4: 'April'}"
   ...:            ")" )
   ...: obj = iDict().fromvalues(data)
   ...: assert obj.__repr__() == expect

In [7]: data = [ 'January', 'February', 'March', 'April' ]
   ...: expect = ( "iDict("
   ...:            "{0: 'January', 1: 'February', 2: 'March', 3: 'April'}"
   ...:            ")" )
   ...: obj = iDict().fromvalues(data, base=0)
   ...: assert obj.__repr__() == expect

In [8]: data = [ 'January', 'February', 'March', 'April' ]
   ...: expect = "iDict({})"
   ...: obj = iDict()
   ...: obj.fromvalues(data, base=1, inplace=True)
   ...: assert obj.__repr__() == expect

```

### fromlists()

Create a new dictionary from two list as keys and values.
Only the number of elements in the shorter of the two lists is processed.
if set `iplace` parameter, it will not cause an error.
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

### to_json() and from_json()

Generate JSON strings from the dictionary.
Generate new dictionary from JSON strings.

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

