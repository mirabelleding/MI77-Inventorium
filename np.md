# NumPy — Essential Methods, Attributes & Concepts

*A detailed, example-driven study guide for someone already fluent in pandas.*

> **Scope:** Practical NumPy fundamentals and high-value operations, with particular emphasis on N-dimensional indexing, slicing, `axis`, broadcasting, vectorization, dtype behavior, views/copies, and the functions you will actually use in data science and numerical data-processing pipelines.
>
> **Version:** Written for modern NumPy 2.x. Most fundamentals also work with NumPy 1.26. Version-specific notes are marked when relevant.
>
> **Examples:** Many code blocks reuse variables defined earlier within the same section; run them in context. Output blocks are illustrative; whitespace, printed dtype and float formatting may differ by platform.

## Table of Contents

1. [Mental model: NumPy vs pandas](#1-mental-model-numpy-vs-pandas)
2. [Creating arrays](#2-creating-arrays)
3. [ndarray attributes you must know](#3-ndarray-attributes-you-must-know)
4. [Data types and conversions](#4-data-types-and-conversions)
5. [Basic indexing, slicing, and stepping](#5-basic-indexing-slicing-and-stepping)
6. [3D and N-dimensional indexing](#6-3d-and-n-dimensional-indexing)
7. [Boolean masks and advanced indexing](#7-boolean-masks-and-advanced-indexing)
8. [Understanding `axis`, `keepdims`, and reductions](#8-understanding-axis-keepdims-and-reductions)
9. [Broadcasting and `np.newaxis`](#9-broadcasting-and-npnewaxis)
10. [Reshaping and changing dimensions](#10-reshaping-and-changing-dimensions)
11. [Views, copies, strides, and memory](#11-views-copies-strides-and-memory)
12. [Vectorized arithmetic, comparisons, and logical operations](#12-vectorized-arithmetic-comparisons-and-logical-operations)
13. [Conditional transformations: `where`, `select`, `clip`](#13-conditional-transformations-where-select-clip)
14. [Aggregations, statistics, and cumulative operations](#14-aggregations-statistics-and-cumulative-operations)
15. [Sorting, searching, uniqueness, and membership](#15-sorting-searching-uniqueness-and-membership)
16. [Combining, splitting, repeating, and tiling](#16-combining-splitting-repeating-and-tiling)
17. [NaN, infinity, and missing-value handling](#17-nan-infinity-and-missing-value-handling)
18. [Random number generation](#18-random-number-generation)
19. [Linear algebra essentials](#19-linear-algebra-essentials)
20. [Dates, numerical sequences, and differences](#20-dates-numerical-sequences-and-differences)
21. [NumPy + pandas interoperability](#21-numpy--pandas-interoperability)
22. [Performance, validation, and common pitfalls](#22-performance-validation-and-common-pitfalls)
23. [Quick-reference tables](#23-quick-reference-tables)
24. [Practice exercises with solutions](#24-practice-exercises-with-solutions)
25. [Suggested learning order and references](#25-suggested-learning-order-and-references)
---

## 1. Mental model: NumPy vs pandas

**NumPy** centers on `ndarray`: a usually homogeneous, N-dimensional array storing values with a common dtype, together with metadata describing shape, strides and layout. **pandas** builds labeled, primarily 1D/2D data structures for tabular analysis; it often delegates numerical work to NumPy or other array implementations.

```python
import numpy as np
import pandas as pd

arr = np.array([[10, 20], [30, 40]])
df = pd.DataFrame(arr, columns=["A", "B"])

print(arr.shape)       # (2, 2)
print(df.shape)        # (2, 2)
print(arr[0, 1])       # 20: positional access
print(df.loc[0, "B"]) # 20: labeled access
```

### Key differences

| Question | NumPy | pandas |
|---|---|---|
| How do I select? | `a[rows, columns]` | `df.loc[...]`, `df.iloc[...]` |
| What labels rows/columns? | Positional axes | Index and column labels |
| Can I have 3+ dimensions? | Yes | Not with a single DataFrame |
| How is data typed? | One dtype per ordinary array | Usually a dtype per column |
| What does `axis` mean? | Reduce/operate along a numbered dimension | Similar concept, with labeled axes |
| What should I use for tables? | Often pandas | Usually pandas |
| What should I use for tensor-like numerical computation? | Usually NumPy | Usually not a DataFrame |

**Critical foundation:** an array's `shape` tells you how many axes exist and how long each axis is. Almost everything else follows from that.

---

## 2. Creating arrays

### `np.array()` — create an array from array-like data

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([[1, 2, 3], [4, 5, 6]])
c = np.array([1, 2, 3], dtype=np.float64)

print(a.shape)  # (3,)
print(b.shape)  # (2, 3)
print(c.dtype)  # float64
```

- Rectangular nested lists become multidimensional arrays.
- Ragged nested sequences generally require explicit `dtype=object` (not recommended for most numerical code).
- NumPy determines a common dtype unless you specify one.

### `np.asarray()` — convert without unnecessarily copying

```python
original = np.array([1, 2, 3])
same = np.asarray(original)
print(same is original)  # True in this straightforward case

as_floats = np.asarray(original, dtype=float)
print(as_floats)  # [1. 2. 3.]
```

Prefer `np.asarray(x)` for function inputs that may be arrays, lists, or other array-like objects; an existing suitable array can be reused. If you **need independent storage**, explicitly call `.copy()`.

### Sequence constructors

```python
np.arange(2, 11, 2)       # array([ 2,  4,  6,  8, 10])
np.linspace(0, 1, 5)      # array([0.  , 0.25, 0.5 , 0.75, 1.  ])
np.logspace(1, 3, 3)      # array([  10.,  100., 1000.])
```

- `arange(start, stop, step)`: **stop is excluded**. Best suited to integer steps; floating-point accumulation may surprise you.
- `linspace(start, stop, num)`: **stop is included by default**. Prefer it when you want a fixed number of evenly spaced values.
- `logspace(start, stop, num, base=10)`: values evenly spaced in log space.

### Arrays filled with values

```python
np.zeros((2, 3))                 # 2x3 floats filled with 0
np.ones((2, 3), dtype=np.int64)  # 2x3 integers filled with 1
np.full((2, 2), 7)               # [[7, 7], [7, 7]]
np.eye(3)                       # 3x3 identity matrix
np.empty((2, 2))                 # uninitialized values: contents arbitrary!

x = np.array([[1, 2], [3, 4]])
np.zeros_like(x)  # same shape and dtype as x, filled with zero
np.ones_like(x)   # same shape and dtype as x, filled with one
np.full_like(x, 9)
```

**Pitfall:** `np.empty` allocates memory but does not initialize its values; never assume they start at zero.

### Shape interpretation

```python
np.array(7).shape                   # ()      scalar / 0D
np.array([7]).shape                 # (1,)    1D, one element
np.array([[7]]).shape               # (1, 1)  2D
np.zeros((3, 2, 4)).shape           # (3, 2, 4) 3D
```

---

## 3. ndarray attributes you must know

```python
a = np.arange(24, dtype=np.int32).reshape(3, 2, 4)
```

| Attribute | Meaning | Example |
|---|---|---|
| `a.ndim` | Number of axes/dimensions | `3` |
| `a.shape` | Length of each axis | `(3, 2, 4)` |
| `a.size` | Total number of elements | `24` |
| `a.dtype` | Data type of elements | `dtype('int32')` |
| `a.itemsize` | Bytes per element | `4` |
| `a.nbytes` | Bytes used by array elements | `96` |
| `a.strides` | Byte jumps for advancing one index along each axis | Layout-dependent |
| `a.T` | Reverses axis order for arrays with 3+ axes; ordinary transpose for 2D | Shape `(4, 2, 3)` |
| `a.flags` | Memory-layout and writeability information | Check `a.flags.c_contiguous` |
| `a.base` | Base object, if any, retaining the underlying storage | May be `None` or another array |

```python
print(a.ndim)       # 3
print(a.shape)      # (3, 2, 4)
print(a.size)       # 24
print(a.itemsize)   # 4
print(a.nbytes)     # 96
print(a.T.shape)    # (4, 2, 3)
```

**Remember:** `len(a)` means `a.shape[0]`, **not** `a.size`.

```python
len(a)   # 3
```

### Functions to introspect shape

```python
np.shape(a)  # (3, 2, 4)
np.ndim(a)   # 3
np.size(a)   # 24
```

Both attribute and function styles are valid; use the attributes when you already have an `ndarray`.

---

## 4. Data types and conversions

### Common dtypes

| dtype | Usage |
|---|---|
| `np.bool_` | Boolean values |
| `np.int32`, `np.int64` | Signed integers |
| `np.uint8` | Unsigned 8-bit integer, common in images |
| `np.float32`, `np.float64` | Floating-point numerical values |
| `np.complex64`, `np.complex128` | Complex numbers |
| `np.str_` | Fixed-width Unicode string dtype |
| `np.datetime64`, `np.timedelta64` | Dates/times and durations |
| `object` | Arbitrary Python objects; often costly for numeric work |

### `astype()` — convert dtype

```python
a = np.array([1, 2, 3])
b = a.astype(np.float64)
print(b)        # [1. 2. 3.]
print(b.dtype)  # float64

c = np.array([1.9, 2.2, -3.8]).astype(np.int64)
print(c)        # [ 1  2 -3]  truncates toward zero
```

`astype()` may copy; `astype(copy=False)` permits returning/reusing storage when an actual conversion isn't needed.

### Dtype promotion

```python
a = np.array([1, 2], dtype=np.int32)
b = np.array([0.5, 1.5], dtype=np.float64)
print((a + b).dtype)       # float64
print(np.result_type(a, b))  # float64
```

NumPy 2.x has updated dtype promotion rules, especially around Python scalars and NumPy scalars. **Do not assume every arithmetic operation preserves dtype.** Inspect `.dtype` when precision or memory matters.

### Overflow and precision

```python
x = np.array([255], dtype=np.uint8)
# NumPy integer arithmetic can overflow within a fixed-width dtype:
print(x + np.array([1], dtype=np.uint8))  # [0]

money = np.array([0.1, 0.2])
print(np.isclose(money.sum(), 0.3))  # True
```

Floating-point numbers generally approximate decimal fractions. For strict decimal financial arithmetic, use an appropriate decimal or integer-scaled representation rather than assuming floats are exact.

---

## 5. Basic indexing, slicing, and stepping

### 1D slicing: `[start:stop:step]`

```python
a = np.arange(10)    # [0 1 2 3 4 5 6 7 8 9]

a[2]        # 2
```

Useful slices (continuing with `a = np.arange(10)`):

```python
a[:4]       # [0 1 2 3]
a[2:7]      # [2 3 4 5 6]
a[2:9:2]    # [2 4 6 8]
a[::2]      # [0 2 4 6 8]
a[1::2]     # [1 3 5 7 9]
a[::-1]     # [9 8 7 6 5 4 3 2 1 0]
a[-3:]      # [7 8 9]
a[::3]      # [0 3 6 9]
```

- Start: included.
- Stop: excluded.
- Step: stride in **elements**, not bytes.
- `step` cannot be zero.
- Negative step traverses in reverse.

### 2D indexing: `[rows, columns]`

```python
m = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8]])

m[0, 2]     # 3 (row 0, column 2)
m[0]        # [1 2 3 4] (integer index removes first axis)
m[:, 1]     # [2 6] (column 1 from every row)
m[1, :]     # [5 6 7 8]
m[:, ::2]   # [[1, 3], [5, 7]]
m[:, 1::2]  # [[2, 4], [6, 8]]
m[:, ::-1]  # reverse each row's columns
m[::-1, :]  # reverse row order
```

### Assignment through slices

```python
m = np.arange(12).reshape(3, 4)
m[:, 0] = -1       # modify first column in-place
m[1, 1:3] = [90, 91]
print(m)
# [[-1  1  2  3]
#  [-1 90 91  7]
#  [-1  9 10 11]]
```

**Warning:** basic slicing usually returns a *view*. If you modify a sliced view, you may modify the source array. See Section 11.

---

## 6. 3D and N-dimensional indexing

Imagine shape `(3, 2, 4)` as **3 matrices, each with 2 rows and 4 columns**.

```python
cube = np.arange(1, 25).reshape(3, 2, 4)
print(cube)
# [[[ 1  2  3  4]
#   [ 5  6  7  8]]
#
#  [[ 9 10 11 12]
#   [13 14 15 16]]
#
#  [[17 18 19 20]
#   [21 22 23 24]]]
```

| Expression | Meaning | Result shape |
|---|---|---|
| `cube[0, :, :]` | First matrix | `(2, 4)` |
| `cube[:, 0, :]` | First row from each matrix | `(3, 4)` |
| `cube[:, :, 0]` | First column from every row | `(3, 2)` |
| `cube[:, :, ::2]` | Every second column | `(3, 2, 2)` |
| `cube[::2, :, ::2]` | Every second matrix and column | `(2, 2, 2)` |
| `cube[0:1, :, :]` | Keep first matrix as a 3D array | `(1, 2, 4)` |
| `cube[0, 0, :]` | First row of first matrix | `(4,)` |
| `cube[0, 0, 0]` | First scalar | `()` |

```python
print(cube[:, :, ::2])
# [[[ 1  3]
#   [ 5  7]]
#  [[ 9 11]
#   [13 15]]
#  [[17 19]
#   [21 23]]]
```

### `...` (ellipsis) and `None` / `np.newaxis`

```python
cube[..., 0]      # equivalent to cube[:, :, 0]
cube[..., ::2]    # equivalent to cube[:, :, ::2]
cube[0, ...]      # equivalent to cube[0, :, :]

v = np.array([1, 2, 3])
v[None, :].shape   # (1, 3)
v[:, None].shape   # (3, 1)
```

**Key dimensionality rule:** Integer indexing (`cube[0]`) removes the indexed axis; slicing (`cube[0:1]`) preserves it.

### Mixed indexing caution

```python
cube[0, :, 1].shape     # (2,)
cube[0:1, :, 1].shape   # (1, 2)
```

Think about the **shape of the result before its values**. This habit will make broadcasting and numerical code much easier.

---

## 7. Boolean masks and advanced indexing

### Boolean masking

```python
a = np.array([3, 12, 7, 20, 5])
mask = a > 10
print(mask)      # [False  True False  True False]
print(a[mask])   # [12 20]
print(a[a % 2 == 1])  # [3 7 5]
```

Combine masks with `&`, `|`, `~`, and **parentheses**:

```python
a[(a >= 5) & (a <= 12)]  # [12  7  5]
a[(a < 5) | (a > 12)]    # [ 3 20]
a[~(a > 10)]            # [3 7 5]
```

**Wrong:** `a > 5 and a < 12` (`and` expects scalar truth values).
**Right:** `(a > 5) & (a < 12)` (elementwise Boolean operation).

### Boolean masks on a 2D array

```python
m = np.array([[1, 2, 3], [4, 5, 6]])
print(m[m > 3])  # [4 5 6] — matching elements become a 1D array
print(m[m[:, 0] > 2])
# [[4 5 6]] — select entire rows by first-column value
```

### Integer-array indexing / fancy indexing

```python
a = np.array([10, 20, 30, 40])
a[[3, 0, 3]]             # [40 10 40], repeated indices allowed

m = np.arange(12).reshape(3, 4)
m[[0, 2]]               # first and third rows
m[[0, 2], [1, 3]]       # [1 11]: coordinates (0,1), (2,3)

m[np.ix_([0, 2], [1, 3])]
# [[ 1  3]
#  [ 9 11]] — Cartesian product of row and column selections
```

**Key distinction:** `m[[0, 2], [1, 3]]` selects two *paired* coordinates; `np.ix_` selects a *rectangular cross-product*.

### `np.nonzero()`, `np.argwhere()`, `np.flatnonzero()`

```python
a = np.array([[0, 5, 0], [6, 0, 7]])

np.nonzero(a)
# (array([0, 1, 1]), array([1, 0, 2]))

np.argwhere(a)
# array([[0, 1], [1, 0], [1, 2]]) — one row per coordinate

np.flatnonzero(a)
# array([1, 3, 5]) — positions in C-order flattening
```

- `nonzero`: tuple of index arrays, one for each axis.
- `argwhere`: stacked coordinate rows.
- `flatnonzero`: flattened positions.

---

## 8. Understanding `axis`, `keepdims`, and reductions

Think of an axis as **the dimension being operated over**.

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])
# shape = (2 rows, 3 columns)

m.sum()         # 21 — all elements
m.sum(axis=0)   # [5 7 9] — collapse rows; output per column
m.sum(axis=1)   # [6 15] — collapse columns; output per row
```

For a 3D array `(layers, rows, columns)`:

```python
cube = np.arange(24).reshape(3, 2, 4)
cube.sum(axis=0).shape     # (2, 4) — sum across layers
cube.sum(axis=1).shape     # (3, 4) — sum across rows within each layer
cube.sum(axis=2).shape     # (3, 2) — sum across columns
cube.sum(axis=(1, 2)).shape # (3,) — one sum per layer
```

### `keepdims=True`

```python
m = np.array([[1, 2, 3], [4, 5, 6]])
row_totals = m.sum(axis=1, keepdims=True)
print(row_totals)
# [[ 6]
#  [15]]
print(row_totals.shape)  # (2, 1), rather than (2,)
```

Keeping a size-1 axis often makes subsequent broadcasting easy:

```python
row_proportions = m / m.sum(axis=1, keepdims=True)
# [[0.16666667 0.33333333 0.5       ]
#  [0.26666667 0.33333333 0.4       ]]
```

**Practical rule:** For `axis=k`, NumPy reduces or operates **along** axis `k`; other axes remain unless an operation explicitly changes them.

---

## 9. Broadcasting and `np.newaxis`

Broadcasting lets arithmetic operate on differently shaped arrays without an explicit Python loop.

### General rules

Compare shapes **from right to left**. Two dimensions are compatible when they are equal or at least one is `1`. Missing leading dimensions behave like `1`.

```text
Array A: (2, 3)
Array B:    (3,)
Result : (2, 3)    compatible

Array A: (2, 3)
Array B: (2, 1)
Result : (2, 3)    compatible

Array A: (2, 3)
Array B:    (2,)
Result : impossible: 3 != 2
```

### Apply a weight to each column

```python
m = np.array([[1, 2, 3], [4, 5, 6]])  # (2, 3)
weights = np.array([10, 20, 30])       # (3,)
print(m * weights)
# [[ 10  40  90]
#  [ 40 100 180]]
```

### Apply a weight to each row

```python
row_weights = np.array([10, 100])   # (2,)
print(m * row_weights[:, None])     # (2, 3) * (2, 1)
# [[ 10  20  30]
#  [400 500 600]]
```

### Pairwise differences / distances without nested loops

```python
x = np.array([1, 3, 6])
y = np.array([2, 5])

diff = x[:, None] - y[None, :]
print(diff)
# [[-1 -4]
#  [ 1 -2]
#  [ 4  1]]
```

Shapes `(3, 1)` and `(1, 2)` broadcast to `(3, 2)`.

### `np.broadcast_to()` and `np.broadcast_arrays()`

```python
a = np.array([1, 2, 3])
b = np.broadcast_to(a, (2, 3))
print(b)
# [[1 2 3]
#  [1 2 3]]
# Returned broadcasted view is typically read-only; avoid modifying it.

x, y = np.broadcast_arrays(np.arange(3)[None, :], np.arange(2)[:, None])
print(x.shape, y.shape)  # (2, 3) (2, 3)
```

Broadcasting is efficient when it avoids materializing repeats, but intermediate arithmetic results can still allocate large arrays.

---

## 10. Reshaping and changing dimensions

### `.reshape()` / `np.reshape()`

```python
a = np.arange(12)
a.reshape(3, 4)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

a.reshape(2, 2, 3).shape   # (2, 2, 3)
a.reshape(3, -1).shape     # (3, 4), inferred dimension
```

Number of elements must remain the same. `reshape` returns a view **if possible**; otherwise it may copy. The `-1` placeholder is allowed for one dimension only.

### `.T`, `.transpose()`, `np.swapaxes()`, `np.moveaxis()`

```python
m = np.arange(6).reshape(2, 3)
m.T.shape                   # (3, 2)
m.transpose().shape         # (3, 2)

cube = np.zeros((2, 3, 4))
cube.T.shape                # (4, 3, 2): reverses *all* axes
cube.transpose(1, 0, 2).shape # (3, 2, 4)
np.swapaxes(cube, 0, 2).shape  # (4, 3, 2)
np.moveaxis(cube, 0, -1).shape # (3, 4, 2)
```

`transpose(axes)` reorders all axes according to the permutation you provide. `swapaxes` swaps two. `moveaxis` moves an axis into a target position while preserving relative order of the others.

### `.ravel()` vs `.flatten()`

```python
m = np.array([[1, 2], [3, 4]])
m.ravel()       # [1 2 3 4]; view when possible
m.flatten()     # [1 2 3 4]; always creates a copy
```

`np.ravel(m)` is the function form. `m.reshape(-1)` is another useful flattening idiom and may share memory.

### `np.expand_dims()`, `np.squeeze()`

```python
v = np.array([1, 2, 3])
np.expand_dims(v, axis=0).shape  # (1, 3)
np.expand_dims(v, axis=1).shape  # (3, 1)

x = np.zeros((1, 3, 1))
np.squeeze(x).shape              # (3,)
np.squeeze(x, axis=0).shape      # (3, 1)
```

Use `squeeze` carefully: it removes length-1 axes, which may be semantically important (e.g., batch or channel dimensions).

---

## 11. Views, copies, strides, and memory

This is among the most important NumPy topics for correctness and performance.

### Basic slices share memory

```python
a = np.array([10, 20, 30, 40])
view = a[1:3]
view[0] = 999
print(a)  # [ 10 999  30  40]
```

### Fancy indexing and Boolean indexing copy

```python
a = np.array([10, 20, 30, 40])
copy = a[[1, 2]]
copy[0] = 999
print(a)  # [10 20 30 40]

mask_copy = a[a > 20]
mask_copy[0] = 0
print(a)  # [10 20 30 40]
```

**Nuance:** `a[a > 20] = 0` **does** mutate `a` because it is an indexed assignment, not a mutation of a separately stored selection.

### `.copy()`, `.view()`, `np.shares_memory()`

```python
a = np.arange(6)
v = a[::2]
c = a.copy()

np.shares_memory(a, v)  # True
np.shares_memory(a, c)  # False

v.base is None          # Typically False here; not a universal proof
```

Prefer `np.shares_memory` over guessing from `base`. `.view()` creates a new array object sharing data; `.copy()` duplicates the array data.

### Memory strides

```python
a = np.arange(12, dtype=np.int64).reshape(3, 4)
print(a.strides)        # (32, 8) for typical C-contiguous int64 array
print(a[:, ::2].strides) # (32, 16)
```

For `(rows, columns)`, `strides` gives the number of **bytes** to move when increasing a row index by 1 or a column index by 1. `::2` doubles the column stride without necessarily allocating another buffer.

### Contiguity

```python
a = np.arange(12).reshape(3, 4)
b = a[:, ::2]
print(a.flags.c_contiguous)  # True in this case
print(b.flags.c_contiguous)  # False in this case

contig = np.ascontiguousarray(b) # copies if required
```

Memory layout can affect NumPy/BLAS performance and compatibility with lower-level libraries.

### Important copy/view distinctions

| Operation | Typical ownership behavior |
|---|---|
| `b = a` | Same Python array object; no copy |
| `a[1:5]`, `a[:, ::2]` | View |
| `a[[1, 3]]`, `a[mask]` | Copy |
| `a.reshape(...)` | View if possible, otherwise copy |
| `a.T`, `a.transpose(...)` | View with rearranged strides (ordinary ndarray) |
| `a.ravel()` | View if possible, otherwise copy |
| `a.flatten()` | Copy |
| `a.copy()` | Copy |
| `np.broadcast_to(...)` | Broadcasted view, usually read-only |

---

## 12. Vectorized arithmetic, comparisons, and logical operations

### Elementwise operations

```python
a = np.array([2, 4, 6])
b = np.array([1, 2, 3])

a + b       # [3 6 9]
a - b       # [1 2 3]
a * b       # [ 2  8 18]
a / b       # [2. 2. 2.]
a // b      # [2 2 2]
a % b       # [0 0 0]
a ** 2      # [ 4 16 36]
```

### Universal functions (ufuncs)

Most NumPy math operations accept entire arrays and operate elementwise:

```python
x = np.array([1.0, 4.0, 9.0])
np.sqrt(x)      # [1. 2. 3.]
np.square(x)    # [ 1. 16. 81.]
np.exp(x)       # elementwise e**x
np.log(x)       # natural logarithm
np.log10(x)     # base-10 logarithm
np.abs([-2, 3]) # [2 3]
np.round([1.234, 2.345], 1)  # [1.2 2.3]
np.floor([1.8, -1.2])        # [ 1. -2.]
np.ceil([1.2, -1.8])         # [ 2. -1.]
```

Also recognize `np.sin`, `np.cos`, `np.tan`, `np.maximum`, and `np.minimum`.

### Comparisons

```python
a = np.array([3, 6, 9])
a > 5            # [False  True  True]
a == 6           # [False  True False]
np.equal(a, 6)   # same idea as a == 6
```

### Logical functions

```python
x = np.array([True, False, True])
y = np.array([True, True, False])

np.logical_and(x, y)  # [ True False False]
np.logical_or(x, y)   # [ True  True  True]
np.logical_not(x)     # [False  True False]
np.logical_xor(x, y)  # [False  True  True]

np.any(x)            # True
np.all(x)            # False
```

**Python `and`, `or`, `not` are not replacements for array-wise logical operators.**

### Matrix multiplication is not elementwise multiplication

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[2, 0], [1, 2]])
A * B       # elementwise [[2, 0], [3, 8]]
A @ B       # matrix product [[4, 4], [10, 8]]
np.matmul(A, B)  # same as A @ B
```

---

## 13. Conditional transformations: `where`, `select`, `clip`

### `np.where(condition, x, y)` — elementwise if/else

```python
scores = np.array([45, 70, 88])
labels = np.where(scores >= 60, "pass", "fail")
print(labels)  # ['fail' 'pass' 'pass']
```

When `x` and `y` are omitted, `np.where(condition)` returns coordinate indices (for a standalone condition, `np.nonzero` is often clearer).

```python
a = np.array([0, 5, 0, 8])
np.where(a > 0)  # (array([1, 3]),)
```

### `np.select(condlist, choicelist, default=...)` — multiple branches

```python
scores = np.array([45, 65, 85, 95])
conditions = [scores >= 90, scores >= 75, scores >= 60]
choices = ["A", "B", "C"]
grades = np.select(conditions, choices, default="F")
print(grades)  # ['F' 'C' 'B' 'A']
```

**Order matters:** the **first matching condition wins**. `np.select` and `np.where` are vectorized selectors, not lazy `if` statements: their input expressions are evaluated before the selection, so potentially invalid arithmetic in an unused branch may still occur.

### `np.clip()` — cap values at lower/upper bounds

```python
a = np.array([-3, 2, 7, 15])
np.clip(a, 0, 10)   # [ 0  2  7 10]
```

Useful for risk caps, score bounds, thresholding and preventing extreme values. One-sided bounds are possible using `None`:

```python
np.clip(a, 0, None)  # [ 0  2  7 15]
```

### `np.maximum()` vs `np.max()`

```python
a = np.array([1, 8, 3])
b = np.array([4, 2, 5])
np.maximum(a, b)   # [4 8 5] elementwise pairwise max
np.max(a)          # 8       aggregate to one maximum
```

### `np.where()` vs Boolean assignment

```python
a = np.array([-5, 0, 8])
b = np.where(a < 0, 0, a)  # returns a new array

a[a < 0] = 0              # mutates a in place
```

---

## 14. Aggregations, statistics, and cumulative operations

```python
m = np.array([[1, 2, 3], [4, 5, 6]])
```

| Method or function | Purpose | Example result |
|---|---|---|
| `m.sum()` | Sum all elements | `21` |
| `m.mean()` | Arithmetic average | `3.5` |
| `m.min()`, `m.max()` | Extrema | `1`, `6` |
| `m.argmin()`, `m.argmax()` | Flat index of extremum by default | `0`, `5` |
| `m.std()` | Population standard deviation by default | `~1.7078` |
| `m.var()` | Population variance by default | `~2.9167` |
| `np.median(m)` | Median | `3.5` |
| `np.quantile(m, 0.25)` | 25th quantile | `2.25` |
| `np.percentile(m, 25)` | 25th percentile | `2.25` |
| `np.ptp(m)` | Max minus min | `5` |
| `m.prod()` | Product | `720` |
| `m.any()`, `m.all()` | Boolean reduction | Truthiness of elements |

### Axis-aware reductions

```python
m.sum(axis=0)   # [5 7 9]
m.sum(axis=1)   # [6 15]
m.mean(axis=0)  # [2.5 3.5 4.5]
m.max(axis=1)   # [3 6]
m.argmax(axis=1) # [2 2] — column index of max per row
```

### Standard deviation: pandas difference

```python
x = np.array([1.0, 2.0, 3.0])
np.std(x)           # sqrt(2/3) ~= 0.8165; ddof=0
np.std(x, ddof=1)   # 1.0; sample standard deviation

pd.Series(x).std()  # 1.0; pandas Series uses ddof=1 by default
```

This is a common source of **unexpected numerical differences** when porting pandas code.

### `cumsum()`, `cumprod()`, `diff()`

```python
a = np.array([2, 3, 5, 7])
a.cumsum()     # [ 2  5 10 17]
a.cumprod()    # [  2   6  30 210]
np.diff(a)     # [1 2 2] differences between consecutive values

m = np.array([[1, 2, 3], [4, 5, 6]])
m.cumsum(axis=0)
# [[1 2 3]
#  [5 7 9]]
m.cumsum(axis=1)
# [[ 1  3  6]
#  [ 4  9 15]]
```

### Weighted average / cumulative logic

```python
scores = np.array([80, 90, 100])
weights = np.array([1, 2, 1])
np.average(scores, weights=weights)  # 90.0

values = np.array([3, 6, 9, 12])
values.cumsum() / np.arange(1, len(values) + 1)  # running mean
```

---

## 15. Sorting, searching, uniqueness, and membership

### `np.sort()` vs `.sort()`

```python
a = np.array([8, 2, 5])
np.sort(a)       # [2 5 8]; returns sorted copy
print(a)        # [8 2 5] unchanged

a.sort()        # sorts array in-place; returns None
print(a)        # [2 5 8]
```

### `np.argsort()` — indices that would sort values

```python
scores = np.array([70, 95, 80])
order = np.argsort(scores)
print(order)         # [0 2 1]
print(scores[order]) # [70 80 95]

# Descending:
print(np.argsort(-scores))  # [1 2 0]
```

For stable sorting, `np.argsort(values, stable=True)` is supported in modern NumPy 2.x; or use `kind="stable"` for compatibility with older versions.

### `np.unique()` — unique values and counts

```python
a = np.array([3, 1, 3, 2, 1, 3])
np.unique(a)    # [1 2 3] — sorted unique values

values, counts = np.unique(a, return_counts=True)
print(values)   # [1 2 3]
print(counts)   # [2 1 3]
```

Other useful options: `return_index=True` (first occurrence indices), `return_inverse=True` (indices to reconstruct original entries), and `axis=0` for unique rows.

```python
rows = np.array([[1, 2], [1, 2], [3, 4]])
np.unique(rows, axis=0)
# [[1 2]
#  [3 4]]
```

### `np.isin()` — membership masks

```python
values = np.array([1, 2, 3, 4, 5])
mask = np.isin(values, [2, 4])
print(mask)           # [False  True False  True False]
print(values[mask])   # [2 4]
```

### `np.searchsorted()` — positions in sorted arrays

```python
bins = np.array([10, 20, 30, 40])  # must be sorted
np.searchsorted(bins, 25)           # 2
np.searchsorted(bins, 20, side="left")  # 1
np.searchsorted(bins, 20, side="right") # 2
```

Useful for bin assignments, lookups and insertion points. If the input is not sorted according to the expected order, results are not meaningful.

### `np.argpartition()` — partially ordered selection

```python
scores = np.array([10, 50, 20, 90, 40])
top_two_idx = np.argpartition(scores, -2)[-2:]
print(np.sort(scores[top_two_idx]))  # [50 90]
```

`argpartition` is useful when you need a top-k subset and do not require it already fully sorted.

---

## 16. Combining, splitting, repeating, and tiling

### `np.concatenate()` — join along an existing axis

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

np.concatenate([a, b], axis=0)
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]] — shape (4, 2)

np.concatenate([a, b], axis=1)
# [[1 2 5 6]
#  [3 4 7 8]] — shape (2, 4)
```

Other dimensions must match except for the joining axis.

### `np.stack()` — join by creating a *new* axis

```python
a = np.array([1, 2])
b = np.array([3, 4])
np.stack([a, b], axis=0)  # [[1 2], [3 4]], shape (2, 2)
np.stack([a, b], axis=1)  # [[1 3], [2 4]], shape (2, 2)

np.concatenate([a, b])   # [1 2 3 4], shape (4,)
```

**Mental model:** `concatenate` adds length to an existing axis; `stack` adds an axis.

### Shortcuts: `vstack`, `hstack`, `column_stack`

```python
a = np.array([1, 2])
b = np.array([3, 4])
np.vstack([a, b])       # [[1 2], [3 4]]
np.hstack([a, b])       # [1 2 3 4] for 1D arrays
np.column_stack([a, b]) # [[1 3], [2 4]]
```

Beware: `hstack` has different shape semantics for 1D vs higher-dimensional inputs; the explicit `stack`/`concatenate` form is often clearer.

### `np.split()`, `np.array_split()`

```python
a = np.arange(8)
np.split(a, 4)           # four arrays of length 2
np.array_split(a, 3)     # uneven groups allowed: lengths 3, 3, 2
```

`np.split` requires even partitioning for an integer number of sections; `array_split` allows uneven sections.

### `np.repeat()` vs `np.tile()`

```python
a = np.array([1, 2, 3])
np.repeat(a, 2)      # [1 1 2 2 3 3] — repeat each element
np.tile(a, 2)        # [1 2 3 1 2 3] — repeat the whole pattern
```

### `np.pad()` — add padding around an array

```python
a = np.array([1, 2, 3])
np.pad(a, pad_width=2, mode="constant", constant_values=0)
# [0 0 1 2 3 0 0]
```

Useful for array boundaries, rolling windows and numerical algorithms.

---

## 17. NaN, infinity, and missing-value handling

### `np.nan` is not equal to itself

```python
x = np.array([1.0, np.nan, 3.0, np.inf, -np.inf])

np.isnan(x)      # [False  True False False False]
np.isfinite(x)   # [ True False  True False False]
np.isinf(x)      # [False False False  True  True]
```

**Do not use:** `x == np.nan` to locate NaNs.
**Do use:** `np.isnan(x)` for numerical arrays.

### NaN-aware reductions

```python
x = np.array([1.0, np.nan, 3.0])
np.sum(x)        # nan
np.nansum(x)     # 4.0
np.mean(x)       # nan
np.nanmean(x)    # 2.0
np.nanmedian(x)  # 2.0
np.nanmin(x)     # 1.0
np.nanmax(x)     # 3.0
np.nanstd(x)     # 1.0, ddof=0
```

Also recognize `np.nanvar`, `np.nanpercentile` and `np.nanquantile`. All-NaN slices have special behaviors (often warnings and/or NaN results); check expected requirements.

### `np.nan_to_num()`

```python
x = np.array([1.0, np.nan, np.inf, -np.inf])
np.nan_to_num(x, nan=0.0, posinf=999.0, neginf=-999.0)
# [   1.    0.  999. -999.]
```

### Important pandas distinction

A numeric NumPy array can represent missing floating values with `NaN`; pandas supports additional missing-value forms such as `pd.NA`, nullable integer arrays, and `NaT`. Converting mixed or nullable pandas data into a NumPy array may change dtype or missing-value representation. Use `pd.isna` for general pandas objects.

### Avoid `np.isnan` on arbitrary object/string arrays

`np.isnan` targets numerical dtypes; calling it on a generic `object` or string array may raise `TypeError`. For mixed Python objects, consider pandas' missing-value handling or explicit normalization first.

---

## 18. Random number generation

Use the modern **Generator** interface, not global random state for new projects.

```python
rng = np.random.default_rng(42)  # seeded generator
```

### Core methods

```python
rng.random(3)                        # 3 floats in [0.0, 1.0)
rng.integers(0, 10, size=5)         # integers in [0, 10)
rng.uniform(2.0, 5.0, size=4)       # uniform floats in [2, 5)
rng.normal(loc=100, scale=15, size=5) # Gaussian samples
rng.choice(["A", "B", "C"], size=3, replace=True)
rng.permutation(np.arange(5))       # shuffled copy
```

For non-replacement samples:

```python
rng = np.random.default_rng(42)
sample = rng.choice(10, size=3, replace=False)
print(sample.shape)  # (3,)
```

### Shuffle in place

```python
rng = np.random.default_rng(42)
a = np.array([1, 2, 3, 4])
rng.shuffle(a)           # modifies a
```

### Reproducibility

```python
r1 = np.random.default_rng(123)
r2 = np.random.default_rng(123)
assert np.array_equal(r1.integers(0, 10, 5), r2.integers(0, 10, 5))
```

A fixed seed makes a given generator configuration reproducible. Exact streams can depend on bit generator choice and implementation/version; record them if long-lived reproducibility is critical.

**Parallel work:** independent generators or spawned child generators are preferable to letting worker processes inherit identical random state.

---

## 19. Linear algebra essentials

### Dot product, matrix multiplication, transpose

```python
u = np.array([1, 2, 3])
v = np.array([4, 5, 6])
np.dot(u, v)   # 32
u @ v         # 32 for 1D vectors

A = np.array([[1, 2], [3, 4]])
B = np.array([[2, 0], [1, 2]])
A @ B         # [[ 4  4], [10  8]]
A.T           # [[1 3], [2 4]]
```

### `np.linalg` essentials

```python
A = np.array([[3.0, 1.0], [1.0, 2.0]])
b = np.array([9.0, 8.0])

x = np.linalg.solve(A, b)
print(x)                  # [2. 3.]
print(np.allclose(A @ x, b)) # True

np.linalg.det(A)         # determinant: approximately 5
np.linalg.inv(A)         # inverse matrix
np.linalg.norm(b)        # Euclidean norm by default for vector
np.linalg.matrix_rank(A) # 2
```

**Best practice:** To solve `A @ x = b`, use `np.linalg.solve(A, b)` rather than explicitly computing `np.linalg.inv(A) @ b`. It is usually numerically preferable and more efficient.

### Decompositions to recognize

```python
np.linalg.eig(A)  # eigenvalues and right eigenvectors
np.linalg.svd(A)  # singular value decomposition
np.linalg.qr(A)   # QR decomposition
```

Useful for numerical methods and machine learning, but you need not memorize detailed signatures until your work requires them.

### Numerical comparisons

```python
np.isclose(0.1 + 0.2, 0.3)  # True, within tolerances
np.allclose(np.array([0.1 + 0.2]), np.array([0.3]))  # True
np.array_equal(np.array([1, 2]), np.array([1, 2]))   # True
```

`np.array_equal` checks exact shape and element equality (with an option for equal NaNs); `np.allclose` permits numeric tolerances. For financial reconciliation, select tolerances deliberately rather than blindly relying on defaults.

---

## 20. Dates, numerical sequences, and differences

### Differences and rates of change

```python
values = np.array([100, 110, 121, 115])
np.diff(values)                  # [ 10  11  -6]
np.diff(values) / values[:-1]    # period-over-period returns
np.gradient(np.array([0., 1., 4., 9.])) # numerical gradient estimate
```

### `np.datetime64` / `np.timedelta64`

```python
dates = np.array(["2026-01-01", "2026-01-03"], dtype="datetime64[D]")
delta = dates[1] - dates[0]
print(delta)              # 2 days
print(delta / np.timedelta64(1, "D")) # 2.0
```

Pandas is usually more ergonomic for business calendars, time zones, time series resampling, and labeled dates; NumPy date types are useful for basic vectorized date math.

---

## 21. NumPy + pandas interoperability

### Convert DataFrame/Series to NumPy

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
arr = df[["a", "b"]].to_numpy()
print(arr.shape)    # (3, 2)
```

**Caveat:** `.to_numpy()` is not guaranteed to be zero-copy. Mixed column dtypes may be coerced to a common dtype (even `object`). The returned array's memory-sharing relationship with the DataFrame is implementation-dependent.

### Use NumPy transformations in pandas

```python
df["tier"] = np.select(
    [df["a"] >= 3, df["a"] >= 2],
    ["high", "medium"],
    default="low"
)

df["capped_b"] = np.clip(df["b"], 0, 25)
```

### Pandas ↔ NumPy concept map

| pandas | NumPy | Caveat |
|---|---|---|
| `df.iloc[1:4, ::2]` | `a[1:4, ::2]` | NumPy has no row/column labels |
| `s.isin(values)` | `np.isin(a, values)` | Both generate membership masks |
| `s.where(cond, other)` | `np.where(cond, x, y)` | NumPy has a different argument convention |
| `df.to_numpy()` | `np.asarray(df)` | Explicit `.to_numpy()` is clearer for pandas |
| `s.value_counts()` | `np.unique(a, return_counts=True)` | Unique output is sorted; result is not a labeled Series |
| `s.cumsum()` | `np.cumsum(a)` | Missing-value behavior may differ |
| `df.mean(axis=0)` | `np.mean(a, axis=0)` | Missing-value behavior differs |
| `s.std()` | `np.std(a, ddof=1)` | pandas defaults to `ddof=1` |
| `pd.concat([...])` | `np.concatenate([...])` | NumPy does not align labels |
| `s.sort_values()` | `np.sort(a)` | NumPy has no labeled index |

### Alignment is a crucial difference

```python
s1 = pd.Series([10, 20], index=["a", "b"])
s2 = pd.Series([100, 200], index=["b", "a"])
print((s1 + s2).to_dict())  # {'a': 210, 'b': 120}: aligns by index!

x = s1.to_numpy()  # [10, 20]
y = s2.to_numpy()  # [100, 200]
print(x + y)        # [110 220]: positional, no label alignment
```

The NumPy result and pandas result have different semantics despite similar syntax.

---

## 22. Performance, validation, and common pitfalls

### Prefer native vectorized computation over Python loops

```python
a = np.arange(100_000)
result = a * 2 + 1  # vectorized

# Usually much slower and harder to optimize:
result_loop = np.array([x * 2 + 1 for x in a])
```

Vectorization can create intermediate arrays; for extremely large workloads, consider `out=`, chunking or an appropriate compiled backend.

### `np.vectorize()` is not a magic compiler

```python
f = np.vectorize(lambda x: x * 2)
```

`np.vectorize` offers broadcasting convenience around a Python function; it **does not typically make it faster** than a Python loop. Prefer built-in NumPy ufuncs or compiled approaches when performance matters.

### In-place arithmetic and `out=`

```python
a = np.array([1., 2., 3.])
a *= 2             # update in place
np.multiply(a, 3, out=a)  # reuse output buffer
```

Be careful with in-place operations when dtype conversion would be required:

```python
a = np.array([1, 2, 3])
# a += 0.5  # raises a casting error for an integer array
b = a + 0.5 # produces a floating-point result
```

### Common errors checklist

| Mistake | Why it fails | Better practice |
|---|---|---|
| `if a > 0:` where `a` has multiple values | Ambiguous truth value | `np.any(a > 0)` or `np.all(a > 0)` |
| `a > 1 & a < 5` | Operator precedence | `(a > 1) & (a < 5)` |
| `a == np.nan` | NaN is not equal to itself | `np.isnan(a)` |
| `a * b` expecting a matrix product | `*` is elementwise | Use `a @ b` |
| `np.std(a)` expecting pandas `.std()` | Default `ddof` differs | Set `ddof=1` |
| `np.arange(0, 1, 0.1)` expecting exact decimals | Floating-point representation | `np.linspace` where appropriate |
| Treating `.reshape()` as always zero-copy | It may copy | Use `np.shares_memory` if important |
| Treating `arr.T` as swapping only axes 0/1 for 3D | `.T` reverses **all** axes | `swapaxes` or `transpose` explicitly |
| Confusing `np.max` with `np.maximum` | Reduction vs elementwise | Select correct operation |
| Calling `.sort()` and storing the return | `ndarray.sort()` returns `None` | Use `np.sort(a)` for a new result |
| Using `np.empty()` as zero-filled | Contents uninitialized | Use `np.zeros()` |
| `m[[0, 2], [1, 3]]` expecting 2x2 | Paired advanced coordinates | Use `m[np.ix_(...)]` |
| Using old `arr.ptp()` in NumPy 2.x | Removed method | Use `np.ptp(arr)` |

### Fast validation patterns

```python
arr = np.arange(12).reshape(3, 4)

assert arr.ndim == 2
assert arr.shape[1] == 4
assert np.issubdtype(arr.dtype, np.integer)
assert np.isfinite(arr).all()

expected = np.array([[0, 1, 2, 3],
                     [4, 5, 6, 7],
                     [8, 9, 10, 11]])
assert np.array_equal(arr, expected)
```

For float results:

```python
actual = np.array([0.1 + 0.2])
expected = np.array([0.3])
assert np.allclose(actual, expected, rtol=1e-10, atol=1e-12)
```

### Useful inspection tools

```python
print(np.__version__)
print(arr.shape, arr.ndim, arr.dtype, arr.strides)
print(arr.flags.c_contiguous)
print(np.shares_memory(arr, arr[:, 0]))
```

For quick method discovery:

```python
help(np.reshape)
help(np.ndarray)
dir(np.ndarray)
```

`dir()` is comprehensive but not an ordered learning curriculum; official documentation is better for understanding behavior.

---

## 23. Quick-reference tables

### Essential ndarray attributes

| Attribute | Purpose |
|---|---|
| `a.shape` | Dimensions and sizes |
| `a.ndim` | Number of axes |
| `a.size` | Number of elements |
| `a.dtype` | Data type |
| `a.itemsize` | Bytes per element |
| `a.nbytes` | Total element buffer size |
| `a.strides` | Memory strides in bytes |
| `a.T` | Transposed view with axes reversed |
| `a.flags` | Memory properties |
| `a.base` | Base/reference relationship |

### Essential methods/functions grouped by purpose

| Category | Methods/functions | Remember this |
|---|---|---|
| Constructors | `array`, `asarray`, `arange`, `linspace`, `logspace` | Array initialization and sequences |
| Fillers | `zeros`, `ones`, `full`, `empty`, `eye`, `*_like` | Choose initialized vs uninitialized storage |
| Type | `astype`, `result_type`, `issubdtype` | Conversion and promotion |
| Select | `[]`, slices, masks, `ix_`, `nonzero`, `argwhere` | Basic slicing vs advanced indexing |
| Conditional | `where`, `select`, `clip`, `maximum`, `minimum` | Elementwise transforms |
| Logical | `logical_and`, `logical_or`, `logical_not`, `any`, `all` | Use elementwise logic, not Python `and` |
| Shape | `reshape`, `transpose`, `swapaxes`, `moveaxis` | Know resulting shapes |
| Axis | `expand_dims`, `squeeze`, `newaxis` | Insert/remove size-1 dimensions |
| Flat | `ravel`, `flatten` | View if possible vs copy always |
| Aggregate | `sum`, `mean`, `min`, `max`, `std`, `var`, `median`, `quantile` | `axis` and `keepdims` matter |
| Cumulative | `cumsum`, `cumprod`, `diff` | Running values and differences |
| Sort/search | `sort`, `argsort`, `argmax`, `unique`, `isin`, `searchsorted` | Order, positions and membership |
| Join/split | `concatenate`, `stack`, `split`, `array_split` | Existing axis vs new axis |
| Repeat | `repeat`, `tile`, `pad` | Elementwise vs pattern repeats |
| Finite values | `isnan`, `isfinite`, `isinf`, `nanmean`, `nansum`, `nan_to_num` | Missing/invalid numeric handling |
| Random | `default_rng`, `integers`, `normal`, `choice`, `shuffle` | Generator API |
| Algebra | `dot`, `matmul`, `linalg.solve`, `linalg.norm`, `linalg.svd` | Linear algebra |
| Compare | `array_equal`, `isclose`, `allclose` | Exact vs approximate equality |
| Memory | `copy`, `view`, `shares_memory`, `ascontiguousarray` | Understand data ownership |

### Array-shape cheat sheet

| Expression | Shape if `a.shape == (3, 2, 4)` |
|---|---|
| `a[0]` | `(2, 4)` |
| `a[0:1]` | `(1, 2, 4)` |
| `a[:, 0]` | `(3, 4)` |
| `a[:, :, ::2]` | `(3, 2, 2)` |
| `a.sum(axis=0)` | `(2, 4)` |
| `a.sum(axis=1)` | `(3, 4)` |
| `a.sum(axis=2)` | `(3, 2)` |
| `a.sum(axis=2, keepdims=True)` | `(3, 2, 1)` |
| `a.T` | `(4, 2, 3)` |
| `a.reshape(6, 4)` | `(6, 4)` |
| `a.ravel()` | `(24,)` |

---

## 24. Practice exercises with solutions

Try these before viewing the solutions. Each exercise begins with `import numpy as np` as needed.

### Exercise 1: slicing

Given `x = np.arange(1, 13).reshape(3, 4)`, select every other column from the last two rows.

```python
x = np.arange(1, 13).reshape(3, 4)
# Your expression: ?
```

**Solution**

```python
x[1:, ::2]
# [[ 5  7]
#  [ 9 11]]
```

### Exercise 2: 3D dimensions

Given `cube = np.arange(24).reshape(3, 2, 4)`, return a shape `(3, 2, 1)` containing the mean over the final axis.

**Solution**

```python
cube.mean(axis=2, keepdims=True)
```

### Exercise 3: row normalization

Normalize every row of a 2D array so each row sums to 1. Assume no row sum is zero.

**Solution**

```python
m = np.array([[2., 3., 5.], [1., 1., 2.]])
normalized = m / m.sum(axis=1, keepdims=True)
assert np.allclose(normalized.sum(axis=1), 1)
```

### Exercise 4: conditional logic

Convert scores into `"high"` (`>=80`), `"medium"` (`>=50`) or `"low"` (otherwise).

**Solution**

```python
scores = np.array([42, 58, 81, 95])
category = np.select([scores >= 80, scores >= 50],
                     ["high", "medium"], default="low")
# ['low' 'medium' 'high' 'high']
```

### Exercise 5: view or copy?

Predict whether `y[0] = 999` modifies `x` in each case.

```python
x = np.arange(6)
y = x[::2]      # A

x = np.arange(6)
y = x[[0, 2]]   # B
```

**Solution**

A: yes, basic slicing yields a view. B: no, integer-array indexing yields a copy.

### Exercise 6: top three scores

Return the three highest values sorted in descending order.

**Solution**

```python
x = np.array([15, 40, 12, 60, 25, 55])
indices = np.argpartition(x, -3)[-3:]
top = np.sort(x[indices])[::-1]
# [60 55 40]
```

### Exercise 7: pandas vs NumPy statistics

Why might `pd.Series(x).std()` differ from `np.std(x)`? Make them match.

**Solution**

Pandas uses `ddof=1` by default for `Series.std()`, whereas NumPy uses `ddof=0` by default. Use `np.std(x, ddof=1)` on fully observed numeric data.

### Exercise 8: build pairwise differences

Given `x = np.array([1, 2, 3])` and `y = np.array([10, 20])`, make a `(3, 2)` matrix of `x[i] - y[j]` without loops.

**Solution**

```python
x = np.array([1, 2, 3])
y = np.array([10, 20])
x[:, None] - y[None, :]
# [[ -9 -19]
#  [ -8 -18]
#  [ -7 -17]]
```

### Exercise 9: find missing data

Replace only the NaNs in `[1.0, nan, 3.0, nan]` with the mean of observed values.

**Solution**

```python
x = np.array([1.0, np.nan, 3.0, np.nan])
filled = np.where(np.isnan(x), np.nanmean(x), x)
# [1. 2. 3. 2.]
```

### Exercise 10: align dimensions

You have an array of shape `(100, 12)` and a vector of 100 weights. Apply each weight to its corresponding row.

**Solution**

```python
arr = np.ones((100, 12))
weights = np.arange(1, 101)
weighted = arr * weights[:, None]
assert weighted.shape == (100, 12)
```

---

## 25. Suggested learning order and references

### What to internalize vs what to look up

**Memorize conceptually** (and practice until automatic):

1. `shape`, `ndim`, `dtype`, `size`; what axes mean.
2. Slicing `start:stop:step`, integer indexing, Boolean masking.
3. N-dimensional indexing and the rule that integer indices remove axes.
4. Broadcasting: trailing dimensions must match or be `1`.
5. `reshape`, `transpose`, `newaxis`, `squeeze`, `ravel`.
6. Views vs copies and when mutating one object changes another.
7. Elementwise vectorization, `where`, `select`, `clip`.
8. Aggregation with `axis`, `keepdims` and `ddof`.
9. Sorting, uniqueness, `isin`, concatenation and stacking.
10. Numerical NaNs, finite checks and approximate comparisons.

**Know how to find and use** rather than memorize signatures: `np.linalg` decompositions, advanced random distributions, uncommon memory utilities, `np.argpartition`, `np.searchsorted`, `np.gradient`, advanced dtype machinery and specialized iteration.

### Suggested practical sequence

- **Stage 1 — Array fluency:** Sections 2–8; predict shapes and outputs without running the code.
- **Stage 2 — Vectorized thinking:** Sections 9–10 and 12–14; eliminate loops for common transforms.
- **Stage 3 — Correctness:** Sections 4, 11, 17 and 22; dtype, memory, NaNs and tolerance.
- **Stage 4 — Useful library coverage:** Sections 15–21; searching, grouping-like operations, random, linear algebra and pandas interoperability.
- **Stage 5 — Retention:** Work through Section 24 and revisit mistakes.

### Official documentation

- [NumPy user guide](https://numpy.org/doc/stable/user/index.html)
- [NumPy reference](https://numpy.org/doc/stable/reference/index.html)
- [Array indexing](https://numpy.org/doc/stable/user/basics.indexing.html)
- [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [Copies and views](https://numpy.org/doc/stable/user/basics.copies.html)
- [NumPy `reshape` reference](https://numpy.org/doc/stable/reference/generated/numpy.reshape.html)
- [Random Generator](https://numpy.org/doc/stable/reference/random/generator.html)
- [NumPy 2.0 migration guide](https://numpy.org/doc/stable/numpy_2_0_migration_guide.html)

---

*End of study notes. For durable NumPy proficiency, favor predicting array **shape, dtype, axis behavior, and memory ownership** over memorizing long method inventories.*
