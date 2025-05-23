snakefunc
=========
A work in progress functional programming library for Python. Inspired by [PyFunctional](https://pyfunctional.pedro.ai/) and [Laravel Collections](https://laravel.com/docs/master/collections).

Usage
-----

### Importing and the `seq` Function

The foundation of the library is the `seq` function, which can be imported like so:

```python
from snakefunc import seq
```

The `seq` function is used to gather a sequence (e.g., a `list`, etc.) which can then be worked with utilizing chained methods.

### `.find()`

Find an item in your sequence and return it if it exists. Otherwise, returns `None`.

```python
objects = [
    {"id": 1, "name": "foo"},
    {"id": 2, "name": "bar"},
]

# Returns the dict with the name "foo".
seq(objects).find(lambda obj: obj["name"] == "foo")
```

### `.first()`

Returns the first item in the sequence, or `None` if the sequence is empty.

```python
# Returns the int 1.
seq([1, 2, 3]).first()
```

### `.last()`

Returns the last item in the sequence, or `None` if the sequence is empty.

```python
# Returns the int 3.
seq([1, 2, 3]).last()
```

### `.len()`

Returns the length of the sequence.

```python
# Returns the int 3.
seq([0, 1, 2]).len()
```

### `.reduce()`

Returns the result of the sequence being reduced to a singular value.

```python
# Returns the int 21.
seq([8, 6, 7]).reduce(lambda accumulator, value: accumulator + value)
```

### `.to_bytes()`

Returns the sequence as bytes.

```python
from snakefunc import seq

assert seq(["h", "e", "l", "l", "o", "!"]).to_bytes() == b"hello!"
```

### `.to_list()`

Returns the sequence as a list.

```python
# Returns the value `[5, 3, 0, 9]`.
seq([5, 3, 0, 9]).to_list()
```

### `.to_str()`

Returns the sequence as a str.

```python
# Returns the value `"8675309"`.
seq([8, 6, 7, 5, 3, 0, 9]).to_str()
```

Optionally, a separator may be specified.

```python
# Returns the value `"85.5.14"`.
seq([85, 5, 14]).to_str(separator=".")
```
