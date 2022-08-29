# DataJuggler

This library provides utility classes and helper functions for data processing.
This is spin-off project from [scrapinghelper](https://github.com/iisaka51/scrapinghelper).


 - class StrCase
   Convert case for object(s).
 - class aDict
   Allow to access using dot notation for dictionary.
 - class uDict
   Allow to change key for Dict.
 - class iDict
   Immutable Dict. iDict object hashable.

utilities for string manupulate helper functions.

 -  is_alpha() - Check word is alphabet.
 -  is_alnum() - Check word is alphabet and digits.
 -  ordereddict_to_dict() - convert object from OrderedDict to Dict.
 -  change_dict_keys() - Change keys of Dict.
 -  replace_values() - Replace objects for object(s).
 -  omit_values() - Omit values for object(s).
 -  add_df() - Add data into DataFrame.
 -  df_compare() - Check DataFrame is equals.
 -  split_chunks() - Split iterable object into chunks.
 -  urange() - Return an object that produces a sequence of integes.


### class StrCase

`strCase` class support convert case.

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
data = "The sky is the limit"
expect = 'the-sky-is-the-limit'
s = StrCase(data)
assert s.convert_case('kebab') == expect

data = "The sky is the limit"
expect = 'theSkyIsTheLimit'
s = StrCase(data)
assert s.convert_case(case='camel') == expect

data = ["Good luck", "The sky is the limit" ]
expect = ["good_luck", "the_sky_is_the_limit"]
s = StrCase(data)
assert s.convert_case() == expect

data = {1: "Good luck", 2: "The sky is the limit" }
expect = {1: "good_luck", 2: "the_sky_is_the_limit" }
s = StrCase(data)
assert s.convert_case() == expect

data = {"Good luck": 1, "The sky is the limit": 2 }
expect = {"good_luck": 1, "the_sky_is_the_limit": 2 }
s = StrCase(data)
assert s.convert_case(replace_for='key') == expect

```

`StrCase` class support nested objects.

```python
data = ["Good luck", "The sky is the limit",
        {1: "Good luck", 2: "The sky is the limit" } ]
expect = ["good_luck", "the_sky_is_the_limit",
        {1: "good_luck", 2: "the_sky_is_the_limit" } ]
s = StrCase(data)
assert s.convert_case() == expect
```

### class aDict
Allow to access using dot notation for dictionary.
This class inspired [munch](https://github.com/Infinidat/munch).

```python
data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
expect = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
result = aDict(data)
assert result == data

data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
expect = 2
result = aDict(data)
assert result.February == expect

data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
expect = 4
result = aDict(data)
assert result.one.two.three.four == expect

data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
expect = "{'one': {'two': {'three': {'four': 4}}}}"
result = aDict(data)
assert result.__str__() == expect

data = { 'one': { 'two': { 'three': { 'four': 4 }}}}
expect = "aDict({'one': aDict({'two': aDict({'three': aDict({'four': 4})})})})"
result = aDict(data)
assert result.__repr__() == expect

data = {"console": "Nintendo Switch",
        "games": ["The Legend of Zelda", "Mario Golf"]}
expect = ( '{"console": "Nintendo Switch", '
           '"games": ["The Legend of Zelda", "Mario Golf"]}' )
obj = aDict(data)
assert obj.to_json() == expect

json_data = ( '{"console": "Nintendo Switch", '
              '"games": ["The Legend of Zelda", "Mario Golf"]}' )
expect = ( "aDict({'console': 'Nintendo Switch', "
           "'games': ['The Legend of Zelda', 'Mario Golf']})" )
obj = aDict()
obj.from_json(json_data)
assert obj.__repr__() == expect

obj = aDict().from_json(json_data)
assert obj.__repr__() == expect
```

```python
from datajuggler import aDict

data = {"console": "Nintendo Switch",
        "games": ["The Legend of Zelda", "Mario Golf"]}
json_data = ( '{"console": "Nintendo Switch", '
              '"games": ["The Legend of Zelda", "Mario Golf"]}' )
obj = aDict(data)
assert obj.to_json() == json_data

repr = ( "aDict({'console': 'Nintendo Switch', "
         "'games': ['The Legend of Zelda', 'Mario Golf']})" )

obj = aDict().from_json(json_data)
assert obj.__repr__() == repr

obj = aDict()
obj.from_json(json_data, inplace=True)
assert obj.__repr__() == repr

data = [ 'January', 'February', 'March', 'April' ]
expect = "aDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
obj = aDict().fromkeys(data, 2)
assert obj.__repr__() == expect

obj = aDict()
obj.fromkeys(data, 2, inplace=True)
assert obj.__repr__() == expect

data = [ 'January', 'February', 'March', 'April' ]
expect = "aDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
obj = aDict().fromvalues(data)
assert obj.__repr__() == expect

obj = aDict()
obj.fromvalues(data, base=1, inplace=True)
assert obj.__repr__() == expect

expect = "aDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})"
obj = aDict().fromvalues(data, base=0)
assert obj.__repr__() == expect

keys = [ 'January', 'February', 'March', 'April' ]
values = [ 1, 2, 3, 4 ]
expect = "aDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
obj = aDict().fromlists(keys, values)
assert obj.__repr__() == expect

obj = aDict()
obj.fromlists(keys, values, inplace=True)
assert obj.__repr__() == expect

keys = [ 'January', 'February' ]
values = [ 1, 2, 3, 4 ]
expect = "aDict({'January': 1, 'February': 2})"
obj = aDict().fromlists(keys, values)
assert obj.__repr__() == expect

keys = [ 'January', 'February', 'March', 'April' ]
values = [ 1, 2 ]
expect = "aDict({'January': 1, 'February': 2})"
obj = aDict().fromlists(keys, values)
assert obj.__repr__() == expect
```

### class uDict
Support change keys  for dict.

```python
from datajuggler import uDict

data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
expect = { 'January': 1, 'February': 2, 'March': 3, 'Apr': 4 }
saved = data.copy()
result = data.replace_key('April', 'Apr')
assert ( result == expect and data == saved )

data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
replace = {'January': 'Jan', 'February': 'Feb' }
expect = { 'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4 }
saved = data.copy()
result = data.replace_key_map(replace)
assert ( result == expect
         and data == saved )

data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
replace = {'January': 'Jan', 'February': 'Feb' }
expect = { 'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4 }
saved = data.copy()
result = data.replace_key_map(replace)
assert ( result == expect and data == saved )

data = uDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })
replace = {'January': 'Jan', 'February': 'Feb' }
expect = { 'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4 }
saved = data.copy()
data.replace_key_map(replace, inplace=True)
assert ( data == expect and data != saved )
```


```python
from datajuggler import uDict
data = {"console": "Nintendo Switch",
        "games": ["The Legend of Zelda", "Mario Golf"]}
json_data = ( '{"console": "Nintendo Switch", '
           '"games": ["The Legend of Zelda", "Mario Golf"]}' )
repr  = ( "uDict({'console': 'Nintendo Switch', "
           "'games': ['The Legend of Zelda', 'Mario Golf']})" )

obj = uDict(data)
assert obj.to_json() == json_data

new = uDict().from_json(json_data)
assert new.__repr__() == repr

obj = uDict()
obj.from_json(json_data, inplace=True)
assert obj.__repr__() == repr

data = [ 'January', 'February', 'March', 'April' ]
expect = "uDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
obj = uDict().fromkeys(data, 2)
assert obj.__repr__() == expect

obj = uDict()
obj.fromkeys(data, 2, inplace=True)
assert obj.__repr__() == expect

data = [ 'January', 'February', 'March', 'April' ]
expect = "uDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
obj = uDict().fromvalues(data)
assert obj.__repr__() == expect

obj = uDict()
obj.fromvalues(data, base=1, inplace=True)
assert obj.__repr__() == expect

expect = "uDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})"
obj = uDict().fromvalues(data, base=0)
assert obj.__repr__() == expect


keys = [ 'January', 'February', 'March', 'April' ]
values = [ 1, 2, 3, 4 ]
expect = "uDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
obj = uDict().fromlists(keys, values)
assert obj.__repr__() == expect

obj = uDict()
obj.fromlists(keys, values, inplace=True)
assert obj.__repr__() == expect

keys = [ 'January', 'February' ]
values = [ 1, 2, 3, 4 ]
expect = "uDict({'January': 1, 'February': 2})"
obj = uDict().fromlists(keys, values)
assert obj.__repr__() == expect

keys = [ 'January', 'February', 'March', 'April' ]
values = [ 1, 2 ]
expect = "uDict({'January': 1, 'February': 2})"
obj = uDict().fromlists(keys, values)
assert obj.__repr__() == expect
```

### class iDict

Immutable Dict. iDict is hashable object.

```python
In [1] from datajuggler import uDict

In [2]: data = iDict({ 'January': 1, 'February': 2, 'March': 3, 'April': 4 })

In [3]: try:
   ...:     data['March']='Mar'
   ...: except TypeError as e:
   ...:     print(e)
   ...:
iDict object does not support item assignment

In [4]: hasattr(data, '__hash__')
Out[4]: True

In [5]: d = dict({data: 2})

In [6]: type(d)
Out[6]: dict

In [7]: d
Out[7]: {{'January': 1, 'February': 2, 'March': 3, 'April': 4}: 2}

In [8]: d[data]
Out[8]: 2

In [9]:
```

```python
from datajuggler import iDict
data = {"console": "Nintendo Switch",
        "games": ["The Legend of Zelda", "Mario Golf"]}
json_data = ( '{"console": "Nintendo Switch", '
              '"games": ["The Legend of Zelda", "Mario Golf"]}' )
obj = iDict(data)
assert obj.to_json() == json_data

expect = "iDict({'console': 'Nintendo Switch', 'games': ['The Legend of Zelda', 'Mario Golf']})"
result = iDict().from_json(json_data)
assert result.__repr__() == expect

# `inplace` parameters will be always ignored.
expect = "iDict({})"
obj = iDict()
obj.from_json(json_data, inplace=True)
assert obj.__repr__() == expect

data = [ 'January', 'February', 'March', 'April' ]
expect = "iDict({'January': 2, 'February': 2, 'March': 2, 'April': 2})"
obj = iDict().fromkeys(data, 2)
assert obj.__repr__() == expect

# `inplace` parameters will be always ignored.
data = [ 'January', 'February', 'March', 'April' ]
expect = "iDict({})"
obj = iDict()
obj.fromkeys(data, 2, inplace=True)
assert obj.__repr__() == expect

data = [ 'January', 'February', 'March', 'April' ]
expect = "iDict({1: 'January', 2: 'February', 3: 'March', 4: 'April'})"
obj = iDict().fromvalues(data)
assert obj.__repr__() == expect

data = [ 'January', 'February', 'March', 'April' ]
expect = "iDict({0: 'January', 1: 'February', 2: 'March', 3: 'April'})"
obj = iDict().fromvalues(data, base=0)
assert obj.__repr__() == expect

# `inplace` parameters will be always ignored.
data = [ 'January', 'February', 'March', 'April' ]
expect = "iDict({})"
obj = iDict()
obj.fromvalues(data, base=1, inplace=True)
assert obj.__repr__() == expect

keys = [ 'January', 'February', 'March', 'April' ]
values = [ 1, 2, 3, 4 ]
expect = "iDict({'January': 1, 'February': 2, 'March': 3, 'April': 4})"
obj = iDict().fromlists(keys, values)
assert obj.__repr__() == expect

# `inplace` parameters will be always ignored.
keys = [ 'January', 'February', 'March', 'April' ]
values = [ 1, 2, 3, 4 ]
expect = "iDict({})"
obj = iDict()
obj.fromlists(keys, values, inplace=True)
assert obj.__repr__() == expect

keys = [ 'January', 'February' ]
values = [ 1, 2, 3, 4 ]
expect = "iDict({'January': 1, 'February': 2})"
obj = iDict().fromlists(keys, values)
assert obj.__repr__() == expect

keys = [ 'January', 'February', 'March', 'April' ]
values = [ 1, 2 ]
expect = "iDict({'January': 1, 'February': 2})"
obj = iDict().fromlists(keys, values)
assert obj.__repr__() == expect

```

### ordereddict_to_dict()

Convert objects from OrderedDict to Dict.

```python
data = OrderedDict([('month', 'January'), ('day', 13 )])
expect = dict({'month': 'January', 'day': 13})
result = ordereddict_to_dict(data)
assert result == expect

data = OrderedDict([('month', 'January'), ('day', 13 ),
                    ('time', OrderedDict([('hours', 7), ('minutes', 30)]))])
expect = dict({'month': 'January', 'day': 13,
               'time': {'hours': 7, 'minutes': 30}})
result = ordereddict_to_dict(data)
assert result == expect
```

### chnage_dict_keys()

Change keys for dict objects.

```python
data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
replace = {'March': 3, 'April': 4 }
expect = { 'January': 1, 'February': 2, 3: 3, 4: 4 }
result = change_dict_keys(data, replace)
assert result == expect

data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
replace = {'April': 4, 'September': 9 }
expect = { 'January': 1, 'February': 2, 3: 3, 4: 4 }
saved = data.copy()
change_dict_keys(data, replace, inplace=True)
assert ( data == expect and data != saved )
```


### split_chunks()

Return split into even chunk_size elements.

```python
data = [11,12,13,14, 21,22,23,31,32,33]
expect = [[11,12,13, 14], [21,22,23,31], [32,33, None, None ]]
result = list(split_chunks(data,4))
assert result == expect

data = [11,12,13,14, 21,22,23,31,32,33]
expect = [[11,12,13, 14], [21,22,23,31], [32,33] ]
result = list(split_chunks(data,4, fill_na=False))
assert result == expect

data = [11,12,13,14, 21,22,23,31,32,33]
expect = [[11,12,13, 14], [21,22,23,31], [32,33, -1, -1] ]
result = list(split_chunks(data,4, na_value=-1))
assert result == expect
```

if pass tuple as input. return list of tuple for chunk data.

```python
data = (11,12,13,21,22,23,31,32,33)
expect = [(11,12,13), (21,22,23), (31,32,33)]
result = list(split_chunks(data,3))
assert result == expect
```

if pass dict objects as input. return list of dict for chunk data.
`fill_na` and `na_value` is always ignored.

```python
data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
expect = [{ 'January': 1, 'February': 2, 'March': 3},
          { 'April': 4 } ]
result = list(split_chunks(data,3))
assert result == expect

data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
expect = [{ 'January': 1, 'February': 2, 'March': 3},
          { 'April': 4 } ]
result = list(split_chunks(data,3, fill_na=True))
assert result == expect

data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
expect = [{ 'January': 1, 'February': 2, 'March': 3},
          { 'April': 4 } ]
result = list(split_chunks(data,3, na_value=None))
```

if pass str objects as input. return list of str for chunk data.
`fill_na` and `na_value` is always ignored.

```python
data = "Peter Piper picked a peck of pickled peppers."
expect = [ "Peter Piper picked a",
           " peck of pickled pep",
           "pers." ]
result = list(split_chunks(data,20))
assert result == expect

data = "Peter Piper picked a peck of pickled peppers."
expect = [ "Peter Piper picked a",
           " peck of pickled pep",
           "pers." ]
result = list(split_chunks(data,20, fill_na=True, na_value=None))
assert result == expect
```

### urange()

`urange()` is almost same as `range()`

```
expect = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
result = list(urange(10))
assert result == expect

expect = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = list(urange(1, 10))
assert result == expect

expect = [1, 3, 5, 7, 9]
result = list(urange(1, 10, 2))
assert result == expect

expect = [10, 8, 6, 4, 2]
result = list(urange(10, 1, -2))
assert result == expect

expect = [10, 9, 8, 7, 6, 5, 4, 3, 2]
result = list(urange(10, 1))
assert result == expect
```

`urange()` support callable as step.

```python
def  gen_step(val):
    return (val * 3)

expect = [1, 4, 16]
result = list(urange(1, 20, gen_step))
assert result == expect
```

### rename_duplicate()

Rename duplicate string for list or values of dict.

```python
data = ["Apple", "Apple", "Banana", "Maple" ]
expect = ["Apple", "Apple_01", "Banana", "Maple" ]
result = rename_duplicates(data)
assert result == expect

data = ["Apple", "Apple", "Banana", "Maple" ]
expect = ["Apple", "Apple__01", "Banana", "Maple" ]
result = rename_duplicates(data, separator='__')
assert result == expect

data = ["Apple", "Apple", "Banana", "Maple" ]
expect = ["Apple", "Apple_001", "Banana", "Maple" ]
result = rename_duplicates(data, format="{:03}")
assert result == expect

data = ["Apple", ["Apple", "Apple", "Banana", "Maple" ]]
expect = ["Apple", ["Apple", "Apple_01", "Banana", "Maple" ]]
result = rename_duplicates(data)
assert result == expect
```

