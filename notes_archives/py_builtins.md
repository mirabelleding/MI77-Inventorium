# Python Built-ins & Standard Library

Scope: Python 3.11+ unless a feature is marked with a higher minimum version. Level: Foundations → intermediate → advanced. Purpose: A practical reference for everyday Python, data processing, automation, package development, testing, and performance-conscious programming.

> **Built-in vs standard library:** `len(items)` is a built-in and needs no import. `itertools.chain(...)` belongs to a standard-library module and needs an import. Neither requires `pip install`.

**Code conventions:** Examples deliberately prefer small, inspectable expressions. A generator expression often reads better than a long chain of higher-order functions; a loop is preferable when mutations or side effects are the main goal.

## Table of Contents

**Part I — Built-in functions**

1. [Choosing tools, iterables and iterators](#1-choosing-tools-iterables-and-iterators)
2. [Iteration and sequence built-ins](#2-iteration-and-sequence-built-ins)
3. [Aggregation, sorting and truth tests](#3-aggregation-sorting-and-truth-tests)
4. [Conversion, representation and formatting](#4-conversion-representation-and-formatting)
5. [Numerical built-ins](#5-numerical-built-ins)
6. [Containers and binary views](#6-containers-and-binary-views)
7. [Object introspection and attributes](#7-object-introspection-and-attributes)
8. [Execution, namespaces and I/O](#8-execution-namespaces-and-io)

**Part II — Standard-library modules**

9. [`itertools`](#9-itertools)
10. [`functools`](#10-functools)
11. [`operator`](#11-operator)
12. [`collections` and `collections.abc`](#12-collections-and-collectionsabc)
13. [`heapq`, `bisect`, `array`](#13-heapq-bisect-array)
14. [`dataclasses`, `enum`, `typing`, `abc`](#14-dataclasses-enum-typing-abc)
15. [`pathlib`, `os`, `glob`, `shutil`, `tempfile`](#15-pathlib-os-glob-shutil-tempfile)
16. [`re`](#16-re)
17. [`json`, `csv`, `tomllib`](#17-json-csv-tomllib)
18. [`datetime`, `zoneinfo`, `time`](#18-datetime-zoneinfo-time)
19. [`math`, `statistics`, `decimal`, `fractions`](#19-math-statistics-decimal-fractions)
20. [`random`, `secrets`, `hashlib`, `hmac`, `uuid`](#20-random-secrets-hashlib-hmac-uuid)
21. [`contextlib`, `io`, `copy`](#21-contextlib-io-copy)
22. [`logging`, `warnings`, `argparse`](#22-logging-warnings-argparse)
23. [`sys`, `importlib`, `subprocess`](#23-sys-importlib-subprocess)
24. [Concurrency](#24-concurrency)
25. [`sqlite3`](#25-sqlite3)
26. [Inspection, debugging, profiling and tests](#26-inspection-debugging-profiling-and-tests)
27. [Other useful modules](#27-other-useful-modules)

**Part III — Application**

28. [Practical recipes](#28-practical-recipes)
29. [Pitfalls and decision guides](#29-pitfalls-and-decision-guides)
30. [Quick-reference index](#30-quick-reference-index)

---

# Part I — Built-in functions

## 1. Choosing tools, iterables and iterators

Begin with the problem you are solving. Do you want to **transform values**, **traverse them once**, **create a concrete collection**, or **inspect objects**? The answer determines which abstraction is most appropriate.

| Goal | First choice | Key distinction |
|---|---|---|
| Produce new values | comprehension or `map` | a list is eager; a generator expression is lazy |
| Select values | comprehension or `filter` | filtering may consume a one-pass source |
| Combine iterables | `zip` or `itertools.chain` | zip aligns; chain concatenates |
| Group records | `itertools.groupby` / `defaultdict` / pandas | consecutive vs key-based grouping |
| Check a condition | `any`, `all` | both short-circuit |
| Deduplicate | `set` / `dict.fromkeys` | order guarantees differ |
| Compare objects | `is`, `==`, `isinstance` | identity, equality, type relationship |
| Inspect an object | `type`, `vars`, `dir`, `inspect` | different questions about the object |

### Iterable, iterator, generator, sequence

An **iterable** supplies an iterator through `iter()`. An **iterator** remembers progress and supplies one next value through `next()`. A **generator** is an iterator created by a generator expression or a function containing `yield`. A **sequence** is an indexable, sized collection such as a list or tuple.

Many iterables can be traversed again; a particular iterator usually cannot restart.

**Example**

```python
values = [10, 20, 30]
stream = iter(values)
print(next(stream))
print(next(stream))
print(list(stream))
print(list(stream))
print(list(values))
```

**Output**

```text
10
20
[30]
[]
[10, 20, 30]
```

`list(stream)` does not rewind the iterator. Calling `iter(stream)` normally returns the same iterator, while `iter(values)` creates a *new* iterator over the list.

**Mental model:** An iterator is not a box containing the entire result. It is a stateful object that knows how to provide the next item.

### Lazy evaluation vs eager materialization

`[expression for item in source]` constructs a list immediately; `(expression for item in source)` creates a generator expression whose expressions are evaluated as values are requested.

**Example**

```python
eager = [n * n for n in range(4)]
lazy = (n * n for n in range(4))
print(eager)
print(next(lazy))
print(list(lazy))
```

**Output**

```text
[0, 1, 4, 9]
0
[1, 4, 9]
```

Laziness can reduce peak memory and allow early stopping. It does **not** necessarily mean constant memory: sorting, `tee()`, `cycle()`, and several combinatoric iterators may buffer values. Also, *when* exceptions and side effects occur changes: deferred operations happen when the iterator is advanced.

### Identity, binding, and mutation when iterating

Iteration yields references to objects, not automatic deep copies. When values are mutable, changing them through one reference may be visible through another.

**Example**

```python
record = {"amount": 10}
items = [record]
for item in items:
    item["amount"] += 5
print(items)
print(item is record)
```

**Output**

```text
[{'amount': 15}]
True
```

Rebinding a loop variable (`item = {...}`) changes the local name, not the list element. Mutating the referenced dictionary (`item["amount"] = ...`) changes the shared object. This follows Python's general name-binding rules.

## 2. Iteration and sequence built-ins

These built-ins are used to traverse, align, count, slice, and transform iterables. The return type matters: several return *iterators* rather than lists.

### `len(obj)`

Returns an object's number of elements using its length protocol (`__len__`). For standard lists, tuples, dictionaries, and strings, this is ordinarily an `O(1)` operation. A general generator has no known length.

**Example**

```python
print(len([10, 20, 30]))
print(len({"a": 1, "b": 2}))
print(len("Python"))
```

**Output**

```text
3
2
6
```

Do not call `len()` on a generator expecting it to count items. `sum(1 for _ in generator)` counts them by exhausting the generator, which can be expensive or impossible for an infinite source.

### `enumerate(iterable, start=0)`

Adds an incrementing index to successive values and yields `(index, value)` pairs. It is better than manually maintaining a counter.

**Example**

```python
names = ["Alice", "Bob", "Cara"]
print(list(enumerate(names, start=1)))
for position, name in enumerate(names, 1):
    print(position, name)
```

**Output**

```text
[(1, 'Alice'), (2, 'Bob'), (3, 'Cara')]
1 Alice
2 Bob
3 Cara
```

`enumerate()` itself returns an iterator. Choose it when the index is *metadata* for a stream; don't use it just to access list items by index.

### `zip(*iterables, strict=False)`

Aligns elements **positionally**: first with first, second with second, etc. By default it stops at the shortest input. `strict=True` (Python 3.10+) raises an error if one iterable runs out before another.

**Example**

```python
names = ["A", "B", "C"]
amounts = [10, 20, 30]
print(list(zip(names, amounts, strict=True)))
print(dict(zip(names, amounts, strict=True)))
print(list(zip([1, 2, 3], ["x", "y"])))
```

**Output**

```text
[('A', 10), ('B', 20), ('C', 30)]
{'A': 10, 'B': 20, 'C': 30}
[(1, 'x'), (2, 'y')]
```

`zip()` does not join records by a key. If mismatched lengths are a programming error, make `strict=True` the default. For padding instead of truncation, see `itertools.zip_longest()`.

### Unpacking with `zip(*pairs)`

The `*` operator unpacks an iterable of argument tuples into separate arguments for `zip`, effectively transposing rows into columns.

**Example**

```python
pairs = [("a", 1), ("b", 2), ("c", 3)]
letters, numbers = zip(*pairs)
print(letters)
print(numbers)
```

**Output**

```text
('a', 'b', 'c')
(1, 2, 3)
```

This fails if `pairs` is empty and you attempt to unpack two outputs. It is the same positional argument-unpacking principle used by `SomeClass(*(f(x) for x in xs))`.

### `map(function, *iterables)`

Applies a function lazily to successive elements. A function receiving two arguments can be mapped over two aligned iterables. `map` returns an iterator and stops when its shortest input ends.

**Example**

```python
print(list(map(int, ["12", "7", "31"])))
print(list(map(pow, [2, 3, 4], [3, 2, 2])))
```

**Output**

```text
[12, 7, 31]
[8, 9, 16]
```

Compare `[int(x) for x in strings]` with `map(int, strings)`. `map` is compact when a named function already expresses the operation; a comprehension is often clearer for multi-step logic.

### `filter(function, iterable)`

Keeps elements whose predicate is truthy, lazily. With `function=None`, it removes **all falsy values**, not merely missing values.

**Example**

```python
values = [0, 3, None, 5, "", 8]
print(list(filter(None, values)))
print(list(filter(lambda n: n % 2 == 0, range(1, 9))))
```

**Output**

```text
[3, 5, 8]
[2, 4, 6, 8]
```

Because `0` and `False` are falsy, `filter(None, ...)` is inappropriate when zeros are meaningful data. A comprehension such as `[x for x in xs if x is not None]` makes that intent explicit.

### `iter(obj)` and `iter(callable, sentinel)`

The one-argument form obtains an iterator. The two-argument form repeatedly calls a **zero-argument callable** until its return value equals the sentinel; the sentinel is not yielded.

**Example**

```python
from functools import partial
from io import BytesIO

source = BytesIO(b"abcdefghij")
chunks = list(iter(partial(source.read, 4), b""))
print(chunks)
```

**Output**

```text
[b'abcd', b'efgh', b'ij']
```

This pattern is useful for reading fixed-size binary chunks until EOF, but remember that a function which never returns the sentinel creates an unbounded iterator.

### `next(iterator, default)`

Requests the next element. Without a default, exhaustion raises `StopIteration`. With a default, exhaustion returns that value.

**Example**

```python
values = iter([10, 20])
print(next(values))
print(next(values))
print(next(values, None))
records = [{"id": 1, "ok": False}, {"id": 2, "ok": True}]
print(next((row for row in records if row["ok"]), None))
```

**Output**

```text
10
20
None
{'id': 2, 'ok': True}
```

`next((x for x in values if condition(x)), None)` is an elegant way to find the first match without building a list. If `None` is also a valid result, use a unique sentinel: `MISSING = object()`.

### `range(start, stop, step)`

Represents an integer arithmetic progression without storing all integers. The stop is **exclusive**. It is a reusable immutable sequence, not an iterator.

**Example**

```python
numbers = range(2, 11, 3)
print(list(numbers))
print(numbers[1])
print(8 in numbers)
print(list(range(8, 0, -3)))
```

**Output**

```text
[2, 5, 8]
5
True
[8, 5, 2]
```

`range()` supports length, indexing and efficient integer membership tests. `itertools.count()` is different: it can continue indefinitely and it can use non-integer steps.

### `reversed(sequence)`

Creates a reverse iterator over an object implementing the reverse protocol (or a suitable sequence protocol). It does not construct a reversed list.

**Example**

```python
values = [1, 2, 3]
reverse_stream = reversed(values)
print(next(reverse_stream))
print(list(reverse_stream))
print(values)
```

**Output**

```text
3
[2, 1]
[1, 2, 3]
```

For a one-shot generator, `reversed(generator)` generally cannot work directly: reverse order requires access to prior values. Materializing a finite generator first may be necessary.

### `slice(start, stop, step)`

A `slice` object stores a reusable selection rule. It is the object underlying `values[start:stop:step]`.

**Example**

```python
every_other = slice(None, None, 2)
print([10, 20, 30, 40, 50][every_other])
print("abcdef"[every_other])
print(slice(2, 100).indices(8))
```

**Output**

```text
[10, 30, 50]
ace
(2, 8, 1)
```

A slice describes *what indices to take*, not the values themselves. Use `itertools.islice()` for iterators, since normal slicing requires an indexable collection.

### `aiter()` and `anext()`  ·  Python 3.10+

Asynchronous analogues of `iter()` and `next()` (Python 3.10+). An async iterator delivers elements with `await anext(iterator)` and works with `async for`.

**Example**

```python
import asyncio

async def produce():
    for x in (10, 20):
        yield x

async def main():
    stream = aiter(produce())
    print(await anext(stream))
    print(await anext(stream))
    print(await anext(stream, "done"))

asyncio.run(main())
```

**Output**

```text
10
20
done
```

`aiter()` itself is not awaitable. Async iteration is about waiting for asynchronous values, not automatically parallelizing CPU-bound computation.

## 3. Aggregation, sorting and truth tests

These functions usually consume their inputs. Pay attention to defaults for empty inputs, tie breaking, short-circuiting, and whether operations mutate their source.

### `sum(iterable, start=0)`

Adds values and includes an optional initial value. It is intended primarily for numbers, not for repeatedly concatenating lists.

**Example**

```python
values = [10, 15, -3]
print(sum(values))
print(sum(values, 100))
print(sum(x * x for x in range(4)))
```

**Output**

```text
22
122
14
```

Use `math.fsum` for accuracy-sensitive floating-point accumulation. To flatten lists, prefer `chain.from_iterable`; `sum(lists, [])` repeatedly copies lists and performs poorly.

### `min()` and `max()` with `key` and `default`

Find the smallest or largest item according to a key function. The *original item* is returned, not the key value. `default` is allowed only for the single-iterable call.

**Example**

```python
rows = [{"id": "A", "exposure": 120}, {"id": "B", "exposure": 350}]
print(max(rows, key=lambda row: row["exposure"]))
print(min(rows, key=lambda row: row["exposure"]))
print(max([], default=None))
```

**Output**

```text
{'id': 'B', 'exposure': 350}
{'id': 'A', 'exposure': 120}
None
```

In a tie, the first encountered maximum/minimum is returned. `max(a, b, default=...)` is invalid because `default` is defined for `max(iterable, ...)`, not the multi-positional form.

### `sorted()` vs `list.sort()`

`sorted(iterable)` makes a **new list**. `some_list.sort()` sorts that same list **in place** and returns `None`. Both support `key` and `reverse` and are stable.

**Example**

```python
values = [3, 1, 2]
new = sorted(values)
returned = values.sort()
print(new)
print(values)
print(returned)
rows = [("B", 2), ("A", 3), ("B", 1)]
print(sorted(rows, key=lambda row: (row[0], row[1])))
```

**Output**

```text
[1, 2, 3]
[1, 2, 3]
None
[('A', 3), ('B', 1), ('B', 2)]
```

*Stable* means that elements with equal sort keys retain their relative input order. This supports multi-stage sorting and predictable data transformations.

### `all()` and `any()`

`all()` checks whether every value is truthy; `any()` checks whether at least one is truthy. Both evaluate lazily and **short-circuit**: `all` stops at the first falsy value; `any` stops at the first truthy value.

**Example**

```python
statuses = ["complete", "complete", "pending"]
print(all(s == "complete" for s in statuses))
print(any(s == "pending" for s in statuses))
print(all([]))
print(any([]))
```

**Output**

```text
False
True
True
False
```

`all([]) == True` (vacuous truth) and `any([]) == False`. In validation, check for nonempty inputs separately if zero records should not count as success.

### `abs()` and `round()`

`abs()` returns magnitude; for complex numbers it returns the Euclidean magnitude. `round()` rounds numeric values, using *ties to even* for exact half ties on standard floats.

**Example**

```python
print(abs(-13))
print(abs(3 + 4j))
print(round(2.5))
print(round(3.5))
print(round(12.345, 2))
```

**Output**

```text
13
5.0
2
4
12.35
```

Binary floating-point approximations can make some decimal-looking ties surprising. For financial rules requiring a specific decimal rounding policy, use `decimal.Decimal` with explicit rounding rules.

## 4. Conversion, representation and formatting

Conversions control the **type** of a value, representations control **how it appears**, and serialization controls **how it is stored or exchanged**. These are distinct concerns.

### `int`, `float`, `complex`, `bool`

`int()` can parse numbers in different bases; `float()` creates floating-point values; `complex()` represents real and imaginary components. `bool()` applies truth-value testing—it does not parse English words as booleans.

**Example**

```python
print(int("1010", 2))
print(int("ff", 16))
print(float("3.5"))
print(complex(2, -3))
print(bool("False"))
print(bool([]))
```

**Output**

```text
10
255
3.5
(2-3j)
True
False
```

`bool("False")` is `True` because the string is nonempty. For text input, compare normalized strings against an explicit accepted set.

### `str()` vs `repr()` vs `ascii()`

`str()` aims for a readable representation; `repr()` typically aims for a debugging-oriented representation; `ascii()` is `repr()` with non-ASCII characters escaped.

**Example**

```python
value = "café"
print(str(value))
print(repr(value))
print(ascii(value))
```

**Output**

```text
café
'café'
'caf\xe9'
```

Implementing `__repr__` makes custom objects more inspectable in logs and interactive sessions. However, `repr()` is **not** a safe or stable serialization format.

### `format()` and f-string specifications

Formatting changes display without changing the underlying numeric value. The *format mini-language* controls precision, alignment, separators, bases and more.

**Example**

```python
amount = 1234567.891
ratio = 0.1842
print(format(amount, ",.2f"))
print(f"{ratio:.1%}")
print(f"{42:08d}")
print(f"{255:#x}")
print(f"{'A':^7}")
```

**Output**

```text
1,234,567.89
18.4%
00000042
0xff
   A
```

Common specs: `.2f` fixed decimal places; `.3g` significant digits; `,.0f` thousands separator; `.1%` multiply by 100 and append `%`; `<`, `>`, `^` alignment; `08d` zero-padded integer; `#x` prefixed hexadecimal. Use `!r` inside an f-string to show `repr(value)`.

### `ord()` and `chr()`

`ord()` converts a single Unicode code point into its integer value; `chr()` maps a code point to a character.

**Example**

```python
print(ord("A"))
print(chr(65))
print(chr(9731))
```

**Output**

```text
65
A
☃
```

One *visible* character can contain multiple Unicode code points, such as a base letter plus a combining accent. These functions operate on code points rather than visual grapheme clusters.

### `bin()`, `oct()`, `hex()`

Return string representations of integers in bases 2, 8 and 16, typically with the prefixes `0b`, `0o`, and `0x`.

**Example**

```python
print(bin(255))
print(oct(255))
print(hex(255))
print(f"{5:08b}")
```

**Output**

```text
0b11111111
0o377
0xff
00000101
```

The result is a string, not a changed integer representation in memory. `int("ff", 16)` performs the reverse parsing operation.

### Encoding: `str` vs `bytes` vs `bytearray`

Text strings contain Unicode characters; bytes contain raw byte values. Encoding converts text to bytes and decoding converts bytes to text. `bytes` is immutable, but `bytearray` is mutable.

**Example**

```python
text = "résumé"
encoded = text.encode("utf-8")
print(encoded)
print(encoded.decode("utf-8"))
raw = bytearray(b"ABC")
raw[0] = 90
print(raw)
```

**Output**

```text
b'r\xc3\xa9sum\xc3\xa9'
résumé
bytearray(b'ZBC')
```

Encoding/decoding belongs at text/binary boundaries: files, protocols and network streams. An integer passed to `bytes(n)` creates *n zero bytes*; it does not encode the decimal digits of `n`.

## 5. Numerical built-ins

Some small built-ins express useful numerical operations more directly than their expanded arithmetic forms.

### `divmod(a, b)`

Returns `(a // b, a % b)` together: the quotient and remainder. This is useful for partitioning durations, pages, or units.

**Example**

```python
hours, minutes = divmod(137, 60)
print(hours, minutes)
print(divmod(-7, 3))
```

**Output**

```text
2 17
(-3, 2)
```

Python integer floor division rounds toward negative infinity, so `divmod(-7, 3)` yields `(-3, 2)`, preserving the identity `a = q * b + r`.

### `pow(base, exp, mod=None)`

With two arguments, `pow` performs exponentiation. With three integer arguments, it computes modular exponentiation efficiently without allocating the full enormous intermediate power.

**Example**

```python
print(pow(2, 10))
print(pow(7, 128, 13))
print(7 ** 128 % 13)
```

**Output**

```text
1024
3
3
```

`pow(a, -1, modulus)` can compute modular inverses when they exist. This is useful in number theory and cryptographic algorithms, not a substitute for a cryptography library.

### `hash(obj)` and hashability

A hash supports dictionary-key lookup and set membership. Hashable objects must have a stable hash value over their lifetime and equality-compatible hashing behavior.

**Example**

```python
key = ("CA", 2026, 10)
print({key: "ready"}[key])
print(hash((1, 2)) == hash((1, 2)))
try:
    hash((1, [2]))
except TypeError as exc:
    print(type(exc).__name__)
```

**Output**

```text
ready
True
TypeError
```

Lists and dictionaries are unhashable, and a tuple becomes unhashable if it contains an unhashable element. `hash()` is **not** cryptographic and may differ across processes for strings and other salted types. Do not serialize it as a persistent identifier.

### `sum()` vs `math.fsum()` vs `statistics.mean()`

These answer different questions: ordinary accumulation, high-accuracy floating-point summation, and arithmetic mean.

**Example**

```python
from math import fsum
from statistics import mean
values = [0.1] * 3
print(sum(values))
print(fsum(values))
print(mean(values))
```

**Output**

```text
0.30000000000000004
0.30000000000000004
0.1
```

For monetary *exact decimal* logic, consider `Decimal` rather than assuming all floating-point rounding errors can be repaired by `fsum`.

## 6. Containers and binary views

Choosing a container entails ordering, identity, uniqueness, mutability, hashability and memory considerations.

### `list`, `tuple`, `dict`, `set`, `frozenset`

`list` is ordered and mutable; `tuple` is ordered and immutable; `dict` maps unique hashable keys to values and preserves insertion order; `set` stores unique hashable elements with no guaranteed ordering; `frozenset` is immutable and hashable if its elements are hashable.

**Example**

```python
values = ["a", "b", "a"]
print(list(values))
print(tuple(values))
print(dict.fromkeys(values))
print(sorted(set(values)))
print(sorted(frozenset(values)))
```

**Output**

```text
['a', 'b', 'a']
('a', 'b', 'a')
{'a': None, 'b': None}
['a', 'b']
['a', 'b']
```

A tuple's **immutability** does not make nested mutable objects immutable. `([1, 2],)` cannot be used as a dictionary key, and mutation of the nested list is still possible. Use `dict.fromkeys(iterable)` for *order-preserving deduplication* of hashable keys.

### `dict.fromkeys()` and ordered deduplication

`dict.fromkeys` constructs a dictionary with keys from an iterable in first-occurrence order. Converting the dictionary back to a list is a compact way to retain unique values in their original order.

**Example**

```python
items = ["x", "y", "x", "z", "y"]
print(list(dict.fromkeys(items)))
print(dict.fromkeys(["A", "B"], 0))
```

**Output**

```text
['x', 'y', 'z']
{'A': 0, 'B': 0}
```

Caution: if you provide one mutable default value, **all keys reference the same object**. Use a comprehension if separate lists/dictionaries are needed for each key.

### `memoryview()`

Creates a view of a binary buffer, allowing slices to share underlying memory rather than necessarily copying bytes. Writable views of writable buffers can modify the source.

**Example**

```python
buffer = bytearray(b"abcdefgh")
view = memoryview(buffer)
segment = view[2:5]
segment[0] = ord("Z")
print(buffer)
print(bytes(segment))
```

**Output**

```text
bytearray(b'abZdefgh')
b'Zde'
```

A `memoryview` of an immutable `bytes` object is read-only. Buffer exports can also restrict resizing of the underlying `bytearray` while views remain active.

### `object()` as a unique sentinel

A fresh `object()` is often used to distinguish "missing" from the legitimate value `None`. Equality with this unique object is less appropriate than identity (`is`).

**Example**

```python
MISSING = object()
record = {"name": None}
print(record.get("name", MISSING) is MISSING)
print(record.get("age", MISSING) is MISSING)
```

**Output**

```text
False
True
```

Sentinels are useful in APIs where optional arguments or mapping values may themselves legitimately be `None`.

## 7. Object introspection and attributes

These built-ins reveal Python’s object model: types, inheritance, binding, managed attributes, namespaces and the method-resolution order.

### `type`, `isinstance`, `issubclass`

`type(obj)` returns an object's class; `isinstance(obj, SomeClass)` permits subclasses; `issubclass(Sub, Base)` checks relationships between classes (including supported virtual ABCs).

**Example**

```python
class Animal:
    pass

class Dog(Animal):
    pass

pet = Dog()
print(type(pet) is Dog)
print(isinstance(pet, Animal))
print(issubclass(Dog, Animal))
print(isinstance(Dog, type))
```

**Output**

```text
True
True
True
True
```

A Python class such as `Dog` is **itself an object**, normally an instance of the metaclass `type`. This is why `isinstance(Dog, type)` is true. `isinstance("A", type)` is false: a string object is an instance of `str`, not a class object.

### `getattr`, `setattr`, `hasattr`, `delattr`

Access or modify attributes dynamically using their names as strings. `getattr(obj, name, fallback)` returns a default if normal lookup raises `AttributeError`.

**Example**

```python
class Config:
    pass

cfg = Config()
setattr(cfg, "batch_size", 100)
print(getattr(cfg, "batch_size"))
print(getattr(cfg, "timeout", 30))
print(hasattr(cfg, "batch_size"))
delattr(cfg, "batch_size")
print(hasattr(cfg, "batch_size"))
```

**Output**

```text
100
30
True
False
```

Attribute lookup may execute descriptors, properties, `__getattribute__`, and `__getattr__`. `hasattr()` attempts access and catches `AttributeError`; it is not merely a static inspection of `__dict__`.

### `vars`, `dir`, `__dict__`

`vars(obj)` normally returns the object's instance namespace (`__dict__`), while `dir(obj)` supplies a list of suggested attribute names, including inherited and class-level names. Not all objects have a `__dict__` (for instance, many `__slots__` classes).

**Example**

```python
class Model:
    category = "risk"

    def __init__(self, name):
        self.name = name

model = Model("baseline")
print(vars(model))
print("category" in dir(model))
print("name" in vars(model))
```

**Output**

```text
{'name': 'baseline'}
True
True
```

`dir()` is an exploration aid rather than a guarantee that all names are usable; it may consult custom `__dir__` implementations.

### `id`, `is`, `==`

`is` asks whether two references point to **the same object**; `==` invokes an equality comparison. `id(obj)` is an identity token unique among objects that coexist, but not a persistent cross-process ID.

**Example**

```python
a = [1, 2]
b = a
c = [1, 2]
print(a is b)
print(a is c)
print(a == c)
print(b is not c)
```

**Output**

```text
True
False
True
True
```

Use `is None` rather than `== None`. Do not rely on incidental object interning of numbers or strings to decide equality.

### `callable()` and `__call__`

A callable can be invoked using parentheses. Functions and classes are callable, and instances are callable if their class implements `__call__`.

**Example**

```python
class Multiply:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, n):
        return self.factor * n

operation = Multiply(3)
print(callable(operation))
print(operation(7))
```

**Output**

```text
True
21
```

This pattern appears in function objects, callback systems and decorators. `callable(x)` doesn't promise that a call with any particular arguments will succeed.

### `super()` and method resolution order

`super()` delegates method/attribute lookup to the **next class in the MRO** relative to the current class and instance. In multiple inheritance, this may not be the immediately declared parent you expect.

**Example**

```python
class Base:
    def execute(self):
        return ["base"]

class Audited(Base):
    def execute(self):
        return [*super().execute(), "audit"]

print(Audited().execute())
print([cls.__name__ for cls in Audited.__mro__])
```

**Output**

```text
['base', 'audit']
['Audited', 'Base', 'object']
```

`super()` does not simply mean “call my parent.” It is an MRO-aware proxy that enables cooperative multiple inheritance when classes are designed to participate.

### `property`, `classmethod`, `staticmethod`

A property exposes managed access like an attribute; a classmethod receives `cls` and can construct subclasses appropriately; a staticmethod receives neither `self` nor `cls` automatically.

**Example**

```python
class Account:
    def __init__(self, cents):
        self._cents = cents

    @property
    def balance(self):
        return self._cents / 100

    @classmethod
    def from_dollars(cls, dollars):
        return cls(round(dollars * 100))

    @staticmethod
    def valid(value):
        return value >= 0

account = Account.from_dollars(19.99)
print(account.balance)
print(Account.valid(10))
```

**Output**

```text
19.99
True
```

Property access calls descriptor machinery. Class methods are particularly useful for **alternative constructors**. Avoid hiding expensive network or database work behind a property if users expect cheap attribute access.

### `__class__`, MRO and class attributes

Classes own attributes and instances typically own instance attributes. Lookup can find values on the class even when absent from the instance namespace.

**Example**

```python
class Parent:
    category = "parent"

class Child(Parent):
    pass

item = Child()
print(item.__class__.__name__)
print(item.category)
print([x.__name__ for x in Child.mro()])
```

**Output**

```text
Child
parent
['Child', 'Parent', 'object']
```

If you assign `item.category = "custom"`, it typically creates an instance attribute that shadows the class attribute; it doesn't mutate `Parent.category`. Descriptors can modify this normal lookup behavior.

## 8. Execution, namespaces and I/O

This category includes low-level facilities. Many are useful, but some—especially `eval` and `exec`—require careful security judgment.

### `open()` and `with`

`open()` creates a file object. A `with` statement calls the context manager's enter/exit protocol and closes the file on exit, even if an exception occurs.

**Example**

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as d:
    path = Path(d) / "example.txt"
    with open(path, "w", encoding="utf-8") as file:
        file.write("alpha\nbeta\n")
    with open(path, "r", encoding="utf-8") as file:
        print(file.read().splitlines())
```

**Output**

```text
['alpha', 'beta']
```

Modes: `r` read, `w` write/truncate, `a` append, `x` exclusive create, `b` binary, `+` read/write. Use `encoding="utf-8"` for predictable text I/O and `newline=""` when working with the `csv` module.

### `print(*objects, sep, end, file, flush)`

`print()` converts objects to strings and writes them to a stream. `sep` joins arguments; `end` controls the trailing text; `file` chooses the destination.

**Example**

```python
from io import StringIO

buffer = StringIO()
print("A", "B", "C", sep="|", end="!", file=buffer)
print(buffer.getvalue())
```

**Output**

```text
A|B|C!
```

`print()` returns `None`. For production diagnostics, configure `logging` so messages have levels, timestamps and flexible destinations.

### `input()`

Reads one line from standard input and returns a **string**, not an automatically parsed integer or boolean.

**Example**

```python
from io import StringIO
from unittest.mock import patch

with patch("builtins.input", lambda prompt="": "42"):
    entered = input("Enter count: ")
print(type(entered).__name__)
print(int(entered) + 1)
```

**Output**

```text
str
43
```

In ordinary interactive use, `name = input("Name: ")` waits for the user. The example substitutes a fixed response to keep the note non-interactive and reproducible.

### `globals()` and `locals()`

These inspect mappings of names to values in the current namespaces. `globals()` refers to module global bindings, while `locals()` reflects the current local scope.

**Example**

```python
threshold = 10

def inspect_value(n):
    adjusted = n + 2
    return sorted(locals()), adjusted >= threshold

print(inspect_value(9))
print("threshold" in globals())
```

**Output**

```text
(['adjusted', 'n'], True)
True
```

Changing a mapping returned by `locals()` within a function is not a reliable way to rebind fast local variables. Use ordinary assignment, arguments and returns for predictable state changes.

### `compile()`, `eval()` and `exec()`

`compile()` produces a code object; `eval()` evaluates an expression and returns a result; `exec()` executes statements and returns `None`. These are powerful but dangerous with untrusted input.

**Example**

```python
expression = compile("2 * (3 + 4)", "<demo>", "eval")
print(eval(expression))
namespace = {}
print(exec("answer = 2 ** 5", namespace))
print(namespace["answer"])
```

**Output**

```text
14
None
32
```

**Security:** Never use `eval()` or `exec()` on user-supplied or otherwise untrusted text. A restricted globals mapping is not a secure sandbox. Use `ast.literal_eval()` only for trusted-size Python literal data; prefer `json.loads()` for interoperable data.

### `help()`, `breakpoint()`, `__import__()`

`help(obj)` displays built-in documentation; `breakpoint()` invokes the configured debugger (often `pdb`); `__import__()` is part of Python's low-level import machinery.

**Example**

```python
import math
print(callable(help))
print(callable(breakpoint))
print(__import__("math") is math)
```

**Output**

```text
True
True
True
```

For ordinary dynamic imports, `importlib.import_module("package.module")` is clearer than calling `__import__()` directly. Debugger execution is interactive and therefore intentionally not triggered in this example.

### Exceptions, `try/except`, and `raise ... from`

Catch exceptions only when you can handle them meaningfully. `raise NewError(...) from exc` records an explicit causal chain, preserving the original failure.

**Example**

```python
def parse_integer(value):
    try:
        return int(value)
    except ValueError:
        return None

print(parse_integer("42"))
print(parse_integer("unknown"))
```

**Output**

```text
42
None
```

Important exceptions include `TypeError`, `ValueError`, `KeyError`, `IndexError`, `AttributeError`, `OSError`, `FileNotFoundError`, `StopIteration`, `ZeroDivisionError`, and `TimeoutError`. Avoid catching broad `Exception` just to silence failures.

---

# Part II — Standard-library modules

## 9. `itertools`

`itertools` is Python's **iterator algebra**: small tools that can be composed into pipelines. Most return lazy iterators. Think of the distinction between `chain(a, b)` and `a + b`: the former exposes the elements one by one, while the latter materializes a new list.

| Family | Functions | Question answered |
|---|---|---|
| Infinite streams | `count`, `cycle`, `repeat` | What values should appear repeatedly? |
| Concatenate and batch | `chain`, `chain.from_iterable`, `batched` | How should streams be combined or divided? |
| Select | `compress`, `filterfalse`, `islice`, `takewhile`, `dropwhile` | Which values should reach the consumer? |
| Transform | `accumulate`, `starmap`, `pairwise` | How should each value relate to previous values or arguments? |
| Group and replicate | `groupby`, `tee`, `zip_longest` | How to collect runs, branch a stream, or align uneven inputs? |
| Combinatorics | `product`, `permutations`, `combinations`, `combinations_with_replacement` | Which arrangements should be generated? |

**Three rules:** Iterators keep state. Some iterator helpers retain input internally. Operations such as `list(...)` and `tuple(...)` materialize values at the end of a pipeline.

### `chain(*iterables)` — concatenate streams

`chain([1, 2], [3, 4])` iterates through the first iterable and then the next, as if their elements were in one long sequence. It does **not** create a concatenated list until you call `list()` or another materializer.

**Example**

```python
from itertools import chain
result = chain([1, 2, 3], [4, 5, 6])
print(next(result))
print(next(result))
print(list(result))
print(list(result))
```

**Output**

```text
1
2
[3, 4, 5, 6]
[]
```

Compare `[1, 2] + [3, 4]`, which allocates a new list immediately. `chain` works on heterogeneous iterable types: `chain([1], (2,), range(3, 5))`. It preserves each source's order and makes only a one-level concatenation.

### `chain.from_iterable()` — flatten one nesting level

This closely related constructor receives *one iterable of iterables*, rather than several iterable arguments. This is especially useful for generator expressions producing iterables.

**Example**

```python
from itertools import chain
nested = [[1, 2], [], [3, 4], [5]]
print(list(chain.from_iterable(nested)))
print(list(chain.from_iterable(range(n) for n in [2, 3])))
```

**Output**

```text
[1, 2, 3, 4, 5]
[0, 1, 0, 1, 2]
```

`chain(a, b, c)` and `chain.from_iterable([a, b, c])` produce the same flattened stream. Neither recursively descends into arbitrary nesting. The equivalent nested comprehension is `[x for group in groups for x in group]`.

### `count(start=0, step=1)` — unbounded progression

Creates an iterator that continues incrementing forever unless a consumer stops it. It accepts numeric steps beyond just integers.

**Example**

```python
from itertools import count, islice
print(list(islice(count(10, 5), 5)))
print(list(zip(count(1001), ["A", "B", "C"])))
```

**Output**

```text
[10, 15, 20, 25, 30]
[(1001, 'A'), (1002, 'B'), (1003, 'C')]
```

`range(10, 35, 5)` is finite and indexable; `count(10, 5)` has no stop. Always limit infinite iterators with `islice`, `zip` against a finite iterable, or a deliberate break.

### `cycle(iterable)` — replay a sequence repeatedly

Cycles through elements indefinitely: once it reaches the end, it starts at the first item again. Good for round-robin allocation.

**Example**

```python
from itertools import cycle, islice
print(list(islice(cycle("ABC"), 8)))
workers = cycle(["w1", "w2"])
print(list(zip(["job1", "job2", "job3"], workers)))
```

**Output**

```text
['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B']
[('job1', 'w1'), ('job2', 'w2'), ('job3', 'w1')]
```

`cycle` must save values from its input for future loops, so it is not appropriate for cycling an enormous or infinite input stream without regard to memory.

### `repeat(object, times=None)` — repeat one reference

Returns the same object repeatedly. With `times=None`, repetition is unbounded; with an integer count, it is finite. This is especially useful for supplying a constant argument to `map`.

**Example**

```python
from itertools import repeat
print(list(repeat("ready", 3)))
print(list(map(pow, [2, 3, 4], repeat(2))))
value = []
items = list(repeat(value, 2))
items[0].append(7)
print(items)
```

**Output**

```text
['ready', 'ready', 'ready']
[4, 9, 16]
[[7], [7]]
```

`repeat([] , 3)` repeats **one mutable list reference**, not three independent lists. If separate mutable objects are required, use a comprehension such as `[[] for _ in range(3)]`.

### `islice(iterable, stop)` or `(iterable, start, stop, step)`

Performs slice-like selection on any iterable by consuming values in order. Unlike normal slicing, it does not need an indexable sequence.

**Example**

```python
from itertools import count, islice
print(list(islice(count(10, 3), 5)))
print(list(islice(range(20), 2, 12, 3)))
```

**Output**

```text
[10, 13, 16, 19, 22]
[2, 5, 8, 11]
```

`islice` advances the underlying iterator even for values it skips, and it cannot use negative indices or step. It is ideal for previewing the first N results of a generator or limiting an infinite stream.

### `batched(iterable, n, *, strict=False)`  ·  Python 3.12+

Consumes values in groups of up to `n`, yielding a tuple per batch. The last batch may be shorter unless `strict=True` (Python 3.13+). The function itself was introduced in 3.12.

**Example**

```python
from itertools import batched
print(list(batched(range(10), 4)))
print(list(batched("abcdef", 3, strict=True)))
```

**Output**

```text
[(0, 1, 2, 3), (4, 5, 6, 7), (8, 9)]
[('a', 'b', 'c'), ('d', 'e', 'f')]
```

A batch of 1000 records does not require copying an entire enormous source, but each batch is eagerly collected into a tuple. This is useful for batch database inserts, API requests, and file processing.

### `compress(data, selectors)` — boolean-mask filtering

Aligns a data iterable with selectors and yields only elements whose matching selector is truthy. Both sources are consumed positionally.

**Example**

```python
from itertools import compress
names = ["A", "B", "C", "D"]
mask = [True, False, True, False]
print(list(compress(names, mask)))
print(list(compress("ABCDE", [1, 0, 1])))
```

**Output**

```text
['A', 'C']
['A', 'C']
```

The second example stops after three selectors: it does not assume missing selectors are false or pad them. This is roughly `(x for x, keep in zip(data, selectors) if keep)`.

### `filterfalse(predicate, iterable)`

The logical inverse of built-in `filter`: retains values for which the predicate returns a falsy result.

**Example**

```python
from itertools import filterfalse
values = [1, 2, 3, 4, 5, 6]
print(list(filterfalse(lambda x: x % 2 == 0, values)))
print(list(filterfalse(None, [0, 1, "", "ok", None])))
```

**Output**

```text
[1, 3, 5]
[0, '', None]
```

With `predicate=None`, `filterfalse` retains falsy values. Compare `filter(None, iterable)`, which retains truthy values.

### `takewhile(predicate, iterable)`

Yields values only **until the predicate fails for the first time**. It is a prefix selector, not a general filter.

**Example**

```python
from itertools import takewhile
values = [1, 2, 3, 7, 4, 5]
print(list(takewhile(lambda x: x < 5, values)))
```

**Output**

```text
[1, 2, 3]
```

The `4` after `7` is never returned, even though `4 < 5`. Also, the failing element is consumed from the source iterator, because `takewhile` must inspect it to know it should stop.

### `dropwhile(predicate, iterable)`

Discards an initial prefix while the predicate is true. From the **first failure onward**, it yields everything without running the predicate again.

**Example**

```python
from itertools import dropwhile
values = [1, 2, 3, 7, 4, 5]
print(list(dropwhile(lambda x: x < 5, values)))
```

**Output**

```text
[7, 4, 5]
```

`dropwhile` is not the inverse of `filter` over the entire input. Compare: `takewhile(x < 5)` gives `[1, 2, 3]`; `dropwhile(x < 5)` gives `[7, 4, 5]`; `filter(x < 5)` gives `[1, 2, 3, 4]`.

### `accumulate(iterable, func=add, *, initial=...)`

Produces a running result after each input value. Addition is the default, but you can accumulate products, running extrema, custom state, or other associative-looking operations.

**Example**

```python
from itertools import accumulate
from operator import mul
print(list(accumulate([1, 2, 3, 4])))
print(list(accumulate([2, 3, 4], mul)))
print(list(accumulate([3, 1, 7, 2], max)))
print(list(accumulate([10, -5, 20], initial=100)))
```

**Output**

```text
[1, 3, 6, 10]
[2, 6, 24]
[3, 3, 7, 7]
[100, 110, 105, 125]
```

With `initial=100`, the initial value itself is the first output, so an input of length three produces **four** output values. Compare `functools.reduce`, which returns only the final accumulated result.

### `starmap(function, iterable_of_argtuples)`

Applies a function to unpacked argument tuples: conceptually `function(*args)` for each `args` in the input. This is analogous to using positional unpacking `*` in a normal call.

**Example**

```python
from itertools import starmap
arguments = [(2, 3), (4, 2), (5, 3)]
print(list(starmap(pow, arguments)))
print(list(map(pow, [2, 4, 5], [3, 2, 3])))
```

**Output**

```text
[8, 16, 125]
[8, 16, 125]
```

Both examples produce `[8, 16, 125]`. `map(f, iterable_a, iterable_b)` uses **separate** argument sources; `starmap(f, iterable_of_tuples)` receives one source whose elements contain all arguments.

### `pairwise(iterable)` — adjacent pairs  ·  Python 3.10+

Yields overlapping pairs `(previous, current)`. This is a direct way to model transitions and period-over-period changes without indexes.

**Example**

```python
from itertools import pairwise
balances = [100, 120, 115, 140]
print(list(pairwise(balances)))
print([curr - prev for prev, curr in pairwise(balances)])
```

**Output**

```text
[(100, 120), (120, 115), (115, 140)]
[20, -5, 25]
```

An input of `n` values yields `max(n - 1, 0)` pairs. It is appropriate for adjacent values; for nonadjacent date offsets, build explicit date-key relationships rather than assuming contiguous input.

### `groupby(iterable, key=None)` — consecutive runs

Collects **adjacent** values having equal keys. Unlike SQL `GROUP BY` or pandas grouping, nonadjacent equal keys form separate groups unless the input is sorted first.

**Example**

```python
from itertools import groupby
values = ["A", "A", "B", "B", "A"]
print([(key, list(group)) for key, group in groupby(values)])
print([(key, list(group)) for key, group in groupby(sorted(values))])
```

**Output**

```text
[('A', ['A', 'A']), ('B', ['B', 'B']), ('A', ['A'])]
[('A', ['A', 'A', 'A']), ('B', ['B', 'B'])]
```

Each `group` is an iterator that shares the underlying source with the outer `groupby`. Consume the group **before** advancing to the next group, or save it as `tuple(group)` if later access is needed.

### `groupby()` with structured records

For records, supply `key=`. Sorting by that same key first ensures all matching keys form a single group when global aggregation is desired.

**Example**

```python
from itertools import groupby
from operator import itemgetter
records = [("B", 20), ("A", 10), ("B", 30), ("A", 15)]
ordered = sorted(records, key=itemgetter(0))
totals = {name: sum(amount for _, amount in group)
          for name, group in groupby(ordered, key=itemgetter(0))}
print(totals)
```

**Output**

```text
{'A': 25, 'B': 50}
```

`groupby` is especially useful for already sorted streams. If sorting the entire dataset is expensive, a `defaultdict` can group by key without pre-sorting, although it materializes groups or totals.

### `tee(iterable, n=2)` — branch one source

Creates multiple iterators with independent reading positions over a single input. The implementation buffers values consumed by fast branches until slower branches need them.

**Example**

```python
from itertools import tee
source = (n * n for n in range(4))
a, b = tee(source)
print(next(a))
print(list(b))
print(list(a))
```

**Output**

```text
0
[0, 1, 4, 9]
[1, 4, 9]
```

`tee` does not deep-copy mutable values. It can use substantial memory if one branch gets far ahead. Once you have created the copies, avoid independently consuming the original iterator: that can confuse which values remain available to each consumer.

### `zip_longest(*iterables, fillvalue=None)`

Aligns iterables as `zip` does but continues to the **longest** input, filling missing positions with the chosen value.

**Example**

```python
from itertools import zip_longest
print(list(zip([1, 2, 3], ["A", "B"])))
print(list(zip_longest([1, 2, 3], ["A", "B"], fillvalue="-")))
```

**Output**

```text
[(1, 'A'), (2, 'B')]
[(1, 'A'), (2, 'B'), (3, '-')]
```

If you mix finite and infinite inputs, `zip_longest` itself can run forever. Use `islice` or another finite stopping condition. For strict length validation, `zip(..., strict=True)` is preferable to silent padding.

### `product(*iterables, repeat=1)` — Cartesian product

Produces every coordinate from multiple input pools. It corresponds to nested loops and is useful for parameter sweeps or test matrices.

**Example**

```python
from itertools import product
currencies = ["USD", "CAD"]
stages = [1, 2]
print(list(product(currencies, stages)))
print(list(product("AB", repeat=2)))
```

**Output**

```text
[('USD', 1), ('USD', 2), ('CAD', 1), ('CAD', 2)]
[('A', 'A'), ('A', 'B'), ('B', 'A'), ('B', 'B')]
```

`product` caches input pools so that inner dimensions can be replayed. The number of results is the product of pool lengths; for a pool of size `n` repeated `r` times, it is `n ** r`. Avoid creating a huge list if you only need to iterate.

### `permutations(iterable, r=None)` — ordered selections

Produces selections of length `r` where the order matters and positions are not reused. Full-length permutations are used if `r` is omitted.

**Example**

```python
from itertools import permutations
print(list(permutations("ABC", 2)))
```

**Output**

```text
[('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]
```

`("A", "B")` and `("B", "A")` are different permutations. With `n` distinct positions and `r` selected, there are `n! / (n-r)!` results. Repeated *values* in the input can still produce duplicate-looking tuples because positions are distinct.

### `combinations(iterable, r)` — unordered selections

Produces selections without positional repetition where ordering doesn't create a new selection.

**Example**

```python
from itertools import combinations
print(list(combinations("ABC", 2)))
```

**Output**

```text
[('A', 'B'), ('A', 'C'), ('B', 'C')]
```

This yields three results rather than the six from permutations of length two. For `n` positions and `r` selected, there are `n! / (r! * (n-r)!)` results (with `0 <= r <= n`).

### `combinations_with_replacement(iterable, r)`

Produces unordered selections while allowing the same input position to be selected more than once.

**Example**

```python
from itertools import combinations_with_replacement
print(list(combinations_with_replacement("ABC", 2)))
```

**Output**

```text
[('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]
```

The output includes `('A', 'A')`, `('B', 'B')`, etc., but not a separate reversed `('B', 'A')`. If the pool has `n` distinct positions, the count is `C(n+r-1, r)` for nonnegative `r` and `n > 0`.

### Choosing among the four combinatoric functions

| Function | Does order matter? | May repeat a position? | `"ABC"`, `r=2` count |
|---|---|---|---|
| `product("ABC", repeat=2)` | Yes | Yes | 9 |
| `permutations("ABC", 2)` | Yes | No | 6 |
| `combinations("ABC", 2)` | No | No | 3 |
| `combinations_with_replacement("ABC", 2)` | No | Yes | 6 |

The functions store their input pools and generate output tuples as requested. If the output space is exponentially large, laziness does not make enumeration *computationally cheap*.

### Composition recipe: concatenate, transform, limit

```python
from itertools import chain, islice

sources = ([1, 2], [3, 4], [5, 6])
result = tuple(islice((n * 10 for n in chain.from_iterable(sources)), 4))
print(result)
```

**Output**

```text
(10, 20, 30, 40)
```

**Execution order:** `chain.from_iterable` flattens one level → the generator multiplies each selected number → `islice` takes four results → `tuple` materializes exactly those four. Understanding *where consumption occurs* makes iterator pipelines predictable.

## 10. `functools`

`functools` offers memoization, partial application, reduction, decorator metadata, dispatch, and class-based ordering utilities. It is especially useful for designing reusable APIs.

### `lru_cache(maxsize=128)`

A decorator caching calls by their hashable argument values. Repeated calls with the same arguments often return the cached result without repeating the computation.

**Example**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def square(n):
    print("computed", n)
    return n * n

print(square(5))
print(square(5))
print(square.cache_info())
```

**Output**

```text
computed 5
25
25
CacheInfo(hits=1, misses=1, maxsize=128, currsize=1)
```

Choose bounded caches for long-running processes with large or varied key spaces. Cached results can be stale if the function depends on external mutable state; avoid caching side-effectful functions by default. Use `cache_clear()` to invalidate.

### `cache` — unbounded memoization

`@cache` (3.9+) is essentially `@lru_cache(maxsize=None)`. It retains all distinct computed keys until manually cleared or the function becomes unreachable.

**Example**

```python
from functools import cache

@cache
def triangular(n):
    return 0 if n == 0 else n + triangular(n - 1)

print(triangular(5))
print(triangular(5))
```

**Output**

```text
15
15
```

Useful when the domain of argument combinations is finite or small. It is not necessarily a good default for services receiving unbounded inputs.

### `cached_property` — compute once per instance

Converts a method into an attribute-like computation that writes its first calculated value into the instance dictionary.

**Example**

```python
from functools import cached_property

class Dataset:
    def __init__(self, values):
        self.values = values

    @cached_property
    def total(self):
        print("calculating")
        return sum(self.values)

data = Dataset([1, 2, 3])
print(data.total)
print(data.total)
```

**Output**

```text
calculating
6
6
```

Changing `data.values` will not automatically invalidate `data.total`. Use `del data.total` to allow recomputation. Instances generally need a writable `__dict__` (plain slotted classes typically do not).

### `partial(function, *args, **kwargs)`

Creates a new callable with some arguments pre-bound. It does not call the original function immediately.

**Example**

```python
from functools import partial
parse_binary = partial(int, base=2)
print(parse_binary("1010"))
power_of_two = partial(pow, 2)
print(power_of_two(5))
```

**Output**

```text
10
32
```

`partial()` is useful for configuring callbacks, parsers and APIs without writing a forwarding function. Bound positional arguments precede newly supplied positional arguments; keyword values may be overridden in ordinary `partial` calls.

### `partialmethod` — prebind arguments on a method

Like `partial`, but supports descriptor binding so that `self` is bound correctly when called on an instance.

**Example**

```python
from functools import partialmethod

class Sender:
    def send(self, channel, message):
        return f"{channel}: {message}"

    alert = partialmethod(send, "alerts")

print(Sender().alert("failed"))
```

**Output**

```text
alerts: failed
```

This is handy for supplying fixed variants of an instance method while preserving ordinary bound-method behavior.

### `reduce(function, iterable, initial?)`

Repeatedly combines values until one final value remains. Unlike `itertools.accumulate`, it does not yield intermediate states.

**Example**

```python
from functools import reduce
from operator import mul
print(reduce(mul, [2, 3, 4], 1))
print(reduce(lambda a, b: a + b, [1, 2, 3, 4], 0))
```

**Output**

```text
24
10
```

For summation and multiplication, `sum()` and `math.prod()` often communicate the intent more clearly. `reduce` becomes valuable when the accumulation operation is genuinely custom.

### `wraps()` — preserve decorator metadata

Decorators often replace a function with a nested wrapper. `@wraps(original)` copies useful function metadata and creates a `__wrapped__` reference used by inspection tools.

**Example**

```python
from functools import wraps

def uppercase(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        return fn(*args, **kwargs).upper()
    return inner

@uppercase
def greet(name):
    return f"Hello {name}"

print(greet("Ada"))
print(greet.__name__)
print(greet.__wrapped__.__name__)
```

**Output**

```text
HELLO ADA
greet
greet
```

`wraps` helps `inspect.signature`, debugging, documentation, and tooling understand the original callable. It does not magically preserve every semantic detail of the original function.

### `singledispatch()`

Registers different implementations by the runtime type of the **first argument**. This is one-dimensional dispatch, not full multi-argument overload resolution.

**Example**

```python
from functools import singledispatch

@singledispatch
def normalize(value):
    return value

@normalize.register
def _(value: str):
    return value.strip().lower()

@normalize.register
def _(value: list):
    return [normalize(x) for x in value]

print(normalize("  READY  "))
print(normalize([" A ", " B "]))
```

**Output**

```text
ready
['a', 'b']
```

`singledispatchmethod` provides method-oriented dispatch. Registration is keyed by types, with class inheritance considered during matching.

### `total_ordering()`

A class decorator that can generate remaining rich comparison methods from `__eq__` and at least one ordering method, such as `__lt__`.

**Example**

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, number):
        self.number = number

    def __eq__(self, other):
        return isinstance(other, Version) and self.number == other.number

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.number < other.number

print(Version(2) >= Version(1))
print(Version(2) == Version(3))
```

**Output**

```text
True
False
```

This reduces boilerplate but may be slower than hand-written comparison methods. For pure data records, consider `@dataclass(order=True)` instead.

## 11. `operator`

`operator` provides callable versions of Python operators and efficient ways to retrieve items, attributes, and method results. This pairs well with `map`, `sorted`, `groupby` and `reduce`.

### `itemgetter()`

Returns a callable that retrieves items using keys or indexes. With multiple keys, the callable returns a tuple.

**Example**

```python
from operator import itemgetter
records = [{"name": "A", "score": 3}, {"name": "B", "score": 1}]
print(sorted(records, key=itemgetter("score")))
print(list(map(itemgetter("name"), records)))
print(itemgetter(0, 2)([10, 20, 30]))
```

**Output**

```text
[{'name': 'B', 'score': 1}, {'name': 'A', 'score': 3}]
['A', 'B']
(10, 30)
```

`itemgetter("score")` is roughly `lambda row: row["score"]`; `itemgetter(0, 2)` is roughly `lambda row: (row[0], row[2])`.

### `attrgetter()`

Returns a callable that retrieves object attributes. It supports dotted paths and multiple attribute names.

**Example**

```python
from operator import attrgetter
from dataclasses import dataclass

@dataclass
class Position:
    desk: str
    exposure: int

items = [Position("B", 200), Position("A", 100)]
print([x.desk for x in sorted(items, key=attrgetter("desk"))])
print(attrgetter("desk", "exposure")(items[0]))
```

**Output**

```text
['A', 'B']
('B', 200)
```

`attrgetter("address.city")` retrieves nested attributes through successive accesses. Contrast `itemgetter` for indexing/mapping keys, not attributes.

### `methodcaller()`

Creates a callable that invokes a named method on whatever object it receives, using the pre-specified arguments.

**Example**

```python
from operator import methodcaller
print(list(map(methodcaller("strip"), ["  a ", " b  "])))
print(methodcaller("replace", "a", "x")("banana"))
```

**Output**

```text
['a', 'b']
bxnxnx
```

It is roughly `lambda obj: obj.method_name(*args, **kwargs)`, useful for concise transformations when the method name and parameters are constant.

### Arithmetic, comparison and membership as callables

`operator.add`, `sub`, `mul`, `truediv`, `floordiv`, `mod`, `pow`, `eq`, `lt`, `contains`, `getitem`, `and_`, `or_` and others allow operations to be passed as values.

**Example**

```python
from operator import add, mul, truediv, contains, getitem
print(add(2, 3))
print(mul(4, 5))
print(truediv(7, 2))
print(contains([1, 2, 3], 2))
print(getitem({"a": 10}, "a"))
```

**Output**

```text
5
20
3.5
True
10
```

`operator.and_` and `operator.or_` implement *bitwise* operators (`&`, `|`) and do **not** short-circuit like Python keywords `and` and `or`.

## 12. `collections` and `collections.abc`

The `collections` module supplies specialized data structures; `collections.abc` exposes abstract interfaces used to reason about iterability, mutability, indexing and mapping behavior.

### `Counter` — frequency maps

A specialized dictionary mapping elements to occurrence counts. A missing key reads as zero, and `most_common` reports frequent items.

**Example**

```python
from collections import Counter
statuses = ["ok", "failed", "ok", "pending", "ok", "failed"]
counts = Counter(statuses)
print(counts["ok"])
print(counts["missing"])
print(counts.most_common(2))
print(counts.total())
```

**Output**

```text
3
0
[('ok', 3), ('failed', 2)]
6
```

Counters can be added and subtracted in multiset-like arithmetic; counts may become zero or negative through direct updates. `Counter.total()` requires Python 3.10+.

### `defaultdict(factory)` — missing-key construction

Invokes `factory()` when a missing key is accessed using indexing, allowing automatic list, set, int, or custom container creation.

**Example**

```python
from collections import defaultdict
rows = [("East", 10), ("West", 20), ("East", 15)]
groups = defaultdict(list)
for region, value in rows:
    groups[region].append(value)
print(dict(groups))
print(groups.get("missing"))
print("missing" in groups)
```

**Output**

```text
{'East': [10, 15], 'West': [20]}
None
False
```

`groups["missing"]` would create a new list, while `groups.get("missing")` does **not** run the factory. This is a subtle but important source of accidental dictionary mutation.

### `deque` — efficient double-ended queue

A double-ended queue provides approximately constant-time appends and pops at both ends, unlike `list.pop(0)` which shifts all following elements.

**Example**

```python
from collections import deque
queue = deque(["first", "second"])
queue.appendleft("urgent")
queue.append("third")
print(queue.popleft())
print(queue.pop())
recent = deque(maxlen=3)
recent.extend([1, 2, 3, 4, 5])
print(list(recent))
```

**Output**

```text
urgent
third
[3, 4, 5]
```

`deque(maxlen=N)` automatically discards older elements as new ones enter. It is useful for moving windows, queues, and breadth-first traversal.

### `namedtuple()`

Creates a tuple subclass with named fields. It preserves tuple behavior (position-based access, unpacking, immutability) while making values self-describing.

**Example**

```python
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)
print(p.x)
print(p[1])
print(p._asdict())
print(p._replace(x=99))
```

**Output**

```text
10
20
{'x': 10, 'y': 20}
Point(x=99, y=20)
```

For type-annotated declarations, `typing.NamedTuple` is convenient. For richer mutable or frozen objects with defaults and derived behavior, `dataclasses.dataclass` is often preferable.

### `ChainMap` — layered mapping lookup

Provides a view over multiple mappings. Lookups search from first to last; updates usually target the **first** mapping.

**Example**

```python
from collections import ChainMap
defaults = {"timeout": 30, "retries": 3}
overrides = {"timeout": 10}
config = ChainMap(overrides, defaults)
print(config["timeout"])
print(config["retries"])
config["retries"] = 5
print(overrides)
print(defaults)
```

**Output**

```text
10
3
{'timeout': 10, 'retries': 5}
{'timeout': 30, 'retries': 3}
```

`ChainMap` avoids allocating a merged dictionary and preserves the layers. For a fixed detached snapshot, use a dictionary merge such as `defaults | overrides`.

### `collections.abc` protocols

Interfaces such as `Iterable`, `Iterator`, `Sequence`, `Mapping`, `MutableMapping`, `Set` and `Callable` describe *what operations objects support*.

**Example**

```python
from collections.abc import Iterable, Iterator, Sequence, Mapping
values = [1, 2]
stream = iter(values)
print(isinstance(values, Iterable))
print(isinstance(values, Iterator))
print(isinstance(stream, Iterator))
print(isinstance(values, Sequence))
print(isinstance({"a": 1}, Mapping))
```

**Output**

```text
True
False
True
True
True
```

An iterator is also iterable. A list is iterable but is not itself an iterator. `collections.abc` is useful for runtime interface checks and annotations; `typing.Protocol` offers static structural typing for custom behaviors.

### `OrderedDict`

Ordinary dictionaries already preserve insertion order (a Python language guarantee since 3.7), so `OrderedDict` is primarily useful for operations such as `move_to_end()` and order-sensitive equality between ordered dictionaries.

**Example**

```python
from collections import OrderedDict
values = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
values.move_to_end("a")
print(list(values))
print(OrderedDict([("a", 1), ("b", 2)]) == OrderedDict([("b", 2), ("a", 1)]))
```

**Output**

```text
['b', 'c', 'a']
False
```

Do not choose `OrderedDict` simply because you assume normal `dict` is unordered. Both retain insertion order, but their specialized semantics differ.

## 13. `heapq`, `bisect`, `array`

These provide efficient priority queues, binary-search insertion locations, and compact typed storage. They solve different problems from normal lists.

### `heapq` — maintain smallest-priority item

A heap keeps the **smallest** value accessible at index zero (min-heap). It is not a globally sorted list.

**Example**

```python
import heapq
heap = [8, 2, 7, 1, 5]
heapq.heapify(heap)
heapq.heappush(heap, 3)
print(heapq.heappop(heap))
print(heapq.nsmallest(3, heap))
print(heapq.nlargest(2, heap))
```

**Output**

```text
1
[2, 3, 5]
[8, 7]
```

`heapify` is `O(n)`; `heappush` and `heappop` are `O(log n)`. `nsmallest`/`nlargest` are useful for small top-k selections. Use a `(priority, sequence, value)` tuple to break ties predictably.

### `bisect_left`, `bisect_right`, `insort`

Binary-searches positions in an **already sorted list**. `bisect_left` finds the left insertion position for duplicates; `bisect_right` finds the right one.

**Example**

```python
from bisect import bisect_left, bisect_right, insort
values = [10, 20, 20, 30]
print(bisect_left(values, 20))
print(bisect_right(values, 20))
insort(values, 25)
print(values)
```

**Output**

```text
1
3
[10, 20, 20, 25, 30]
```

Searching takes `O(log n)` comparisons. Inserting into a Python list remains `O(n)` due to shifting elements. These functions use ordering rather than invoking equality as the primary search test.

### `array.array` — typed compact storage

Stores many values of one primitive C-compatible type, with less Python-object overhead than a general-purpose list in some workloads.

**Example**

```python
from array import array
values = array("d", [1.5, 2.5, 3.5])
values.append(4.5)
print(values.tolist())
print(values.itemsize)
```

**Output**

```text
[1.5, 2.5, 3.5, 4.5]
8
```

Type code `"d"` represents a C double (commonly eight bytes). `array` is not a replacement for NumPy's vectorized numerical features; it is an option when only the standard library is available.

## 14. `dataclasses`, `enum`, `typing`, `abc`

These modules help express structured records, finite symbolic choices, static type contracts, and explicit abstract interfaces. Type hints help editors and type checkers; Python usually does not enforce annotations at runtime.

### `@dataclass`

A dataclass generates commonly needed methods based on annotated fields, including `__init__`, `__repr__` and `__eq__`. It is a compact way to declare objects whose primary role is to hold named data.

**Example**

```python
from dataclasses import dataclass, field

@dataclass
class ModelConfig:
    name: str
    horizon: int = 12
    tags: list[str] = field(default_factory=list)

config = ModelConfig("baseline")
config.tags.append("approved")
print(config)
```

**Output**

```text
ModelConfig(name='baseline', horizon=12, tags=['approved'])
```

Why `default_factory=list`? The factory creates a **new list per instance**, avoiding shared mutable defaults. Options include `frozen=True`, `slots=True`, `order=True`, `kw_only=True` and per-field `repr=False`/`compare=False`.

### `__post_init__`, `InitVar`, `replace`

`__post_init__` runs after the generated constructor and can validate or derive values. `InitVar` accepts constructor-only inputs that are not stored as normal fields. `replace` constructs a new instance with selected fields changed.

**Example**

```python
from dataclasses import InitVar, dataclass, field, replace

@dataclass(frozen=True)
class Position:
    units: float
    price: float
    scale: InitVar[float] = 1.0
    value: float = field(init=False)

    def __post_init__(self, scale):
        object.__setattr__(self, "value", self.units * self.price * scale)

position = Position(10, 25, scale=1.2)
print(position)
print(replace(position, units=12))
```

**Output**

```text
Position(units=10, price=25, value=300.0)
Position(units=12, price=25, value=300.0)
```

Because a frozen dataclass blocks ordinary assignment, derived fields may be initialized through `object.__setattr__` in `__post_init__`. `replace()` executes initialization again, so derived values can be recomputed.

### `Enum`, `IntEnum`, `StrEnum`

Enums define a finite set of named members. Regular `Enum` members are distinct symbolic values. `IntEnum` can interact with integer operations; `StrEnum` behaves like a string-valued enum (Python 3.11+).

**Example**

```python
from enum import Enum, StrEnum, auto

class Status(Enum):
    PENDING = 1
    DONE = 2

class Environment(StrEnum):
    DEV = auto()
    PROD = auto()

print(Status.PENDING.name)
print(Status.PENDING.value)
print(Environment.DEV.value)
print(Environment.DEV == "dev")
```

**Output**

```text
PENDING
1
dev
True
```

Use `Enum` when a symbolic choice should not be confused with an arbitrary number or string. `StrEnum` is useful at string boundaries but permits more implicit interchangeability.

### `typing`: collection and callable annotations

Annotations document contracts and enable static analysis. `Iterable[T]` promises traversal; `Iterator[T]` promises `next`; `Sequence[T]` promises indexing and length; `Mapping[K,V]` promises key-based read access.

**Example**

```python
from collections.abc import Callable, Iterable

def transform(values: Iterable[int], fn: Callable[[int], int]) -> list[int]:
    return [fn(value) for value in values]

print(transform([1, 2, 3], lambda x: x * 2))
```

**Output**

```text
[2, 4, 6]
```

Other useful forms: `T | None`, `Literal["a", "b"]`, `TypedDict` for dictionary shapes, `ClassVar`, `Final`, `Annotated`, `TypeVar`, `Self`, and `Protocol`. An annotation alone does **not** reject incompatible values at runtime.

### `TypedDict` and `Literal`

`TypedDict` describes expected keys and value types of a dictionary. `Literal` restricts values for static analysis to explicitly listed options.

**Example**

```python
from typing import Literal, TypedDict

class Record(TypedDict):
    id: int
    balance: float

def classify(value: float, mode: Literal["high", "low"] = "high") -> bool:
    return value > 100 if mode == "high" else value < 100

record: Record = {"id": 1, "balance": 120.0}
print(classify(record["balance"]))
```

**Output**

```text
True
```

`TypedDict` does not automatically instantiate a validating runtime class: `record` remains a regular dictionary. Check types explicitly or use an appropriate runtime validation library if needed.

### `Protocol` — structural typing

A protocol describes the operations an object must support, without requiring the object to inherit from the protocol.

**Example**

```python
from typing import Protocol

class Executable(Protocol):
    def execute(self) -> int: ...

class Task:
    def execute(self) -> int:
        return 7

def run(task: Executable) -> int:
    return task.execute()

print(run(Task()))
```

**Output**

```text
7
```

Static type checkers recognize `Task` as compatible because it has the required method. `@runtime_checkable` enables limited `isinstance` checks of runtime presence, not a thorough verification of parameter and return types.

### `TypeVar`, generics and `Self`

Type variables express relationships between inputs and outputs rather than merely saying both are `object`. `Self` represents the current class and supports subclass-aware return annotations.

**Example**

```python
from typing import Self, TypeVar

T = TypeVar("T")

def first_or(items: list[T], default: T) -> T:
    return items[0] if items else default

class Builder:
    def __init__(self):
        self.values = []

    def add(self, value: str) -> Self:
        self.values.append(value)
        return self

print(first_or([3, 4], 0))
print(Builder().add("A").add("B").values)
```

**Output**

```text
3
['A', 'B']
```

Python 3.12+ introduces a newer generic syntax, such as `def first[T](...)`, but `TypeVar` remains useful in code supporting Python 3.11 and earlier.

### `ABC` and `@abstractmethod`

An abstract base class defines an explicit inheritance-based contract. A subclass must implement abstract methods before it can be instantiated.

**Example**

```python
from abc import ABC, abstractmethod

class Reader(ABC):
    @abstractmethod
    def load(self, source: str) -> bytes: ...

class MemoryReader(Reader):
    def load(self, source: str) -> bytes:
        return source.encode()

print(issubclass(MemoryReader, Reader))
print(MemoryReader().load("abc"))
```

**Output**

```text
True
b'abc'
```

An ABC is appropriate when common inherited behavior or an explicit nominal contract is desirable. A protocol is often better when accepting third-party objects satisfying an interface without requiring inheritance.

## 15. `pathlib`, `os`, `glob`, `shutil`, `tempfile`

File-system operations are usually clearer through `pathlib.Path`, while `os`, `shutil`, `glob` and `tempfile` supply environment, copying, pattern matching and safe temporary workspace features.

### `pathlib.Path` — path objects

A `Path` can be composed with `/`, inspected with `.name`, `.suffix`, `.parent`, and used for reading/writing. Paths are objects, not merely formatted strings.

**Example**

```python
from pathlib import Path
path = Path("reports") / "2026" / "results.csv"
print(path.name)
print(path.stem)
print(path.suffix)
print(path.parent)
print(path.with_suffix(".json"))
```

**Output**

```text
results.csv
results
.csv
reports/2026
reports/2026/results.json
```

`Path.read_text()` and `.write_text()` are convenient for small files; stream large files instead. `Path.resolve()` computes an absolute path, while `Path.exists()` checks the file system.

### Safe creation, reading, and listing

Temporary workspaces allow reproducible file examples without depending on the user's real directory structure.

**Example**

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    root = Path(directory)
    (root / "a.txt").write_text("alpha", encoding="utf-8")
    (root / "b.txt").write_text("beta", encoding="utf-8")
    print(sorted(p.name for p in root.glob("*.txt")))
    print((root / "a.txt").read_text(encoding="utf-8"))
```

**Output**

```text
['a.txt', 'b.txt']
alpha
```

`Path.iterdir()` lists direct children, `Path.glob("*.csv")` matches children, and `Path.rglob("*.csv")` searches recursively. Set explicit encodings when handling text.

### `os.environ` and environment variables

`os.environ` behaves like a mutable mapping of environment variables for the current process and its subsequently launched child processes.

**Example**

```python
import os
os.environ["PY_NOTES_EXAMPLE"] = "ready"
print(os.getenv("PY_NOTES_EXAMPLE"))
print(os.getenv("PY_NOTES_MISSING", "default"))
del os.environ["PY_NOTES_EXAMPLE"]
```

**Output**

```text
ready
default
```

Do not hardcode passwords or tokens in code examples. An environment variable is a configuration mechanism, not an encryption or secret-storage mechanism.

### `glob` filename matching

`glob.glob(pattern)` returns path strings that match a wildcard pattern; `Path.glob()` provides path objects. Pattern matching uses shell-like wildcards, not full regular expressions.

**Example**

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    folder = Path(directory)
    for name in ("a.csv", "b.csv", "notes.md"):
        (folder / name).touch()
    print(sorted(p.name for p in folder.glob("*.csv")))
```

**Output**

```text
['a.csv', 'b.csv']
```

Do not depend on file-system traversal order; sort when deterministic output is important. Use `re` when your matching rules require more expressive patterns.

### `shutil` file and directory operations

`shutil` is a high-level tool for copying, moving and deleting. `copy2()` attempts to preserve more metadata than `copy()`. `copytree()` copies a directory tree.

**Example**

```python
from pathlib import Path
from shutil import copy2
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    folder = Path(directory)
    source = folder / "source.txt"
    source.write_text("hello", encoding="utf-8")
    target = folder / "target.txt"
    copy2(source, target)
    print(target.read_text(encoding="utf-8"))
```

**Output**

```text
hello
```

Operations such as `shutil.rmtree()` are destructive; verify your target before using them on real data. `Path.rename()` and `shutil.move()` also differ across file systems.

### `tempfile` temporary files and directories

Temporary resources avoid hardcoded paths and can be cleaned automatically by context managers. They are ideal for tests and short-lived processing.

**Example**

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    output = Path(directory) / "result.txt"
    output.write_text("ok", encoding="utf-8")
    print(output.exists())
print(output.exists())
```

**Output**

```text
True
False
```

The first result is `True` while inside the context; the second is `False` once the temporary directory has been deleted.

## 16. `re`

The `re` module performs **regular-expression** pattern matching. Use it when plain string methods are insufficient, but prefer `str.startswith`, `str.split`, `str.replace`, etc. when the pattern is simple.

### `search` vs `match` vs `fullmatch`

`search` scans for a match anywhere; `match` attempts a match at the beginning; `fullmatch` requires the entire string to conform.

**Example**

```python
import re
text = "ID: 123"
print(re.search(r"\d+", text).group())
print(re.match(r"\d+", text))
print(bool(re.fullmatch(r"\d+", "123")))
```

**Output**

```text
123
None
True
```

Use `fullmatch` for validating a whole field, `search` for finding a pattern, and `match` for prefix matching. A successful call returns a match object, not simply `True`.

### Capture groups and named groups

Parenthesized groups capture submatches. Named groups (`?P<name>`) make extractions self-documenting and support `.groupdict()`.

**Example**

```python
import re
text = "2026-11-02"
match = re.fullmatch(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", text)
print(match.group(1))
print(match.group("month"))
print(match.groupdict())
```

**Output**

```text
2026
11
{'year': '2026', 'month': '11', 'day': '02'}
```

Use raw strings (`r"..."`) for regex patterns to avoid accidental Python string escape processing. `\d`, `\w`, `\s`, `+`, `*`, `?`, `^`, `$`, `[]`, and `{m,n}` are common regex constructs.

### `findall()` vs `finditer()`

`findall()` collects matches into a list of strings or groups. `finditer()` lazily yields match objects with access to positions and capture metadata.

**Example**

```python
import re
text = "A12 B34 C56"
print(re.findall(r"\d+", text))
print([(m.group(), m.span()) for m in re.finditer(r"\d+", text)])
```

**Output**

```text
['12', '34', '56']
[('12', (1, 3)), ('34', (5, 7)), ('56', (9, 11))]
```

Use `finditer` for potentially large inputs or when positional context matters. Capturing groups can change the structure returned by `findall`.

### `sub()` and `split()`

`re.sub()` replaces matched patterns; `re.split()` splits on a pattern rather than a single literal delimiter.

**Example**

```python
import re
print(re.sub(r"\s+", "_", "a   b	c"))
print(re.split(r"[,;]\s*", "a, b; c"))
```

**Output**

```text
a_b_c
['a', 'b', 'c']
```

A replacement can be a string or a function receiving each match. Beware catastrophic backtracking on adversarial text with badly designed nested quantifiers.

### Regex quick notation

| Construct | Meaning | Example |
|---|---|---|
| `.` | Almost any character | `a.c` |
| `\d` | Digit | `\d{4}` |
| `\w` | Word character | `\w+` |
| `\s` | Whitespace | `\s+` |
| `*`, `+`, `?` | 0+, 1+, optional | `ab+` |
| `{m,n}` | Repetition range | `\d{2,4}` |
| `[abc]` | Character class | `[A-Z]` |
| `(...)` | Capturing group | `(\d+)` |
| `(?:...)` | Noncapturing group | `(?:ab)+` |
| `^`, `$` | Start/end anchors | `^A` |

For repeated use, `pattern = re.compile(r"...")` stores a reusable compiled regex object.

## 17. `json`, `csv`, `tomllib`

These modules handle common text-based data interchange formats. Always distinguish serializing to a **string**, writing to a **file**, and parsing text back into Python objects.

### `json.dumps`, `loads`, `dump`, `load`

`dumps` converts an object to a JSON **string**; `dump` writes JSON into a file. `loads` parses a JSON string; `load` reads and parses a file-like object.

**Example**

```python
import json
record = {"name": "A", "active": True, "balance": 12.5}
encoded = json.dumps(record, sort_keys=True)
print(encoded)
print(json.loads(encoded)["active"])
```

**Output**

```text
{"active": true, "balance": 12.5, "name": "A"}
True
```

JSON supports objects, arrays, strings, numbers, booleans and null. It does not natively represent sets, arbitrary classes, dates, or `Decimal` values without a conversion policy. Never use `eval` to parse JSON.

### Custom JSON serialization

`json.dumps` can accept `default=` for objects it cannot natively encode. Create a deliberate format rather than losing important type information silently.

**Example**

```python
import json
from datetime import date
record = {"date": date(2026, 11, 2)}
encoded = json.dumps(record, default=lambda obj: obj.isoformat())
print(encoded)
```

**Output**

```text
{"date": "2026-11-02"}
```

A stringified date does not automatically become a `date` when reloaded. You must implement the reverse conversion if preserving the original type matters.

### `csv.DictReader` and `DictWriter`

These map CSV columns to dictionary keys. CSV is plain text: values read from fields are generally strings unless you explicitly convert them.

**Example**

```python
import csv
from io import StringIO

source = StringIO("name,score\nAda,10\nBob,20\n")
rows = list(csv.DictReader(source))
print(rows)
output = StringIO()
writer = csv.DictWriter(output, fieldnames=["name", "score"])
writer.writeheader()
writer.writerows(rows)
print(output.getvalue().strip())
```

**Output**

```text
[{'name': 'Ada', 'score': '10'}, {'name': 'Bob', 'score': '20'}]
name,score
Ada,10
Bob,20
```

When opening real files for CSV, use `open(path, newline="", encoding="utf-8")`. For complex quoted fields, prefer the CSV parser over manual `.split(",")`.

### `tomllib` — parse TOML

`tomllib` (3.11+) reads TOML, commonly used in `pyproject.toml`. It supports loading but does not provide a TOML-writing API.

**Example**

```python
import tomllib
text = b'[project]\nname = "demo"\nversion = "0.1.0"\n'
config = tomllib.loads(text.decode())
print(config["project"]["name"])
print(config["project"]["version"])
```

**Output**

```text
demo
0.1.0
```

Use `tomllib.load(binary_file)` to read TOML from an open binary file. JSON is natural for APIs; CSV for rectangular data; TOML for human-edited structured configuration.

## 18. `datetime`, `zoneinfo`, `time`

Time handling has two distinct concerns: **calendar dates/timestamps** and **elapsed durations**. Use `datetime` and time zones for wall-clock values; use monotonic clocks for durations.

### `date`, `datetime`, `time`, `timedelta`

`date` represents a calendar date, `time` a time of day, `datetime` a date and time, and `timedelta` a duration. Their arithmetic behaves according to these distinct roles.

**Example**

```python
from datetime import date, datetime, time, timedelta
print(date(2026, 11, 2) + timedelta(days=7))
print(datetime(2026, 11, 2, 9, 30).date())
print(time(9, 30))
print(timedelta(hours=2, minutes=15))
```

**Output**

```text
2026-11-09
2026-11-02
09:30:00
2:15:00
```

`timedelta` arithmetic is ideal for fixed durations. “Add one calendar month” is not a fixed number of days and needs explicit calendar logic.

### Parsing and formatting dates

`datetime.strptime` parses a string according to a format specification; `.strftime` formats a datetime back into a string. `date.fromisoformat` and `datetime.fromisoformat` handle ISO-style input.

**Example**

```python
from datetime import date, datetime
value = datetime.strptime("2026-11-02 09:30", "%Y-%m-%d %H:%M")
print(value.strftime("%d/%m/%Y"))
print(date.fromisoformat("2026-11-02"))
```

**Output**

```text
02/11/2026
2026-11-02
```

Common tokens: `%Y` four-digit year, `%m` month, `%d` day, `%H` 24-hour, `%M` minute, `%S` second. Parsing errors raise `ValueError`.

### Timezone-aware timestamps with `zoneinfo`

A *naive* datetime has no timezone information. An *aware* datetime uses a `tzinfo` object, enabling meaningful conversion between zones.

**Example**

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
utc = datetime(2026, 11, 2, 15, 0, tzinfo=timezone.utc)
toronto = utc.astimezone(ZoneInfo("America/Toronto"))
print(utc.isoformat())
print(toronto.isoformat())
```

**Output**

```text
2026-11-02T15:00:00+00:00
2026-11-02T10:00:00-05:00
```

Do not add a timezone label to a local naive datetime unless you know that time's interpretation. Timezone rules include daylight-saving transitions and ambiguous/nonexistent local times.

### `time.perf_counter` and `time.monotonic`

Both provide clocks suitable for measuring elapsed time. They are not timestamps to store as wall-clock dates. Subtract readings to calculate durations.

**Example**

```python
import time
start = time.perf_counter()
value = sum(range(1000))
elapsed = time.perf_counter() - start
print(value)
print(elapsed >= 0)
```

**Output**

```text
499500
True
```

`time.time()` measures system wall-clock seconds since an epoch and may be adjusted. `perf_counter()` is appropriate for benchmarking elapsed time; `process_time()` tracks process CPU time rather than waiting time.

### `calendar` helpers

The `calendar` module provides calendar-aware properties and utilities such as leap-year checks and month lengths.

**Example**

```python
import calendar
print(calendar.isleap(2024))
print(calendar.monthrange(2026, 2))
```

**Output**

```text
True
(calendar.SUNDAY, 28)
```

`monthrange` returns `(weekday_of_first_day, days_in_month)`, with Monday represented as 0. Useful for reporting periods and validation.

## 19. `math`, `statistics`, `decimal`, `fractions`

These numerical modules serve different kinds of arithmetic: mathematical functions, descriptive statistics, exact decimal policies, and rational fractions.

### `math` essentials

The `math` module provides functions such as `sqrt`, `prod`, `factorial`, `gcd`, `comb`, `perm`, `ceil`, `floor`, `log`, `exp`, and numerical constants.

**Example**

```python
import math
print(math.sqrt(81))
print(math.prod([2, 3, 4]))
print(math.factorial(5))
print(math.comb(5, 2))
print(math.gcd(24, 36))
```

**Output**

```text
9.0
24
120
10
12
```

`math.comb(n, r)` counts combinations; `math.perm(n, r)` counts permutations. Unlike the `itertools` counterparts, these return **counts**, not iterators producing combinations.

### Floating-point closeness: `math.isclose`

Binary floats approximate many decimal values. `math.isclose` tests closeness using relative and absolute tolerances rather than requiring exact equality.

**Example**

```python
import math
print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
print(math.isclose(0.001, 0, abs_tol=0.01))
```

**Output**

```text
False
True
True
```

For comparison near zero, set an explicit `abs_tol`; relative tolerance alone is often insufficient. In tests, define tolerances appropriate to the domain rather than using arbitrary values.

### `statistics` descriptive functions

`mean`, `median`, `mode`, `stdev` and `variance` summarize numerical collections. They do not replace advanced statistical modeling libraries.

**Example**

```python
from statistics import mean, median, stdev
values = [10, 10, 20, 30]
print(mean(values))
print(median(values))
print(round(stdev(values), 3))
```

**Output**

```text
17.5
15.0
9.574
```

Sample `stdev()` uses a sample denominator; `pstdev()` gives population standard deviation. Empty or insufficient inputs can raise `StatisticsError`.

### `Decimal` — decimal arithmetic and rounding

Construct decimal values from **strings** when exact decimal text is important. `Decimal` can perform calculations and apply explicit rounding rules using `.quantize()`.

**Example**

```python
from decimal import Decimal, ROUND_HALF_UP
amount = Decimal("2.675")
print(amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
print(Decimal("0.1") + Decimal("0.2"))
```

**Output**

```text
2.68
0.3
```

`Decimal(0.1)` imports the underlying binary floating-point approximation rather than the ideal textual decimal `0.1`. Always check the relevant regulatory/business rounding policy for financial computations.

### `Fraction` — exact rational arithmetic

Represents an exact ratio of integers and automatically reduces fractions to simplest form.

**Example**

```python
from fractions import Fraction
print(Fraction(1, 3) + Fraction(1, 6))
print(Fraction(6, 8))
print(Fraction("0.125"))
```

**Output**

```text
1/2
3/4
1/8
```

Fractions are useful when rational exactness matters. Numerators and denominators can become large, so they are not always the most practical representation for huge computations.

## 20. `random`, `secrets`, `hashlib`, `hmac`, `uuid`

These tools distinguish *simulation randomness* from *security randomness*, hashes from authentication, and generated identifiers from durable guarantees of uniqueness.

### `random` for reproducible simulations

The `random` module uses a deterministic pseudorandom generator. Set a seed or use a dedicated `Random(seed)` object when you want reproducible results.

**Example**

```python
from random import Random
rng = Random(7)
print(rng.randint(1, 10))
print(rng.choice(["A", "B", "C"]))
print(rng.sample(range(10), 3))
```

**Output**

```text
6
A
[6, 0, 1]
```

Never use `random` to generate passwords, session tokens, or other sensitive secrets. Reproducible sequences are valuable in testing and simulation, not in adversarial contexts.

### `secrets` for security-sensitive values

`secrets` uses operating-system-backed randomness suited to security tokens. Its output is intentionally nondeterministic.

**Example**

```python
import secrets
value = secrets.token_hex(8)
print(len(value))
print(all(char in "0123456789abcdef" for char in value))
```

**Output**

```text
16
True
```

`secrets.token_urlsafe(n)` creates a URL-safe text token; `secrets.choice()` chooses securely. Avoid printing or logging actual secrets in production.

### `hashlib` cryptographic digests

A hash function produces a fixed-length digest of bytes. Hashes are useful for integrity checks, content fingerprints, and cryptographic building blocks.

**Example**

```python
import hashlib
payload = b"hello"
digest = hashlib.sha256(payload).hexdigest()
print(len(digest))
print(digest[:16])
```

**Output**

```text
64
2cf24dba5fb0a30e
```

Cryptographic hashing differs from Python's built-in `hash()`. A bare fast hash of a password is not an appropriate password-storage scheme; use dedicated password hashing/KDF tools.

### `hmac` message authentication

HMAC combines a shared secret key and message with a cryptographic hash to provide integrity **and** evidence that the message was produced by a key holder.

**Example**

```python
import hashlib
import hmac
key = b"shared-key"
message = b"amount=100"
tag = hmac.new(key, message, hashlib.sha256).hexdigest()
print(len(tag))
print(hmac.compare_digest(tag, tag))
```

**Output**

```text
64
True
```

Use `compare_digest()` for digest comparisons to reduce timing side channels. Message digests alone do not prove authenticity; authentication requires a suitable secret or signature.

### `uuid` identifiers

UUIDs are 128-bit identifiers commonly used to give records or transactions globally unlikely-to-collide IDs. `uuid4()` uses random values, while other UUID versions have different generation semantics.

**Example**

```python
import uuid
value = uuid.UUID("12345678-1234-5678-1234-567812345678")
print(str(value))
print(value.hex)
print(value.version)
```

**Output**

```text
12345678-1234-5678-1234-567812345678
12345678123456781234567812345678
None
```

`uuid4()` is useful for generating new identifiers, but its printed value changes each run. A UUID is not a secret or an authorization token simply because it is hard to guess.

## 21. `contextlib`, `io`, `copy`

Context managers govern resource lifetime; in-memory streams emulate file-like objects; and copying controls which objects are shared.

### `contextmanager` — build a context manager from a generator

Decorating a generator function with `@contextmanager` makes its code before `yield` run on entry and after `yield` run on exit. A `finally` block is useful for cleanup.

**Example**

```python
from contextlib import contextmanager

@contextmanager
def session():
    print("enter")
    try:
        yield {"status": "ready"}
    finally:
        print("exit")

with session() as state:
    print(state["status"])
```

**Output**

```text
enter
ready
exit
```

The code following `yield` is cleanup/exit logic. This is not the same role as a normal generator used for repeatedly yielding data. A class-based context manager instead implements `__enter__` and `__exit__`.

### `ExitStack` — manage variable numbers of contexts

An `ExitStack` dynamically enters multiple context managers and exits all registered contexts in reverse order, even if an exception occurs.

**Example**

```python
from contextlib import ExitStack
from io import StringIO

with ExitStack() as stack:
    first = stack.enter_context(StringIO("a"))
    second = stack.enter_context(StringIO("b"))
    print(first.read() + second.read())
print(first.closed, second.closed)
```

**Output**

```text
ab
True True
```

Useful when you cannot express a fixed number of resources in a single `with` statement: for example, processing a variable set of input files.

### `nullcontext` and `suppress`

`nullcontext(value)` returns a no-op context manager whose `__enter__` yields the given value. `suppress(ErrorType)` deliberately ignores specified exceptions within a block.

**Example**

```python
from contextlib import nullcontext, suppress
with nullcontext("ready") as status:
    print(status)
with suppress(KeyError):
    {}["missing"]
print("continued")
```

**Output**

```text
ready
continued
```

Use `suppress` narrowly—silencing an unexpected exception type can hide data loss or programming mistakes.

### `redirect_stdout` and `StringIO`

`redirect_stdout()` temporarily changes where `print()` writes. `StringIO` stores text in memory as a file-like object.

**Example**

```python
from contextlib import redirect_stdout
from io import StringIO
buffer = StringIO()
with redirect_stdout(buffer):
    print("captured")
print(buffer.getvalue().strip())
```

**Output**

```text
captured
```

These utilities help test printed output or redirect diagnostics from third-party code, but redirecting process-global streams can be unsuitable for concurrent multi-threaded usage.

### `BytesIO` vs `StringIO`

`StringIO` handles text strings, while `BytesIO` handles binary byte streams. Both provide methods such as `.write`, `.read`, `.seek`, and `.getvalue`.

**Example**

```python
from io import BytesIO, StringIO
text = StringIO()
text.write("hello")
raw = BytesIO()
raw.write(b"hello")
print(text.getvalue())
print(raw.getvalue())
```

**Output**

```text
hello
b'hello'
```

This distinction mirrors text vs binary file modes (`"r"` vs `"rb"`). Bytes may require decoding before text-processing operations.

### `copy()` vs `deepcopy()`

A **shallow copy** builds a new outer container but retains references to nested objects. A **deep copy** recursively copies nested structures where supported.

**Example**

```python
from copy import copy, deepcopy
source = [[1], [2]]
shallow = copy(source)
deep = deepcopy(source)
source[0].append(9)
print(shallow)
print(deep)
print(source is shallow)
```

**Output**

```text
[[1, 9], [2]]
[[1], [2]]
False
```

`deepcopy` can be expensive and is not appropriate for all resources or object graphs. Copying has different semantics from rebinding a name: `alias = source` creates no new object at all.

## 22. `logging`, `warnings`, `argparse`

These support production-friendly diagnostics, warnings about suspicious or deprecated behavior, and structured command-line interfaces.

### `logging`: severity and messages

Logging separates the diagnostic message from its destination/format and assigns a level such as `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.

**Example**

```python
import logging
from io import StringIO

buffer = StringIO()
handler = logging.StreamHandler(buffer)
logger = logging.getLogger("notes.example")
logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False
logger.debug("hidden")
logger.info("processed %s records", 3)
print(buffer.getvalue().strip())
```

**Output**

```text
processed 3 records
```

Libraries should generally use named loggers and leave application-wide configuration to the application. Lazy `%s` interpolation can avoid needless string formatting when a log level is disabled.

### Exception logging

Within an exception handler, `logger.exception` includes exception information and traceback, supporting diagnosis without manually printing stack traces.

**Example**

```python
import logging
from io import StringIO
buffer = StringIO()
logger = logging.getLogger("notes.errors")
logger.handlers.clear()
logger.addHandler(logging.StreamHandler(buffer))
logger.setLevel(logging.ERROR)
logger.propagate = False
try:
    int("bad")
except ValueError:
    logger.error("parse failed")
print(buffer.getvalue().strip())
```

**Output**

```text
parse failed
```

Use `logger.exception("...")` instead of `logger.error("...")` when you need a full traceback. Avoid including secrets or sensitive source data in logs.

### `warnings.warn()` and filters

Warnings signal noteworthy behavior without immediately raising an exception. Common categories include `DeprecationWarning` and `UserWarning`.

**Example**

```python
import warnings
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    warnings.warn("legacy behavior", DeprecationWarning)
print(len(caught))
print(caught[0].category.__name__)
print(str(caught[0].message))
```

**Output**

```text
1
DeprecationWarning
legacy behavior
```

Warning filters determine which categories are shown, suppressed or turned into errors. In tests, promote relevant warnings to failures when preventing regressions matters.

### `argparse`: command-line arguments

`ArgumentParser` defines a CLI contract, handles conversion and help text, and produces a namespace of parsed values. You can pass an explicit argument list for testing.

**Example**

```python
import argparse
parser = argparse.ArgumentParser(prog="model")
parser.add_argument("--months", type=int, default=12)
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args(["--months", "6", "--verbose"])
print(args.months)
print(args.verbose)
```

**Output**

```text
6
True
```

`--help` and invalid-argument errors are handled by `argparse`. For larger CLIs, use subparsers or a dedicated interface layer; treat command-line inputs as untrusted text that must be validated.

## 23. `sys`, `importlib`, `subprocess`

These modules expose interpreter and runtime information, dynamic imports, package resources, and safe external-process execution.

### `sys` runtime properties

`sys` exposes interpreter-level state, including version details, paths, command-line arguments and standard streams.

**Example**

```python
import sys
print(sys.version_info.major >= 3)
print(sys.platform in {"darwin", "linux", "win32"})
print(isinstance(sys.argv, list))
```

**Output**

```text
True
True
True
```

Avoid modifying `sys.path` at runtime to work around packaging problems when proper package installation or project layout can solve the issue. `sys.executable` identifies the interpreter executable.

### `importlib.import_module()`

Dynamically imports a module by name. It is more readable than invoking the low-level `__import__()` when ordinary module loading is intended.

**Example**

```python
from importlib import import_module
math = import_module("math")
print(math.sqrt(49))
print(math.__name__)
```

**Output**

```text
7.0
math
```

Dynamic imports are useful for plugin systems and optional dependencies. Importing executes module top-level code, so the module name and source should be trusted.

### `importlib.resources`

Reads data packaged with a Python library, avoiding assumptions about the current working directory. `files(package)` provides resource traversal.

**Example**

```python
from importlib import resources
print(callable(resources.files))
print(callable(resources.as_file))
```

**Output**

```text
True
True
```

A package may be loaded from a zip file or another importer, so treat resources as package-managed objects rather than always expecting ordinary on-disk relative paths.

### `subprocess.run()`

Runs an external program and waits for completion. Pass a **list of arguments** for ordinary use; `capture_output=True` collects stdout/stderr; `check=True` raises on nonzero exit status.

**Example**

```python
import subprocess
import sys
result = subprocess.run(
    [sys.executable, "-c", "print(2 + 3)"],
    capture_output=True,
    text=True,
    check=True,
)
print(result.returncode)
print(result.stdout.strip())
```

**Output**

```text
0
5
```

Avoid `shell=True` with untrusted input; argument lists are normally safer and more portable. Consider `timeout=` for external programs that could hang.

### `subprocess.Popen()`

`Popen` gives lower-level lifecycle control of a child process and is useful for streaming or interactive communication. `communicate()` safely exchanges data while collecting output.

**Example**

```python
import subprocess
import sys
process = subprocess.Popen(
    [sys.executable, "-c", "print('child')"],
    stdout=subprocess.PIPE,
    text=True,
)
stdout, _ = process.communicate()
print(process.returncode)
print(stdout.strip())
```

**Output**

```text
0
child
```

When all you need is one completed command and its result, prefer `subprocess.run`. For running multiple processes concurrently, manage timeouts and clean shutdown explicitly.

## 24. Concurrency

Concurrency is not synonymous with parallel CPU execution. Choose an execution model based on *what the program is waiting for*.

| Model | Appropriate work | Important constraint |
|---|---|---|
| `ThreadPoolExecutor` | Blocking I/O: file or network requests | CPU parallelism depends on interpreter and whether code releases the GIL |
| `ProcessPoolExecutor` | CPU-intensive independent tasks | Data must generally be picklable; startup and IPC cost |
| `asyncio` | Cooperative asynchronous I/O | Blocking CPU work stalls the event loop |
| `threading` primitives | Shared state among threads | Synchronization and races require care |

Always measure performance rather than assuming adding workers speeds a workload.

### `ThreadPoolExecutor.map()`

A thread pool runs callables using worker threads. Mapping returns results in **input order**, even if individual tasks finish in a different order.

**Example**

```python
from concurrent.futures import ThreadPoolExecutor

def square(n):
    return n * n

with ThreadPoolExecutor(max_workers=2) as pool:
    print(list(pool.map(square, [1, 2, 3, 4])))
```

**Output**

```text
[1, 4, 9, 16]
```

Thread pools are especially convenient for independent I/O tasks. Worker exceptions propagate when the corresponding result is requested.

### `submit()` and `as_completed()`

`submit()` immediately schedules a task and returns a `Future`. `as_completed()` yields futures as they complete, which is not necessarily submission order.

**Example**

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(lambda n: n * n, x) for x in (1, 2, 3)]
    print(sorted(f.result() for f in as_completed(futures)))
```

**Output**

```text
[1, 4, 9]
```

The `sorted(...)` here is deliberate so the example's output is stable regardless of completion order. Cancellation only succeeds before work has begun; closing the executor normally waits for in-flight work.

### `ProcessPoolExecutor`

Uses child processes rather than threads, which can help with CPU-bound operations in ordinary CPython builds. Functions and arguments must generally be serializable for child-process execution.

**Example**

```python
from concurrent.futures import ProcessPoolExecutor
print(ProcessPoolExecutor.__name__)
print(callable(ProcessPoolExecutor.map))
```

**Output**

```text
ProcessPoolExecutor
True
```

A full runnable multiprocessing example belongs in a `.py` file with top-level functions and `if __name__ == "__main__":` protection where required. Notebook/interactive functions, lambdas and closures are often not reliably picklable. Large DataFrames can incur considerable IPC overhead.

### `threading.Lock`

A lock protects critical sections where multiple threads may read and update shared state. `with lock:` acquires and releases it safely.

**Example**

```python
from threading import Lock
lock = Lock()
shared = {"count": 0}
with lock:
    shared["count"] += 1
print(shared)
```

**Output**

```text
{'count': 1}
```

Even simple-looking read/modify/write operations are not always atomic across threads. Use a lock, a queue, or ownership-based design to avoid data races.

### `asyncio.gather()`

Runs awaitables concurrently on an event loop and produces results in the input order, even if completion order differs.

**Example**

```python
import asyncio

async def double(n):
    await asyncio.sleep(0)
    return n * 2

async def main():
    print(await asyncio.gather(double(1), double(2), double(3)))

asyncio.run(main())
```

**Output**

```text
[2, 4, 6]
```

`gather` coordinates coroutines, not CPU-bound parallelism. Long blocking calls should be adapted through suitable async APIs or offloaded to threads/processes.

### `asyncio.TaskGroup()`  ·  Python 3.11+

Task groups provide structured concurrency: tasks belong to an explicit scope and the group coordinates cleanup when child tasks fail. Introduced in Python 3.11.

**Example**

```python
import asyncio

async def task(n):
    await asyncio.sleep(0)
    return n * n

async def main():
    async with asyncio.TaskGroup() as group:
        a = group.create_task(task(3))
        b = group.create_task(task(4))
    print(a.result(), b.result())

asyncio.run(main())
```

**Output**

```text
9 16
```

With task failures, task groups use cancellation and exception groups to coordinate sibling tasks. This gives stronger structured-lifetime guarantees than ad hoc background tasks.

### `asyncio.to_thread()` and `asyncio.timeout()`  ·  Python 3.11+

`to_thread` offloads a blocking synchronous callable to a worker thread; `asyncio.timeout` gives a deadline-like scope for awaiting work.

**Example**

```python
import asyncio

def blocking():
    return 10

async def main():
    async with asyncio.timeout(5):
        print(await asyncio.to_thread(blocking))

asyncio.run(main())
```

**Output**

```text
10
```

`to_thread` is mainly for blocking I/O; it does not automatically make arbitrary Python CPU loops parallel under a GIL-based interpreter. `asyncio.timeout()` was introduced in 3.11.

## 25. `sqlite3`

SQLite is an embedded relational database accessible without a separate server. It is useful for tests, local data management, small applications and relational experiments.

### Connect, create, insert, and query

A SQLite connection executes SQL. `:memory:` creates an in-memory database. Cursors and row results expose query output independently of Pandas.

**Example**

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE trades (id INTEGER, amount REAL)")
conn.executemany("INSERT INTO trades VALUES (?, ?)", [(1, 10.0), (2, 20.0)])
print(conn.execute("SELECT id, amount FROM trades ORDER BY id").fetchall())
print(conn.execute("SELECT SUM(amount) FROM trades").fetchone()[0])
conn.close()
```

**Output**

```text
[(1, 10.0), (2, 20.0)]
30.0
```

`fetchone()` returns one result tuple or `None`; `fetchall()` returns all remaining rows. Consider streaming with cursor iteration for large query results.

### Parameterized SQL queries

Placeholders (`?`) separate input values from SQL syntax and avoid manual string interpolation of user-supplied parameters.

**Example**

```python
import sqlite3
with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE items (name TEXT)")
    conn.execute("INSERT INTO items VALUES (?)", ("Ada",))
    name = "Ada"
    print(conn.execute("SELECT name FROM items WHERE name = ?", (name,)).fetchone())
```

**Output**

```text
('Ada',)
```

Never build untrusted SQL values with f-strings. Parameters substitute **values**, not arbitrary column names or table identifiers; identifier selection requires a separate trusted allowlist.

### `sqlite3.Row` and transaction boundaries

`sqlite3.Row` provides column-name access to query results. A connection's `with` block manages commit/rollback for a transaction, but does not necessarily close the connection.

**Example**

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
with conn:
    conn.execute("CREATE TABLE runs (id INTEGER, status TEXT)")
    conn.execute("INSERT INTO runs VALUES (1, 'done')")
row = conn.execute("SELECT * FROM runs").fetchone()
print(dict(row))
conn.close()
```

**Output**

```text
{'id': 1, 'status': 'done'}
```

Explicitly manage connection lifetime. A successful transaction commit and closing a connection are separate concerns. Use an appropriate migration and concurrency strategy for larger databases.

## 26. Inspection, debugging, profiling and tests

Python’s standard library can reveal signatures, execution paths, bytecode, call times, and test behavior. Inspection is useful for understanding *what an object exposes*; profiling determines *where a program spends resources*.

### `inspect.signature()` and `getmembers()`

`inspect.signature(callable)` describes parameters, defaults and return annotations where supported. `inspect.getmembers(obj)` enumerates members with their values.

**Example**

```python
import inspect

def calculate(a: int, b: int = 2) -> int:
    return a + b

print(inspect.signature(calculate))
print(inspect.isfunction(calculate))
print("__name__" in dict(inspect.getmembers(calculate)))
```

**Output**

```text
(a: int, b: int = 2) -> int
True
True
```

Not every C-level or dynamically generated callable has an inspectable signature. `inspect.getattr_static()` is useful when you want to examine an attribute without invoking normal descriptor lookup.

### `Signature.bind()`

Checks whether a proposed set of arguments fits a callable's signature, producing a mapping from parameter names to the supplied values without invoking the callable.

**Example**

```python
from inspect import signature

def f(a, b=2):
    return a + b

bound = signature(f).bind(10, b=7)
print(bound.arguments)
print(f(*bound.args, **bound.kwargs))
```

**Output**

```text
{'a': 10, 'b': 7}
17
```

Useful in decorators, generic API adapters, dependency injection or validation of forwarded arguments. `bind_partial()` permits missing required arguments.

### `traceback`

Extracts and formats exception tracebacks, which is helpful for error reporting and debugging. For normal exception handling, preserving the actual exception object and chained cause is usually preferable to parsing traceback text.

**Example**

```python
import traceback
try:
    1 / 0
except ZeroDivisionError as exc:
    print(type(exc).__name__)
    print(bool(traceback.format_exception(exc)))
```

**Output**

```text
ZeroDivisionError
True
```

`traceback.format_exc()` operates on the currently handled exception; outside an exception handler, its meaning differs. Avoid exposing full tracebacks with credentials or sensitive inputs to end users.

### `timeit` — benchmark short operations

`timeit` repeats a callable or code snippet to estimate execution cost and reduce measurement noise compared with a single manual timer.

**Example**

```python
import timeit
elapsed = timeit.timeit("sum(range(100))", number=100)
print(isinstance(elapsed, float))
print(elapsed >= 0)
```

**Output**

```text
True
True
```

Benchmark performance under representative workloads and include setup/teardown cost only when it belongs to the measured operation. Run multiple trials to understand variability.

### `cProfile` and `pstats`

`cProfile` records call counts and time spent in functions. `pstats` sorts and reports the measurements, helping locate bottlenecks.

**Example**

```python
import cProfile
import pstats
from io import StringIO

profile = cProfile.Profile()
profile.enable()
sum(i * i for i in range(100))
profile.disable()
buffer = StringIO()
pstats.Stats(profile, stream=buffer).sort_stats("cumulative").print_stats(3)
print("function calls" in buffer.getvalue())
```

**Output**

```text
True
```

Profiling adds overhead and measurements can vary between runs. A profiler tells you **where time is spent**; it does not by itself prescribe the right algorithmic fix.

### `dis` bytecode inspection

`dis` displays CPython bytecode instructions generated for a function. It is useful for learning implementation details and comparing compilation patterns.

**Example**

```python
import dis

def square(x):
    return x * x

instructions = list(dis.get_instructions(square))
print(any(i.opname == "RETURN_VALUE" for i in instructions))
print([i.opname for i in instructions][-1])
```

**Output**

```text
True
RETURN_VALUE
```

Exact bytecode is an implementation detail and changes across Python versions. Do not base public application semantics on bytecode layout.

### `pdb` and `breakpoint()`

`pdb` is Python’s interactive debugger. `breakpoint()` enters the configured debugging tool at the current execution point when enabled.

**Example**

```python
import pdb
print(callable(pdb.set_trace))
print(callable(breakpoint))
```

**Output**

```text
True
True
```

Useful debugger commands include `n` (next), `s` (step into), `c` (continue), `p expression` (print), and `q` (quit). This note does not trigger an interactive debug session.

### `unittest` assertions

`unittest.TestCase` provides assertions and test discovery in the standard library. It can check expected values, exceptions and floating-point approximations.

**Example**

```python
import unittest

class CalculationTests(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(2 + 3, 5)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(CalculationTests)
result = unittest.TestResult()
suite.run(result)
print(result.testsRun)
print(result.wasSuccessful())
```

**Output**

```text
1
True
```

Testing a calculation function should include edge cases, empty inputs and expected failures—not just a happy path. For approximate numerical outputs, use an appropriate tolerance.

### `unittest.mock`

Mocks and patches replace dependencies in tests so behavior can be verified without external services. `patch` temporarily changes a binding, while `Mock`/`MagicMock` can record calls.

**Example**

```python
from unittest.mock import Mock
client = Mock()
client.fetch.return_value = {"status": "ok"}
print(client.fetch(123))
client.fetch.assert_called_once_with(123)
print(client.fetch.call_count)
```

**Output**

```text
{'status': 'ok'}
1
```

Patch the **name used by the code under test**, not necessarily the object at its original definition location. Excessive mocking can make tests brittle by coupling them to internal implementation details.

## 27. Other useful modules

These smaller tools often eliminate unnecessary dependencies for formatting, matching, file compression, graph ordering, in-memory queues, and AST inspection.

### `textwrap`

Wraps or dedents multiline text while respecting indentation conventions. Useful for building CLI help, documentation and formatted logs.

**Example**

```python
import textwrap
text = """
    one
    two
"""
print(repr(textwrap.dedent(text).strip()))
print(textwrap.fill("alpha beta gamma delta", width=12))
```

**Output**

```text
'one\ntwo'
alpha beta
gamma delta
```

`dedent` removes common indentation from lines; `fill` creates line wraps. Formatting does not change the semantic text content in the same way that parsing would.

### `pprint`

Pretty-prints nested Python objects for humans, usually with indentation and line wrapping that improve exploratory readability.

**Example**

```python
from pprint import pformat
value = {"b": [1, 2], "a": {"nested": True}}
print("nested" in pformat(value))
```

**Output**

```text
True
```

`pformat` returns a string while `pprint` writes it. Neither is a stable data-exchange format; use JSON for interoperability when applicable.

### `difflib`

Provides sequence comparisons and human-readable diffs. It can help diagnose changes in code, text outputs or ordered records.

**Example**

```python
from difflib import ndiff
before = ["alpha", "beta"]
after = ["alpha", "gamma"]
print(list(ndiff(before, after)))
```

**Output**

```text
['  alpha', '- beta', '+ gamma']
```

For structural data, compare normalized values or use explicit field-level checks instead of relying exclusively on text diffs.

### `fnmatch`

Matches shell-style wildcard patterns in strings, such as `*.csv`, independent of actual file-system traversal.

**Example**

```python
from fnmatch import fnmatch
print(fnmatch("report.csv", "*.csv"))
print(fnmatch("report.md", "*.csv"))
```

**Output**

```text
True
False
```

This is not a regex engine. Use `re` for capture groups and complex character-pattern rules.

### `shlex`

Tokenizes shell-like command text and provides safe argument quoting helpers. It is useful when interpreting command syntax or displaying quoted arguments.

**Example**

```python
import shlex
print(shlex.split('python script.py --name "Ada Lovelace"'))
print(shlex.quote("two words"))
```

**Output**

```text
['python', 'script.py', '--name', 'Ada Lovelace']
'two words'
```

Prefer supplying a list of arguments to `subprocess.run`; do not assume shell quoting makes executing arbitrary untrusted command strings safe.

### `queue.Queue`

A thread-safe queue coordinating producer/consumer threads. It supports `put`, `get`, `task_done`, and `join`.

**Example**

```python
from queue import Queue
q = Queue()
q.put("task-a")
q.put("task-b")
print(q.get())
q.task_done()
print(q.get())
q.task_done()
print(q.empty())
```

**Output**

```text
task-a
task-b
True
```

For coroutine-based concurrency, use `asyncio.Queue`. For simple one-thread FIFO behavior, `collections.deque` can be more direct.

### `weakref`

A weak reference points to an object without necessarily keeping it alive. Useful for caches, observers and metadata associated with objects managed elsewhere.

**Example**

```python
import weakref

class Item:
    pass

obj = Item()
ref = weakref.ref(obj)
print(ref() is obj)
del obj
print(ref() is None)
```

**Output**

```text
True
True
```

Not every built-in object supports weak references. Weak references are about lifetime, not a general replacement for ownership or explicit cleanup.

### `graphlib.TopologicalSorter`

Computes an ordering of nodes that respects dependency precedence. A graph of dependencies must be acyclic for topological ordering.

**Example**

```python
from graphlib import TopologicalSorter
nodes = {"compile": {"load"}, "execute": {"compile"}, "load": set()}
print(tuple(TopologicalSorter(nodes).static_order()))
```

**Output**

```text
('load', 'compile', 'execute')
```

In the dictionary mapping, keys are nodes and their values are **predecessor dependencies**. The computed plan is deterministic for a given graph and insertion structure, but a graph can admit more than one valid topological ordering.

### `ast` for parsing Python syntax

`ast.parse` converts Python source into an abstract syntax tree. `ast.literal_eval` handles specific literal expressions without executing arbitrary program statements.

**Example**

```python
import ast
expression = ast.parse("a + 2", mode="eval")
print(type(expression.body).__name__)
print(ast.literal_eval("{'x': [1, 2]}"))
```

**Output**

```text
BinOp
{'x': [1, 2]}
```

`literal_eval` can still consume substantial resources if fed deeply nested or enormous input. It is not equivalent to evaluating general formulas. Build a controlled expression parser or use an appropriate formula language for user-authored expressions.

### `zipfile` and `gzip`

`zipfile` handles archives containing multiple files; `gzip` compresses and decompresses a single stream of bytes. Neither is an encryption mechanism.

**Example**

```python
import gzip
payload = b"hello hello hello"
compressed = gzip.compress(payload)
print(gzip.decompress(compressed))
print(len(compressed) > 0)
```

**Output**

```text
b'hello hello hello'
True
```

Validate archive member paths before extracting untrusted ZIPs to disk, and impose size limits on potentially malicious compressed content.

### `pickle` serialization

`pickle` serializes and restores many Python-specific objects, which is convenient for trusted internal workflows but not suitable for interoperability or untrusted input.

**Example**

```python
import pickle
value = {"ids": [1, 2, 3]}
encoded = pickle.dumps(value)
print(pickle.loads(encoded))
```

**Output**

```text
{'ids': [1, 2, 3]}
```

**Security:** Never unpickle untrusted bytes: loading can execute arbitrary code. Use JSON, CSV, or other safer formats for external data exchanges.

### Additional modules to recognize

| Module | What it is useful for |
|---|---|
| `inspect` | Signatures, source information and object members |
| `types` | Runtime helper types and coroutine-related utilities |
| `functools` | Caching, dispatch, partial application, reduction |
| `contextvars` | Context-local state for asynchronous code |
| `concurrent.futures` | Executor abstractions, futures |
| `argparse` | Command-line interfaces |
| `ipaddress` | IP address and network parsing |
| `urllib.parse` | URL encoding and parsing |
| `statistics` | Descriptive statistical functions |
| `platform` | Platform and interpreter metadata |
| `shutil` | File-tree copying/moving and disk usage |
| `tempfile` | Safe temporary workspaces |
| `socket` | Low-level networking |
| `struct` | Packed binary layout conversion |
| `decimal` | Decimal arithmetic with configurable precision/rounding |

---

# Part III — Practical recipes and engineering guidance

## 28. Practical recipes

These examples combine the earlier tools in realistic workflows, emphasizing input/output behavior and transparent intermediate results.

### Recipe 1 — Group records and calculate totals

Sort the input by grouping key, group consecutive equal keys, and compute a summary for each group.

**Example**

```python
from itertools import groupby
from operator import itemgetter
records = [("West", 15), ("East", 10), ("West", 20)]
key = itemgetter(0)
result = {name: sum(amount for _, amount in rows)
          for name, rows in groupby(sorted(records, key=key), key=key)}
print(result)
```

**Output**

```text
{'East': 10, 'West': 35}
```

For huge unordered datasets, sorting may dominate cost. If you only need per-key totals in memory, `defaultdict(int)` can aggregate in one pass.

### Recipe 2 — Validate aligned fields

Use `zip(..., strict=True)` when multiple columns must describe the same number of records.

**Example**

```python
ids = [101, 102]
amounts = [10.0, 20.0]
print([{"id": i, "amount": a}
       for i, a in zip(ids, amounts, strict=True)])
```

**Output**

```text
[{'id': 101, 'amount': 10.0}, {'id': 102, 'amount': 20.0}]
```

Without `strict=True`, a mismatched final row could be silently dropped, which is dangerous for data pipelines.

### Recipe 3 — Read a large binary stream in chunks

Sentinel-form `iter()` combines naturally with `functools.partial()` to read until EOF without a manual `while` loop.

**Example**

```python
from functools import partial
from io import BytesIO
source = BytesIO(b"ABCDEFGHI")
print(list(iter(partial(source.read, 4), b"")))
```

**Output**

```text
[b'ABCD', b'EFGH', b'I']
```

Use larger chunk sizes for real file I/O as appropriate; loading every chunk into `list()` here is only to display the output.

### Recipe 4 — Partition valid vs invalid records

For small inputs, two comprehensions make the categorization explicit. A single traversal can also do both using a loop or dictionary accumulation.

**Example**

```python
values = [5, -2, 0, 7, -1]
valid = [n for n in values if n >= 0]
invalid = [n for n in values if n < 0]
print(valid)
print(invalid)
```

**Output**

```text
[5, 0, 7]
[-2, -1]
```

The two-comprehension version reads the input twice. That is fine for a list, but not for a one-shot generator; use one traversal if the source can be consumed only once.

### Recipe 5 — Multi-key sorting

Compose a key tuple when primary and secondary ordering must be deterministic.

**Example**

```python
records = [{"desk": "B", "priority": 2}, {"desk": "A", "priority": 3}, {"desk": "B", "priority": 1}]
print(sorted(records, key=lambda row: (row["desk"], row["priority"])))
```

**Output**

```text
[{'desk': 'A', 'priority': 3}, {'desk': 'B', 'priority': 1}, {'desk': 'B', 'priority': 2}]
```

For mixed ascending/descending criteria, use a stable multi-pass sort or construct deliberate transformed keys rather than relying on string manipulation hacks.

### Recipe 6 — Cached metadata lookup

Use caching for deterministic lookups when repeated requests share the same arguments.

**Example**

```python
from functools import lru_cache
calls = []

@lru_cache(maxsize=32)
def metadata(name):
    calls.append(name)
    return {"name": name, "length": len(name)}

print(metadata("model"))
print(metadata("model"))
print(calls)
```

**Output**

```text
{'name': 'model', 'length': 5}
{'name': 'model', 'length': 5}
['model']
```

Caching is inappropriate if the lookup should reflect mutable database state unless you define an invalidation strategy.

### Recipe 7 — Dependency-ordered execution

Represent a static dependency graph and derive a topological execution plan before running calculations.

**Example**

```python
from graphlib import TopologicalSorter
dependencies = {"RRM": set(), "SIR": {"RRM"}, "FLA": {"SIR"}, "ECL": {"FLA"}}
print(tuple(TopologicalSorter(dependencies).static_order()))
```

**Output**

```text
('RRM', 'SIR', 'FLA', 'ECL')
```

`TopologicalSorter` raises `CycleError` for cycles. Separate **planning** from **execution** when you need to validate the entire dependency graph before any side effects occur.

### Recipe 8 — Dataclass implementing an abstract API

Combine an ABC contract with a dataclass implementation to make calculation components explicit.

**Example**

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

class Calculator(ABC):
    @abstractmethod
    def calculate(self) -> int: ...

@dataclass
class AddCalculator(Calculator):
    a: int
    b: int

    def calculate(self) -> int:
        return self.a + self.b

print(AddCalculator(3, 4).calculate())
```

**Output**

```text
7
```

The ABC declares required behavior; the dataclass provides structural initialization and representation. For duck-typed public interfaces, consider a `Protocol` instead.

### Recipe 9 — Layered configuration

Use `ChainMap` when overrides should take precedence over defaults while retaining the original mapping layers.

**Example**

```python
from collections import ChainMap
defaults = {"timeout": 30, "retries": 3}
overrides = {"timeout": 10}
print(dict(ChainMap(overrides, defaults)))
```

**Output**

```text
{'timeout': 10, 'retries': 3}
```

For a detached materialized configuration, `defaults | overrides` is often simpler. The order matters: leftmost mapping is searched first.

### Recipe 10 — Compare floating-point outputs

Express tolerance explicitly instead of comparing calculated floats using exact equality.

**Example**

```python
from math import isclose
expected = [0.3, 1.2]
actual = [0.1 + 0.2, 1.200000000001]
print(all(isclose(a, b, rel_tol=1e-8, abs_tol=1e-10)
          for a, b in zip(actual, expected, strict=True)))
```

**Output**

```text
True
```

Choose tolerances based on the model's actual numeric error requirements. For arrays and DataFrames, vectorized comparison tools may be more appropriate.

### Recipe 11 — Detect consecutive state transitions

`pairwise` avoids manual position management when changes depend on adjacent values.

**Example**

```python
from itertools import pairwise
states = ["pending", "pending", "active", "active", "closed"]
print([(a, b) for a, b in pairwise(states) if a != b])
```

**Output**

```text
[('pending', 'active'), ('active', 'closed')]
```

This finds transitions, not durations. For durations, pair states with timestamps and check that the timestamps are ordered.

### Recipe 12 — Select top N

A heap can return the highest-ranked few values without fully sorting an entire collection.

**Example**

```python
from heapq import nlargest
records = [{"id": "A", "risk": 5}, {"id": "B", "risk": 8}, {"id": "C", "risk": 3}]
print(nlargest(2, records, key=lambda x: x["risk"]))
```

**Output**

```text
[{'id': 'B', 'risk': 8}, {'id': 'A', 'risk': 5}]
```

For very large N near the dataset size, normal sorting may be more efficient. Benchmark under representative workloads.

### Recipe 13 — CSV to JSON

Stream rows through the CSV parser, convert fields to the types you intend, and serialize the result deliberately.

**Example**

```python
import csv
import json
from io import StringIO
source = StringIO("name,amount\nA,10\nB,20\n")
rows = [{"name": row["name"], "amount": int(row["amount"])} for row in csv.DictReader(source)]
print(json.dumps(rows))
```

**Output**

```text
[{"name": "A", "amount": 10}, {"name": "B", "amount": 20}]
```

Without the `int()` conversion, JSON would contain `"10"` rather than numeric `10`. Schema and type conversion belong at data boundaries.

### Recipe 14 — A timing decorator

Use `wraps` for metadata and `perf_counter` for elapsed duration. The example records the result without depending on an unpredictable time value.

**Example**

```python
from functools import wraps
from time import perf_counter

def measured(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        elapsed = perf_counter() - start
        return result, elapsed
    return inner

@measured
def calculate(n):
    return sum(range(n))

value, seconds = calculate(5)
print(value)
print(seconds >= 0)
print(calculate.__name__)
```

**Output**

```text
10
True
calculate
```

For a robust profiler, measure CPU time and memory separately, account for exceptions, and avoid misleading performance claims from a single run.

### Recipe 15 — Composite-key deduplication

Use tuples of hashable field values as dictionary keys to identify repeated business coordinates while retaining first-occurrence order.

**Example**

```python
records = [(1, "USD"), (2, "CAD"), (1, "USD"), (1, "CAD")]
print(tuple(dict.fromkeys(records)))
```

**Output**

```text
((1, 'USD'), (2, 'CAD'), (1, 'CAD'))
```

A tuple is hashable only when all its elements are hashable. For unhashable nested values, normalize them or write a suitable key-extraction function.

### Recipe 16 — Optional configuration and sentinels

A unique sentinel distinguishes an absent value from an explicitly supplied `None`.

**Example**

```python
MISSING = object()
config = {"timeout": None}
value = config.get("timeout", MISSING)
print(value is MISSING)
print(config.get("retries", MISSING) is MISSING)
```

**Output**

```text
False
True
```

This is particularly important for APIs where `None` means “disable the option” rather than “not provided.”

### Recipe 17 — Rolling windows

For a rolling window of size three, combine a bounded deque with an iterator. Only a fixed number of values is kept in memory.

**Example**

```python
from collections import deque
values = [1, 2, 3, 4, 5]
window = deque(maxlen=3)
windows = []
for value in values:
    window.append(value)
    if len(window) == 3:
        windows.append(tuple(window))
print(windows)
```

**Output**

```text
[(1, 2, 3), (2, 3, 4), (3, 4, 5)]
```

For overlapping pairs, `pairwise()` is simpler. For large numerical arrays, NumPy or Pandas may support faster vectorized rolling operations.

### Recipe 18 — Temporary SQLite data checks

Use a temporary in-memory SQLite database when you need to test SQL joins or aggregation without a remote database.

**Example**

```python
import sqlite3
with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE measures (category TEXT, balance INT)")
    conn.executemany("INSERT INTO measures VALUES (?, ?)", [("A", 10), ("A", 5), ("B", 20)])
    print(conn.execute("SELECT category, SUM(balance) FROM measures GROUP BY category ORDER BY category").fetchall())
```

**Output**

```text
[('A', 15), ('B', 20)]
```

SQLite syntax and behavior are not identical to every enterprise database. This is excellent for lightweight logic checks but not a complete substitute for integration tests against the target engine.

## 29. Pitfalls and decision guides

The most common errors arise not from obscure functions but from mistaken assumptions about **types**, **state**, **mutability**, and **execution timing**.

| Pitfall | Why it matters | Safer habit |
|---|---|---|
| Iterate a generator twice | The first pass exhausts it | Recreate it, cache deliberately, or use `tee` sparingly |
| `list.sort()` returned `None` | It mutates in place | Use `sorted()` for a new list |
| `zip` drops trailing elements | Stops at shortest source | Use `strict=True` for validation |
| `groupby` splits equal keys | Only consecutive grouping | Sort by key first if global grouping is intended |
| `repeat([])` shares an object | Repeated references, not copies | Construct independent objects |
| `dict.fromkeys(keys, [])` shares values | One list across all keys | Comprehension or `defaultdict` |
| Tuple contains a list | Tuple becomes unhashable | Use hashable nested fields |
| `filter(None, xs)` removes zero | Falsy is broader than missing | Check `is not None` explicitly |
| Binary float used for policy rounding | Decimal-looking values can be approximations | `Decimal` with rounding rules |
| `eval` on external input | Arbitrary code execution risk | Structured parsers or controlled DSL |
| `pickle.loads` on external bytes | Arbitrary code execution risk | Use safe serialization |
| `tee` consumers diverge | Buffered memory grows | Avoid extreme lag or materialize carefully |
| `product` used on many dimensions | Combinatorial explosion | Calculate result count first |
| `hash()` used as stable ID | Hash salt and runtime behavior vary | Use domain IDs or cryptographic digests appropriately |

### Loops vs comprehensions vs `map` vs generators

| Situation | Typical choice |
|---|---|
| Need a list of transformed items | List comprehension |
| Need a one-pass lazy transformation | Generator expression / `map` |
| Existing function applies unchanged to each value | `map(existing_function, xs)` |
| Need multiple statements or side effects | Explicit `for` loop |
| Need to flatten streams | `chain.from_iterable` |
| Need successive argument-tuples unpacked | `starmap` |

Avoid transforming a clear comprehension into several nested lambdas simply to make the code shorter. In data work, **clarity about consumption and shape** is often more important than syntax compactness.

### Grouping: choose the right abstraction

| Need | Tool |
|---|---|
| Group adjacent equal keys in an already ordered stream | `itertools.groupby` |
| Accumulate lists/totals from an unordered stream | `collections.defaultdict` |
| Count discrete labels | `collections.Counter` |
| Analyze tabular columns, calculate vectorized group summaries | `pandas.DataFrame.groupby` |
| Aggregate persistent relational data | SQL `GROUP BY` |

`groupby` from `itertools` gives a stream of `(key, group_iterator)` pairs. Pandas and SQL operate on richer tabular/relational abstractions.

### Storage and representation

| Want to... | Recommended tools |
|---|---|
| Exchange simple structured data | `json` |
| Read/write simple tables | `csv` |
| Read project configuration | `tomllib` |
| Persist relational local data | `sqlite3` |
| Represent a fixed structured record | dataclass / `NamedTuple` |
| Compress a stream | `gzip` |
| Create a multi-file archive | `zipfile` |
| Serialize a trusted Python-specific object | `pickle` (trusted-only) |
| Record a durable identifier | `uuid` or a domain key, depending on constraints |

### Rough complexity reference

| Operation | Typical time | Notes |
|---|---|---|
| `len(list)` | O(1) | Uses stored size |
| `x in list` | O(n) | General scan |
| `x in set` / `key in dict` | O(1) average | Hashability and collisions matter |
| `list.append` | O(1) amortized | Occasional resize |
| `list.pop(0)` | O(n) | Shifts elements |
| `deque.popleft` | O(1) | Efficient front removal |
| `sorted(xs)` | O(n log n) worst case | Creates a new list |
| `heapq.heappush` / `heappop` | O(log n) | Heap already maintained |
| `heapq.heapify` | O(n) | In-place heap transformation |
| `bisect_left` search | O(log n) | Sorted input required |
| `insort` into list | O(n) overall | Element shifting dominates |
| `chain` traversal | O(total items) | Generally no combined-list allocation |
| `groupby` traversal | O(n) | Sorting if required adds cost |
| `product` enumeration | Product of pool sizes | Can grow exponentially |

These are high-level complexity guides for common CPython implementations, not hard guarantees for arbitrary custom objects.

## 30. Quick-reference index

This section is a final review index. It is intentionally concise because the preceding chapters provide full explanations and runnable outputs.

| Concept | Function/module | Remember |
|---|---|---|
| Index values | `enumerate` | Iterator of index-value pairs |
| Align values | `zip` | Shortest wins unless strict |
| Concatenate sources | `itertools.chain` | Lazy flattening of one level |
| Flatten nested sources | `chain.from_iterable` | Receives one iterable of iterables |
| Batch records | `itertools.batched` | Tuple chunks, 3.12+ |
| Keep prefix | `takewhile` | Stops at first failure |
| Discard prefix | `dropwhile` | Yields all after first failure |
| Running computation | `accumulate` | Every intermediate result |
| Final computation | `reduce` | One result |
| Adjacent transitions | `pairwise` | Overlapping previous/current pairs |
| Consecutive groups | `itertools.groupby` | Sort first for global grouping |
| Duplicated reading position | `tee` | Buffers when consumers diverge |
| Argument tuple mapping | `starmap` | Calls `f(*args)` |
| Cartesian coordinates | `product` | Full dimension grid |
| Ordered selections | `permutations` | Order matters |
| Unordered selections | `combinations` | Order does not matter |
| Frequency counts | `Counter` | Missing count reads as 0 |
| Missing-key factories | `defaultdict` | `mapping[key]` triggers factory |
| Double-ended queue | `deque` | Efficient operations at both ends |
| Bound arguments | `functools.partial` | Configured callable |
| Memoization | `functools.lru_cache` | Stale/cache-size considerations |
| Key functions | `operator.itemgetter` | Efficient extraction |
| Data records | `dataclass` | Generated methods |
| Structural contracts | `Protocol` | No explicit inheritance required |
| Explicit interfaces | `ABC` | Abstract methods |
| Path objects | `pathlib.Path` | Compose with `/` |
| Date/time | `datetime`, `zoneinfo` | Timezone awareness matters |
| Timings | `time.perf_counter` | Elapsed duration |
| Local database | `sqlite3` | SQL without server |
| Profiling | `cProfile`, `timeit` | Measure before optimizing |
| Dependency graph | `graphlib.TopologicalSorter` | Predecessor-based DAG order |

### Suggested study order

1. **Iteration model:** `iter`, `next`, generators, `zip`, comprehensions, `islice`.
2. **Iterator composition:** `chain`, `chain.from_iterable`, `groupby`, `pairwise`, `starmap`, `accumulate`.
3. **Object mechanics:** names vs objects, `type`, `isinstance`, attributes, `__dict__`, `super`, descriptors.
4. **Functional tools:** `partial`, `reduce`, `wraps`, `operator` extractors, caching.
5. **Structured data:** `dataclass`, `NamedTuple`, `Protocol`, `ABC`, `Enum`, `collections`.
6. **Engineering utilities:** `pathlib`, `contextlib`, `logging`, `sqlite3`, `inspect`, `unittest`.
7. **Scaling and performance:** `heapq`, `bisect`, concurrency choices, benchmarking, profiling.

When practicing, predict the output **before running the code**. Pay special attention to whether a function returns a list, a tuple, a generator/iterator, a scalar, or `None`, and whether it consumes or mutates the input.

### Official documentation and further reading

- [Python built-in functions](https://docs.python.org/3/library/functions.html)
- [Python standard library index](https://docs.python.org/3/library/index.html)
- [Iterator protocol and data model](https://docs.python.org/3/reference/datamodel.html)
- [`itertools` reference and recipes](https://docs.python.org/3/library/itertools.html)
- [`functools`](https://docs.python.org/3/library/functools.html)
- [`operator`](https://docs.python.org/3/library/operator.html)
- [`collections`](https://docs.python.org/3/library/collections.html)
- [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [`typing`](https://docs.python.org/3/library/typing.html)
- [`contextlib`](https://docs.python.org/3/library/contextlib.html)
- [Python HOWTO: Functional Programming](https://docs.python.org/3/howto/functional.html)

**Last note:** Python's built-ins and standard library are deliberately composable. Learning what each operation *returns*, what it *consumes*, and what it *mutates* often matters more than memorizing its signature.