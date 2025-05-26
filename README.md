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

### `.clear()`

Remove all items from the underlying sequence.

```python
from snakefunc import seq

sequence = seq([1, 2, 3])
sequence.clear()

assert sequence.value() == []
```

### `.count()`

Get the number of times an item occurs in the sequence.

```python
from snakefunc import seq

assert seq([1, 3, 3, 7]).count(3) == 2
```

Optionally, sequences of `bytearray`, `bytes`, and `str` types support the `start` and `end` arguments. Other types will raise a `TypeError` if they are provided.

```python
from snakefunc import seq

assert seq[bytes](b"123455555").count(b"5", 0, 5) == 1
```

### `.deduplicate()`

Deduplicate the items in the sequence.

```python
from snakefunc import seq

assert seq((1, 2, 2, 3, 4, 4, 5)).deduplicate().value() == (1, 2, 3, 4, 5)
```

### `.duplicates()`

Find the duplicate items in the sequence.

```python
from snakefunc import seq

assert seq("Hello, world!").duplicates().to_tuple() == ("l", "o")
```

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

### `.index()`

Returns the index of the first occurrence of `item` in the sequence.

```python
from snakefunc import seq

assert seq("abc").index("c") == 2
```

Optionally, `start` and `stop` arguments can also be provided.

```python
from snakefunc import seq

assert seq(("foo", "bar", "foo", "foo")).index("foo", 1, 3) == 2
```

Note that if the sequence is of the `range` type, then the `start` and `stop` arguments are not supported.

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
from snakefunc import seq

assert seq((5, 3, 0, 9)).to_list() == [5, 3, 0, 9]
```

### `.to_str()`

Get the value of the sequence as a string.

```python
from snakefunc import seq

assert seq([8, 6, 7, 5, 3, 0, 9]).to_str() == "8675309"
```

Optionally, joined together with a separator.

```python
from snakefunc import seq

assert seq([85, 5, 14]).to_str(separator=".") == "85.5.14"
```

### `.to_tuple()`

Get the value of the sequence as a tuple.

```python
from snakefunc import seq

assert seq([1, 2, 3]).to_tuple() == (1, 2, 3)
```

### `.unique()`

Find the unique items in the sequence.

```python
from snakefunc import seq

assert seq((1, 2, 2, 3, 4, 4, 5)).unique().value() == (1, 3, 5)
```

### `.value()`

Get the value of the sequence.

```python
from snakefunc import seq

assert seq("Hi!").value() == "Hi!"
```
