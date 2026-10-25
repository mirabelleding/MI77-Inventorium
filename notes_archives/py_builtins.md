# Python Built-in Functions and Standard Library: Extensive Study Notes

**Scope:** Python 3.11+ unless a feature is marked with a higher minimum version.
**Level:** Foundations → intermediate → advanced.
**Purpose:** A practical reference for everyday Python, data processing, automation, package development, testing, and performance-conscious programming.

> **Built-in function vs. standard-library module:** `len()` works without an import because it is a built-in. `itertools.chain()` requires `import itertools` because `itertools` is a standard-library module. Both ship with Python; neither requires `pip install`.

**Example convention:** Code blocks show illustrative Python 3 code. Most are self-contained; examples that explicitly refer to previous definitions should be run with the surrounding example. Code is intentionally presented without inline comments or docstrings.

## Table of Contents

1. [How to choose Python's built-in tools](#1-how-to-choose-pythons-built-in-tools)
2. [Iteration and sequence built-ins](#2-iteration-and-sequence-built-ins)
3. [Aggregations, ordering, and comparisons](#3-aggregations-ordering-and-comparisons)
4. [Conversions, representation, and formatting](#4-conversions-representation-and-formatting)
5. [Numbers and numeric built-ins](#5-numbers-and-numeric-built-ins)
6. [Containers, slices, and binary data](#6-containers-slices-and-binary-data)
7. [Introspection, attributes, and object model](#7-introspection-attributes-and-object-model)
8. [Execution, namespaces, input, and files](#8-execution-namespaces-input-and-files)
9. [`itertools`: iterator pipelines](#9-itertools-iterator-pipelines)
10. [`functools`: reusable functional tools](#10-functools-reusable-functional-tools)
11. [`operator`: functions for operations](#11-operator-functions-for-operations)
12. [`collections` and `collections.abc`](#12-collections-and-collectionsabc)
13. [`heapq`, `bisect`, and `array`](#13-heapq-bisect-and-array)
14. [`dataclasses`, `enum`, `typing`, and `abc`](#14-dataclasses-enum-typing-and-abc)
15. [`pathlib`, `os`, `glob`, `shutil`, and `tempfile`](#15-pathlib-os-glob-shutil-and-tempfile)
16. [`re`: regular expressions](#16-re-regular-expressions)
17. [`json`, `csv`, and `tomllib`](#17-json-csv-and-tomllib)
18. [`datetime`, `zoneinfo`, and `time`](#18-datetime-zoneinfo-and-time)
19. [`math`, `statistics`, `decimal`, and `fractions`](#19-math-statistics-decimal-and-fractions)
20. [`random`, `secrets`, `hashlib`, `hmac`, and `uuid`](#20-random-secrets-hashlib-hmac-and-uuid)
21. [`contextlib`, `io`, and `copy`](#21-contextlib-io-and-copy)
22. [`logging`, `warnings`, and `argparse`](#22-logging-warnings-and-argparse)
23. [`sys`, `importlib`, and `subprocess`](#23-sys-importlib-and-subprocess)
24. [Concurrency: `concurrent.futures`, `threading`, and `asyncio`](#24-concurrency-concurrentfutures-threading-and-asyncio)
25. [`sqlite3`: a database without extra dependencies](#25-sqlite3-a-database-without-extra-dependencies)
26. [Inspection, debugging, profiling, and testing](#26-inspection-debugging-profiling-and-testing)
27. [More useful standard-library modules](#27-more-useful-standard-library-modules)
28. [Practical recipes](#28-practical-recipes)
29. [Pitfalls and decision guides](#29-pitfalls-and-decision-guides)
30. [Quick-reference index](#30-quick-reference-index)

---

# Part I — Built-in Functions

## 1. How to choose Python's built-in tools

Built-ins are best learned by **the problem they solve**, rather than alphabetically.

| Task | First tools to consider | Important distinction |
|---|---|---|
| Loop with row numbers | `enumerate()` | Avoid manual counters |
| Align two iterables | `zip()` | `strict=True` catches length mismatches |
| Transform iterable items | Comprehension, `map()` | Comprehensions are often easier to read |
| Keep matching items | Comprehension, `filter()` | Prefer a comprehension for nontrivial predicates |
| Check all/any conditions | `all()`, `any()` | Short-circuit; empty results differ |
| Order elements | `sorted()`, `list.sort()` | Copy vs. in-place mutation |
| Find extrema | `min()`, `max()` | `key=` customizes ordering |
| Build keyed collections | `dict()`, `set()`, `frozenset()` | Mapping vs. uniqueness vs. immutability |
| Inspect unknown objects | `type()`, `isinstance()`, `dir()`, `vars()` | Identity vs. inheritance vs. attributes |
| Access optional attribute | `getattr()` | Supply a default only for genuinely optional data |
| Handle files | `open()` | Use `with` for deterministic cleanup |
| Process lazily | `iter()`, `next()` | Iterators are generally consumed once |
| Compute quotient and remainder | `divmod()` | Returns both results in one expression |
| Build formatted strings | `format()`, f-strings | Formatting specifications are reusable |

### Iterables, iterators, and sequences

An **iterable** can produce an iterator. An **iterator** stores iteration state and supports `next()`. A **sequence** additionally supports indexing and generally has a length.

```python
values = [10, 20, 30]
iterator = iter(values)

first = next(iterator)
second = next(iterator)
remaining = list(iterator)

print(first, second, remaining)
```

Output: `10 20 [30]`.

- A `list` can be iterated over repeatedly.
- A generator object is usually a one-shot iterator.
- `iter(obj)` invokes the iteration protocol; `next(iterator)` requests another item.
- Exhaustion produces `StopIteration` unless a default is provided to `next()`.
- Iterator processing can save memory when input sizes are large.

```python
numbers = (n * n for n in range(5))
print(list(numbers))
print(list(numbers))
```

Output: `[0, 1, 4, 9, 16]`, then `[]`.

## 2. Iteration and sequence built-ins

### `len(obj)`

Return the number of elements in a sized object. For standard built-in containers, this is normally an `O(1)` operation; `len()` is not defined for a general generator or iterator unless that object also implements the length protocol.

```python
records = [{"id": 1}, {"id": 2}, {"id": 3}]

print(len(records))
print(len({"A": 1, "B": 2}))
print(len("Python"))
```

For a custom class, `len(instance)` delegates to `instance.__len__()`. Python expects a nonnegative integer length. Counting all the elements in a generator using `sum(1 for _ in generator)` **consumes** it.

### `enumerate(iterable, start=0)`

Yield pairs of `(index, value)` without maintaining your own counter.

```python
columns = ["customer_id", "balance", "status"]

for position, column in enumerate(columns, start=1):
    print(position, column)
```

**Choose it when:** reporting row positions, building indexes, or retaining a stable ordinal alongside each item. It returns an iterator, not a list.

### `zip(*iterables, strict=False)`

Combine iterables element by element. By default, `zip()` stops at the shortest iterable. Set `strict=True` when different lengths indicate a bug (Python 3.10+).

```python
names = ["Alice", "Bob", "Charlie"]
scores = [92, 85, 88]

records = list(zip(names, scores, strict=True))
score_by_name = dict(zip(names, scores, strict=True))

print(records)
print(score_by_name)
```

Unzip a list of pairs:

```python
pairs = [("a", 1), ("b", 2), ("c", 3)]
letters, numbers = zip(*pairs)

print(letters)
print(numbers)
```

`zip(*pairs)` on an empty list produces zero outputs, so direct unpacking fails; account for emptiness when it is possible.

### `map(function, iterable, ...)`

Apply a function lazily to each item. With multiple iterables, the function takes one argument from each and iteration stops at the shortest.

```python
raw_values = ["12", "17", "30"]
converted = list(map(int, raw_values))
print(converted)

pairs = list(map(pow, [2, 3, 4], [3, 2, 2]))
print(pairs)
```

Equivalent comprehension:

```python
raw_values = ["12", "17", "30"]
converted = [int(value) for value in raw_values]
print(converted)
```

**Guideline:** Use `map()` when an existing function exactly describes the transformation; otherwise prefer a comprehension for clarity.

### `filter(function, iterable)`

Lazily keep items for which the predicate returns truthy. If `function=None`, retain only truthy values.

```python
values = [0, 3, None, 5, "", 8]
nonempty = list(filter(None, values))
positive_even = list(filter(lambda x: x > 0 and x % 2 == 0, [1, 2, 3, 4, 6]))

print(nonempty)
print(positive_even)
```

Be careful: `filter(None, ...)` removes valid zeroes and `False` values, not just missing values.

### `iter(obj)` and `iter(callable, sentinel)`

The first form obtains an iterator. The second repeatedly calls a zero-argument function until its return value equals the sentinel; that sentinel value is omitted.

```python
from functools import partial
from io import BytesIO

source = BytesIO(b"abcdefghij")
chunks = list(iter(partial(source.read, 4), b""))

print(chunks)
```

Output: `[b'abcd', b'efgh', b'ij']`.

**Use case:** reading fixed-size chunks until EOF without writing a manual `while` loop.

### `next(iterator, default)`

Retrieve one item; optionally return a default if exhausted.

```python
transactions = iter([{"id": 101}, {"id": 102}])
first = next(transactions, None)
next(transactions, None)
missing = next(transactions, None)

print(first, missing)
```

To get the first matching item without creating a full list:

```python
records = [{"id": 1, "valid": False}, {"id": 2, "valid": True}]
first_valid = next((r for r in records if r["valid"]), None)
print(first_valid)
```

### `range(start, stop, step)`

Represent arithmetic integer sequences efficiently. `stop` is excluded; `range` is not a materialized list.

```python
print(list(range(5)))
print(list(range(2, 11, 2)))
print(list(range(10, 0, -3)))
print(1_000_000 in range(0, 2_000_000, 2))
```

Membership tests for an integer are efficient because `range` can check the arithmetic progression without iterating every member.

### `reversed(sequence)`

Return a reverse iterator for a reversible object without copying the underlying sequence.

```python
items = ["first", "middle", "last"]
print(list(reversed(items)))
```

For non-reversible iterators, materialize first if necessary: `reversed(list(iterator))`. This incurs memory use.

### `slice(start, stop, step)`

Store reusable slice specifications.

```python
values = [10, 20, 30, 40, 50, 60]
every_second = slice(None, None, 2)

print(values[every_second])
print("abcdef"[every_second])
print(slice(2, 100).indices(8))
```

`slice.indices(length)` normalizes the slice against a sequence length and yields `(start, stop, step)`.

### `aiter()` and `anext()`

Operate on asynchronous iterables and iterators (Python 3.10+). They relate to `async for` the way `iter()` and `next()` relate to `for`.

```python
import asyncio

async def produce():
    for value in (10, 20):
        yield value

async def main():
    iterator = aiter(produce())
    print(await anext(iterator, None))
    print(await anext(iterator, None))
    print(await anext(iterator, None))

asyncio.run(main())
```

Do not write `await aiter(...)`: `aiter()` returns an asynchronous iterator directly.

## 3. Aggregations, ordering, and comparisons

### `sum(iterable, start=0)`

Add numeric values with an optional starting value.

```python
amounts = [12.5, 7.5, 20.0]
print(sum(amounts))
print(sum(amounts, 100.0))
```

For improved accuracy with floating-point sums, consider `math.fsum()`. Avoid `sum(list_of_lists, [])` because repeated list concatenation is inefficient; use `itertools.chain.from_iterable()`.

### `min()` and `max()`

Find extrema using `key=` and optionally `default=` for the single-iterable form.

```python
accounts = [
    {"id": "A", "exposure": 120},
    {"id": "B", "exposure": 350},
    {"id": "C", "exposure": 200},
]

largest = max(accounts, key=lambda row: row["exposure"])
smallest = min(accounts, key=lambda row: row["exposure"])
empty_result = max([], default=None)

print(largest, smallest, empty_result)
```

`max(a, b, default=...)` is invalid: `default=` applies only when a single iterable argument is provided.

### `sorted(iterable, *, key=None, reverse=False)`

Return a new **list** in ascending order by default. Sorting is stable: equal keys retain their original order.

```python
records = [
    {"region": "West", "priority": 2},
    {"region": "East", "priority": 1},
    {"region": "West", "priority": 1},
]

result = sorted(records, key=lambda row: (row["region"], row["priority"]))
print(result)
```

Compare:

```python
values = [3, 1, 2]
new_list = sorted(values)
return_value = values.sort()

print(new_list)
print(values)
print(return_value)
```

`sorted()` returns a new list; `list.sort()` mutates in place and returns `None`. Both use a stable sorting algorithm with worst-case time complexity `O(n log n)`.

### `all()` and `any()`

- `all(iterable)`: `True` if every element is truthy; `all([])` is `True`.
- `any(iterable)`: `True` if at least one element is truthy; `any([])` is `False`.
- Both short-circuit and work well with generator expressions.

```python
statuses = ["complete", "complete", "pending"]

all_complete = all(value == "complete" for value in statuses)
any_pending = any(value == "pending" for value in statuses)

print(all_complete, any_pending)
```

**Subtle pitfall:** `all([])` being true does not mean a validation actually checked any records. If at least one record must exist, combine `bool(records)` with `all(...)`.

### `abs()` and `round()`

```python
print(abs(-13))
print(abs(3 + 4j))
print(round(12.345, 2))
print(round(2.5))
print(round(3.5))
```

Python's tie-breaking for `round()` uses **round half to even** for exact ties: `round(2.5)` is `2`; `round(3.5)` is `4`. Binary floating-point representation can make decimal-looking values behave unexpectedly. Use `Decimal` with an explicit rounding policy for financial rules.

## 4. Conversions, representation, and formatting

### `int()`, `float()`, `complex()`, and `bool()`

```python
print(int("1010", 2))
print(int("ff", 16))
print(float("3.14159"))
print(complex(2, -3))
print(bool([]), bool([0]))
```

`bool("False")` is `True` because a nonempty string is truthy. Do not parse textual booleans with `bool(text)`; compare normalized text against explicit accepted values.

### `str()`, `repr()`, and `ascii()`

- `str(obj)` emphasizes readable presentation.
- `repr(obj)` emphasizes unambiguous/debug-oriented representation.
- `ascii(obj)` is `repr`-like but escapes non-ASCII characters.

```python
value = "café"
print(str(value))
print(repr(value))
print(ascii(value))
```

`repr()` is not a serialization format. Do not rely on it for persistent or interoperable data.

### `format(value, format_spec)` and f-strings

```python
amount = 1_234_567.891
ratio = 0.1842

print(format(amount, ",.2f"))
print(f"{ratio:.1%}")
print(f"{amount:>16,.2f}")
print(f"{amount=:.2f}")
```

Common format specifications:

| Specification | Effect | Example |
|---|---|---|
| `.2f` | Two decimals, fixed-point | `f"{3.14159:.2f}"` |
| `.3g` | Three significant digits | `f"{12345:.3g}"` |
| `,.0f` | Group thousands, zero decimals | `f"{12345:,.0f}"` |
| `.1%` | Multiply by 100 and add `%` | `f"{0.256:.1%}"` |
| `>12` | Right-align in width 12 | `f"{'A':>12}"` |
| `<12` | Left-align in width 12 | `f"{'A':<12}"` |
| `^12` | Center in width 12 | `f"{'A':^12}"` |
| `08d` | Zero-pad integer to width 8 | `f"{42:08d}"` |
| `#x` | Hexadecimal including prefix | `f"{255:#x}"` |
| `!r` | Use `repr()` in an f-string | `f"{value!r}"` |

### `ord()` and `chr()`

Convert a Unicode character to its code point and back.

```python
code_point = ord("A")
character = chr(9731)

print(code_point)
print(character)
```

A Unicode code point is not necessarily a complete human-perceived character; combining marks and multi-code-point emoji exist.

### `bin()`, `oct()`, and `hex()`

Represent integers in binary, octal, and hexadecimal.

```python
value = 255
print(bin(value))
print(oct(value))
print(hex(value))
print(f"{value:08b}")
```

### `bytes()`, `bytearray()`, and encoding

```python
text = "résumé"
encoded = text.encode("utf-8")
decoded = encoded.decode("utf-8")
mutable = bytearray(b"ABC")
mutable[0] = 90

print(encoded, decoded, mutable)
```

Text (`str`) and bytes (`bytes`) are fundamentally different types. Encode at text-to-bytes boundaries and decode at bytes-to-text boundaries.

## 5. Numbers and numeric built-ins

### `divmod(a, b)`

Return `(a // b, a % b)` as a tuple.

```python
minutes = 137
hours, remaining_minutes = divmod(minutes, 60)
print(hours, remaining_minutes)
```

For negative numbers, Python floor division rounds toward negative infinity; the remainder follows `a == (a // b) * b + (a % b)`.

### `pow(base, exp, mod=None)`

Two arguments calculate exponentiation. Three arguments compute modular exponentiation efficiently for integers.

```python
print(pow(2, 10))
print(pow(7, 128, 13))
print(7 ** 128 % 13)
```

The three-argument form avoids explicitly constructing a potentially enormous intermediate power. Python also supports a modular inverse using `pow(a, -1, modulus)` when the inverse exists.

### `hash(obj)`

Return an integer hash for hashable objects. Hashes support dictionary keys and sets.

```python
key = ("CA", 2026, 10)
print(hash(key))
print({key: "ready"}[key])
```

Never treat `hash()` as cryptographic hashing or a stable identifier across Python processes. Hash values for some types are intentionally randomized between runs.

### `sum()` vs. `math.fsum()` vs. `statistics.mean()`

```python
import math
import statistics

values = [0.1, 0.1, 0.1]

print(sum(values))
print(math.fsum(values))
print(statistics.mean(values))
```

These have different goals: accumulation, more accurate floating-point accumulation, and arithmetic average.

## 6. Containers, slices, and binary data

### `list()`, `tuple()`, `set()`, `frozenset()`, `dict()`

```python
values = ["a", "b", "a"]

print(list(values))
print(tuple(values))
print(set(values))
print(frozenset(values))
print(dict([("A", 1), ("B", 2)]))
```

| Type | Ordered iteration? | Mutable? | Duplicate items? | Can be a dictionary key? |
|---|---|---|---|---|
| `list` | Yes | Yes | Yes | No |
| `tuple` | Yes | No | Yes | Only if all elements hashable |
| `dict` | Insertion order | Yes | Keys unique | No |
| `set` | No ordering guarantee | Yes | No | No |
| `frozenset` | No ordering guarantee | No | No | Yes, if elements hashable |

`set` should not be used as a substitute for order-preserving deduplication. Use `dict.fromkeys(iterable)` when elements are hashable and original order must be retained.

```python
items = ["x", "y", "x", "z", "y"]
unique_in_order = list(dict.fromkeys(items))
print(unique_in_order)
```

### `memoryview()`

Create a zero-copy view over suitable binary buffers. The view holds a reference to its underlying buffer and can expose portions without copying.

```python
buffer = bytearray(b"abcdefgh")
view = memoryview(buffer)
segment = view[2:5]
segment[0] = ord("Z")

print(buffer)
print(bytes(segment))
```

A writable view requires a writable underlying buffer; `memoryview(bytes_obj)` is read-only. This is useful for binary protocols and high-throughput buffer handling.

### `object()`

Create a distinct sentinel when `None` is a legitimate value.

```python
MISSING = object()

record = {"name": None}
value = record.get("name", MISSING)

if value is MISSING:
    print("Key not present")
else:
    print("Key present", value)
```

Sentinels distinguish **missing** from **explicitly supplied `None`**.

## 7. Introspection, attributes, and object model

### `type()`, `isinstance()`, and `issubclass()`

```python
class Animal:
    pass

class Dog(Animal):
    pass

pet = Dog()

print(type(pet) is Dog)
print(isinstance(pet, Animal))
print(issubclass(Dog, Animal))
```

- `type(obj)` returns an object's concrete type.
- `isinstance(obj, Class)` respects inheritance and some runtime-defined type protocols.
- `issubclass(Sub, Base)` checks class relationships.
- Prefer `isinstance()` over exact `type(...) is ...` when subclass compatibility is intended.

### `getattr()`, `setattr()`, `hasattr()`, and `delattr()`

```python
class Settings:
    pass

settings = Settings()
setattr(settings, "batch_size", 100)

print(getattr(settings, "batch_size"))
print(getattr(settings, "timeout", 30))
print(hasattr(settings, "batch_size"))

delattr(settings, "batch_size")
print(hasattr(settings, "batch_size"))
```

`hasattr(obj, name)` effectively attempts attribute access and suppresses `AttributeError`. It may execute properties or other custom access logic; it does not merely inspect a static attribute table.

### `dir()` and `vars()`

```python
class Model:
    category = "risk"

    def __init__(self, name):
        self.name = name

model = Model("baseline")

print(vars(model))
print("category" in dir(model))
```

- `dir(obj)` returns suggested attribute names including inherited members.
- `vars(obj)` returns `obj.__dict__` when present; not every object has one, particularly slot-based objects.
- `vars()` without arguments accesses the current local namespace dictionary.

### `id()` and `is`

```python
first = [1, 2]
second = first
third = [1, 2]

print(first is second)
print(first is third)
print(first == third)
print(id(first))
```

`is` checks object identity; `==` checks equality. Do not use identity tests for equality of strings, numbers, or collections. Use `is None` when checking the singleton `None`.

### `callable()`

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return value * self.factor

operation = Multiplier(3)
print(callable(operation))
print(operation(7))
```

A callable can be a function, class, method, or instance implementing `__call__`.

### `super()`

Delegate to a parent or next class in the method resolution order (MRO).

```python
class BaseProcessor:
    def execute(self):
        return ["base"]

class AuditProcessor(BaseProcessor):
    def execute(self):
        steps = super().execute()
        return [*steps, "audit"]

print(AuditProcessor().execute())
```

In multiple inheritance, `super()` follows the MRO, not necessarily a single lexical parent.

### `property()`, `classmethod()`, and `staticmethod()`

```python
class Account:
    currency = "CAD"

    def __init__(self, cents):
        self._cents = cents

    @property
    def balance(self):
        return self._cents / 100

    @classmethod
    def from_dollars(cls, amount):
        return cls(round(amount * 100))

    @staticmethod
    def is_valid_amount(amount):
        return amount >= 0

account = Account.from_dollars(19.99)
print(account.balance)
print(Account.is_valid_amount(19.99))
```

| Decorator | Receives | Typical role |
|---|---|---|
| `@property` | `self` | Computed/controlled instance attribute |
| `@classmethod` | `cls` | Alternative constructors; subclass-aware factories |
| `@staticmethod` | No automatic `self` or `cls` | Utility function logically grouped with class |

Property setters are possible using `@balance.setter`. Prefer regular methods when access performs surprising, slow, or expensive work.

### `object.__class__`, `__dict__`, and class MRO

```python
class A:
    pass

class B(A):
    pass

instance = B()

print(instance.__class__)
print(B.__mro__)
print(B.mro())
```

`__mro__` shows the order used for method lookup. Python's standard `inspect` module provides additional tools in Part II.

## 8. Execution, namespaces, input, and files

### `open()`

Use a context manager to guarantee resource cleanup under normal exits and exceptions.

```python
from pathlib import Path

path = Path("example.txt")

with open(path, "w", encoding="utf-8") as file:
    file.write("alpha\nbeta\n")

with open(path, "r", encoding="utf-8") as file:
    lines = [line.rstrip("\n") for line in file]

print(lines)
path.unlink()
```

Common file modes:

| Mode | Meaning |
|---|---|
| `r` | Read text; file must exist |
| `w` | Write text; truncate/create |
| `a` | Append text; create if needed |
| `x` | Exclusive create; fail if exists |
| `rb` | Read binary |
| `wb` | Write binary |
| `r+` | Read and write without automatic truncation |
| `w+` | Read and write; truncate/create |

Use `encoding="utf-8"` for portable text operations. For CSV, `newline=""` matters; see the CSV section.

### `print(*objects, sep=" ", end="\n", file=None, flush=False)`

```python
from io import StringIO

buffer = StringIO()
print("A", "B", "C", sep="|", end="\n", file=buffer)
print(buffer.getvalue())
```

For production diagnostics, prefer `logging` over ad hoc `print()` statements.

### `input(prompt="")`

```python
name = input("Enter a name: ")
print(f"Hello, {name}")
```

`input()` always returns a string (or raises `EOFError`). Validate and convert user input explicitly. This interactive example requires console input.

### `globals()` and `locals()`

Inspect the current namespace mappings.

```python
threshold = 10

def check(value):
    adjusted = value + 2
    return {"local_names": sorted(locals()), "passes": adjusted >= threshold}

print(check(9))
print("threshold" in globals())
```

Do not depend on mutating `locals()` to update function-local variables; its write-back behavior is not a general-purpose assignment mechanism.

### `eval()`, `exec()`, and `compile()`

- `eval(expression)` evaluates an expression and returns its value.
- `exec(source)` executes statements and returns `None`.
- `compile(source, filename, mode)` compiles source for subsequent execution (`mode` commonly `"eval"` or `"exec"`).

```python
expression = compile("2 * (3 + 4)", "<expression>", "eval")
print(eval(expression))

namespace = {}
exec("result = 2 ** 5", namespace)
print(namespace["result"])
```

**Security:** Never pass untrusted input to `eval()` or `exec()`. Providing restricted `globals` is **not** a reliable sandbox. For literal Python data structures, use `ast.literal_eval()`; for interoperable input, prefer JSON.

```python
import ast

parsed = ast.literal_eval("{'ids': [1, 2], 'enabled': True}")
print(parsed)
```

`ast.literal_eval()` does not run arbitrary expressions, but sufficiently large or maliciously complex inputs can still exhaust resources. Treat untrusted input sizes carefully.

### `breakpoint()` and `help()`

- `breakpoint()` enters the configured debugger, commonly `pdb`, when the environment supports it.
- `help(obj)` opens built-in interactive documentation.
- `__import__()` is Python's low-level import hook; use `importlib.import_module()` for ordinary dynamic imports.

### Built-in exceptions and exception handling

```python
def safe_parse_integer(text):
    try:
        return int(text)
    except ValueError:
        return None

print(safe_parse_integer("42"))
print(safe_parse_integer("unknown"))
```

Know these common built-in exception classes: `TypeError`, `ValueError`, `KeyError`, `IndexError`, `AttributeError`, `FileNotFoundError`, `OSError`, `StopIteration`, `RuntimeError`, `NotImplementedError`, `ZeroDivisionError`, `OverflowError`, `TimeoutError`, `PermissionError`, and `AssertionError`.

Use `raise ... from exc` to preserve an underlying cause when translating exceptions:

```python
def parse_count(text):
    try:
        return int(text)
    except ValueError as exc:
        raise ValueError(f"Invalid count: {text!r}") from exc
```

### Other built-ins worth recognizing

| Built-in | Purpose | Example |
|---|---|---|
| `enumerate` | Pair indices and values | `enumerate(rows, 1)` |
| `zip` | Align iterables | `zip(names, values, strict=True)` |
| `iter` | Obtain iterator | `iter(items)` |
| `next` | Advance iterator | `next(it, None)` |
| `all` / `any` | Quantify predicates | `all(x > 0 for x in xs)` |
| `sorted` | New sorted list | `sorted(xs, key=len)` |
| `reversed` | Reverse iterator | `reversed(items)` |
| `divmod` | Quotient and remainder | `divmod(125, 60)` |
| `pow` | Exponentiation or modular power | `pow(2, 10, 17)` |
| `getattr` | Dynamic attribute lookup | `getattr(obj, "name", None)` |
| `setattr` | Dynamic attribute assignment | `setattr(obj, "name", "A")` |
| `hasattr` | Test access to attribute | `hasattr(obj, "run")` |
| `callable` | Test callability | `callable(obj)` |
| `vars` | Instance namespace | `vars(instance)` |
| `dir` | Attribute-name exploration | `dir(instance)` |
| `isinstance` | Inheritance-aware type check | `isinstance(x, str)` |
| `issubclass` | Class ancestry check | `issubclass(bool, int)` |
| `memoryview` | Memory-sharing binary view | `memoryview(buffer)` |
| `frozenset` | Immutable set | `frozenset({1, 2})` |
| `ascii` | ASCII-safe representation | `ascii("café")` |
| `chr` / `ord` | Code points ↔ characters | `chr(65)` / `ord("A")` |
| `format` | Formatting protocol | `format(3.14, ".1f")` |
| `slice` | Reusable slice | `slice(1, None, 2)` |
| `aiter` / `anext` | Async iteration | `await anext(it, None)` |
| `breakpoint` | Enter debugger | `breakpoint()` |
| `compile` | Compile source | `compile("1+2", "<x>", "eval")` |
| `property` | Managed attribute | `@property` |
| `classmethod` | Class-bound method | `@classmethod` |
| `staticmethod` | Class-namespaced function | `@staticmethod` |

---

# Part II — The Standard Library

## 9. `itertools`: iterator pipelines

`itertools` contains composable, generally lazy iterator operations. It is especially useful when you want to avoid intermediate lists.

### `chain()` and `chain.from_iterable()`

Flatten **one level** of nesting or concatenate independent iterables.

```python
from itertools import chain

combined = list(chain([1, 2], [3, 4], [5]))
nested = [[1, 2], [], [3, 4]]
flattened = list(chain.from_iterable(nested))

print(combined)
print(flattened)
```

### `islice(iterable, start, stop, step)`

Perform slice-like selection on an iterator.

```python
from itertools import count, islice

first_five = list(islice(count(10, 3), 5))
every_third = list(islice(range(20), 0, 15, 3))

print(first_five)
print(every_third)
```

`islice()` consumes the underlying iterator as needed. It does not provide random access or support negative slice arguments.

### `batched(iterable, n)` (Python 3.12+)

Group an iterable into tuples of up to `n` elements.

```python
from itertools import batched

batches = list(batched(range(11), 4))
print(batches)
```

Output: `[(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10)]`. Python 3.13+ adds `strict=True` to require every batch to have exactly `n` elements.

For Python 3.11, an equivalent pattern is:

```python
from itertools import islice

def batches(iterable, size):
    iterator = iter(iterable)
    while chunk := tuple(islice(iterator, size)):
        yield chunk

print(list(batches(range(11), 4)))
```

### `groupby(iterable, key=None)`

Group **consecutive** values with the same key. Unlike pandas `groupby()`, it does not automatically collect nonadjacent rows into the same group; sort first if global grouping is intended.

```python
from itertools import groupby

rows = [
    {"region": "West", "sales": 15},
    {"region": "East", "sales": 10},
    {"region": "West", "sales": 20},
]

rows.sort(key=lambda r: r["region"])
totals = {
    region: sum(item["sales"] for item in group)
    for region, group in groupby(rows, key=lambda r: r["region"])
}

print(totals)
```

Each `group` shares the underlying iterator; consume it before advancing to the next group.

### `accumulate(iterable, func=operator.add, *, initial=None)`

Yield running aggregates.

```python
from itertools import accumulate
from operator import mul

print(list(accumulate([10, -3, 4, 2])))
print(list(accumulate([2, 3, 4], mul)))
print(list(accumulate([10, 20], initial=100)))
```

### `pairwise(iterable)` (Python 3.10+)

Yield overlapping consecutive pairs.

```python
from itertools import pairwise

balances = [100, 115, 105, 130]
changes = [current - previous for previous, current in pairwise(balances)]
print(changes)
```

### `product()`, `permutations()`, and `combinations()`

```python
from itertools import combinations, combinations_with_replacement, permutations, product

print(list(product(["A", "B"], [1, 2])))
print(list(permutations(["A", "B", "C"], 2)))
print(list(combinations(["A", "B", "C"], 2)))
print(list(combinations_with_replacement(["A", "B"], 2)))
```

- `product`: Cartesian product; order and repetitions are meaningful.
- `permutations`: ordered selections without reusing positions.
- `combinations`: unordered selections without reusing positions.
- `combinations_with_replacement`: unordered selections allowing repetition.

Combinatorial output grows extremely quickly; avoid materializing huge products in a list.

### `compress()`, `takewhile()`, `dropwhile()`, `filterfalse()`

```python
from itertools import compress, dropwhile, filterfalse, takewhile

print(list(compress("ABCDE", [1, 0, 1, 0, 1])))
print(list(takewhile(lambda x: x < 4, [1, 3, 5, 2])))
print(list(dropwhile(lambda x: x < 4, [1, 3, 5, 2])))
print(list(filterfalse(lambda x: x % 2, range(7))))
```

`takewhile()` and `dropwhile()` depend on the **first transition**, not a global predicate over all values.

### `count()`, `cycle()`, `repeat()`, and `starmap()`

```python
from itertools import count, cycle, islice, repeat, starmap

print(list(islice(count(100, 10), 4)))
print(list(islice(cycle(["A", "B"]), 5)))
print(list(repeat("ready", 3)))
print(list(starmap(pow, [(2, 3), (3, 2), (4, 2)])))
```

`count()` and `cycle()` can generate infinite sequences. Pair them with finite consumers such as `islice()`.

### `tee(iterable, n=2)`

```python
from itertools import tee

first, second = tee(x * x for x in range(4))
print(list(first))
print(list(second))
```

`tee()` may buffer values when consumers advance at different speeds. It is not free duplication and is not a thread-safety mechanism.

## 10. `functools`: reusable functional tools

### `lru_cache(maxsize=128)`

Memoize function results. Useful for repeated deterministic calculations.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(35))
print(fibonacci.cache_info())
fibonacci.cache_clear()
```

Cache keys must be hashable, and cached values remain held until evicted or cleared. A cache can return stale data when a function depends on mutable external state.

### `cache`

`@cache` (Python 3.9+) is equivalent to an unbounded `lru_cache(maxsize=None)`.

```python
from functools import cache

@cache
def triangular(n):
    if n <= 1:
        return n
    return n + triangular(n - 1)

print(triangular(100))
```

### `cached_property`

Compute an attribute on first access and store the result on the instance.

```python
from functools import cached_property

class Dataset:
    def __init__(self, values):
        self.values = values

    @cached_property
    def total(self):
        print("Computing total")
        return sum(self.values)

dataset = Dataset([1, 2, 3])
print(dataset.total)
print(dataset.total)
```

Cached values are not automatically invalidated if dependencies change. Delete `dataset.total` to trigger recomputation on the next access. Standard usage requires an instance with a writable `__dict__`.

### `partial()` and `partialmethod()`

Bind selected arguments ahead of time.

```python
from functools import partial, partialmethod

parse_binary = partial(int, base=2)
print(parse_binary("101101"))

class Processor:
    def send(self, channel, message):
        return f"{channel}: {message}"

    send_alert = partialmethod(send, "alerts")

print(Processor().send_alert("Job failed"))
```

### `reduce()`

Cumulatively combine values into a single result.

```python
from functools import reduce
from operator import mul

factorial_five = reduce(mul, range(1, 6), 1)
print(factorial_five)
```

Prefer `sum()`, `math.prod()`, `any()`, `all()`, or clearer loops when they express the intended operation directly.

### `wraps()`

Preserve wrapped-function metadata when defining decorators.

```python
from functools import wraps

def uppercase_result(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs).upper()
    return wrapper

@uppercase_result
def greet(name):
    return f"Hello, {name}"

print(greet("Ada"))
print(greet.__name__)
```

`wraps()` also creates a `__wrapped__` reference, useful for inspection and tooling.

### `singledispatch()`

Register implementations based on the type of the **first argument**.

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
    return [normalize(item) for item in value]

print(normalize("  READY  "))
print(normalize([" A ", " B "]))
```

`singledispatchmethod` provides a method-oriented counterpart. Dispatch is not based on every parameter and is not a full multiple-dispatch system.

### `total_ordering()`

With `__eq__` and one of `__lt__`, `__le__`, `__gt__`, or `__ge__`, generate remaining rich comparison methods. Convenient for custom ordered types, though writing all comparisons can be faster.

## 11. `operator`: functions for operations

The `operator` module exposes common operators as functions. Its biggest practical advantage is concise, efficient key extraction.

### `itemgetter()`, `attrgetter()`, and `methodcaller()`

```python
from operator import attrgetter, itemgetter, methodcaller

records = [
    {"name": "A", "score": 3},
    {"name": "B", "score": 1},
]

print(sorted(records, key=itemgetter("score")))
print(list(map(itemgetter("name"), records)))
print(list(map(methodcaller("strip"), ["  a ", " b  "])))
```

```python
from dataclasses import dataclass
from operator import attrgetter

@dataclass
class Trade:
    desk: str
    exposure: float

trades = [Trade("B", 200), Trade("A", 100)]
print(sorted(trades, key=attrgetter("desk", "exposure")))
```

`itemgetter("a", "b")` returns a tuple, making it useful for multi-column sorting. `attrgetter("address.city")` supports dotted attribute access.

### Arithmetic, comparison, and membership functions

```python
from operator import add, eq, floordiv, mul, truediv, contains

print(add(2, 3))
print(mul(4, 5))
print(truediv(7, 2))
print(floordiv(7, 2))
print(eq("A", "A"))
print(contains([1, 2, 3], 2))
```

Common choices: `add`, `sub`, `mul`, `truediv`, `floordiv`, `mod`, `pow`, `eq`, `ne`, `lt`, `le`, `gt`, `ge`, `and_`, `or_`, `xor`, `not_`, `is_`, `is_not`, `contains`, `getitem`.

Do not confuse bitwise `operator.and_` and `operator.or_` with the short-circuiting logical keywords `and` and `or`.

## 12. `collections` and `collections.abc`

### `Counter`

Count occurrences, inspect frequencies, and perform multiset operations.

```python
from collections import Counter

statuses = ["success", "failed", "success", "pending", "success", "failed"]
counts = Counter(statuses)

print(counts)
print(counts.most_common(2))
print(counts["unknown"])
print(counts.total())
```

`counts["unknown"]` returns zero without inserting a new key. `Counter.total()` requires Python 3.10+.

### `defaultdict`

Automatically create missing dictionary values through a factory.

```python
from collections import defaultdict

rows = [
    ("East", 10),
    ("West", 20),
    ("East", 15),
]

grouped = defaultdict(list)
totals = defaultdict(float)

for region, amount in rows:
    grouped[region].append(amount)
    totals[region] += amount

print(dict(grouped))
print(dict(totals))
```

**Pitfall:** `mapping[key]` creates missing entries; `mapping.get(key)` does not invoke the default factory.

### `deque`

Efficient append/pop at both ends; ideal for queues and fixed-size rolling windows.

```python
from collections import deque

queue = deque(["first", "second"])
queue.append("third")
queue.appendleft("urgent")

print(queue.popleft())
print(queue.pop())

recent = deque(maxlen=3)
recent.extend([1, 2, 3, 4, 5])
print(list(recent))
```

A list's `pop(0)` is generally `O(n)` because later elements shift. `deque.popleft()` is approximately `O(1)`.

### `namedtuple`

Create lightweight tuple subclasses with named fields.

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
point = Point(10, 20)

print(point.x)
print(point[1])
print(point._asdict())
print(point._replace(x=99))
```

Use a dataclass for richer object behavior; use `NamedTuple` from `typing` when annotation-oriented tuple records are desired.

### `ChainMap`

View multiple mappings as one lookup scope. Earlier mappings take precedence.

```python
from collections import ChainMap

defaults = {"timeout": 30, "retries": 3}
overrides = {"timeout": 10}
config = ChainMap(overrides, defaults)

print(config["timeout"])
print(config["retries"])
```

Writes target the first mapping by default. This is a view, not necessarily a fully merged copy.

### `collections.abc`

Use abstract base classes to describe collection protocols at runtime.

```python
from collections.abc import Iterable, Iterator, Mapping, MutableMapping, Sequence

print(isinstance([1, 2], Sequence))
print(isinstance({"x": 1}, Mapping))
print(isinstance(iter([1, 2]), Iterator))
print(isinstance((x for x in range(3)), Iterable))
```

Important interfaces include `Iterable`, `Iterator`, `Generator`, `Sequence`, `MutableSequence`, `Mapping`, `MutableMapping`, `Set`, `MutableSet`, `Collection`, and `Callable`.

### `OrderedDict`

Since normal dictionaries preserve insertion order, `OrderedDict` is usually not needed for basic ordering. It still has specialized operations such as `move_to_end()` and order-sensitive equality between two `OrderedDict` instances.

## 13. `heapq`, `bisect`, and `array`

### `heapq`

Maintain a min-heap to retrieve the smallest item efficiently.

```python
import heapq

priorities = [8, 2, 7, 1, 5]
heapq.heapify(priorities)
heapq.heappush(priorities, 3)

print(heapq.heappop(priorities))
print(heapq.nsmallest(3, priorities))
print(heapq.nlargest(2, priorities))
```

Typical operation costs: `heapify` is `O(n)`; `heappush`/`heappop` are `O(log n)`; inspecting `heap[0]` is `O(1)`. A heap is **not** a globally sorted list.

Priority queue with a tie-breaking counter:

```python
import heapq
from itertools import count

queue = []
sequence = count()

heapq.heappush(queue, (1, next(sequence), "urgent-task"))
heapq.heappush(queue, (2, next(sequence), "normal-task"))
heapq.heappush(queue, (1, next(sequence), "another-urgent-task"))

print([heapq.heappop(queue)[2] for _ in range(len(queue))])
```

### `bisect`

Binary-search insertion positions in a **sorted** list.

```python
from bisect import bisect_left, bisect_right, insort

thresholds = [10, 20, 20, 30]
print(bisect_left(thresholds, 20))
print(bisect_right(thresholds, 20))

insort(thresholds, 25)
print(thresholds)
```

Searching is `O(log n)`, but inserting into a list remains `O(n)` because elements may shift. `bisect` uses ordering (`<`) rather than checking equality directly.

### `array`

Typed arrays compactly store many primitive values of one C-compatible type.

```python
from array import array

values = array("d", [1.5, 2.5, 3.5])
values.append(4.5)

print(values.tolist())
print(values.itemsize)
```

Compared with NumPy, `array` has a much smaller feature set; it is useful when you need standard-library-only packed numeric storage.

## 14. `dataclasses`, `enum`, `typing`, and `abc`

These modules make interfaces and object models more explicit without third-party dependencies.

### `dataclasses.dataclass`

Automatically generate commonly needed methods such as `__init__`, `__repr__`, and `__eq__` for classes describing structured data.

```python
from dataclasses import dataclass, field

@dataclass(slots=True)
class ModelConfig:
    name: str
    horizon: int = 12
    tags: list[str] = field(default_factory=list)

config = ModelConfig("baseline")
config.tags.append("approved")
print(config)
```

Why `default_factory`? A fresh mutable list is created for each instance. Mutable values should not be shared accidentally across instances.

Useful dataclass options:

| Option | Effect |
|---|---|
| `frozen=True` | Prevent ordinary assignment to fields; not deeply immutable |
| `slots=True` | Generate slots, often reducing instance memory (Python 3.10+) |
| `order=True` | Generate ordering comparisons based on fields |
| `kw_only=True` | Make fields keyword-only (Python 3.10+) |
| `repr=False` on field | Exclude specific field from generated `repr` |
| `compare=False` on field | Exclude field from generated equality/order |
| `init=False` on field | Exclude field from generated constructor |

### `__post_init__`, `InitVar`, and `replace()`

```python
from dataclasses import InitVar, dataclass, field, replace

@dataclass(frozen=True)
class Position:
    units: float
    price: float
    scale: InitVar[float] = 1.0
    market_value: float = field(init=False)

    def __post_init__(self, scale):
        object.__setattr__(self, "market_value", self.units * self.price * scale)

position = Position(10, 25, scale=1.2)
updated = replace(position, units=12)

print(position)
print(updated)
```

`replace()` constructs a new instance and reruns initialization. `asdict()` recursively converts nested dataclasses and also recursively processes built-in containers; it is not a guaranteed zero-copy operation.

### `enum.Enum`, `IntEnum`, and `StrEnum`

Enums name a finite set of allowed constants.

```python
from enum import Enum, StrEnum, auto

class Status(Enum):
    PENDING = 1
    COMPLETED = 2

class Environment(StrEnum):
    DEV = auto()
    PROD = auto()

print(Status.PENDING.name)
print(Status.PENDING.value)
print(Environment.DEV.value)
```

`StrEnum` was added in Python 3.11. Prefer regular `Enum` when you want distinct symbolic values without implicit integer/string interchangeability.

### `typing`: type hints for interfaces

Type hints support static analysis and editor tooling; they do not automatically enforce types at runtime.

```python
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Literal, TypedDict

class Record(TypedDict):
    id: int
    balance: float

def aggregate(
    records: Sequence[Record],
    transform: Callable[[float], float],
    mode: Literal["sum", "max"] = "sum",
) -> float:
    values = [transform(record["balance"]) for record in records]
    return sum(values) if mode == "sum" else max(values, default=0.0)

rows: list[Record] = [{"id": 1, "balance": 10.0}]
print(aggregate(rows, abs))
```

Know these distinctions:

| Annotation | Intended meaning |
|---|---|
| `Iterable[T]` | Can be traversed; possibly one-pass |
| `Iterator[T]` | Can be advanced with `next()`; one-pass behavior |
| `Sequence[T]` | Ordered, indexable, sized, read-oriented interface |
| `Mapping[K, V]` | Read-only mapping interface |
| `MutableMapping[K, V]` | Mapping supporting mutation |
| `Callable[[A], B]` | A callable accepting `A` and returning `B` |
| `T | None` | `T` or `None` |
| `Literal["a", "b"]` | Specific permitted literal values |
| `TypedDict` | Expected keys and value types of dictionaries |
| `Protocol` | Structural typing based on supported members |
| `TypeVar` | A type variable expressing relationships |
| `Self` | Current enclosing class type (Python 3.11+) |
| `Annotated[T, metadata]` | Type with extra metadata for cooperating tools |
| `ClassVar[T]` | Intended class-level variable |
| `Final[T]` | Intended prohibition on reassignment by type checker |

### `Protocol`: structural interfaces

```python
from typing import Protocol

class Executable(Protocol):
    def execute(self) -> int:
        ...

class Task:
    def execute(self) -> int:
        return 1

def run_task(task: Executable) -> int:
    return task.execute()

print(run_task(Task()))
```

A class does not have to inherit `Executable` to satisfy this interface for static type checking. For runtime `isinstance` checks, decorate a protocol with `@runtime_checkable`, recognizing that runtime checks only examine limited structural presence rather than full type signatures.

### `TypeVar`, generics, and `Self`

```python
from typing import Self, TypeVar

T = TypeVar("T")

def first_or_default(items: list[T], default: T) -> T:
    return items[0] if items else default

class Builder:
    def __init__(self):
        self.items = []

    def add(self, item: str) -> Self:
        self.items.append(item)
        return self

print(first_or_default([3, 4], 0))
print(Builder().add("a").add("b").items)
```

Python 3.12+ also supports newer generic parameter syntax such as `def first[T](...)`; the `TypeVar` form is useful across a wider range of Python versions.

### `abc.ABC` and `abstractmethod`

```python
from abc import ABC, abstractmethod

class Reader(ABC):
    @abstractmethod
    def load(self, source: str) -> bytes:
        raise NotImplementedError

class FileReader(Reader):
    def load(self, source: str) -> bytes:
        from pathlib import Path
        return Path(source).read_bytes()

print(issubclass(FileReader, Reader))
```

Use an ABC when you need an explicit inheritance-based contract and possibly shared implementation. Use a `Protocol` when consumer code should accept structurally compatible implementations without inheritance.

## 15. `pathlib`, `os`, `glob`, `shutil`, and `tempfile`

### `pathlib.Path`

`Path` is generally the most convenient interface for path manipulation in modern Python.

```python
from pathlib import Path

base = Path("data")
path = base / "raw" / "transactions.csv"

print(path.name)
print(path.stem)
print(path.suffix)
print(path.parent)
print(path.with_suffix(".parquet"))
```

Useful `Path` methods:

| Method | Purpose |
|---|---|
| `exists()` | Test existence |
| `is_file()` / `is_dir()` | Test file or directory |
| `mkdir(parents=True, exist_ok=True)` | Create directory tree |
| `iterdir()` | Iterate direct children |
| `glob(pattern)` | Match descendants by pattern |
| `rglob(pattern)` | Recursive pattern search |
| `read_text()` / `write_text()` | Read/write text |
| `read_bytes()` / `write_bytes()` | Read/write bytes |
| `resolve()` | Produce a resolved absolute path |
| `relative_to()` | Express relative to another path (raises if not relative) |
| `with_name()` / `with_suffix()` | Construct modified paths |
| `rename()` / `replace()` | Move/rename an entry |
| `unlink()` | Remove a file |
| `stat()` | Get file metadata |

### Safe create/read/list using temporary directories

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    root = Path(directory)
    (root / "raw").mkdir()
    (root / "raw" / "a.txt").write_text("alpha", encoding="utf-8")
    (root / "raw" / "b.txt").write_text("beta", encoding="utf-8")

    paths = sorted((root / "raw").glob("*.txt"))
    contents = {path.name: path.read_text(encoding="utf-8") for path in paths}
    print(contents)
```

Use `pathlib` for path objects and common operations; use `os` for process/environment operations and lower-level filesystem features.

### `os` and `os.environ`

```python
import os

home = os.getenv("HOME")
process_id = os.getpid()
path_entries = os.get_exec_path()

print(home is not None)
print(process_id > 0)
print(len(path_entries) > 0)
```

`os.getenv(name, default)` reads an environment variable. `os.environ` is a mutable mapping of environment variables for the current process.

Do not store sensitive values in logs simply because they came from environment variables.

### `glob`

```python
from glob import glob

matches = glob("src/**/*.py", recursive=True)
print(sorted(matches)[:10])
```

`glob.glob()` returns path strings, whereas `Path.glob()` returns `Path` objects. Ordering from globbing is not guaranteed; sort results when determinism matters.

### `shutil`

High-level file/directory copy, move, and deletion operations.

```python
from pathlib import Path
from shutil import copy2, make_archive
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    root = Path(directory)
    source = root / "input.txt"
    target = root / "copy.txt"
    source.write_text("dataset", encoding="utf-8")

    copy2(source, target)
    archive = make_archive(str(root / "backup"), "zip", root_dir=root)

    print(target.read_text(encoding="utf-8"))
    print(Path(archive).exists())
```

- `copy()` copies file data and permissions.
- `copy2()` attempts to preserve additional metadata.
- `copytree()` copies a directory tree.
- `move()` moves files or directories.
- `rmtree()` recursively removes a directory tree; be extremely careful with path selection.
- `disk_usage()` reports total/used/free disk space.
- `which()` finds an executable on `PATH`.

### `tempfile`

Use `TemporaryDirectory` or `NamedTemporaryFile` instead of constructing predictable temporary filenames.

```python
from pathlib import Path
from tempfile import NamedTemporaryFile

with NamedTemporaryFile(mode="w+", suffix=".txt", encoding="utf-8") as file:
    file.write("temporary data")
    file.seek(0)
    print(Path(file.name).suffix)
    print(file.read())
```

Temporary file visibility, delete behavior, and simultaneous reopening differ by platform, especially on Windows. Prefer using the provided file handle directly when possible.

## 16. `re`: regular expressions

The `re` module helps extract, validate, replace, and split structured text. Favor ordinary string operations (`in`, `split`, `replace`, `startswith`) when a pattern is simple.

### `search`, `match`, and `fullmatch`

```python
import re

text = "Account: ACC-2026-0042"

print(re.search(r"ACC-\d{4}-\d{4}", text).group())
print(re.match(r"Account", text).group())
print(bool(re.fullmatch(r"[A-Z]{3}-\d{4}-\d{4}", "ACC-2026-0042")))
```

- `search()` looks anywhere in the string.
- `match()` matches at the beginning.
- `fullmatch()` requires the entire string to satisfy the pattern.

### Capture groups and named groups

```python
import re

pattern = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
match = pattern.fullmatch("2026-10-19")

if match:
    print(match.group("year"))
    print(match.groupdict())
```

### `findall()` vs. `finditer()`

```python
import re

text = "invoice 120, credit 45, adjustment 9"

print(re.findall(r"\d+", text))
print([(m.group(), m.span()) for m in re.finditer(r"\d+", text)])
```

`findall()` returns a list; `finditer()` yields match objects lazily, including location and capture metadata. `findall()` changes its return structure when capturing groups are present.

### `sub()` and `split()`

```python
import re

raw = "  alpha   beta\t gamma  "
clean = re.sub(r"\s+", " ", raw).strip()
parts = re.split(r"[,;]\s*", "A,B; C")

print(clean)
print(parts)
```

Replacement via a function:

```python
import re

def double_number(match):
    return str(2 * int(match.group()))

print(re.sub(r"\d+", double_number, "A=10; B=15"))
```

### Pattern notation

| Pattern | Meaning |
|---|---|
| `\d` | Unicode decimal digit |
| `\w` | Unicode word character (approximately alphanumeric/underscore) |
| `\s` | Whitespace |
| `.` | Any character except newline unless DOTALL |
| `^` / `$` | Start/end anchor (with flag nuances) |
| `\A` / `\Z` | Start/end of full string |
| `[A-Z]` | Character class/range |
| `[^,]` | Anything except comma |
| `*` / `+` / `?` | Zero-or-more / one-or-more / optional |
| `{m,n}` | Repeat between `m` and `n` times |
| `(?:...)` | Noncapturing group |
| `(?P<name>...)` | Named capture |
| `(?=...)` | Positive lookahead |
| `(?!...)` | Negative lookahead |
| `\b` | Word boundary |

Use raw string notation (`r"..."`) for most regex patterns. Avoid unbounded complex regexes on untrusted data: some patterns cause catastrophic backtracking.

## 17. `json`, `csv`, and `tomllib`

### `json.dumps()`, `json.loads()`, `json.dump()`, `json.load()`

- `dumps()` serializes to a **string**.
- `loads()` deserializes from a **string/bytes**.
- `dump()` serializes to a **file-like object**.
- `load()` deserializes from a **file-like object**.

```python
import json

payload = {"name": "résumé", "active": True, "scores": [10, 20]}
text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
restored = json.loads(text)

print(text)
print(restored)
```

File-based example:

```python
import json
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    path = Path(directory) / "config.json"
    data = {"retries": 3, "enabled": True}

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    with path.open("r", encoding="utf-8") as file:
        loaded = json.load(file)

    print(loaded)
```

### JSON limitations and custom serialization

Standard JSON has strings, numbers, booleans, null, arrays, and objects. Standard `json` does not automatically serialize `datetime`, `Decimal`, `set`, or arbitrary user-defined objects.

```python
import json
from dataclasses import asdict, dataclass

@dataclass
class Job:
    id: int
    status: str

job = Job(42, "complete")
serialized = json.dumps(asdict(job))
print(serialized)
```

Useful options: `default=`, `object_hook=`, `parse_float=`, `indent=`, `sort_keys=`, `ensure_ascii=`, `allow_nan=`.

```python
import json
from decimal import Decimal

payload = json.loads('{"amount": 0.1}', parse_float=Decimal)
print(payload)
```

When interoperability matters, consider `allow_nan=False`; JSON's standard syntax does not include NaN or Infinity.

### `csv.DictReader` and `csv.DictWriter`

```python
import csv
from io import StringIO

source = StringIO("id,name,balance\n1,Alice,12.5\n2,Bob,20.0\n")
rows = list(csv.DictReader(source))
print(rows)

output = StringIO(newline="")
writer = csv.DictWriter(output, fieldnames=["id", "name", "balance"])
writer.writeheader()
writer.writerows(rows)
print(output.getvalue())
```

**Important:** CSV fields are read as strings by default. Apply schema-aware conversion explicitly.

When opening a real CSV file, use:

```python
import csv
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    path = Path(directory) / "data.csv"

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "amount"])
        writer.writerow([1, 12.5])

    with path.open("r", newline="", encoding="utf-8") as file:
        print(list(csv.DictReader(file)))
```

`newline=""` lets the CSV module handle newlines correctly on all supported platforms.

### `tomllib` (Python 3.11+)

Parse TOML configuration files. It has `load()` and `loads()` but no built-in `dump()` or `dumps()`.

```python
import tomllib

config = tomllib.loads('''
[database]
host = "localhost"
port = 5432

[features]
caching = true
''')

print(config["database"]["host"])
print(config["features"]["caching"])
```

TOML is commonly used in `pyproject.toml`. For writing TOML, use a separate library if the project permits one.

### Choosing a data format

| Format | Strength | Main limitation |
|---|---|---|
| JSON | Interoperable structured interchange | Limited native types; no comments |
| CSV | Simple tabular interchange | Flat data; weak typing/schema |
| TOML | Human-edited configuration | Not a general-purpose large data interchange format |
| Pickle | Convenient Python object snapshots | Unsafe to unpickle untrusted bytes |

## 18. `datetime`, `zoneinfo`, and `time`

### `date`, `time`, `datetime`, and `timedelta`

```python
from datetime import date, datetime, timedelta

start = date(2026, 10, 19)
end = start + timedelta(days=30)
when = datetime(2026, 10, 19, 9, 30)

print(end)
print(when.isoformat())
print((end - start).days)
```

### Parsing and formatting

```python
from datetime import datetime

parsed = datetime.strptime("2026-10-19 14:45", "%Y-%m-%d %H:%M")
formatted = parsed.strftime("%d %b %Y, %I:%M %p")
iso = datetime.fromisoformat("2026-10-19T14:45:00+00:00")

print(formatted)
print(iso.tzinfo)
```

Frequent directives: `%Y` year, `%m` month, `%d` day, `%H` hour (24h), `%M` minute, `%S` second, `%f` microsecond, `%z` numeric UTC offset, `%a` weekday abbreviation, `%b` month abbreviation.

### Naive vs. aware datetimes

A **naive** `datetime` has no timezone information. An **aware** `datetime` includes offset/timezone information. Prefer aware datetimes for timestamps representing real instants.

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

now_utc = datetime.now(timezone.utc)
toronto = now_utc.astimezone(ZoneInfo("America/Toronto"))

print(now_utc.isoformat())
print(toronto.isoformat())
```

`ZoneInfo` uses an IANA time zone database. Some systems, especially Windows installations, may need the `tzdata` package to provide zone definitions.

**Important:** Do not attach a timezone with `replace(tzinfo=...)` as a generic substitute for converting an existing aware instant; use `.astimezone(...)`. Handling ambiguous/nonexistent local times around daylight saving transitions needs explicit policy.

### `time.perf_counter()` and `time.monotonic()`

```python
import time

start = time.perf_counter()
result = sum(range(1_000_000))
elapsed = time.perf_counter() - start

print(result)
print(elapsed >= 0)
```

Use `perf_counter()` for elapsed-duration benchmarking and `monotonic()` for clocks that should not move backward with wall-clock adjustments. Use `datetime.now(timezone.utc)` when you need a timestamp with civil-time meaning.

### Calendar-related standard library

```python
import calendar

print(calendar.isleap(2028))
print(calendar.monthrange(2026, 10))
```

For working with calendar months, remember that a month is not a fixed number of days; `timedelta(days=30)` is not generally “one calendar month.”

## 19. `math`, `statistics`, `decimal`, and `fractions`

### `math`: common numerical functions

```python
import math

print(math.sqrt(81))
print(math.isqrt(82))
print(math.ceil(3.2))
print(math.floor(3.8))
print(math.trunc(-3.8))
print(math.gcd(36, 60))
print(math.lcm(6, 8))
print(math.factorial(6))
print(math.comb(10, 3))
print(math.perm(10, 3))
```

| Function | Purpose |
|---|---|
| `sqrt(x)` | Floating-point square root |
| `isqrt(n)` | Integer floor square root |
| `ceil(x)` / `floor(x)` | Round toward +∞ / −∞ |
| `trunc(x)` | Remove fractional part toward zero |
| `gcd(*numbers)` | Greatest common divisor |
| `lcm(*numbers)` | Least common multiple |
| `factorial(n)` | `n!` |
| `comb(n, k)` | Number of combinations |
| `perm(n, k)` | Number of ordered selections |
| `prod(iterable)` | Product of values |
| `fsum(iterable)` | Accurate floating-point sum |
| `isclose(a, b, ...)` | Relative/absolute tolerance comparison |
| `isfinite(x)` | Neither infinite nor NaN |
| `log()`, `log1p()`, `exp()`, `expm1()` | Logarithmic/exponential functions |
| `hypot(*coords)` | Euclidean norm |
| `dist(p, q)` | Euclidean distance |

### Floating-point comparisons

```python
import math

print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
print(math.isclose(0.000001, 0, abs_tol=0.00001))
```

`math.isclose()` uses relative and optional absolute tolerances. Choose tolerances appropriate to numerical scale and the domain, rather than relying on its defaults in every setting.

### `statistics`

```python
from statistics import mean, median, mode, multimode, pstdev, stdev, variance

values = [10, 12, 13, 15, 20]

print(mean(values))
print(median(values))
print(mode(values))
print(multimode([1, 2, 2, 3, 3]))
print(pstdev(values))
print(stdev(values))
print(variance(values))
```

- `stdev()` and `variance()` are **sample** estimates (denominator `n - 1`).
- `pstdev()` and `pvariance()` are **population** measures (denominator `n`).
- `quantiles()`, `geometric_mean()`, `harmonic_mean()`, `covariance()`, `correlation()`, and `linear_regression()` are also available.

```python
from statistics import correlation, linear_regression

x = [1, 2, 3, 4]
y = [3, 5, 7, 9]

print(correlation(x, y))
print(linear_regression(x, y))
```

For large array computations and vectorization, NumPy remains better suited than Python's `statistics` module.

### `Decimal`: exact decimal representation and rounding policy

```python
from decimal import Decimal, ROUND_HALF_UP, localcontext

amount = Decimal("12.345")
rounded = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

print(rounded)
print(Decimal("0.1") + Decimal("0.2"))

with localcontext() as context:
    context.prec = 8
    print(Decimal("1") / Decimal("7"))
```

Always construct decimal amounts from strings or integers when you want exact decimal values. `Decimal(0.1)` preserves the inexact binary floating-point input rather than magically recovering the intended decimal literal.

`Decimal` is particularly useful for accounting and business rules with specified decimal precision. Do not assume all domain-specific monetary rounding requirements are solved just by using Decimal; you must explicitly choose precision and rounding rules.

### `Fraction`

```python
from fractions import Fraction

ratio = Fraction(2, 3) + Fraction(1, 6)
exact = Fraction("0.125")

print(ratio)
print(exact)
print(float(ratio))
```

`Fraction` gives exact rational arithmetic, at the expense of potentially large numerators and denominators.

## 20. `random`, `secrets`, `hashlib`, `hmac`, and `uuid`

### `random`: simulation and reproducibility

```python
import random

rng = random.Random(42)

print(rng.random())
print(rng.randint(1, 6))
print(rng.randrange(0, 100, 5))
print(rng.choice(["A", "B", "C"]))
print(rng.sample(range(20), 5))
print(rng.choices(["A", "B"], weights=[0.8, 0.2], k=5))
```

- `choice()` picks one element; `choices()` samples with replacement and supports weights.
- `sample()` samples without replacement.
- `shuffle()` mutates a list in place.
- A dedicated `random.Random(seed)` instance isolates reproducible pseudorandom state from other modules.

The `random` module is **not cryptographically secure**.

### `secrets`: security-sensitive randomness

```python
import secrets

api_token = secrets.token_urlsafe(24)
random_number = secrets.randbelow(1000)

print(len(api_token) > 0)
print(0 <= random_number < 1000)
```

Use `secrets` for passwords, tokens, reset links, and security-sensitive nonces rather than `random`.

### `hashlib`: cryptographic digests

```python
import hashlib

payload = b"some bytes to hash"
digest = hashlib.sha256(payload).hexdigest()

print(digest)
```

For reading a large file incrementally:

```python
import hashlib
from io import BytesIO

stream = BytesIO(b"abc" * 1_000)
hasher = hashlib.sha256()

while chunk := stream.read(1024):
    hasher.update(chunk)

print(hasher.hexdigest())
```

A bare SHA-256 digest is not a password-storage scheme. Password storage requires a purpose-built salted, work-factor-based password hashing approach.

### `hmac`: message authentication

```python
import hashlib
import hmac

key = b"example-key"
payload = b"important-message"
signature = hmac.new(key, payload, hashlib.sha256).digest()
expected = hmac.new(key, payload, hashlib.sha256).digest()

print(hmac.compare_digest(signature, expected))
```

Use `hmac.compare_digest()` for comparisons involving secret authentication values, rather than ordinary `==`.

### `uuid`

```python
import uuid

identifier = uuid.uuid4()
parsed = uuid.UUID(str(identifier))

print(identifier)
print(identifier == parsed)
```

`uuid4()` creates a random UUID, useful for identifiers where centralized allocation is undesirable. Random UUIDs are not a substitute for authentication or access control.

## 21. `contextlib`, `io`, and `copy`

### `contextlib.contextmanager`

Write reusable setup/teardown behavior with a generator-based context manager.

```python
from contextlib import contextmanager
from time import perf_counter

@contextmanager
def timed():
    start = perf_counter()
    try:
        yield
    finally:
        print(f"Elapsed: {perf_counter() - start:.6f}s")

with timed():
    sum(range(100_000))
```

The code after `yield` executes when exiting the context. The `finally` block runs even if the body raises an exception.

### `ExitStack`

Dynamically manage a varying number of context managers.

```python
from contextlib import ExitStack
from io import StringIO

with ExitStack() as stack:
    buffers = [stack.enter_context(StringIO()) for _ in range(3)]
    for index, buffer in enumerate(buffers):
        buffer.write(str(index))
    print([buffer.getvalue() for buffer in buffers])
```

This is valuable for pipelines that open an unknown number of files/resources. `AsyncExitStack` supports analogous asynchronous cleanup.

### `nullcontext()` and `suppress()`

```python
from contextlib import nullcontext, suppress
from pathlib import Path

with nullcontext("already available") as value:
    print(value)

with suppress(FileNotFoundError):
    Path("file-that-does-not-exist.txt").unlink()
```

Do not use `suppress(Exception)` indiscriminately; broad suppression hides bugs.

### `redirect_stdout()`

```python
from contextlib import redirect_stdout
from io import StringIO

buffer = StringIO()
with redirect_stdout(buffer):
    print("captured")

print(buffer.getvalue())
```

Redirecting the process-level standard stream can affect other concurrent code; it is better suited to controlled scripts/tests than parallel server work.

### `io.StringIO()` and `io.BytesIO()`

```python
from io import BytesIO, StringIO

text_stream = StringIO()
text_stream.write("hello")
text_stream.seek(0)
print(text_stream.read())

binary_stream = BytesIO(b"abc")
print(binary_stream.read(2))
```

In-memory streams are useful in tests and when APIs expect file-like objects.

### `copy.copy()` vs. `copy.deepcopy()`

```python
import copy

original = {"name": "A", "values": [1, 2]}
shallow = copy.copy(original)
deep = copy.deepcopy(original)

original["values"].append(3)

print(shallow["values"])
print(deep["values"])
```

- Shallow copy duplicates the outer container while sharing nested objects.
- Deep copy recursively copies many nested objects (with memoization), but is not necessarily appropriate for files, sockets, locks, or resources.
- Prefer explicit data transformations for complex business objects when you need precise copying semantics.

## 22. `logging`, `warnings`, and `argparse`

### `logging`: levels and configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("pipeline")
logger.info("Loaded %s rows", 1250)
logger.warning("Skipped %s invalid rows", 3)
```

Use parameterized logging (`logger.info("Rows: %s", n)`) so message formatting can be deferred when the level is disabled.

Common levels in increasing severity: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

### Exception logging

```python
import logging

logger = logging.getLogger("example")

try:
    int("not-a-number")
except ValueError:
    logger.exception("Parsing failed")
```

`logger.exception()` records stack-trace information inside an exception handler. In libraries, configure a module logger but generally let the consuming application configure handlers and global logging policy.

### `warnings`

```python
import warnings

def legacy_function():
    warnings.warn("Use new_function instead", DeprecationWarning, stacklevel=2)
    return 10

with warnings.catch_warnings(record=True) as recorded:
    warnings.simplefilter("always")
    legacy_function()
    print(str(recorded[0].message))
```

A warning signals a condition users may need to know about while allowing execution to continue. Use exceptions when the current operation cannot proceed correctly.

### `argparse`

Create script command-line interfaces with typed arguments and built-in help.

```python
import argparse

parser = argparse.ArgumentParser(description="Process transactions")
parser.add_argument("source")
parser.add_argument("--months", type=int, default=12)
parser.add_argument("--dry-run", action="store_true")

args = parser.parse_args(["transactions.csv", "--months", "6", "--dry-run"])

print(args.source)
print(args.months)
print(args.dry_run)
```

Useful features include mutually exclusive groups, `choices=`, `required=True` for options, `nargs=`, subparsers, and custom validation. `argparse` turns small scripts into reusable command-line tools without external CLI packages.

## 23. `sys`, `importlib`, and `subprocess`

### `sys`: interpreter and runtime information

```python
import sys

print(sys.version_info[:3])
print(sys.executable)
print(sys.platform)
print(sys.getrecursionlimit())
```

Frequently encountered attributes/functions:

| API | Use |
|---|---|
| `sys.argv` | Command-line argument strings |
| `sys.path` | Module search locations |
| `sys.modules` | Modules already loaded |
| `sys.executable` | Running Python interpreter path |
| `sys.version_info` | Structured Python version |
| `sys.platform` | Platform indicator |
| `sys.stdin` / `stdout` / `stderr` | Standard streams |
| `sys.exit(code)` | Request program termination via `SystemExit` |
| `sys.getsizeof(obj)` | Shallow object size, not total nested footprint |

Avoid mutating `sys.path` as a routine package-management solution. Prefer an installable package structure, proper imports, and an isolated environment.

### `importlib.import_module()`

Import a module by name at runtime.

```python
from importlib import import_module

module = import_module("math")
print(module.sqrt(144))
```

Use an explicit allowlist if a module name is supplied externally; arbitrary import names can have side effects or load unintended code.

### `importlib.resources`

Access files bundled inside packages without hard-coding source-tree paths.

```python
from importlib.resources import files

package_root = files("email")
print(package_root.is_dir())
```

`files(package)` returns a traversable resource reference. For package data, e.g. a bundled `.json` file, an application can use `files("my_package").joinpath("defaults.json").read_text(encoding="utf-8")`. Do not assume every package resource maps directly to an ordinary on-disk path.

### `subprocess.run()`

Run external commands while capturing output and checking their exit status.

```python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-c", "print(2 + 2)"],
    capture_output=True,
    text=True,
    check=True,
    timeout=10,
)

print(result.stdout.strip())
```

Important parameters:

- `capture_output=True`: collect stdout and stderr.
- `text=True`: decode streams into strings.
- `check=True`: raise `CalledProcessError` for nonzero exit status.
- `timeout=...`: bound execution time; timeout raises `TimeoutExpired`.
- `cwd=...`: set working directory.
- `env=...`: supply an environment mapping.

**Security:** Prefer argument lists and the default `shell=False` when command arguments could contain external input. With `shell=True`, the shell interprets metacharacters and quoting, increasing injection risk. `subprocess` executes real programs and should never be given arbitrary untrusted command targets.

### `Popen`

Use `subprocess.Popen` when you need streaming output, interaction with a long-running subprocess, or more detailed process lifecycle control. Prefer `run()` for simple “execute and collect result” workflows.

## 24. Concurrency: `concurrent.futures`, `threading`, and `asyncio`

### Choosing a model

| Technique | Strong fit | Key limitation |
|---|---|---|
| `ThreadPoolExecutor` | I/O-bound blocking calls | CPU-bound pure Python often limited by GIL in common builds |
| `ProcessPoolExecutor` | CPU-bound calculations | Serialization/process startup overhead |
| `asyncio` | Many cooperative asynchronous I/O tasks | Blocking functions freeze the event loop |
| `threading` | Explicit shared-state threads | Locks and races require care |

Details of the GIL vary by interpreter and Python build; do not assume every environment has identical thread parallelism behavior.

### `ThreadPoolExecutor`

```python
from concurrent.futures import ThreadPoolExecutor

def square(value):
    return value * value

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(square, range(10)))

print(results)
```

`executor.map()` returns results in input order even if execution completes out of order.

### `submit()` and `as_completed()`

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def compute(value):
    return value, value ** 2

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(compute, value) for value in range(5)]
    results = [future.result() for future in as_completed(futures)]

print(sorted(results))
```

`as_completed()` yields futures by completion rather than submission order. A future's `.result()` propagates exceptions from its task.

### `ProcessPoolExecutor`

```python
from concurrent.futures import ProcessPoolExecutor

def heavy_calculation(value):
    return sum(i * i for i in range(value))

def main():
    with ProcessPoolExecutor(max_workers=2) as executor:
        return list(executor.map(heavy_calculation, [10_000, 20_000]))

if __name__ == "__main__":
    print(main())
```

For portable process pools, define worker functions at the module top level, make arguments/results serializable, and put entry-point execution under `if __name__ == "__main__":`. Interactive notebooks and some execution contexts can behave differently.

### `threading.Lock`

```python
from threading import Lock, Thread

lock = Lock()
results = []

def worker(value):
    with lock:
        results.append(value * 2)

threads = [Thread(target=worker, args=(n,)) for n in range(5)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(sorted(results))
```

Locks protect critical sections involving shared state. Other useful primitives include `Event`, `Semaphore`, `Condition`, `RLock`, and `Barrier`.

### `asyncio.gather()`

```python
import asyncio

async def fetch_simulated(identifier):
    await asyncio.sleep(0.01)
    return f"item-{identifier}"

async def main():
    results = await asyncio.gather(*(fetch_simulated(i) for i in range(5)))
    print(results)

asyncio.run(main())
```

`asyncio` enables concurrency when operations **await**. It does not automatically make blocking filesystem/network calls or heavy CPU-bound Python code nonblocking.

### `asyncio.TaskGroup` (Python 3.11+)

Use structured concurrency so tasks belong to a managed scope.

```python
import asyncio

async def compute(value):
    await asyncio.sleep(0.01)
    return value ** 2

async def main():
    async with asyncio.TaskGroup() as group:
        first = group.create_task(compute(3))
        second = group.create_task(compute(4))

    return first.result(), second.result()

print(asyncio.run(main()))
```

`TaskGroup` has important error propagation and sibling cancellation behavior; it is often preferable to unmanaged background tasks when related work must complete as a unit.

### `asyncio.to_thread()` and `asyncio.timeout()`

```python
import asyncio
import time

def blocking_operation():
    time.sleep(0.01)
    return "done"

async def main():
    async with asyncio.timeout(1):
        return await asyncio.to_thread(blocking_operation)

print(asyncio.run(main()))
```

`to_thread()` is useful for placing a blocking operation into a worker thread; it is not a general fix for CPU-bound pure-Python parallelism.

## 25. `sqlite3`: a database without extra dependencies

SQLite is a local relational database engine accessed through Python's standard library. Useful for lightweight persistence, prototypes, tests, and ETL staging.

### Create tables, insert, query, and aggregate

```python
import sqlite3

with sqlite3.connect(":memory:") as connection:
    connection.execute(
        "CREATE TABLE transactions (id INTEGER PRIMARY KEY, region TEXT, amount REAL)"
    )
    connection.executemany(
        "INSERT INTO transactions (id, region, amount) VALUES (?, ?, ?)",
        [(1, "East", 10.0), (2, "West", 20.0), (3, "East", 30.0)],
    )

    rows = connection.execute(
        "SELECT region, SUM(amount) FROM transactions GROUP BY region ORDER BY region"
    ).fetchall()

    print(rows)
```

### Parameterized queries

```python
import sqlite3

connection = sqlite3.connect(":memory:")
try:
    connection.execute("CREATE TABLE users (name TEXT, active INTEGER)")
    connection.execute("INSERT INTO users VALUES (?, ?)", ("Alice", 1))

    name = "Alice"
    row = connection.execute("SELECT active FROM users WHERE name = ?", (name,)).fetchone()
    print(row)
finally:
    connection.close()
```

Use SQL placeholders such as `?` and bind parameters. Never splice externally supplied values into SQL strings using f-strings or string concatenation.

### `sqlite3.Row`

```python
import sqlite3

connection = sqlite3.connect(":memory:")
try:
    connection.row_factory = sqlite3.Row
    connection.execute("CREATE TABLE metrics (name TEXT, value INTEGER)")
    connection.execute("INSERT INTO metrics VALUES (?, ?)", ("errors", 3))

    row = connection.execute("SELECT * FROM metrics").fetchone()
    print(row["name"], row["value"])
finally:
    connection.close()
```

**Connection context-manager subtlety:** `with sqlite3.connect(...) as connection:` manages transaction commit/rollback, but does **not** necessarily close the connection at block exit. Use `connection.close()`, `contextlib.closing`, or an explicit ownership policy when resource cleanup matters.

### Transactions

Transactions let related writes commit atomically or roll back together. Exceptions within a `with connection:` transaction scope trigger rollback rather than partial commit. Carefully design transaction boundaries around business operations.

## 26. Inspection, debugging, profiling, and testing

### `inspect`: discover function signatures, class relationships, and members

```python
import inspect

class Base:
    def run(self, value: int) -> str:
        return str(value)

class Derived(Base):
    pass

print(inspect.signature(Derived().run))
print(inspect.getmro(Derived))
print(inspect.isclass(Derived))
print(inspect.getmembers(Derived, inspect.isfunction))
```

Useful functions:

| API | What it answers |
|---|---|
| `inspect.signature(fn)` | What parameters and return annotation does it expose? |
| `inspect.getmembers(obj)` | Which member names/values are visible? |
| `inspect.getmembers_static(obj)` | Which members exist without triggering dynamic attribute lookup? |
| `inspect.getmro(cls)` | What is the method resolution order? |
| `inspect.isclass(x)` | Is this object a class? |
| `inspect.isfunction(x)` | Is this a Python function? |
| `inspect.ismethod(x)` | Is this a bound method? |
| `inspect.iscoroutinefunction(x)` | Is this an asynchronous coroutine function? |
| `inspect.getsource(obj)` | What Python source defines it, if available? |
| `inspect.getfile(obj)` | Where is its defining file, if available? |
| `inspect.unwrap(fn)` | Follow `__wrapped__` chains to original function |

Some built-ins/extension objects do not expose Python source; `inspect.getsource()` can fail.

### `inspect.Signature.bind()`

Validate/bind argument sets according to a callable's declared signature.

```python
import inspect

def transform(data, *, threshold=0.5):
    return data, threshold

signature = inspect.signature(transform)
bound = signature.bind([1, 2], threshold=0.8)

print(bound.arguments)
```

Useful when developing decorators, dispatchers, and framework-style public APIs.

### `traceback`

```python
import traceback

try:
    1 / 0
except ZeroDivisionError:
    lines = traceback.format_exc()
    print("ZeroDivisionError" in lines)
```

For structured exception details, use `traceback.TracebackException.from_exception(exc)`.

### `timeit`

```python
import timeit

runtime = timeit.timeit("sum(range(100))", number=10_000)
print(runtime >= 0)
```

Benchmark multiple runs, representative inputs, and correct alternatives. Avoid drawing strong conclusions from extremely short single-shot timings.

### `cProfile` and `pstats`

```python
import cProfile
import io
import pstats

profiler = cProfile.Profile()
profiler.enable()

sum(i * i for i in range(100_000))

profiler.disable()
output = io.StringIO()
statistics = pstats.Stats(profiler, stream=output)
statistics.sort_stats("cumulative").print_stats(10)
print(output.getvalue())
```

`cProfile` helps locate expensive call paths. Profiling changes execution overhead and should complement representative benchmarks.

### `dis`: bytecode disassembly

```python
import dis

def calculate(x):
    return x * 2 + 1

dis.dis(calculate)
```

Bytecode changes across Python versions and is useful for understanding interpreter behavior, not as a stable public API contract.

### `pdb`

```python
import pdb

value = {"status": "ready"}
pdb.set_trace()
print(value)
```

This opens an interactive debugger. Common debugger commands include `n` (next), `s` (step), `c` (continue), `p expr` (print), `l` (list), `w` (where), and `q` (quit). For quick entry, use the built-in `breakpoint()`.

### `unittest`

```python
import unittest

def normalize_amount(value):
    if value < 0:
        raise ValueError("Negative amount")
    return round(value, 2)

class NormalizeAmountTests(unittest.TestCase):
    def test_rounding(self):
        self.assertEqual(normalize_amount(1.236), 1.24)

    def test_negative(self):
        with self.assertRaises(ValueError):
            normalize_amount(-1)

if __name__ == "__main__":
    unittest.main()
```

Common assertions: `assertEqual`, `assertIs`, `assertTrue`, `assertFalse`, `assertIn`, `assertAlmostEqual`, `assertRaises`, and `assertLogs`.

### `unittest.mock`

Replace external dependencies during tests, or assert how an interface was called.

```python
from unittest.mock import Mock, patch

client = Mock()
client.fetch.return_value = {"rows": 3}

result = client.fetch("source-a")
client.fetch.assert_called_once_with("source-a")
print(result)

with patch("time.sleep") as fake_sleep:
    import time
    time.sleep(10)
    fake_sleep.assert_called_once_with(10)
```

Prefer patching the name **where the code under test looks it up**, not necessarily where the dependency was originally defined. `AsyncMock` is designed for awaitable collaborators, and `spec=`/`autospec=True` can catch interface mistakes.

## 27. More useful standard-library modules

These are smaller modules that solve common problems with little setup.

### `textwrap`

```python
import textwrap

paragraph = "Python offers a very broad standard library that can simplify many everyday tasks."
print(textwrap.fill(paragraph, width=30))

raw = """
    first line
    second line
"""
print(textwrap.dedent(raw).strip())
```

### `pprint`

```python
from pprint import pprint

payload = {"model": {"name": "baseline", "options": {"months": 24, "enabled": True}}}
pprint(payload, sort_dicts=True, width=50)
```

### `difflib`

```python
from difflib import SequenceMatcher, unified_diff

before = ["alpha\n", "beta\n", "gamma\n"]
after = ["alpha\n", "delta\n", "gamma\n"]

print("".join(unified_diff(before, after, fromfile="old", tofile="new")))
print(SequenceMatcher(None, "dataset", "data-set").ratio())
```

Useful when comparing configuration files or constructing readable text diffs. Similarity ratios are heuristic, not a semantic distance metric.

### `fnmatch`

```python
from fnmatch import fnmatch

names = ["sales_2025.csv", "sales_2026.csv", "readme.md"]
print([name for name in names if fnmatch(name, "sales_*.csv")])
```

### `shlex`

```python
import shlex

command = 'tool --name "long file name" --limit 5'
print(shlex.split(command))
```

`shlex` handles shell-like lexical splitting; it does not execute commands. Prefer passing an already constructed argument list to `subprocess` when possible.

### `queue.Queue`

```python
from queue import Queue

work = Queue()
work.put("task-1")
work.put("task-2")

while not work.empty():
    item = work.get_nowait()
    print(item)
    work.task_done()
```

This single-threaded example illustrates the interface. In concurrent code, `empty()` is not a reliable guard against races; use blocking `get()`, timeouts, or sentinel-based shutdown strategies. `Queue` is thread-safe, while a plain `deque` is not a drop-in replacement for every coordinated producer/consumer workflow.

### `weakref`

```python
import weakref

class Resource:
    pass

resource = Resource()
reference = weakref.ref(resource)

print(reference() is resource)
del resource
print(reference())
```

Weak references do not keep their referent alive. The exact collection timing of unreachable objects can vary across implementations.

### `graphlib.TopologicalSorter`

Topologically order tasks with dependencies, useful for pipelines and build systems.

```python
from graphlib import TopologicalSorter

dependencies = {
    "extract": set(),
    "transform": {"extract"},
    "validate": {"transform"},
    "load": {"validate"},
}

execution_order = list(TopologicalSorter(dependencies).static_order())
print(execution_order)
```

The mapping maps each **node to its predecessor dependencies**, not to downstream dependents. Cycles raise `graphlib.CycleError`.

### `ast`

```python
import ast

expression = ast.parse("a + b * 2", mode="eval")
print(ast.dump(expression, indent=2))
```

`ast` is useful for code analysis, source transformation, and safe parsing of restricted literal structures; it does not eliminate the risks of executing untrusted code.

### `zipfile` and `gzip`

```python
import gzip
from io import BytesIO
from zipfile import ZipFile

compressed = gzip.compress(b"data" * 100)
print(gzip.decompress(compressed)[:8])

buffer = BytesIO()
with ZipFile(buffer, mode="w") as archive:
    archive.writestr("report.txt", "completed")

buffer.seek(0)
with ZipFile(buffer) as archive:
    print(archive.read("report.txt").decode("utf-8"))
```

When extracting third-party ZIP archives, inspect member names and use safe extraction practices to avoid unintended paths or resource exhaustion. Archive compression and encryption serve different purposes.

### `pickle`

```python
import pickle

payload = {"version": 1, "items": [1, 2, 3]}
serialized = pickle.dumps(payload)
restored = pickle.loads(serialized)

print(restored)
```

**Major security warning:** Loading malicious pickle data can execute code. Only deserialize pickle files from fully trusted sources; prefer JSON, CSV, or other constrained formats for untrusted interchange. Pickle is also Python-centric and not a stable cross-language schema.

### Other modules to know

| Module | What it helps with |
|---|---|
| `string` | Constants such as `ascii_letters`, `digits`, `punctuation` |
| `platform` | OS, Python implementation, and platform reporting |
| `socket` | Low-level networking and hostname-related APIs |
| `urllib.parse` | URL quoting, parsing, and query-string manipulation |
| `urllib.request` | Basic HTTP client functionality |
| `ipaddress` | IPv4/IPv6 address and network calculations |
| `email` | Parsing and constructing MIME/email messages |
| `mimetypes` | Guessing content types from filenames |
| `types` | Runtime type helper objects and `MappingProxyType` |
| `gc` | Garbage collector controls and introspection |
| `atexit` | Process-exit callbacks |
| `signal` | Process signal handling on supported platforms |
| `sched` | Simple event scheduling |
| `struct` | Pack/unpack binary C-style data layouts |
| `base64` | Base64 and related encodings, not encryption |
| `secrets` | Security-grade random token generation |
| `tokenize` | Python lexical tokenization |
| `token` | Python token constants |
| `keyword` | Python keyword lists |
| `site` | Python site-package initialization context |
| `venv` | Create isolated Python environments |
| `ensurepip` | Bootstrap pip where supported |

---

# Part III — Practical Recipes and Engineering Guidance

## 28. Practical recipes

### Recipe 1: Group rows and compute multiple aggregations

```python
from collections import defaultdict

rows = [
    {"portfolio": "A", "loss": 10.0},
    {"portfolio": "B", "loss": 4.0},
    {"portfolio": "A", "loss": 7.0},
]

summary = defaultdict(lambda: {"count": 0, "loss": 0.0})

for row in rows:
    result = summary[row["portfolio"]]
    result["count"] += 1
    result["loss"] += row["loss"]

print(dict(summary))
```

Why this works: `defaultdict` creates a fresh accumulator for each key, yielding a one-pass aggregation. For more accurate floating-point sums, store grouped values and use `math.fsum()` where justified.

### Recipe 2: Validate aligned column inputs

```python
periods = ["Jan", "Feb", "Mar"]
amounts = [10.0, 12.5, 11.0]

records = [
    {"period": period, "amount": amount}
    for period, amount in zip(periods, amounts, strict=True)
]

print(records)
```

`strict=True` prevents silent truncation if one column has fewer records.

### Recipe 3: Stream a large file in chunks

```python
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    path = Path(directory) / "large.bin"
    path.write_bytes(b"0123456789" * 1_000)

    total_bytes = 0
    with path.open("rb") as file:
        for chunk in iter(partial(file.read, 1024), b""):
            total_bytes += len(chunk)

    print(total_bytes)
```

Only one chunk is held in the loop at a time, rather than reading all content into memory.

### Recipe 4: Partition valid and invalid records

```python
rows = [
    {"id": 1, "amount": 10},
    {"id": 2, "amount": -5},
    {"id": 3, "amount": 20},
]

valid = []
rejected = []

for row in rows:
    (valid if row["amount"] >= 0 else rejected).append(row)

print(valid)
print(rejected)
```

An explicit loop is often clearer than compressing two related destinations into an elaborate comprehension. The conditional-expression example is concise, but readability can favor a full `if`/`else` in production code.

### Recipe 5: Sort records with multiple criteria

```python
from operator import itemgetter

rows = [
    {"desk": "B", "risk": 5},
    {"desk": "A", "risk": 7},
    {"desk": "A", "risk": 2},
]

print(sorted(rows, key=itemgetter("desk", "risk")))
print(sorted(rows, key=lambda row: (row["desk"], -row["risk"])))
```

The first sorts both keys ascending; the second sorts desk ascending and risk descending. Negating values works for suitable numeric keys but is not a universal descending-sort strategy for arbitrary data types.

### Recipe 6: Build a cached metadata lookup

```python
from functools import lru_cache

METADATA = {
    "A": {"region": "West", "currency": "CAD"},
    "B": {"region": "East", "currency": "USD"},
}

@lru_cache(maxsize=128)
def get_currency(portfolio):
    return METADATA[portfolio]["currency"]

print(get_currency("A"))
print(get_currency.cache_info())
```

Cache values only when repeated lookup matters and the underlying information has an appropriate invalidation policy. In this tiny example, caching might add complexity without meaningful performance benefit.

### Recipe 7: Build a dependency-ordered pipeline

```python
from graphlib import TopologicalSorter

operations = {
    "source": lambda: print("source"),
    "features": lambda: print("features"),
    "score": lambda: print("score"),
    "report": lambda: print("report"),
}

dependencies = {
    "source": set(),
    "features": {"source"},
    "score": {"features"},
    "report": {"score"},
}

for name in TopologicalSorter(dependencies).static_order():
    operations[name]()
```

This pattern translates a dependency graph into a deterministic valid execution order, subject to ties between independent nodes. If deterministic tie-breaking among independent nodes matters, define it explicitly in your scheduling design.

### Recipe 8: Use a dataclass with an abstract execution API

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class CalculationResult:
    name: str
    value: float

class Calculation(ABC):
    @abstractmethod
    def execute(self, values: list[float]) -> CalculationResult:
        raise NotImplementedError

class TotalCalculation(Calculation):
    def execute(self, values: list[float]) -> CalculationResult:
        return CalculationResult("total", sum(values))

result = TotalCalculation().execute([2.0, 3.0, 5.0])
print(result)
```

This keeps result data separate from the execution interface and is suitable for extensible package APIs.

### Recipe 9: Build configuration from layered mappings

```python
from collections import ChainMap

user = {"parallelism": 4}
environment = {"timeout": 15}
defaults = {"parallelism": 1, "timeout": 30, "retries": 3}

config = ChainMap(user, environment, defaults)
print(dict(config))
```

Precedence is left to right. Changes to source dictionaries are reflected in the view.

### Recipe 10: Compare expected and actual outputs with tolerances

```python
import math

expected = {"A": 100.0, "B": 75.0}
actual = {"A": 100.0000001, "B": 74.9999998}

keys_match = expected.keys() == actual.keys()
values_match = all(
    math.isclose(actual[key], expected[key], rel_tol=1e-8, abs_tol=1e-6)
    for key in expected
)

print(keys_match and values_match)
```

This validates mapping shape and floating-point values separately. Tolerances must reflect the business significance, numerical algorithms, and magnitude of expected results.

### Recipe 11: Detect consecutive-state transitions

```python
from itertools import pairwise

states = ["pending", "pending", "running", "running", "done"]
transitions = [
    (previous, current)
    for previous, current in pairwise(states)
    if previous != current
]

print(transitions)
```

### Recipe 12: Maintain the top N items without sorting everything

```python
import heapq
from operator import itemgetter

records = [
    {"id": "A", "score": 10},
    {"id": "B", "score": 55},
    {"id": "C", "score": 21},
    {"id": "D", "score": 44},
]

top_two = heapq.nlargest(2, records, key=itemgetter("score"))
print(top_two)
```

For small `N` relative to large input, a bounded heap may be more efficient than sorting all records.

### Recipe 13: Read CSV, transform, and write JSON

```python
import csv
import json
from io import StringIO

source = StringIO("portfolio,amount\nA,12.5\nB,8.0\n")
rows = [
    {"portfolio": row["portfolio"], "amount": float(row["amount"])}
    for row in csv.DictReader(source)
]

output = json.dumps(rows, indent=2)
print(output)
```

For financial amounts, consider `Decimal` and an explicit decimal-to-JSON representation policy.

### Recipe 14: Implement a timing decorator

```python
from functools import wraps
from time import perf_counter

def timed(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        try:
            return function(*args, **kwargs)
        finally:
            elapsed = perf_counter() - start
            print(f"{function.__name__}: {elapsed:.6f}s")
    return wrapper

@timed
def calculate(n):
    return sum(range(n))

print(calculate(10_000))
```

The `finally` ensures a timing result is emitted even when the wrapped function raises. To support async functions, create an async-aware decorator rather than wrapping coroutine creation as if it were completion.

### Recipe 15: Identify duplicate records by a composite key

```python
records = [
    {"customer": "A", "period": "2026-01", "amount": 10},
    {"customer": "A", "period": "2026-01", "amount": 20},
    {"customer": "B", "period": "2026-01", "amount": 30},
]

seen = set()
duplicates = []

for row in records:
    key = (row["customer"], row["period"])
    if key in seen:
        duplicates.append(row)
    else:
        seen.add(key)

print(duplicates)
```

Sets support efficient membership-based deduplication for hashable composite keys. This is a useful pure-Python analogue to detecting duplicate keys in a DataFrame.

### Recipe 16: Use sentinel values for optional configuration

```python
MISSING = object()

def resolve_setting(config, name, default=MISSING):
    if name in config:
        return config[name]
    if default is not MISSING:
        return default
    raise KeyError(name)

print(resolve_setting({"timeout": None}, "timeout", 30))
print(resolve_setting({}, "timeout", 30))
```

The distinction between a missing entry and an entry explicitly set to `None` is preserved.

### Recipe 17: Build a rolling window without extra dependencies

```python
from collections import deque

values = [10, 20, 30, 40, 50]
window = deque(maxlen=3)
rolling_mean = []

for value in values:
    window.append(value)
    if len(window) == window.maxlen:
        rolling_mean.append(sum(window) / len(window))

print(rolling_mean)
```

For very large windows, maintain a running sum to avoid an `O(window_size)` sum at every step.

### Recipe 18: Use a temporary SQLite database for data checks

```python
import sqlite3
from contextlib import closing

with closing(sqlite3.connect(":memory:")) as connection:
    with connection:
        connection.execute("CREATE TABLE model_output (stage TEXT, value REAL)")
        connection.executemany(
            "INSERT INTO model_output VALUES (?, ?)",
            [("RM", 10.0), ("SER", 20.0), ("ECL", 30.0)],
        )

    stages = {
        row[0] for row in connection.execute("SELECT DISTINCT stage FROM model_output")
    }
    print(stages == {"RM", "SER", "ECL"})
```

This uses `closing()` for resource cleanup and an inner connection context for transaction semantics.

## 29. Pitfalls and decision guides

### Pitfalls to memorize

1. **Iterators are not collections.** Consuming a generator once can exhaust it.
2. **`zip()` truncates silently by default.** Add `strict=True` when aligned inputs must match.
3. **`sorted()` and `.sort()` differ.** The former returns a new list; the latter changes the list and returns `None`.
4. **`all([])` is `True`.** Check nonemptiness separately if required.
5. **`filter(None, values)` removes zeros and false values.** It does not mean “drop only nulls.”
6. **`groupby()` groups consecutive runs.** Sort first if needed or use a mapping accumulator.
7. **`defaultdict` can create keys during indexing.** `get()` does not invoke its factory.
8. **`round()` is not always business rounding.** Exact ties use half-to-even; binary floats complicate decimal ties.
9. **Never use `eval()`/`exec()` with untrusted input.** Restricting globals does not create a safe sandbox.
10. **Never unpickle untrusted data.** Deserialization can execute arbitrary code.
11. **Do not interpolate untrusted values into SQL or shell commands.** Bind SQL parameters and pass subprocess argument lists.
12. **Hashing is not encryption.** Neither `hash()` nor Base64 protects secrets.
13. **`random` is not suitable for security tokens.** Use `secrets`.
14. **Naive datetimes are ambiguous for real instants.** Prefer aware UTC timestamps at system boundaries.
15. **`timedelta(days=30)` does not mean a calendar month.** Months vary in length.
16. **`copy.copy()` shares nested objects.** Choose shallow vs. deep copies deliberately.
17. **`Path.exists()` followed by a write is not an atomic file-creation policy.** Use modes like `x` or other suitable atomic operations when races matter.
18. **`with sqlite3.connect(...)` does not imply a closed connection.** It controls a transaction context.
19. **`ThreadPoolExecutor` is not universally a CPU speedup.** Test with your interpreter, workload, and execution model.
20. **Type hints are not runtime validation.** Add explicit checks at input boundaries when needed.
21. **`is` is not a substitute for `==`.** Use `is None` for identity checks against `None`.
22. **Default values should not be mutable shared state.** Use `None` with internal construction or dataclass `default_factory`.
23. **A key's presence differs from its truthiness.** `if key in mapping` is not the same as `if mapping.get(key)`.
24. **`list.sort()` is stable.** You can use stable multi-pass sorting when that improves clarity.
25. **`inspect.getsource()` is not guaranteed.** Built-in/native functions may have no retrievable Python source.

### Decision guide: loops, comprehensions, `map`, and generators

| Need | Good default |
|---|---|
| Create a new list by transformation | List comprehension |
| Construct key-to-value mapping | Dict comprehension |
| Create unique transformed values | Set comprehension |
| Stream transformed values lazily | Generator expression |
| Reuse an existing unary transformation | `map(fn, iterable)` |
| Filter using a complex condition | Comprehension or generator expression |
| Find just one matching item | `next((x for x in xs if condition), default)` |
| Perform multiple side effects or branches | Explicit `for` loop |
| Flatten exactly one nesting level | `itertools.chain.from_iterable()` |

### Decision guide: grouping

| Need | Use |
|---|---|
| Frequency counts | `Counter` |
| Group values into lists | `defaultdict(list)` |
| Accumulate numeric totals | `defaultdict(float)` or explicit dict |
| Group already sorted/consecutive records | `itertools.groupby()` |
| Tabular vectorized grouping at scale | pandas/Polars rather than a pure-Python loop |

### Decision guide: storage and communication

| Need | Use |
|---|---|
| Human-edited app config | TOML or JSON |
| Cross-language structured message | JSON |
| Spreadsheet-like flat exchange | CSV |
| Small relational datastore | SQLite |
| Python-only trusted snapshots | Pickle, only with clear trust boundary |
| Temporary intermediate bytes/text | `BytesIO` / `StringIO` |

### Rough complexity reference

Assume standard built-in container implementations and amortized expectations where noted.

| Operation | Typical time |
|---|---|
| `list.append(x)` | Amortized `O(1)` |
| `list.pop()` (last) | `O(1)` |
| `list.pop(0)` | `O(n)` |
| `deque.appendleft(x)` / `deque.popleft()` | `O(1)` |
| `x in list` | `O(n)` |
| `x in set` | Expected `O(1)` |
| `mapping[key]` | Expected `O(1)` |
| `sorted(sequence)` | `O(n log n)` |
| `min(iterable)` / `max(iterable)` | `O(n)` |
| `heapq.heapify(items)` | `O(n)` |
| `heapq.heappush` / `heappop` | `O(log n)` |
| `bisect_left(sorted_list, value)` | `O(log n)` |
| `insort(sorted_list, value)` | `O(n)` due to insertion |
| `range` integer membership | `O(1)` arithmetic check |
| `dict.fromkeys(iterable)` | Expected `O(n)` |
| Repeated list concatenation in a loop | Can grow quadratically |

Complexities are general guidance, not a guarantee about constant factors, adversarial hash behavior, or alternate Python implementations.

## 30. Quick-reference index

### Built-in functions by category

| Category | Functions |
|---|---|
| Iteration | `iter`, `next`, `enumerate`, `zip`, `map`, `filter`, `reversed`, `range`, `aiter`, `anext` |
| Aggregation | `sum`, `min`, `max`, `all`, `any` |
| Ordering | `sorted` |
| Numeric | `abs`, `round`, `pow`, `divmod` |
| Numeric conversion | `int`, `float`, `complex`, `bool` |
| Text/representation | `str`, `repr`, `ascii`, `format`, `chr`, `ord` |
| Base conversion | `bin`, `oct`, `hex` |
| Collection constructors | `list`, `tuple`, `set`, `frozenset`, `dict`, `slice` |
| Binary | `bytes`, `bytearray`, `memoryview` |
| Type/object information | `type`, `isinstance`, `issubclass`, `id`, `hash`, `callable` |
| Attribute access | `getattr`, `setattr`, `hasattr`, `delattr` |
| Introspection | `dir`, `vars`, `help`, `globals`, `locals` |
| Object model | `object`, `super`, `property`, `classmethod`, `staticmethod` |
| I/O | `print`, `input`, `open` |
| Dynamic execution/debugging | `compile`, `eval`, `exec`, `__import__`, `breakpoint` |
| Other | `len` |

### Useful standard-library modules by task

| Goal | Modules |
|---|---|
| Iterator processing | `itertools`, `functools`, `operator` |
| Data structures | `collections`, `collections.abc`, `heapq`, `bisect`, `array` |
| Interfaces and data models | `dataclasses`, `typing`, `abc`, `enum` |
| Filesystem | `pathlib`, `os`, `glob`, `shutil`, `tempfile` |
| Text handling | `re`, `string`, `textwrap`, `difflib`, `fnmatch` |
| Structured formats | `json`, `csv`, `tomllib`, `pickle` |
| Dates and clocks | `datetime`, `zoneinfo`, `time`, `calendar` |
| Mathematics | `math`, `statistics`, `decimal`, `fractions` |
| Randomness and IDs | `random`, `secrets`, `uuid` |
| Integrity/authentication | `hashlib`, `hmac` |
| Resource management | `contextlib`, `io`, `copy` |
| Process environment | `sys`, `platform`, `argparse`, `importlib` |
| External programs | `subprocess`, `shlex` |
| Concurrency | `concurrent.futures`, `threading`, `asyncio`, `queue` |
| Database | `sqlite3` |
| Testing/debugging | `unittest`, `unittest.mock`, `pdb`, `inspect`, `traceback` |
| Performance | `timeit`, `cProfile`, `pstats`, `dis` |
| Dependency ordering | `graphlib` |
| Parsing Python | `ast`, `tokenize` |
| Archive/compression | `zipfile`, `gzip` |
| Networking basics | `urllib.parse`, `urllib.request`, `ipaddress`, `socket` |

### Study sequence

1. **First pass:** `enumerate`, `zip`, `sorted`, `min/max`, `any/all`, comprehensions, `iter/next`, `getattr`, `isinstance`, file context managers.
2. **Second pass:** `collections`, `itertools`, `functools`, `operator`, `pathlib`, `json/csv`, `datetime`, `logging`.
3. **Third pass:** `dataclasses`, `typing`, `abc`, `contextlib`, `heapq/bisect`, `decimal`, `inspect`, `sqlite3`.
4. **Advanced pass:** `asyncio`, executor pools, dynamic import, decorators, structured pipeline scheduling, debugging/profiling, secure subprocess and serialization boundaries.

### Official documentation

- [Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Python Standard Library](https://docs.python.org/3/library/index.html)
- [Built-in Types](https://docs.python.org/3/library/stdtypes.html)
- [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html)
- [Iterator Tools](https://docs.python.org/3/library/itertools.html)
- [Type Hints](https://docs.python.org/3/library/typing.html)
- [Data Model](https://docs.python.org/3/reference/datamodel.html)
- [Time Complexity Reference (Python Wiki)](https://wiki.python.org/moin/TimeComplexity)

---

**End of study notes.** The most transferable skill is recognizing which standard-library primitive already expresses the operation you need, then combining those primitives into small, testable functions rather than rebuilding them from scratch.
