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

### `.all()`

Iterate over the items in the sequence and return a `bool` indicating if all the items match the callback predicate.

```python
from snakefunc import seq

assert seq([2, 4, 6, 8, 10]).all(lambda number: number % 2 == 0) is True
```

### `.any()`

Iterate over the items in the sequence and return a `bool` indicating if any item matches the callback predicate.

```python
from snakefunc import seq

assert seq(("foo", "bar", "baz")).any(lambda item: item == "foo") is True
```

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

### `.filter()`

Iterate over the sequence and retain the items for which the predicate callback returns `True`.

```python
from snakefunc import seq

assert seq([1, 2, 3, 4, 5, 6]).filter(lambda number: number % 2 == 0).value() == [2, 4, 6]
```

### `.find()`

Iterate over the sequence and return the first item for which the predicate callback returns `True`. Returns `None` if nothing is found.

```python
from snakefunc import seq

assert seq([0, 1, 2, 3, 4, 5, 6]).find(lambda number: number % 2 == 0).value() == 2
```

### `.first()`

Returns the first item in the sequence, or `None` if the sequence is empty.

```python
from snakefunc import seq

assert seq([1, 2, 3, 4, 5]).first() == 1
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

### `.join_into_str()`

Get the value of the sequence joined into a string. Optionally, joined together with a separator.

```python
from snakefunc import seq

assert seq(["H", "e", "l", "l", "o", "!"]).join_into_str() == "Hello!"
```

Optionally, joined together with a separator.

```python
from snakefunc import seq

assert seq(("foo", "bar", "baz")).join_into_str(separator=", ") == "foo, bar, baz"
```

### `.last()`

Returns the last item in the sequence, or `None` if the sequence is empty.

```python
from snakefunc import seq

assert seq([1, 2, 3, 4, 5]).last() == 5
```

### `.len()`

Returns the length of the sequence.

```python
from snakefunc import seq

assert seq([1, 2, 3, 4, 5]).len() == 5
```

### `.map()`

Create a new sequence populated by the results of the callback applied to each item in the current sequence.

```python
from snakefunc import seq

assert seq([1, 2, 3]).map(lambda number: number * 2).value() == [2, 4, 6]
```

### `.reduce()`

Returns the result of the sequence being reduced to a singular value.

```python
from snakefunc import seq

assert seq([1, 2, 3]).reduce(lambda accumulator, value: accumulator + value) == 6
```

An optional `initial_value` argument can be provided to seed the accumulator.

```python
from snakefunc import seq

assert seq([1, 2, 3]).reduce(lambda accumulator, value: accumulator + value, 5) == 11
```

The callback may also optionally include `index` and `sequence` arguments.

```python
from snakefunc import seq

assert seq([1, 2, 3]).reduce(lambda accumulator, value, index, sequence: accumulator + value + index + len(sequence)) == 18
```

### `.to_bytes()`

Returns the sequence as bytes.

```python
from snakefunc import seq

assert seq(["h", "e", "l", "l", "o", "!"]).to_bytes() == b"hello!"
```

### `.to_json()`

Get the value of the sequence as a JSON string.

```python
from snakefunc import seq

assert seq([{"foo": "bar"}, {"baz": "blue"}]).to_json() == '[{"foo": "bar"}, {"baz": "blue"}]'
```

Sequences which are of type `bytearray` or `range` are represented as arrays.

```python
from snakefunc import seq

assert seq(range(5)).to_json() == "[0, 1, 2, 3, 4]"
```

Lastly, `byte` sequences are represented as strings.

```python
from snakefunc import seq

assert seq(b"Hi!").to_json() == "\"b'Hi!'\""
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

assert seq([1, 2, 3]).to_str() == "[1, 2, 3]"
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
