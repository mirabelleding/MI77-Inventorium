# Polars — Comprehensive Study Notes

A detailed reference for Python Polars covering the expression system, DataFrame and LazyFrame operations, data types, selectors, joins, aggregation, reshaping, strings, datetimes, nested data, missing values, time series, I/O, SQL, interoperability, testing, lazy execution, optimization, and pandas-to-Polars translation patterns.

# Table of Contents

1. [Core mental model](#1-core-mental-model)
2. [Core Polars objects](#2-core-polars-objects)
3. [Creating DataFrames and Series](#3-creating-dataframes-and-series)
4. [Expressions](#4-expressions)
5. [Column selection](#5-column-selection)
6. [Selectors](#6-selectors)
7. [Selecting and creating columns](#7-selecting-and-creating-columns)
8. [Filtering rows](#8-filtering-rows)
9. [Conditional expressions](#9-conditional-expressions)
10. [Sorting and row selection](#10-sorting-and-row-selection)
11. [Renaming, dropping, and schema operations](#11-renaming-dropping-and-schema-operations)
12. [Casting and data types](#12-casting-and-data-types)
13. [Missing values and NaN](#13-missing-values-and-nan)
14. [Numeric expressions](#14-numeric-expressions)
15. [Aggregations and descriptive statistics](#15-aggregations-and-descriptive-statistics)
16. [GroupBy](#16-groupby)
17. [Window functions with `over`](#17-window-functions-with-over)
18. [Cumulative, shift, diff, and ranking operations](#18-cumulative-shift-diff-and-ranking-operations)
19. [Joins](#19-joins)
20. [Concatenation and stacking](#20-concatenation-and-stacking)
21. [Reshaping](#21-reshaping)
22. [String expressions](#22-string-expressions)
23. [Date and datetime expressions](#23-date-and-datetime-expressions)
24. [List expressions](#24-list-expressions)
25. [Array expressions](#25-array-expressions)
26. [Struct expressions](#26-struct-expressions)
27. [Categorical and Enum data](#27-categorical-and-enum-data)
28. [Horizontal operations](#28-horizontal-operations)
29. [Time-series operations](#29-time-series-operations)
30. [Rolling and dynamic grouping](#30-rolling-and-dynamic-grouping)
31. [LazyFrame](#31-lazyframe)
32. [Lazy optimization and query plans](#32-lazy-optimization-and-query-plans)
33. [Streaming and sinks](#33-streaming-and-sinks)
34. [Input and output](#34-input-and-output)
35. [Database operations](#35-database-operations)
36. [SQL interface](#36-sql-interface)
37. [Interoperability](#37-interoperability)
38. [Python UDFs and when to avoid them](#38-python-udfs-and-when-to-avoid-them)
39. [Pipelines with `pipe`](#39-pipelines-with-pipe)
40. [Iteration and Python conversion](#40-iteration-and-python-conversion)
41. [Testing Polars code](#41-testing-polars-code)
42. [Common ETL patterns](#42-common-etl-patterns)
43. [Pandas → Polars translation reference](#43-pandas--polars-translation-reference)
44. [Common pandas habits to unlearn](#44-common-pandas-habits-to-unlearn)
45. [High-value method reference](#45-high-value-method-reference)

```python
import polars as pl
import polars.selectors as cs
```
---
```
                   POLARS
                      │
        ┌─────────────┴──────────────┐
        │                            │
   DATA OBJECTS                COMPUTATIONS
        │                            │
   ┌────┴─────┐                   pl.Expr
   │          │                      │
DataFrame   Series                pl.col()
   │          │                   pl.lit()
   │          │                   pl.when()
   │          │                      │
   │          │                      ▼
   │          │               Expression tree
   │          │                      │
   │          │                      │
   ▼          │                      │
 .lazy()      │                      │
   │          │                      │
   ▼          │                      │
LazyFrame ◄───┼──────────────────────┘
   │          │
   │          │
.collect()    │
   │          │
   ▼          │
DataFrame     │
   │          │
   │      df["col"]
   └─────────►Series
```
---

# 1. Core mental model

Polars is built around **columnar expressions**.

In pandas, code often manipulates a `Series` immediately:

```python
df["revenue"] = df["price"] * df["quantity"]
```

In Polars:

```python
df = df.with_columns(
    revenue=pl.col("price") * pl.col("quantity")
)
```

`pl.col("price")` is an **expression** (`pl.Expr`), not a materialized `Series`.

An expression describes a computation:

```python
expr = (
    pl.col("price")
    .cast(pl.Float64)
    .fill_null(0)
    .clip(0, 10_000)
    .round(2)
)
```

The expression must be evaluated in a context:

```python
df.select(expr)
```

or:

```python
df.with_columns(clean_price=expr)
```

This expression model enables Polars to:

- reason about the whole query;
- execute operations in parallel;
- optimize lazy queries;
- push filters and column selection toward data sources;
- avoid many Python-level loops.

A useful mental model is:

```text
DataFrame / LazyFrame
        ↓
    expressions
        ↓
query/execution engine
        ↓
      result
```

---

# 2. Core Polars objects

## `pl.DataFrame`

A materialized two-dimensional table.

```python
df: pl.DataFrame
```

Example:

```python
df = pl.DataFrame(
    {
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "score": [91.5, 84.0, 95.2],
    }
)
```

## `pl.LazyFrame`

A deferred query plan.

```python
lf: pl.LazyFrame
```

Example:

```python
lf = pl.scan_parquet("data.parquet")
```

Operations are accumulated and executed when you call:

```python
result = lf.collect()
```

## `pl.Series`

A materialized one-dimensional column.

```python
s = pl.Series("values", [10, 20, 30])
```

## `pl.Expr`

A symbolic computation.

```python
expr = pl.col("amount").sum()
```

## Important distinction

```python
pl.col("amount")
```

returns an expression.

```python
df["amount"]
```

returns a Series.

Use expressions for most DataFrame transformations.

---

# 3. Creating DataFrames and Series

## `pl.DataFrame()`

From a dictionary:

```python
df = pl.DataFrame(
    {
        "id": [1, 2, 3],
        "name": ["A", "B", "C"],
    }
)
```

With an explicit schema:

```python
df = pl.DataFrame(
    {
        "id": [1, 2, 3],
        "value": [10, 20, 30],
    },
    schema={
        "id": pl.Int64,
        "value": pl.Int32,
    },
)
```

## `pl.Series()`

```python
s = pl.Series(
    "score",
    [10, 20, 30],
    dtype=pl.Int64,
)
```

## Conversion constructors

```python
pl.from_dict(...)
pl.from_dicts(...)
pl.from_records(...)
pl.from_numpy(...)
pl.from_pandas(...)
pl.from_arrow(...)
```

Example:

```python
records = [
    {"id": 1, "name": "A"},
    {"id": 2, "name": "B"},
]

df = pl.from_dicts(records)
```

---

# 4. Expressions

## `pl.col()`

Reference one or more columns.

```python
pl.col("amount")
```

Multiple columns:

```python
pl.col("amount", "cost")
```

By dtype:

```python
pl.col(pl.Int64)
pl.col(pl.Int64, pl.Float64)
```

Regex column matching can be used where appropriate:

```python
pl.col("^sales_.*$")
```

## `pl.lit()`

Create a literal expression:

```python
pl.lit(100)
pl.lit("active")
pl.lit(True)
pl.lit(None)
```

Example:

```python
df.with_columns(
    source=pl.lit("model_upload")
)
```

## `pl.all()`

Select all columns:

```python
df.select(pl.all())
```

Apply an expression to all columns:

```python
df.select(
    pl.all().null_count()
)
```

Exclude columns:

```python
df.select(
    pl.all().exclude("id")
)
```

## `pl.exclude()`

Select all columns except specified columns:

```python
df.select(
    pl.exclude("id", "timestamp")
)
```

## `alias()`

Rename an expression result:

```python
pl.col("amount").sum().alias("total_amount")
```

Keyword naming is often cleaner:

```python
df.select(
    total_amount=pl.col("amount").sum()
)
```

## `name` namespace

Expression name operations can dynamically manipulate output names.

Examples include concepts such as:

```python
pl.col("^sales_.*$").name.prefix("clean_")
pl.col("^sales_.*$").name.suffix("_sum")
```

Useful when one expression expands to multiple columns.

## Expression composition

An expression is a description of a calculation (`pl.Expr`), not the calculated column itself. Assigning it to a Python variable makes the **calculation reusable**; it does not immediately evaluate the DataFrame or create a materialized column.

```python
distance = pl.col("speed") * pl.col("duration")
remaining = pl.col("target_distance") - distance

df.with_columns(
    distance=distance,
    remaining=remaining,
)
```

For `speed=[3, 5]`, `duration=[4, 2]`, and `target_distance=[20, 15]`:

| distance | remaining |
|---:|---:|
| 12 | 8 |
| 10 | 5 |

Both expressions can run within **one** `with_columns()` call because `remaining` reuses the `distance` expression itself. By contrast, `pl.col("distance")` looks for a column called `distance` in that call's **input** DataFrame.

In a lazy query, Polars may also identify equivalent subexpressions and optimize repeated computations. Reusing a Python `Expr` object does not itself guarantee that an intermediate result is materialized or calculated only once.

Reusable expression functions:

```python
def normalize_amount(column: str) -> pl.Expr:
    return (
        pl.col(column)
        .cast(pl.Float64, strict=False)
        .fill_null(0)
        .clip(lower_bound=0)
    )

df.with_columns(
    amount_clean=normalize_amount("amount")
)
```

---

# 5. Column selection

## `select()`

Return only selected/computed expressions.

```python
df.select(
    "id",
    "name",
)
```

Expressions:

```python
df.select(
    "id",
    doubled=pl.col("amount") * 2,
)
```

Multiple transformations:

```python
df.select(
    pl.col("amount").sum().alias("sum"),
    pl.col("amount").mean().alias("mean"),
)
```

## Select by dtype

```python
df.select(
    pl.col(pl.Int64)
)
```

## Select all except

```python
df.select(
    pl.exclude("temporary_column")
)
```

## `select_seq()`

Evaluates expressions sequentially rather than in parallel.

```python
df.select_seq(
    pl.col("a") + 1,
    pl.col("b") + 1,
)
```

Useful when individual expressions are very cheap and parallelization overhead is unnecessary.

`select()` may execute independent expressions concurrently; `select_seq()` avoids the overhead of doing so. **Sequential evaluation does not imply that one expression can reference an alias created by its sibling.** Each expression still uses the input schema.

```python
df = pl.DataFrame({"a": [1, 2], "b": [5, 8]})

df.select_seq(
    next_a=pl.col("a") + 1,
    next_b=pl.col("b") + 1,
)
```

| next_a | next_b |
|---:|---:|
| 2 | 6 |
| 3 | 9 |

For larger or more expensive independent expressions, normal `select()` is usually the better default. Measure with `timeit` or an appropriate benchmark instead of assuming sequential execution is faster.

`timeit` is a module in Python's **standard library**, while `time.perf_counter()` is a high-resolution timer often used for measuring one code block. The former repeats a statement to reduce noise:

```python
from timeit import repeat

measurements = repeat(
    lambda: df.select_seq(
        a=pl.col("x") + 1,
        b=pl.col("y") + 1,
    ),
    number=100,
    repeat=5,
)

best_seconds_per_call = min(measurements) / 100
```

Compare this with an otherwise identical `select()` benchmark on representative data. For a **lazy** query, include `.collect()` in what you time; otherwise you may only measure the cost of constructing the query plan.

---

# 6. Selectors

Import:

```python
import polars.selectors as cs
```

Selectors are especially useful for wide DataFrames.

## Type selectors

```python
cs.numeric()
cs.integer()
cs.float()
cs.string()
cs.boolean()
cs.temporal()
cs.date()
cs.datetime()
cs.duration()
cs.categorical()
```

Examples:

```python
df.select(cs.numeric())
```

```python
df.with_columns(
    cs.numeric().fill_null(0)
)
```

## Name selectors

```python
cs.starts_with("sales_")
cs.ends_with("_id")
cs.contains("amount")
cs.matches(r"^feature_\d+$")
```

## Selector set operations

Union:

```python
cs.integer() | cs.float()
```

Intersection:

```python
cs.numeric() & cs.starts_with("sales_")
```

Difference:

```python
cs.numeric() - cs.ends_with("_id")
```

Complement:

```python
~cs.string()
```

## Example: transform all feature columns

```python
feature_cols = (
    cs.numeric()
    & cs.starts_with("feature_")
)

df = df.with_columns(
    feature_cols.fill_null(0)
)
```

---

# 7. Selecting and creating columns

## `with_columns()`

Add or replace columns **without discarding the others**. It accepts expressions, so its role is broader than merely assigning new columns: the same method also casts types, cleans values, derives features, applies conditional logic, and computes grouped/window transformations.

```python
df = df.with_columns(
    kinetic_energy=0.5 * pl.col("mass") * pl.col("velocity") ** 2
)
```

Several independent operations in one call:

```python
df = df.with_columns(
    temperature=pl.col("temperature").cast(pl.Float64, strict=False),
    station=pl.col("station").str.strip_chars().str.to_uppercase(),
    year=pl.col("observed_at").dt.year(),
    above_freezing=pl.col("temperature").cast(pl.Float64, strict=False) > 0,
)
```

Notice that `temperature` is **replaced** because the expression's output name matches an existing column; `year` and `above_freezing` are **added**. The new DataFrame is returned; the original is not modified in place. Unchanged columns need not have all their underlying data copied.

Other useful patterns:

```python
df.with_columns(
    sensor_status=pl.when(pl.col("reading").is_null())
                    .then(pl.lit("missing"))
                    .otherwise(pl.lit("recorded")),
    reading=pl.col("reading").fill_null(0),
    local_hour=pl.col("timestamp").dt.hour(),
)
```

Each expression above reads the original columns. In particular, `sensor_status` checks the **original** nulls; it does not see the filled `reading` from the same call.

### Important expression dependency detail

Expressions within the same `with_columns()` call should generally be thought of as evaluated from the input schema of that context.

If one new expression depends on another newly created column, use a second `with_columns()` call:

```python
df = (
    df
    .with_columns(
        revenue=pl.col("price") * pl.col("quantity")
    )
    .with_columns(
        margin=pl.col("revenue") - pl.col("cost")
    )
)
```

or reuse the underlying expression:

```python
revenue = pl.col("price") * pl.col("quantity")

df = df.with_columns(
    revenue=revenue,
    margin=revenue - pl.col("cost"),
)
```

The second form repeats the **definition** of `revenue` in the expression graph; it does not fetch a newly stored `revenue` column. This distinction matters in formula pipelines with intermediate dependencies.

## `with_columns_seq()`

Sequential counterpart to `with_columns()` for cheap expressions.

```python
df.with_columns_seq(
    pl.col("a").cast(pl.Int64),
    pl.col("b").cast(pl.Int64),
)
```

As with `select_seq()`, sequential execution is a performance choice for independent, cheap expressions. It is **not** a mechanism for referring to a column created earlier in the same call. Use chained `with_columns()` calls for actual column dependencies.

## `with_row_index()`

Add an explicit row index column:

```python
df.with_row_index()
```

Custom name and offset:

```python
df.with_row_index(
    name="row_id",
    offset=100,
)
```

Polars does not use a pandas-style implicit row index as a central abstraction.

In pandas, every DataFrame has an `Index`, which can carry labels (`0, 1, 2`, dates, identifiers) separately from the data columns. pandas can align Series by these labels, not merely by position.

In Polars, rows have positions, but no independent, implicit index used for label alignment. `with_row_index()` adds an **ordinary column** (normally named `index`) containing consecutive integers.

```python
df = pl.DataFrame({"species": ["oak", "pine", "elm"]})
df.with_row_index(name="row_id", offset=100)
```

| row_id | species |
|---:|---|
| 100 | oak |
| 101 | pine |
| 102 | elm |

If you filter that result, surviving `row_id` values retain their original numbers; they are not automatically renumbered. To assign fresh positions after filtering, call `with_row_index()` on the filtered frame instead. For cross-frame alignment, use explicit keys and `join()`.

---

# 8. Filtering rows

## `filter()`

```python
df.filter(
    pl.col("amount") > 100
)
```

Multiple conditions:

```python
df.filter(
    (pl.col("amount") > 100)
    & (pl.col("status") == "active")
)
```

Multiple predicate arguments are ANDed:

```python
df.filter(
    pl.col("amount") > 100,
    pl.col("status") == "active",
)
```

These two calls are **equivalent**: the first supplies one combined boolean expression, whereas the second supplies two separate predicate arguments that Polars combines with AND.

```python
df = pl.DataFrame({
    "temperature": [15, 30, 38],
    "humidity": [20, 45, 80],
})

df.filter(
    pl.col("temperature") > 25,
    pl.col("humidity") < 60,
)
```

Result: only `temperature=30, humidity=45`.

For **OR**, join the conditions explicitly using `|`:

```python
df.filter(
    (pl.col("temperature") < 20)
    | (pl.col("humidity") > 70)
)
```

For simple equality conditions, keyword constraints are convenient: `df.filter(status="active")`. Keyword constraints are ANDed with other predicates.

## Comparison operators

```python
pl.col("x") == 10
pl.col("x") != 10
pl.col("x") > 10
pl.col("x") >= 10
pl.col("x") < 10
pl.col("x") <= 10
```

## Boolean operators

AND:

```python
condition_a & condition_b
```

OR:

```python
condition_a | condition_b
```

NOT:

```python
~condition
```

Use parentheses around compound comparison expressions.

## `is_in()`

```python
df.filter(
    pl.col("country").is_in(["CA", "US", "GB"])
)
```

Pandas equivalent:

```python
df["country"].isin(...)
```

## `is_between()`

```python
df.filter(
    pl.col("age").is_between(18, 65)
)
```

## `is_null()` / `is_not_null()`

```python
df.filter(
    pl.col("value").is_not_null()
)
```

## `is_nan()` / `is_not_nan()`

```python
df.filter(
    pl.col("value").is_not_nan()
)
```

## `is_finite()` / `is_infinite()`

```python
df.filter(
    pl.col("value").is_finite()
)
```

These predicates distinguish concepts that are easily confused:

| Value | `is_null()` | `is_nan()` | `is_finite()` | `is_infinite()` |
|---|---|---|---|---|
| `3.5` | false | false | true | false |
| `float("nan")` | false | true | false | false |
| `float("inf")` | false | false | false | true |
| `float("-inf")` | false | false | false | true |
| `None` → null | true | null | null | null |

Here, `null` in a predicate result means **unknown**, not `false`. `filter()` retains only rows where the predicate evaluates to `true`.

`NaN` is a floating-point number encoding an undefined numerical result (for example `0.0 / 0.0` in NumPy), not the same as Polars' missing-value marker `null`. In NumPy, `np.nan` is often used *as* a missing-value sentinel because a traditional floating-point array has no separate null mask. In Polars, null and NaN are distinct.

**Finite** means a real numeric value other than positive/negative infinity or NaN. `is_not_nan()` still accepts `±inf`; use `is_finite()` when both NaN and infinity should be excluded.

## `remove()`

The inverse concept of `filter`: drop rows matching predicates.

```python
df.remove(
    pl.col("status") == "invalid"
)
```

This can read more naturally when the intent is explicitly to remove matching rows.

---

# 9. Conditional expressions

## `pl.when().then().otherwise()`

Equivalent to many uses of `np.where` and `np.select`.

```python
df.with_columns(
    category=(
        pl.when(pl.col("amount") >= 1000)
        .then(pl.lit("large"))
        .otherwise(pl.lit("small"))
    )
)
```

The first matching condition determines the value returned for each row. However, **Polars does not short-circuit the evaluation of branch expressions**: the expressions in all branches must be valid independently. For example, `when(pl.col("x") > 0).then(pl.col("missing_column"))` still fails if that column does not exist, even if the condition is false for every row.

Multiple branches:

```python
df.with_columns(
    risk=(
        pl.when(pl.col("score") >= 90)
        .then(pl.lit("high"))
        .when(pl.col("score") >= 70)
        .then(pl.lit("medium"))
        .otherwise(pl.lit("low"))
    )
)
```

Use expressions in branches:

```python
df.with_columns(
    adjusted=(
        pl.when(pl.col("currency") == "USD")
        .then(pl.col("amount") * pl.col("fx_rate"))
        .otherwise(pl.col("amount"))
    )
)
```

## `coalesce()`

Return the first non-null expression:

```python
df.with_columns(
    display_name=pl.coalesce(
        "preferred_name",
        "legal_name",
        "username",
    )
)
```

SQL analogy:

```sql
COALESCE(preferred_name, legal_name, username)
```

`coalesce()` chooses the first **non-null** value on each row—not the first truthy value. Thus `0`, `False`, and `""` are all valid values and are **not** skipped; only null is.

For `preferred_name=[null, "", "Ada"]` and `legal_name=["Alice", "Bob", "Ada L."]`, the result is `["Alice", "", "Ada"]`.

---

# 10. Sorting and row selection

## `sort()`

```python
df.sort("amount")
```

`DataFrame.sort()` reorders **entire rows** according to one or more keys, keeping column values from each record together.

Descending:

```python
df.sort(
    "amount",
    descending=True,
)
```

Multiple keys:

```python
df.sort(
    ["region", "amount"],
    descending=[False, True],
)
```

Control null placement when needed:

```python
df.sort(
    "amount",
    nulls_last=True,
)
```

## Expression `sort()`

```python
pl.col("value").sort()
```

## `sort_by()`

Sort one expression using another:

```python
pl.col("customer").sort_by(
    "revenue",
    descending=True,
)
```

Compare all three forms on a small observational dataset:

```python
df = pl.DataFrame({
    "specimen": ["A", "B", "C"],
    "mass": [30, 10, 20],
})

df.sort("mass")
```

| specimen | mass |
|---|---:|
| B | 10 |
| C | 20 |
| A | 30 |

```python
df.select(
    sorted_mass=pl.col("mass").sort(),
    specimen_by_mass=pl.col("specimen").sort_by("mass"),
)
```

| sorted_mass | specimen_by_mass |
|---:|---|
| 10 | B |
| 20 | C |
| 30 | A |

- `df.sort("mass")`: sorts the **DataFrame** by mass.
- `pl.col("mass").sort()`: sorts the **values of that expression**.
- `pl.col("specimen").sort_by("mass")`: returns specimen values ordered according to a **different expression**, mass.

Be careful when mixing independently sorted expressions with untouched columns in `select()`: it does **not** mean the whole row was reordered. Use `df.sort()` to preserve row associations.

Useful inside aggregation:

```python
df.group_by("region").agg(
    top_customers=(
        pl.col("customer")
        .sort_by("revenue", descending=True)
        .head(3)
    )
)
```

## `head()`

```python
df.head()
df.head(20)
```

## `tail()`

```python
df.tail()
df.tail(20)
```

## `limit()`

```python
df.limit(100)
```

## `first()`

```python
df.first()
```

Expression:

```python
pl.col("value").first()
```

## `last()`

```python
df.last()
```

Expression:

```python
pl.col("value").last()
```

## `slice()`

```python
df.slice(
    offset=10,
    length=5,
)
```

## `gather()`

Select rows by index positions:

```python
df.gather([0, 3, 7])
```

## `gather_every()`

Select every nth row:

```python
df.gather_every(10)
```

## `sample()`

Fixed number:

```python
df.sample(
    n=100,
    seed=42,
)
```

Fraction:

```python
df.sample(
    fraction=0.10,
    seed=42,
)
```

Shuffle:

```python
df.sample(
    fraction=1.0,
    shuffle=True,
    seed=42,
)
```

## `top_k()`

```python
df.top_k(
    10,
    by="revenue",
)
```

## `bottom_k()`

```python
df.bottom_k(
    10,
    by="revenue",
)
```

---

# 11. Renaming, dropping, and schema operations

## `rename()`

```python
df.rename(
    {
        "old": "new",
        "amt": "amount",
    }
)
```

## `drop()`

```python
df.drop("temporary")
```

Multiple:

```python
df.drop(
    "temporary",
    "debug_column",
)
```

## `columns`

```python
df.columns
```

## `dtypes`

```python
df.dtypes
```

## `schema`

```python
df.schema
```

Example:

```python
Schema({
    "id": Int64,
    "name": String,
    "amount": Float64,
})
```

## `collect_schema()` on LazyFrame

Prefer:

```python
lf.collect_schema()
```

when resolving a lazy schema.

## `shape`

```python
df.shape
# (rows, columns)
```

## `height`

```python
df.height
```

## `width`

```python
df.width
```

## `estimated_size()`

Estimate memory size:

```python
df.estimated_size()
```

Useful for memory diagnostics.

## `clear()`

Create an empty frame preserving schema:

```python
empty = df.clear()
```

Or an empty frame with a requested number of null rows where supported:

```python
empty = df.clear(n=5)
```

## `clone()`

```python
copy = df.clone()
```

Polars' immutable-style expression workflow means explicit copying is needed much less often than in pandas.

---

# 12. Casting and data types

## Common scalar data types

An integer type ending in `8`, `16`, `32`, or `64` uses that many **bits**. With `n` bits, there are `2ⁿ` possible bit patterns.

| Type | Value range | Interpretation |
|---|---|---|
| `Int8` | −128 to 127 | Signed, 8 bits |
| `UInt8` | 0 to 255 | Unsigned, 8 bits |
| `Int16` | −32,768 to 32,767 | Signed, 16 bits |
| `UInt16` | 0 to 65,535 | Unsigned, 16 bits |
| `Int32` | −2³¹ to 2³¹−1 | Signed, 32 bits |
| `UInt32` | 0 to 2³²−1 | Unsigned, 32 bits |
| `Int64` | −2⁶³ to 2⁶³−1 | Signed, 64 bits |
| `UInt64` | 0 to 2⁶⁴−1 | Unsigned, 64 bits |

In general:

- **Signed `IntN`**: −2^(N−1) through 2^(N−1)−1; can store negative and positive integers.
- **Unsigned `UIntN`**: 0 through 2^N−1; dedicates all bit patterns to nonnegative values.

For instance, an 8-bit sensor counter that never drops below zero can use `UInt8` for 0–255 readings; `Int8` can represent −128–127. These are fixed-width types, unlike Python's arbitrary-precision `int`. Casting an out-of-range value may raise (or produce null with `strict=False`).

Signed integers:

```python
pl.Int8
pl.Int16
pl.Int32
pl.Int64
pl.Int128
```

Unsigned integers:

```python
pl.UInt8
pl.UInt16
pl.UInt32
pl.UInt64
```

Floating point:

```python
pl.Float32
pl.Float64
```

Other primitives:

```python
pl.Boolean
pl.String
pl.Binary
pl.Decimal
```

“Primitive” here means a **single scalar value per cell**, in contrast with nested values such as `List`, `Array`, and `Struct`. This is a useful conceptual distinction rather than an exact claim about physical storage: `String` and `Binary` are variable-width, and `Decimal` has fixed-precision numeric semantics.

- `Boolean`: `True` / `False`, plus possible null.
- `String`: Unicode text.
- `Binary`: arbitrary bytes (such as encoded measurement packets).
- `Decimal(precision=10, scale=3)`: exact decimal representation with ten total digits, three after the decimal point—useful when binary floating-point rounding is unacceptable.

Temporal:

```python
pl.Date
pl.Datetime
pl.Time
pl.Duration
```

Nested:

```python
pl.List
pl.Array
pl.Struct
```

Categorical:

```python
pl.Categorical
pl.Enum
```

Special:

```python
pl.Null
pl.Object
```

## `cast()`

```python
df.with_columns(
    pl.col("amount").cast(pl.Float64)
)
```

Non-strict casting:

```python
df.with_columns(
    pl.col("amount").cast(
        pl.Float64,
        strict=False,
    )
)
```

Values that cannot be converted can become null instead of raising.

For example:

```python
df = pl.DataFrame({"reading": ["12.5", "bad", "8.0"]})

df.with_columns(
    reading=pl.col("reading").cast(pl.Float64, strict=False)
)
```

The output is `reading=[12.5, null, 8.0]` (`Float64`). With the default `strict=True`, `"bad"` causes an exception instead. For scientific measurement inputs, non-strict parsing can be paired with a separate rejection flag to preserve evidence of malformed entries.

## Cast multiple columns

```python
df.with_columns(
    cs.integer().cast(pl.Int64)
)
```

## DataFrame-level `cast()`

Cast by mapping:

```python
df.cast(
    {
        "id": pl.Int64,
        "amount": pl.Float64,
    }
)
```

## Schema validation pattern

```python
expected_schema = {
    "id": pl.Int64,
    "amount": pl.Float64,
    "date": pl.Date,
}

df = df.cast(expected_schema)
```

## `match_to_schema()`

Useful when evolving or aligning a frame to a target schema under controlled rules.

This is valuable in production pipelines where schemas can evolve and you need explicit behavior for missing or additional fields.

Unlike a plain `cast()`, this operation can apply schema-evolution policies to **missing and extra columns**, as well as dtypes. For example, an older observation batch might lack a newly introduced `sensor_quality` column, while a newer batch contains it. Explicit schema matching lets a pipeline decide whether to insert that field, reject the batch, or handle extra fields—instead of relying on implicit concatenation behavior.

---

# 13. Missing values and NaN

Polars distinguishes **null** from **NaN**.

- `null`: an absent value, represented separately from the underlying data values. Any supported dtype can contain nulls.
- `NaN`: an IEEE floating-point value meaning “not a number”; not the same as a missing entry.
- `+inf` / `-inf`: positive/negative infinity in floating-point arithmetic; neither null nor NaN.

For scientific observations:

| Observation | Meaning | Polars representation |
|---|---|---|
| Sensor failed to record | Measurement is absent | `null` |
| Numeric operation yielded an undefined result | A floating-point value exists, but is NaN | `float("nan")` |
| Numeric operation overflowed to positive infinity | Non-finite floating point | `float("inf")` |

`np.nan` is commonly treated as a “missing value” in NumPy/pandas numeric arrays, but Polars keeps null and NaN separate. Consequently, `fill_null()` does not replace NaN, and `fill_nan()` does not replace null.

## Null checks

```python
pl.col("x").is_null()
pl.col("x").is_not_null()
```

## NaN checks

```python
pl.col("x").is_nan()
pl.col("x").is_not_nan()
```

## `null_count()`

```python
df.null_count()
```

Expression:

```python
df.select(
    pl.all().null_count()
)
```

## `fill_null()`

Literal:

```python
pl.col("x").fill_null(0)
```

Forward fill:

```python
pl.col("x").fill_null(
    strategy="forward"
)
```

Backward fill:

```python
pl.col("x").fill_null(
    strategy="backward"
)
```

Statistical strategies can also be used where compatible.

**Forward fill** takes the most recent **preceding** non-null value. **Backward fill** uses the next **following** non-null value.

```python
df = pl.DataFrame({"signal": [10, None, None, 40, None]})

df.select(
    original="signal",
    forward=pl.col("signal").fill_null(strategy="forward"),
    backward=pl.col("signal").fill_null(strategy="backward"),
)
```

| original | forward | backward |
|---:|---:|---:|
| 10 | 10 | 10 |
| null | 10 | 40 |
| null | 10 | 40 |
| 40 | 40 | 40 |
| null | 40 | null |

Forward fill cannot fill **leading** nulls without an earlier valid reading; backward fill cannot fill **trailing** nulls without a later valid reading. Both use the **current row order**, not an implicit time axis. Sort by timestamp first if chronological order matters.

```python
df.sort(["sensor_id", "timestamp"]).with_columns(
    signal_filled=(
        pl.col("signal")
        .fill_null(strategy="forward")
        .over("sensor_id")
    )
)
```

The `over("sensor_id")` limits the fill to each sensor; it avoids carrying a reading from one sensor into another. Use `limit=...` with forward/backward strategies when only a limited number of consecutive nulls may be imputed.

This replacement of missing observations is called **imputation**. Choosing forward fill assumes the last observation remains applicable; backward fill makes the analogous assumption about the next observation. These assumptions are often inappropriate for rapidly changing signals.

## `fill_nan()`

```python
pl.col("x").fill_nan(0)
```

## `drop_nulls()`

Entire row if any selected column is null:

```python
df.drop_nulls()
```

Subset:

```python
df.drop_nulls(
    subset=["id", "amount"]
)
```

## `drop_nans()`

```python
df.drop_nans()
```

Subset where applicable:

```python
df.drop_nans(
    subset=["score"]
)
```

## `interpolate()`

Interpolate missing numeric values:

```python
df.interpolate()
```

Expression:

```python
pl.col("value").interpolate()
```

Unlike forward/backward fill, **linear interpolation** estimates intermediate values from the readings **on both sides** of a gap.

```python
df = pl.DataFrame({"temperature": [10.0, None, None, 40.0]})
df.with_columns(
    estimated=pl.col("temperature").interpolate()
)
```

| temperature | estimated |
|---:|---:|
| 10.0 | 10.0 |
| null | 20.0 |
| null | 30.0 |
| 40.0 | 40.0 |

Here the gap spans three equal row intervals, so each interval adds `(40−10)/3 = 10`.

By default, interpolation assumes **equal spacing between rows**, even when measurements happened at irregular times. If a numeric/date x-coordinate matters, use `interpolate_by()`:

```python
df = pl.DataFrame({
    "day": [1, 2, 5],
    "temperature": [10.0, None, 40.0],
})

df.select(
    equal_steps=pl.col("temperature").interpolate(),
    actual_days=pl.col("temperature").interpolate_by("day"),
)
```

| equal_steps | actual_days |
|---:|---:|
| 10.0 | 10.0 |
| 25.0 | 17.5 |
| 40.0 | 40.0 |

The actual-day estimate is `10 + (40−10) × (2−1)/(5−1) = 17.5`.

`interpolate(method="nearest")` instead takes the nearest known value by position. Standard interpolation normally leaves leading/trailing nulls without two surrounding values unchanged. It interpolates **nulls**, not NaNs; clean NaNs separately if needed.

Interpolation is appropriate when continuity between measurements is a defensible assumption—for example, a moderately smooth sensor signal. It is not equivalent to recovering the original missing measurement.

## Missing-value summary

```python
df.select(
    [
        pl.col(c).null_count().alias(c)
        for c in df.columns
    ]
)
```

Or:

```python
df.select(
    pl.all().null_count()
)
```

---

# 14. Numeric expressions

Arithmetic:

```python
pl.col("a") + pl.col("b")
pl.col("a") - pl.col("b")
pl.col("a") * pl.col("b")
pl.col("a") / pl.col("b")
pl.col("a") // pl.col("b")
pl.col("a") % pl.col("b")
pl.col("a") ** 2
```

## `abs()`

```python
pl.col("x").abs()
```

## `round()`

```python
pl.col("price").round(2)
```

## `floor()`

```python
pl.col("x").floor()
```

## `ceil()`

```python
pl.col("x").ceil()
```

## `sqrt()`

```python
pl.col("x").sqrt()
```

## `exp()`

```python
pl.col("x").exp()
```

## `log()`

```python
pl.col("x").log()
```

Custom base:

```python
pl.col("x").log(base=10)
```

## `log1p()`

Log of `1 + x` where available through the expression API.

Useful for skewed features with zeros.

## `pow()`

```python
pl.col("x").pow(2)
```

## `clip()`

```python
pl.col("probability").clip(0, 1)
```

Only lower bound:

```python
pl.col("amount").clip(
    lower_bound=0
)
```

Clipping **caps** every value to an interval without removing rows:

```python
df = pl.DataFrame({"probability": [-0.2, 0.3, 1.4, None]})
df.select(
    original="probability",
    clipped=pl.col("probability").clip(0, 1),
)
```

| original | clipped |
|---:|---:|
| −0.2 | 0.0 |
| 0.3 | 0.3 |
| 1.4 | 1.0 |
| null | null |

Mathematically, `clip(x, a, b) = min(max(x, a), b)`. A lower-only bound computes `max(x, a)`. It is useful for limiting outliers or bounding a model prediction, but it **does not validate** whether an out-of-range input was legitimate.

## `sign()`

```python
pl.col("x").sign()
```

Returns the sign of each number: negative → `-1`, zero → `0`, positive → `+1`; null remains null.

```python
pl.DataFrame({"change": [-12, 0, 7]}).select(
    direction=pl.col("change").sign()
)
```

Result: `direction = [-1, 0, 1]`. This identifies direction without retaining magnitude.

## `dot()`

Dot product:

```python
pl.col("a").dot(pl.col("b"))
```

The dot product of two equally sized numeric vectors is **elementwise multiplication followed by a sum**:

\[
\mathbf{a}\cdot\mathbf{b}=\sum_{i=1}^{n}a_i b_i.
\]

```python
df = pl.DataFrame({
    "a": [1, 3, 5],
    "b": [2, 4, 6],
})

df.select(
    dot=pl.col("a").dot(pl.col("b")),
    equivalent=(pl.col("a") * pl.col("b")).sum(),
)
```

Both outputs are `44`, because `1×2 + 3×4 + 5×6 = 44`.

| Operation | Result |
|---|---|
| `pl.col("a") * pl.col("b")` | `[2, 12, 30]` (elementwise) |
| `pl.col("a").dot(pl.col("b"))` | `44` (one scalar) |

This is **not** a Cartesian product: a Cartesian product would pair **every** element of `a` with **every** element of `b` (`3×3=9` pairs). The dot product pairs corresponding positions (`3` pairs) and sums their products. For per-row dot products of fixed-size array-valued columns, see `arr.dot()` instead.

## Trigonometric functions

Polars exposes numeric trigonometric operations such as:

```python
pl.col("x").sin()
pl.col("x").cos()
pl.col("x").tan()
```

and related inverse/hyperbolic functions where supported.

---

# 15. Aggregations and descriptive statistics

## `sum()`

```python
pl.col("amount").sum()
```

## `mean()`

```python
pl.col("amount").mean()
```

## `median()`

```python
pl.col("amount").median()
```

## `min()`

```python
pl.col("amount").min()
```

## `max()`

```python
pl.col("amount").max()
```

## `std()`

```python
pl.col("amount").std()
```

Standard deviation measures dispersion in the original units of the data. By default, Polars uses the sample correction (`ddof=1`). For a population standard deviation, use `std(ddof=0)`.

## `var()`

```python
pl.col("amount").var()
```

Variance is the squared standard deviation (and therefore has **squared units**). `var(ddof=0)` calculates population variance; the default sample variance uses `ddof=1`.

## `quantile()`

```python
pl.col("amount").quantile(0.95)
```

The 0.95 quantile is the estimated value below which approximately 95% of observations fall. The answer can depend on the interpolation rule (`interpolation="nearest"` by default). Quantiles describe a **distribution**; `interpolate()` estimates **missing values between observations**—two distinct operations.

## `product()`

```python
pl.col("factor").product()
```

`product()` multiplies **all values in one expression**, reducing them to one scalar:

```python
df = pl.DataFrame({"factor": [2, 3, 4]})
df.select(
    product=pl.col("factor").product(),
    sum=pl.col("factor").sum(),
)

df.select(
    cumulative=pl.col("factor").cum_prod()
)
```

| Operation | Result |
|---|---|
| `product()` | `2 × 3 × 4 = 24` |
| `sum()` | `2 + 3 + 4 = 9` |
| `cum_prod()` | `[2, 6, 24]` |
| `dot(other)` | `sum(factorᵢ × otherᵢ)`—requires another vector |

`product()` and `dot()` both multiply, but perform fundamentally different reductions. Nulls are ignored by `product()`, and its multiplicative identity for no non-null values is `1`.
## `count()`

Count non-null values:

```python
pl.col("amount").count()
```

## `pl.len()`

Count rows:

```python
pl.len()
```

Important difference:

```python
df.select(
    rows=pl.len(),
    non_null_amounts=pl.col("amount").count(),
)
```

## `n_unique()`

```python
pl.col("customer_id").n_unique()
```

**Cardinality** in set theory means the number of elements in a set, written `|S|`. The cardinality of a column's **distinct values** is therefore its number of unique values:

```python
values = ["oak", "pine", "oak", "birch", "pine"]

len(set(values))

df = pl.DataFrame({"species": values})
df.select(
    rows=pl.len(),
    distinct_species=pl.col("species").n_unique(),
)
```

Result: `rows=5`, `distinct_species=3`. In Polars, null is counted as one distinct category if it occurs.

This is the same mathematical concept as `len(set(values))` for hashable Python values. In database language, *cardinality* can also describe row counts or relationship multiplicities depending on context; “distinct cardinality” specifically denotes unique-value count.

## `approx_n_unique()`

Approximate cardinality:

```python
pl.col("customer_id").approx_n_unique()
```

Useful for very large datasets when exact cardinality is unnecessary.

Uses a probabilistic sketch (HyperLogLog++) to estimate the number of distinct values using relatively little memory. For millions of observational identifiers it may be substantially cheaper than exact set counting, but the answer is an **estimate**, not necessarily identical to `n_unique()`.

```python
df.select(
    exact=pl.col("specimen_id").n_unique(),
    estimated=pl.col("specimen_id").approx_n_unique(),
)
```

Use exact `n_unique()` for validation or integrity checks; approximation is more appropriate for exploratory cardinality estimates.

## `unique()`

Unique values in a column:

```python
pl.col("category").unique()
```

Maintain first-seen ordering when required:

```python
pl.col("category").unique(
    maintain_order=True
)
```

## `value_counts()`

```python
pl.col("category").value_counts()
```

On Series:

```python
df["category"].value_counts()
```

## `mode()`

```python
pl.col("category").mode()
```

## `arg_min()` / `arg_max()`

Positions of min/max values:

```python
pl.col("value").arg_min()
pl.col("value").arg_max()
```

## `describe()`

```python
df.describe()
```

## Correlation

```python
df.select(
    pl.corr("x", "y")
)
```

Pearson correlation measures the strength of a **linear association** on a scale from `-1` (perfect negative linear relation) to `+1` (perfect positive linear relation). A value near `0` indicates little linear association, not necessarily statistical independence.

For `x=[1, 2, 3]` and `y=[2, 4, 6]`, `pl.corr("x", "y")` is `1.0`. Doubling one variable changes the slope but not the correlation.

## Covariance

```python
df.select(
    pl.cov("x", "y")
)
```

Covariance measures how two variables vary **together**, retaining the product of their units. Positive covariance indicates they generally move in the same direction; negative covariance indicates opposite movement. Correlation normalizes covariance by both standard deviations:

$$
\operatorname{corr}(X,Y)=
\frac{\operatorname{cov}(X,Y)}
{\sigma_X\sigma_Y}.
$$

Covariance is **not** a “difference of variances” or a “variance of differences.” It is a separate measure of joint variation.

---

# 16. GroupBy

`group_by()` divides rows into partitions defined by one or more keys. An aggregation then produces **one row per group**; a window expression with `over()` usually preserves the original rows instead.

## Basic `group_by()`

```python
df.group_by("region").agg(
    pl.col("sales").sum()
)
```

Example with ecological observations:

```python
df = pl.DataFrame({
    "habitat": ["forest", "lake", "forest", "lake"],
    "species": ["oak", "trout", "pine", "frog"],
    "count": [8, 12, 5, 3],
})

df.group_by("habitat").agg(
    total=pl.col("count").sum(),
    species=pl.col("species"),
)
```

| habitat | total | species |
|---|---:|---|
| forest | 13 | ["oak", "pine"] |
| lake | 15 | ["trout", "frog"] |

Without `maintain_order=True`, the order of group rows is not guaranteed; the order within each group's collected list follows the input order.

Multiple keys:

```python
df.group_by(
    "region",
    "year",
).agg(
    total_sales=pl.col("sales").sum()
)
```

## Multiple aggregations

```python
df.group_by("region").agg(
    total_sales=pl.col("sales").sum(),
    avg_sales=pl.col("sales").mean(),
    max_sales=pl.col("sales").max(),
    customers=pl.col("customer_id").n_unique(),
    rows=pl.len(),
)
```

## `group_by().len()`

Count rows per group:

```python
df.group_by("region").len()
```

Equivalent conceptually to:

```python
df.groupby("region").size()
```

in pandas.

## Collect values into lists

```python
df.group_by("region").agg(
    pl.col("customer_id")
)
```

Without reducing the expression, each group's values are collected into a list.

This differs from `pl.col("count").sum()` (one scalar per group). The expression `pl.col("species")` produces a **List** column: each output cell contains all species names in that habitat.

## Multiple list aggregations

```python
df.group_by("region").agg(
    customers=pl.col("customer_id"),
    sales=pl.col("sales"),
)
```

## Maintain order

```python
df.group_by(
    "region",
    maintain_order=True,
).agg(...)
```

Use only when output group order is semantically required.

## Named aggregation style

```python
df.group_by("department").agg(
    mean_salary=pl.col("salary").mean(),
    p95_salary=pl.col("salary").quantile(0.95),
)
```

## Group-specific filtering

```python
df.group_by("department").agg(
    high_earners=(
        pl.col("employee")
        .filter(pl.col("salary") > 100_000)
    )
)
```

## Sorted top-N per group

```python
df.group_by("department").agg(
    top_people=(
        pl.col("employee")
        .sort_by("salary", descending=True)
        .head(3)
    )
)
```

---

# 17. Window functions with `over`

`over()` applies an expression within groups while preserving row-level shape in many common cases.

SQL analogy:

```sql
AVG(salary) OVER (PARTITION BY department)
```

Polars:

```python
df.with_columns(
    department_avg=(
        pl.col("salary")
        .mean()
        .over("department")
    )
)
```

The most important distinction is **output shape**:

```python
df = pl.DataFrame({
    "lab": ["A", "A", "B"],
    "measurement": [10.0, 20.0, 90.0],
})

df.group_by("lab").agg(
    mean=pl.col("measurement").mean()
)

df.with_columns(
    lab_mean=pl.col("measurement").mean().over("lab")
)
```

`group_by().agg()` produces **2 rows** (`A → 15`, `B → 90`). `with_columns(...over("lab"))` produces **3 rows**:

| lab | measurement | lab_mean |
|---|---:|---:|
| A | 10.0 | 15.0 |
| A | 20.0 | 15.0 |
| B | 90.0 | 90.0 |

This is similar to SQL's `OVER (PARTITION BY ...)` or pandas' grouped `transform`. Use a window when each original observation must remain available alongside the statistic of its group.

## Pandas `transform` equivalent

Pandas:

```python
df["dept_mean"] = (
    df.groupby("department")["salary"]
      .transform("mean")
)
```

Polars:

```python
df.with_columns(
    dept_mean=(
        pl.col("salary")
        .mean()
        .over("department")
    )
)
```

## Group-standardized values

```python
df.with_columns(
    zscore=(
        (
            pl.col("salary")
            - pl.col("salary").mean().over("department")
        )
        / pl.col("salary").std().over("department")
    )
)
```

## Group rank

```python
df.with_columns(
    rank_in_department=(
        pl.col("salary")
        .rank(
            method="dense",
            descending=True,
        )
        .over("department")
    )
)
```

## Group cumulative sum

```python
df.with_columns(
    cumulative_sales=(
        pl.col("sales")
        .cum_sum()
        .over("customer_id")
    )
)
```

Sort appropriately first when ordering matters:

```python
df = (
    df
    .sort(["customer_id", "date"])
    .with_columns(
        cumulative_sales=(
            pl.col("sales")
            .cum_sum()
            .over("customer_id")
        )
    )
)
```

## Multi-key windows

```python
pl.col("value").mean().over(
    ["region", "product"]
)
```

---

# 18. Cumulative, shift, diff, and ranking operations

These methods are **order-sensitive**. Polars does not invent a chronological index, so sort explicitly before applying them to time-series data.

## `shift()`

Lag:

```python
pl.col("sales").shift(1)
```

Lead:

```python
pl.col("sales").shift(-1)
```

By group:

```python
pl.col("sales").shift(1).over("customer_id")
```

Given `x=[10, 20, 40]`:

| x | `shift(1)` (previous) | `shift(-1)` (next) | `diff()` | `pct_change()` |
|---:|---:|---:|---:|---:|
| 10 | null | 20 | null | null |
| 20 | 10 | 40 | 10 | 1.0 |
| 40 | 20 | null | 20 | 1.0 |

`shift()` moves values by positions and fills the exposed boundary with nulls. `diff()` subtracts the previous value; `pct_change()` computes `current / previous - 1` (so `1.0` means 100% growth, not 1%).

## `diff()`

```python
pl.col("sales").diff()
```

Grouped:

```python
pl.col("sales").diff().over("customer_id")
```

## `pct_change()`

```python
pl.col("price").pct_change()
```

## Cumulative methods

```python
pl.col("x").cum_sum()
pl.col("x").cum_prod()
pl.col("x").cum_min()
pl.col("x").cum_max()
pl.col("x").cum_count()
```

For `x=[2, 3, 4]`:

| Method | Result |
|---|---|
| `cum_sum()` | `[2, 5, 9]` |
| `cum_prod()` | `[2, 6, 24]` |
| `cum_min()` | `[2, 2, 2]` |
| `cum_max()` | `[2, 3, 4]` |
| `cum_count()` | `[1, 2, 3]` |

Unlike a single aggregation, a cumulative operation emits an answer at **each position**. `cum_count()` counts non-null observations so far.

Reverse cumulative operations where supported:

```python
pl.col("x").cum_sum(reverse=True)
```

## `rank()`

```python
pl.col("score").rank()
```

Common methods include concepts such as:

```python
pl.col("score").rank("average")
pl.col("score").rank("min")
pl.col("score").rank("max")
pl.col("score").rank("dense")
pl.col("score").rank("ordinal")
```

Descending:

```python
pl.col("score").rank(
    method="dense",
    descending=True,
)
```

Methods differ in how tied values are treated. With `score=[90, 90, 70]` in **descending** order:

| score | `average` | `min` | `max` | `dense` | `ordinal` |
|---:|---:|---:|---:|---:|---:|
| 90 | 1.5 | 1 | 2 | 1 | 1 |
| 90 | 1.5 | 1 | 2 | 1 | 2 |
| 70 | 3.0 | 3 | 3 | 2 | 3 |

`dense` assigns equal ranks to ties **without gaps**, whereas `min` and `max` leave gaps. `ordinal` follows occurrence order, giving each value a distinct rank. `random` can break ties randomly (with a seed for reproducibility).

## `arg_sort()`

Return row indices that would sort a column:

```python
pl.col("score").arg_sort()
```

Returns **positions**, not sorted values. For `score=[30, 10, 20]`, `arg_sort()` yields `[1, 2, 0]`, whereas `sort()` yields `[10, 20, 30]`. This is analogous to NumPy's `argsort`.

## `arg_unique()`

Return indices of first unique values:

```python
pl.col("category").arg_unique()
```

---

# 19. Joins

Relational joins match **rows from two DataFrames** using keys or predicates. A key's cardinality determines whether the join preserves, duplicates, or discards rows.

## `join()`

```python
df.join(
    other,
    on="id",
    how="left",
)
```

Multiple keys:

```python
df.join(
    other,
    on=["id", "month"],
    how="left",
)
```

Different column names:

```python
df.join(
    other,
    left_on="customer_id",
    right_on="id",
    how="left",
)
```

## Join types

Let the left table be `(id, color) = [(1, "red"), (2, "blue")]` and the right table be `(id, density) = [(2, 5.0), (3, 7.0)]`.

| Join type | Output IDs | Interpretation |
|---|---|---|
| `inner` | `[2]` | Keys present in both |
| `left` | `[1, 2]` | All left rows; missing right fields become null |
| `full` | `[1, 2, 3]` | All keys from either side (possibly separate coalesced key handling) |
| `semi` | `[2]` | Left records with a matching right key, no right columns |
| `anti` | `[1]` | Left records with no matching right key |
| `cross` | four pairs | Every left row paired with every right row |

These ID sequences illustrate membership; join result **order is not guaranteed** unless the API's order controls are specified.

### Inner

```python
how="inner"
```

Keep matched rows.

### Left

```python
how="left"
```

Keep all rows from the left frame.

### Full

```python
how="full"
```

Keep rows from both sides.

### Semi

```python
how="semi"
```

Return left rows that have a match, without adding right-side columns.

Example:

```python
valid = facts.join(
    dimension,
    on="hierarchy_id",
    how="semi",
)
```

### Anti

```python
how="anti"
```

Return left rows that have no match.

Example:

```python
invalid = facts.join(
    dimension,
    on="hierarchy_id",
    how="anti",
)
```

This is particularly useful for dimension validation.

### Cross

```python
how="cross"
```

Cartesian product.

## Join suffixes

When both frames contain duplicate non-key column names:

```python
df.join(
    other,
    on="id",
    suffix="_right",
)
```

## Join validation

Where supported, validate expected join cardinality to catch accidental many-to-many relationships.

Relationship cases:

```python
measurements.join(
    sensors,
    on="sensor_id",
    how="left",
    validate="m:1",
)
```

`m:1` means each measurement may match at most one sensor metadata record; the left table may repeat its key, but the right key must be unique. `1:1` requires both keys unique, `1:m` requires unique left keys, and `m:m` imposes no uniqueness restriction.

If the right table accidentally has two rows for one sensor, a left join can **duplicate** measurement rows. Validation exposes that violation instead of silently changing the row count. Some validation options are unavailable with streaming execution.

## `join_asof()`

Match nearest ordered key rather than exact equality.

```python
trades.join_asof(
    quotes,
    on="timestamp",
    strategy="backward",
)
```

Consider a weather station reporting at `09:00`, `09:10`, and `09:20`. An event occurring at `09:12` can match:

| Strategy | Selected observation |
|---|---|
| `"backward"` | `09:10` (latest observation at/before event) |
| `"forward"` | `09:20` (first observation at/after event) |
| `"nearest"` | `09:10` (closest timestamp) |

Both inputs must be **sorted by their as-of join key**. A `tolerance` limits the permissible time/distance gap; if no candidate qualifies, the right-side fields are null.

Strategies:

```python
strategy="backward"
strategy="forward"
strategy="nearest"
```

Tolerance:

```python
trades.join_asof(
    quotes,
    on="timestamp",
    strategy="backward",
    tolerance="5m",
)
```

Match within groups:

```python
trades.join_asof(
    quotes,
    on="timestamp",
    by="ticker",
)
```

Typical applications:

- market data;
- timestamped events;
- slowly changing measurements;
- "most recent record before event" logic.

## `join_where()`

Join using one or more equality/inequality predicates rather than only exact key equality.

Conceptual interval join:

```python
events.join_where(
    periods,
    pl.col("event_time") >= pl.col("start"),
    pl.col("event_time") <= pl.col("end"),
)
```

Useful for:

- range joins;
- interval matching;
- threshold relationships;
- non-equi joins.

Unlike a standard equality join, an event can match **several intervals**, and every matching combination can appear in the output. Use it when the condition is a relationship between rows (`x ≥ start` and `x ≤ end`), not merely equal identifiers.

## `merge_sorted()`

Merge two already-sorted DataFrames using a sorted key.

Useful when data is known to be sorted and you want to preserve/merge sorted structure.

For example, two independently recorded sorted timestamp streams `[1, 4, 9]` and `[2, 6]` can be merged into a sorted stream `[1, 2, 4, 6, 9]`. Both input frames must already be sorted on the key and have compatible schemas; `merge_sorted()` does not sort arbitrary unsorted inputs.

---

# 20. Concatenation and stacking

## `pl.concat()`

Vertical concatenation:

```python
pl.concat(
    [df1, df2, df3],
    how="vertical",
)
```

Relaxed vertical concatenation can reconcile compatible numeric types where appropriate:

```python
pl.concat(
    [df1, df2],
    how="vertical_relaxed",
)
```

Diagonal concatenation can combine differing schemas:

```python
pl.concat(
    [df1, df2],
    how="diagonal",
)
```

The modes answer different schema questions:

| Mode | Effect | Example |
|---|---|---|
| `vertical` | Append rows with the same schema | Two batches with `(id, reading)` |
| `vertical_relaxed` | Append rows while finding compatible common dtypes | `Int32` + `Int64` readings |
| `diagonal` | Union column names; absent values become null | `(id, x)` + `(id, y)` |
| `horizontal` | Place columns side by side, aligned by row position | Separate feature matrices with matching row order |

For example, diagonal concatenation of `{"id":[1],"x":[10]}` with `{"id":[2],"y":[20]}` produces:

| id | x | y |
|---:|---:|---:|
| 1 | 10 | null |
| 2 | null | 20 |

Horizontal concatenation does **not** match rows by key; use `join()` for key-based alignment.

Horizontal concatenation:

```python
pl.concat(
    [df1, df2],
    how="horizontal",
)
```

## `vstack()`

```python
df1.vstack(df2)
```

Stacks **rows** (same column schema), producing more records. Compare `pl.concat([df1, df2], how="vertical")` when combining multiple frames.

## `hstack()`

```python
df.hstack(
    [
        pl.Series("new_a", [1, 2, 3]),
        pl.Series("new_b", [4, 5, 6]),
    ]
)
```

Stacks **columns** by position (compatible heights), producing more variables per record. It does not perform key matching or value alignment; use `join()` if rows must be paired by an identifier.

## `extend()`

Append rows from another DataFrame in-place-like fashion where the API allows.

This can be useful for repeated extension scenarios but should be used intentionally; for many frames, a single `pl.concat(...)` is often clearer.

`extend()` mutates the receiver, unlike ordinary expression-style transformations that return a new frame. For a collection of observational batches, one `pl.concat(batches)` is usually easier to reason about; `extend()` is useful for appending to an existing owned DataFrame.

---

# 21. Reshaping

## `pivot()`

Long → wide.

Input:

```text
id   metric   value
1    sales    100
1    cost      60
2    sales    200
2    cost     120
```

```python
df.pivot(
    on="metric",
    index="id",
    values="value",
)
```

`pivot()` is an **eager** operation because output column names arise from observed values. For a lazy pipeline, collect before pivoting or construct an equivalent aggregation when the possible columns are known in advance.

Output conceptually:

```text
id   sales   cost
1     100     60
2     200    120
```

Aggregation:

```python
df.pivot(
    on="metric",
    index="id",
    values="value",
    aggregate_function="sum",
)
```

## `unpivot()`

Wide → long.

```python
df.unpivot(
    on=["sales_2025", "sales_2026"],
    index="customer_id",
    variable_name="year",
    value_name="sales",
)
```

Conceptually replaces pandas `melt()`.

For scientific measurements, a wide table with `sample_id`, `temperature`, and `pressure` can become three columns: `sample_id`, `variable` (`"temperature"` or `"pressure"`), and `value`. This changes **column layout**, not the meaning of measurements.

## `explode()`

List column → rows.

Before:

```text
id   tags
1    ["a", "b"]
2    ["c"]
```

```python
df.explode("tags")
```

After:

```text
id   tags
1    a
1    b
2    c
```

Multiple compatible list columns may be exploded together.

## `unnest()`

Expand struct fields to columns.

```python
df.unnest("location")
```

## `transpose()`

```python
df.transpose()
```

Use sparingly for large analytical data because transposition works against the usual columnar orientation.

Transposition swaps the row and column axes; it is **not** the same as pivot/unpivot, which transform data between long and wide record layouts using identifier and variable columns. A `3×2` DataFrame becomes `2×3` (subject to naming/schema details). Transposing mixed-dtype columns may require coercion to a common dtype.

## `partition_by()`

Split a DataFrame into groups.

```python
parts = df.partition_by("region")
```

Dictionary form:

```python
parts = df.partition_by(
    "region",
    as_dict=True,
)
```

Useful for:

- writing one file per partition;
- feeding group-specific downstream processes;
- exporting separate workbooks.

---

# 22. String expressions

String operations use `.str`.

```python
pl.col("name").str...
```

## Case conversion

```python
pl.col("name").str.to_uppercase()
pl.col("name").str.to_lowercase()
```

## Strip whitespace/characters

```python
pl.col("name").str.strip_chars()
```

Specific characters:

```python
pl.col("code").str.strip_chars("-_ ")
```

Leading only:

```python
pl.col("name").str.strip_chars_start()
```

Trailing only:

```python
pl.col("name").str.strip_chars_end()
```

## Prefix/suffix checks

```python
pl.col("code").str.starts_with("ABC")
pl.col("filename").str.ends_with(".csv")
```

## Contains

Regex-aware:

```python
pl.col("text").str.contains(r"\d+")
```

Regular expressions are patterns, not ordinary substrings. For example:

```python
df = pl.DataFrame({"sample": ["A-42", "B-test", "C-7"]})
df.select(
    has_digits=pl.col("sample").str.contains(r"\d+"),
    has_dash=pl.col("sample").str.contains("-", literal=True),
)
```

| sample | has_digits | has_dash |
|---|---|---|
| A-42 | true | true |
| B-test | false | true |
| C-7 | true | true |

`literal=True` treats regex characters as ordinary text. `str.contains(".")` matches any character, but `str.contains(".", literal=True)` specifically searches for a period.

## Replace

First occurrence/pattern:

```python
pl.col("text").str.replace(
    "old",
    "new",
)
```

All occurrences:

```python
pl.col("text").str.replace_all(
    "old",
    "new",
)
```

## Extract regex group

```python
pl.col("text").str.extract(
    r"ID=(\d+)",
    group_index=1,
)
```

For `text=["ID=42", "ID=7", "missing"]`, the results are `["42", "7", null]`. Parentheses create a **capture group**; `group_index=1` retrieves the first captured group, not the entire matched substring. The digits are returned as strings until explicitly cast:

```python
pl.col("text").str.extract(r"ID=(\d+)", 1).cast(pl.Int64)
```

## Extract all matches

```python
pl.col("text").str.extract_all(
    r"\d+"
)
```

Produces a list column.

## Split

```python
pl.col("tags").str.split(",")
```

Then:

```python
df.with_columns(
    tags=pl.col("tags").str.split(",")
).explode("tags")
```

## Split exact

When a known number of fields is expected:

```python
pl.col("code").str.split_exact("-", 2)
```

The `2` means **two splits**, yielding **three fields**. For `"X-07-A"`, the resulting struct contains `"X"`, `"07"`, and `"A"`. Unlike `str.split()` (a variable-length `List`), `str.split_exact()` produces a fixed-field `Struct` that can be unnested.

## String length

Characters:

```python
pl.col("name").str.len_chars()
```

Bytes:

```python
pl.col("name").str.len_bytes()
```

Character count and byte count differ for Unicode text.

For example, `"é"` has **one Unicode character** but **two UTF-8 bytes**: `len_chars() = 1` and `len_bytes() = 2`.

## Slice

```python
pl.col("code").str.slice(
    offset=0,
    length=3,
)
```

## Head/tail characters

```python
pl.col("code").str.head(3)
pl.col("code").str.tail(4)
```

## Pad

```python
pl.col("id").str.pad_start(
    8,
    "0",
)
```

## Concatenate strings

Horizontal:

```python
pl.concat_str(
    ["first_name", "last_name"],
    separator=" ",
)
```

## Encode/decode

The string namespace includes encoding and decoding operations for supported formats.

## JSON strings

Polars provides methods for extracting/decoding JSON string content where applicable.

For nested structured data, consider parsing into `Struct`/`List` instead of repeatedly manipulating raw JSON strings.

```python
df = pl.DataFrame({"payload": ['{"pH": 7.2}', '{"pH": 6.8}']})

df.with_columns(
    parsed=pl.col("payload").str.json_decode(
        pl.Struct({"pH": pl.Float64})
    )
).unnest("parsed")
```

The resulting `pH` field is numeric, while `payload` remains the original string. Specifying the nested dtype gives a predictable schema.

## String parsing to date/datetime

```python
pl.col("date_text").str.strptime(
    pl.Date,
    "%Y-%m-%d",
)
```

Non-strict:

```python
pl.col("date_text").str.strptime(
    pl.Date,
    "%Y-%m-%d",
    strict=False,
)
```

---

# 23. Date and datetime expressions

Temporal operations use `.dt`.

## Extract components

```python
pl.col("timestamp").dt.year()
pl.col("timestamp").dt.month()
pl.col("timestamp").dt.day()
pl.col("timestamp").dt.week()
pl.col("timestamp").dt.weekday()
pl.col("timestamp").dt.ordinal_day()
pl.col("timestamp").dt.quarter()
pl.col("timestamp").dt.hour()
pl.col("timestamp").dt.minute()
pl.col("timestamp").dt.second()
pl.col("timestamp").dt.millisecond()
pl.col("timestamp").dt.microsecond()
pl.col("timestamp").dt.nanosecond()
```

## Convert datetime → date

```python
pl.col("timestamp").dt.date()
```

## Extract time

```python
pl.col("timestamp").dt.time()
```

## `strftime()`

Format temporal values:

```python
pl.col("date").dt.strftime("%Y-%m")
```

## `truncate()`

Floor to a time bucket:

```python
pl.col("timestamp").dt.truncate("1h")
pl.col("timestamp").dt.truncate("1d")
pl.col("timestamp").dt.truncate("1mo")
```

Truncation **floors** timestamps to a bucket boundary. `2026-11-18 14:37` truncated to `"1h"` becomes `14:00`; truncated to `"1mo"` it becomes `2026-11-01 00:00`.

## `round()`

Round to nearest temporal interval:

```python
pl.col("timestamp").dt.round("15m")
```

Rounding selects the nearest time boundary. `14:08` rounded to `"15m"` becomes `14:15`, whereas truncation becomes `14:00`.

## `offset_by()`

Calendar-aware offsets:

```python
pl.col("date").dt.offset_by("1mo")
pl.col("date").dt.offset_by("-3mo")
pl.col("date").dt.offset_by("1y")
```

Calendar-aware offsets matter because months differ in length. Adding `"1mo"` advances by a calendar month with month-end handling; it does **not** mean adding 30 days. Fixed elapsed durations and calendar periods have different semantics.

## Month boundaries

Normalize a date to the first or last date of its calendar month:

```python
pl.col("date").dt.month_start()
pl.col("date").dt.month_end()
```

For `2024-02-12`, these produce `2024-02-01` and `2024-02-29`. The end-of-month result accounts for leap years; it is not equivalent to always adding 30 days.

## Time zone conversion

Convert an aware datetime to another time zone:

```python
pl.col("timestamp").dt.convert_time_zone(
    "America/Toronto"
)
```

Replace/assign timezone interpretation:

```python
pl.col("timestamp").dt.replace_time_zone(
    "America/Toronto"
)
```

These operations are semantically different.

- `convert_time_zone("America/Toronto")`: preserve the **same instant**, changing the displayed clock time.
- `replace_time_zone("America/Toronto")`: reinterpret a **clock reading** as belonging to another time zone, potentially changing the represented instant.

For example, UTC `2026-01-01 12:00` converted to Toronto displays `07:00` on the same date while representing the same instant. Replacing the timezone instead interprets `12:00` as Toronto local time. Daylight-saving transitions can introduce ambiguous or nonexistent local times.

## Duration arithmetic

```python
duration = (
    pl.col("end_time")
    - pl.col("start_time")
)
```

Extract totals:

```python
duration.dt.total_days()
duration.dt.total_hours()
duration.dt.total_minutes()
duration.dt.total_seconds()
duration.dt.total_milliseconds()
duration.dt.total_microseconds()
duration.dt.total_nanoseconds()
```

## Create ranges

Date range:

```python
from datetime import date

dates = pl.date_range(
    date(2026, 1, 1),
    date(2026, 1, 31),
    interval="1d",
    eager=True,
)
```

Datetime range:

```python
pl.datetime_range(
    start,
    end,
    interval="1h",
    eager=True,
)
```

## Common duration strings

```text
1ns
1us
1ms
1s
1m
1h
1d
1w
1mo
1q
1y
```

Calendar units such as month/year are not interchangeable with fixed numbers of seconds.

---

# 24. List expressions

A `List` column stores variable-length sequences.

Example:

```text
id   scores
1    [10, 20, 30]
2    [40, 50]
```

Unlike scalar arithmetic on ordinary columns, `.list` operations work **within each row's sequence**. Each row can contain a different number of elements.

List operations use `.list`.

## Length

```python
pl.col("scores").list.len()
```

## First/last

```python
pl.col("scores").list.first()
pl.col("scores").list.last()
```

## Get by index

```python
pl.col("scores").list.get(0)
pl.col("scores").list.get(-1)
```

## Slice

```python
pl.col("scores").list.slice(
    offset=1,
    length=2,
)
```

## Head/tail

```python
pl.col("scores").list.head(2)
pl.col("scores").list.tail(2)
```

## Sum/mean/min/max

```python
pl.col("scores").list.sum()
pl.col("scores").list.mean()
pl.col("scores").list.min()
pl.col("scores").list.max()
```

For `scores=[[10, 20, 30], [40, 50]]`:

| scores | `list.len()` | `list.sum()` | `list.mean()` |
|---|---:|---:|---:|
| [10, 20, 30] | 3 | 60 | 20.0 |
| [40, 50] | 2 | 90 | 45.0 |

Compare `pl.col("scores").list.sum()` (one result **per row**) with `pl.col("measurement").sum()` (one aggregation **across rows**).

## Contains

```python
pl.col("tags").list.contains("python")
```

## Count matches

Use list evaluation or related list counting operations depending on the desired predicate.

## Unique

```python
pl.col("values").list.unique()
```

## Sort

```python
pl.col("values").list.sort()
```

## Reverse

```python
pl.col("values").list.reverse()
```

## Join list of strings

```python
pl.col("tags").list.join(",")
```

## Difference/intersection/set operations

List namespace supports set-style operations for list columns where applicable.

For sets `A={1, 2, 3}` and `B={3, 4}`:

```python
a = pl.col("observed_species")
b = pl.col("reference_species")

a.list.set_difference(b)
a.list.set_intersection(b)
a.list.set_union(b)
a.list.set_symmetric_difference(b)
```

| Operation | Mathematical result for A, B |
|---|---|
| Difference `A \\ B` | `{1, 2}` |
| Intersection `A ∩ B` | `{3}` |
| Union `A ∪ B` | `{1, 2, 3, 4}` |
| Symmetric difference `A △ B` | `{1, 2, 4}` |

Set operations use membership semantics rather than preserving duplicate occurrences; output order is not necessarily the input order.

## `list.eval()`

Apply an expression to each element in each list.

```python
pl.col("values").list.eval(
    pl.element() * 2
)
```

For `values=[[1, 2], [3, 5, 8]]`, the result is `[[2, 4], [6, 10, 16]]`. `pl.element()` represents each **element of the current list**, not the DataFrame row.

Filter elements:

```python
pl.col("values").list.eval(
    pl.element().filter(
        pl.element() > 0
    )
)
```

Transform strings inside a list:

```python
pl.col("tags").list.eval(
    pl.element().str.to_lowercase()
)
```

## `pl.element()`

Within `list.eval`, represents the current list element.

```python
pl.col("numbers").list.eval(
    pl.element().sqrt()
)
```

## Explode lists

```python
df.explode("tags")
```

---

# 25. Array expressions

`Array` differs from `List`.

- `List`: variable length.
- `Array`: fixed shape/width.

For example, each 3D position has exactly three coordinates. A fixed-size `Array` can encode this invariant:

```python
df = pl.DataFrame({
    "position": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
}, schema={"position": pl.Array(pl.Float64, 3)})

df.select(
    total=pl.col("position").arr.sum(),
    x=pl.col("position").arr.get(0),
)
```

| total | x |
|---:|---:|
| 6.0 | 1.0 |
| 15.0 | 4.0 |

The equivalent `List` type would allow 3 elements in one row and 5 in another.

Array namespace:

```python
pl.col("vector").arr...
```

Common operations parallel many list operations:

```python
.arr.get(...)
.arr.first()
.arr.last()
.arr.sum()
.arr.mean()
.arr.min()
.arr.max()
.arr.sort()
.arr.reverse()
.arr.unique()
```

## `arr.dot()` versus `Expr.dot()`

```python
df.with_columns(
    projected=pl.col("position").arr.dot([0.0, 1.0, 0.0])
)
```

Result: `projected=[2.0, 5.0]`—a dot product **within each row's 3-element array**. In contrast, `pl.col("a").dot(pl.col("b"))` computes one dot product **down two scalar columns**.

Use `Array` for fixed-size vector-like data where the fixed width is part of the schema.

Use `List` for variable-length sequences.

---

# 26. Struct expressions

A `Struct` is a nested record with named fields.

Unlike a `List` or `Array` whose elements are accessed primarily by position, a struct's fields are accessed by **names**, and its fields can have different dtypes.

## Create a struct

```python
df.with_columns(
    location=pl.struct(
        "latitude",
        "longitude",
    )
)
```

## Access fields

```python
pl.col("location").struct.field("latitude")
```

With `latitude=[43.7, 45.5]` and `longitude=[-79.4, -73.6]`, `pl.struct("latitude", "longitude")` creates one record per row. `struct.field("latitude")` retrieves `[43.7, 45.5]` without flattening the entire record.

## Rename fields

```python
pl.col("location").struct.rename_fields(
    ["lat", "lon"]
)
```

This changes field **names inside the struct**; it does not by itself turn those fields into DataFrame columns. Use `unnest("location")` if actual top-level `lat` and `lon` columns are required. Names are positional in the declared struct field order.

## Unnest

```python
df.unnest("location")
```

## Why structs matter

Structs are useful for:

- nested JSON-like data;
- returning multiple related fields from one transformation;
- composite records;
- grouping related values without flattening immediately;
- manipulating nested datasets.

## Struct pattern for duplicate detection

A composite struct can be useful when reasoning about multi-column combinations.

```python
pl.struct(
    "id",
    "date",
    "type",
)
```

---

# 27. Categorical and Enum data

Both store repeated string-like categories with compact encodings. The important difference is **who defines the allowed values** and whether categories have a defined order.

## `pl.Categorical`

Useful for repeated string-like category values.

```python
df.with_columns(
    pl.col("category").cast(pl.Categorical)
)
```

Useful when labels are discovered from the data or can expand:

```python
df = pl.DataFrame({"species": ["oak", "pine", "oak", "birch"]})
df.with_columns(pl.col("species").cast(pl.Categorical))
```

The category set is inferred (`oak`, `pine`, `birch`). More species labels can appear later. Current categorical sorting is lexical, not an explicitly declared biological or ordinal progression.

## `pl.Enum`

Use when the complete allowed category set is known and fixed.

Conceptually:

```python
dtype = pl.Enum(
    ["low", "medium", "high"]
)
```

Then:

```python
df.with_columns(
    pl.col("risk").cast(dtype)
)
```

An Enum is both a **restricted category domain** and an **explicit ordering**. For example, biological stages have a predefined progression:

```python
stage = pl.Enum(["seed", "sprout", "mature"])

df = pl.DataFrame({
    "plant": ["A", "B", "C"],
    "stage": ["mature", "seed", "sprout"],
}).with_columns(
    pl.col("stage").cast(stage)
)

df.sort("stage")
```

Plants sort in the order `B` (seed), `C` (sprout), `A` (mature)—the **declared Enum order**, not alphabetical order. Strictly casting the new label `"flowering"` to this Enum raises because it is not an allowed category.
## Categorical vs Enum

`Categorical`:

- categories can be discovered from data;
- useful for repeated categories where set is not necessarily fixed beforehand.

`Enum`:

- allowed values are explicitly defined;
- useful when category domain is known;
- sorting follows the declared category order;
- invalid values normally raise on strict casting; with `strict=False` they can become null.

**Rule of thumb:** `Categorical` for open-ended labels such as species or equipment identifiers; `Enum` for intentional fixed domains like `["queued", "running", "complete"]` or `["seed", "sprout", "mature"]`.

---

# 28. Horizontal operations

Horizontal functions operate across columns for each row.

“Horizontal” and “vertical” refer to the axis of calculation:

```python
df = pl.DataFrame({
    "trial_1": [2.0, 4.0],
    "trial_2": [3.0, 8.0],
    "trial_3": [5.0, 12.0],
})

df.with_columns(
    trial_mean=pl.mean_horizontal("trial_1", "trial_2", "trial_3")
)
```

| trial_1 | trial_2 | trial_3 | trial_mean |
|---:|---:|---:|---:|
| 2.0 | 3.0 | 5.0 | 3.333... |
| 4.0 | 8.0 | 12.0 | 8.0 |

By contrast, `pl.col("trial_1").mean()` returns a **single scalar** `3.0` computed down the first column. Horizontal aggregates generally treat nulls differently from ordinary boolean unknowns; check the function's null semantics when missing data matters.

## `pl.sum_horizontal()`

```python
df.with_columns(
    total=pl.sum_horizontal(
        "q1",
        "q2",
        "q3",
        "q4",
    )
)
```

## `pl.mean_horizontal()`

```python
df.with_columns(
    avg=pl.mean_horizontal(
        "x1",
        "x2",
        "x3",
    )
)
```

## `pl.min_horizontal()`

```python
pl.min_horizontal("a", "b", "c")
```

## `pl.max_horizontal()`

```python
pl.max_horizontal("a", "b", "c")
```

## `pl.any_horizontal()`

```python
pl.any_horizontal(
    pl.col("a") > 0,
    pl.col("b") > 0,
)
```

This is an OR across expressions **within each row**: at least one test must be true. `pl.all_horizontal(...)` is an AND across expressions: every test must be true. These are especially useful for validating several measurement channels at once.

## `pl.all_horizontal()`

```python
pl.all_horizontal(
    pl.col("a").is_not_null(),
    pl.col("b").is_not_null(),
)
```

## `pl.concat_str()`

```python
pl.concat_str(
    ["first", "last"],
    separator=" ",
)
```

## `pl.concat_list()`

Combine columns into list values:

```python
pl.concat_list(
    ["a", "b", "c"]
)
```

## `pl.fold()`

General left fold across expressions.

```python
pl.fold(
    acc=pl.lit(0),
    function=lambda acc, x: acc + x,
    exprs=cs.numeric(),
)
```

Analogous to functional programming's left fold: apply the binary function successively, **starting from an explicit initial accumulator**. For one row with `a=2`, `b=3`, and `c=4`:

```python
pl.fold(
    acc=pl.lit(100),
    function=lambda acc, x: acc - x,
    exprs=["a", "b", "c"],
)
```

Result: `((100 - 2) - 3) - 4 = 91`.

## `pl.reduce()`

Reduce expressions without manually supplying an initial accumulator.

```python
pl.reduce(
    function=lambda acc, x: acc - x,
    exprs=["a", "b", "c"],
)
```

For the same row, this starts with the **first selected expression**, giving `(2 - 3) - 4 = -5`.

Both functions operate **horizontally on Polars expressions**, rather than iterating over Python row objects. They are analogous in spirit to `functools.reduce`, but build native expression computations. Use `sum_horizontal` / `min_horizontal` / `max_horizontal` where those named operations already express the intent.

Use specialized horizontal functions when one exists; use fold/reduce for custom expression-level reduction.

---

# 29. Time-series operations

Time-series work usually combines:

- sorting;
- `shift`;
- `diff`;
- `pct_change`;
- rolling expressions;
- `group_by_dynamic`;
- `rolling`;
- `join_asof`.

An essential invariant is that time-series calculations follow a **meaningful chronological order**. Neither `shift(1)` nor `rolling_mean(3)` knows what “previous” means unless the input is already sorted appropriately.

## Lag within entity

```python
df = (
    df
    .sort(["sensor_id", "date"])
    .with_columns(
        previous_reading=(
            pl.col("reading")
            .shift(1)
            .over("sensor_id")
        )
    )
)
```

This produces a previous reading for each sensor **without borrowing the previous row of another sensor**. The first observation within each sensor receives null.

## Month-over-month difference

```python
df.with_columns(
    change=(
        pl.col("amount")
        .diff()
        .over("customer_id")
    )
)
```

## Percent change

```python
df.with_columns(
    growth=(
        pl.col("amount")
        .pct_change()
        .over("customer_id")
    )
)
```

## Expanding cumulative total

```python
pl.col("amount").cum_sum().over("customer_id")
```

## Temporal alignment

Use `join_asof()` when one time series should be matched to the latest/nearest timestamp in another series.

---

# 30. Rolling and dynamic grouping

There are three related but distinct ideas:

| Operation | Window is based on | Output |
|---|---|---|
| `Expr.rolling_mean(window_size=3)` | The previous 3 row positions | One value per input row |
| `df.rolling(index_column="time", period="7d")` | A trailing interval relative to each observation | Aggregations for observation-based windows |
| `df.group_by_dynamic("time", every="1d")` | Regular calendar/time buckets | One aggregated row per populated bucket |

## Rolling expression methods

Common methods include:

```python
pl.col("x").rolling_sum(...)
pl.col("x").rolling_mean(...)
pl.col("x").rolling_min(...)
pl.col("x").rolling_max(...)
pl.col("x").rolling_std(...)
pl.col("x").rolling_var(...)
pl.col("x").rolling_median(...)
pl.col("x").rolling_quantile(...)
```

Example:

```python
df.with_columns(
    moving_avg=(
        pl.col("sales")
        .rolling_mean(window_size=7)
    )
)
```

For `reading=[2.0, 4.0, 8.0, 16.0]` and a 3-row rolling mean:

| reading | 3-row rolling mean |
|---:|---:|
| 2.0 | null |
| 4.0 | null |
| 8.0 | 4.6667 |
| 16.0 | 9.3333 |

The default minimum observations generally equals the window size for these fixed-size rolling aggregations, hence the first two nulls. Use `min_samples=1` if a partial window should produce a value; this changes the meaning of the early estimates.

## DataFrame/LazyFrame `rolling()`

Create rolling groups based on a temporal or integer index.

```python
df.rolling(
    index_column="timestamp",
    period="7d",
).agg(
    rolling_sales=pl.col("sales").sum()
)
```

Useful for trailing windows tied to actual timestamps.

Unlike a fixed 7-**row** rolling expression, a `"7d"` interval uses the **time distance**. A 7-day window may contain two observations or thousands, depending on sampling density. The index must be sorted (within each partition if grouping by another key). Window boundary inclusion is controlled by parameters such as `closed`.

## `group_by_dynamic()`

Create regular time buckets.

Monthly:

```python
df.group_by_dynamic(
    "timestamp",
    every="1mo",
).agg(
    total_sales=pl.col("sales").sum()
)
```

With readings at `09:03`, `09:25`, and `10:08`, hourly buckets can aggregate the first two readings into the `09:00` interval and the third into the `10:00` interval. Unlike pandas' `resample`, Polars does **not** automatically create empty time buckets for intervals with no observations.

Input must be sorted by the time index. When `period` is omitted, each bucket normally has the width specified by `every`. Using `every="1d", period="7d"` produces **overlapping 7-day windows that begin one day apart**, so a single reading can contribute to several outputs.

Hourly:

```python
df.group_by_dynamic(
    "timestamp",
    every="1h",
).agg(
    avg_value=pl.col("value").mean()
)
```

Overlapping dynamic windows:

```python
df.group_by_dynamic(
    "timestamp",
    every="1d",
    period="7d",
).agg(
    seven_day_sales=pl.col("sales").sum()
)
```

Important parameters include:

```text
every
period
offset
closed
label
group_by
start_by
```

## Conceptual difference

`group_by_dynamic`:

- creates regular time windows/buckets at chosen boundaries, including overlapping windows when configured.

`rolling`:

- creates windows relative to **each observation's index value**.

Use the one matching the temporal semantics of the problem.

---

# 31. LazyFrame

A `LazyFrame` describes a **query plan**. Most operations construct a new plan without executing it; `collect()` executes it and returns a materialized `DataFrame`.

## Create from a DataFrame

```python
lf = df.lazy()
```

## Prefer scanning when source is a file

```python
lf = pl.scan_csv("data.csv")
lf = pl.scan_parquet("data.parquet")
lf = pl.scan_ipc("data.arrow")
lf = pl.scan_ndjson("data.ndjson")
```

Starting with `scan_*` lets the lazy optimizer reason about the read itself.

## Build a lazy query

```python
lf = (
    pl.scan_parquet("transactions.parquet")
    .filter(
        pl.col("status") == "complete"
    )
    .with_columns(
        revenue=pl.col("price") * pl.col("quantity")
    )
    .group_by("customer_id")
    .agg(
        total=pl.col("revenue").sum()
    )
)
```

At this point the result is still a `LazyFrame`.

An analogy is constructing an expression tree: `filter`, `with_columns`, and `group_by` become nodes that Polars can inspect and optimize before any data must be loaded.

## `collect()`

Materialize:

```python
result = lf.collect()
```

`type(lf)` is `pl.LazyFrame`; `type(result)` is `pl.DataFrame`. Collect at the boundary where results are actually needed, rather than after each transformation.

## `collect_schema()`

Resolve output schema:

```python
schema = lf.collect_schema()
```

This returns the query's output schema (column names and dtypes) **without collecting all result rows**. Schema resolution can still require metadata access or other work; it is not equivalent to evaluating every row.

## `fetch` / small-query development

Current APIs favor explicit row limiting and collection for inspecting subsets:

```python
lf.head(20).collect()
```

## `inspect()`

Insert an inspection point into a lazy computation graph.

Useful for debugging intermediate results without permanently restructuring the pipeline.

## `cache()`

Cache an intermediate lazy result at a node in the plan.

Use carefully: the optimizer can often make better decisions without manually forcing caching.

---

# 32. Lazy optimization and query plans

Lazy execution allows whole-query optimization.

Important optimizer concepts include:

## Projection pushdown

If only a few columns are required, Polars can often avoid reading unrelated columns.

```python
result = (
    pl.scan_parquet("wide.parquet")
    .select(
        "customer_id",
        "amount",
    )
    .collect()
)
```

## Predicate pushdown

Filters can be moved toward the data source.

```python
result = (
    pl.scan_parquet("data.parquet")
    .filter(
        pl.col("year") == 2026
    )
    .collect()
)
```

For formats such as Parquet, this can substantially reduce I/O.

## Common subexpression optimization

Repeated equivalent expressions may be optimized so redundant computation is reduced.

For example, when both `zscore` and `threshold_flag` use the same costly normalized signal expression, Polars may calculate shared components once as part of its optimized execution plan. Writing a reusable Python `Expr` object makes definitions consistent; it does not require intermediate materialization.

## Join optimization

The optimizer can reason about join ordering/strategies under supported scenarios.

## `explain()`

Inspect query plan:

```python
print(lf.explain())
```

`explain()` returns a **string representation of a query plan**, not query results. An optimized plan may show filters placed close to a `SCAN` (predicate pushdown) and unnecessary columns omitted (projection pushdown). Inspect the plan when performance is surprising.

Useful for verifying:

- filters are pushed down;
- unnecessary columns are pruned;
- expected joins appear;
- expensive operations occur in the intended place.

## `show_graph()`

Visualize the query plan:

```python
lf.show_graph()
```

## `profile()`

Execute and collect profiling information:

```python
result, profile = lf.profile()
```

This **executes** the query and returns both the result DataFrame and timing/profiling information as a second DataFrame. Unlike `explain()`, it measures runtime stages; small timings may be noisy, so compare repeated runs for meaningful benchmarks.
Useful for locating expensive query stages.

## `serialize()`

Serialize a logical plan:

```python
lf.serialize(...)
```

## `deserialize()`

Reconstruct a lazy plan from serialized form where supported.

---

# 33. Streaming and sinks

Streaming execution can process data in batches rather than requiring the entire result to be held in memory at once.

Streaming is an **execution strategy**, not a separate DataFrame type. It is especially useful for large scans, filters, and aggregations whose computation can be processed in batches. Some operations still require global state, ordering, or materialization.

## Collect using streaming engine

```python
df = lf.collect(
    engine="streaming"
)
```

Not every operation has identical streaming characteristics, so inspect the plan for large workloads.

## `collect_batches()`

Evaluate a lazy query and consume ready batches.

Useful for integrating with batch-oriented downstream systems.

Compared with `collect()` (one complete `DataFrame`), `collect_batches()` yields DataFrame batches that a consumer can process incrementally. Example pattern:

```python
for batch in lf.collect_batches():
    process_batch(batch)
```

The downstream function can write, aggregate, or otherwise consume each batch without building a Python list of all rows. Check engine support and batch lifetimes for the Polars version in use.
## `sink_parquet()`

Write a lazy query directly to Parquet:

```python
lf.sink_parquet(
    "output.parquet"
)
```

## `sink_csv()`

```python
lf.sink_csv(
    "output.csv"
)
```

## `sink_ipc()`

```python
lf.sink_ipc(
    "output.arrow"
)
```

## `sink_ndjson()`

```python
lf.sink_ndjson(
    "output.ndjson"
)
```

## Delta/Iceberg sinks

Where installed/supported, Polars exposes sink integrations for table formats such as Delta Lake and Iceberg.

## Why sinks matter

Instead of:

```python
df = lf.collect()
df.write_parquet("output.parquet")
```

you may be able to:

```python
lf.sink_parquet("output.parquet")
```

This can reduce peak memory usage.

---

# 34. Input and output

## CSV

Read:

```python
df = pl.read_csv("data.csv")
```

Lazy:

```python
lf = pl.scan_csv("data.csv")
```

Useful parameters include:

```text
columns
schema
schema_overrides
separator
has_header
new_columns
null_values
missing_utf8_is_empty_string
try_parse_dates
skip_rows
n_rows
encoding
```

Example:

```python
df = pl.read_csv(
    "data.csv",
    columns=["id", "amount", "date"],
    schema_overrides={
        "id": pl.Int64,
        "amount": pl.Float64,
    },
    try_parse_dates=True,
)
```

Write:

```python
df.write_csv("output.csv")
```

## Parquet

Read:

```python
df = pl.read_parquet("data.parquet")
```

Lazy:

```python
lf = pl.scan_parquet("data.parquet")
```

Write:

```python
df.write_parquet("output.parquet")
```

Parquet is generally preferable to CSV for analytical storage because it is:

- columnar;
- typed;
- compressible;
- schema-preserving;
- compatible with projection/filter pushdown.

## IPC / Arrow

```python
pl.read_ipc(...)
pl.scan_ipc(...)
df.write_ipc(...)
```

## NDJSON

```python
pl.read_ndjson(...)
pl.scan_ndjson(...)
df.write_ndjson(...)
```

## JSON

```python
pl.read_json(...)
df.write_json(...)
```

Use NDJSON rather than monolithic JSON for many streaming/data-engineering workloads.

## Excel

Read:

```python
df = pl.read_excel("input.xlsx")
```

Write:

```python
df.write_excel("output.xlsx")
```

Excel is useful for business interchange but not usually an optimal storage format for large analytical pipelines.

## Avro

Polars includes Avro support where enabled:

```python
pl.read_avro(...)
```

## Delta Lake

Where dependencies are installed:

```python
pl.read_delta(...)
pl.scan_delta(...)
```

and corresponding write/sink operations.

## Cloud/object storage

Many Polars readers support cloud storage URLs and storage options through the relevant filesystem/cloud integrations.

---

# 35. Database operations

## `pl.read_database()`

Read using an existing connection:

```python
df = pl.read_database(
    query="SELECT * FROM transactions",
    connection=connection,
)
```

This accepts a query and an existing supported connection/engine (for example a SQLAlchemy connection). It is useful when connection lifecycle or transactions are managed elsewhere in the application.

## `pl.read_database_uri()`

Read through a connection URI where supported:

```python
df = pl.read_database_uri(
    query="SELECT id, amount FROM transactions",
    uri=uri,
)
```

This accepts a connection **URI** rather than an already-open connection and uses supported URI-based backends (for example ConnectorX or ADBC). The best choice depends on the backend, dependencies, and connection-management needs.

In both cases, `read_database*` materializes a **Polars DataFrame**. It is not a lazy SQL scan: include filters/projections in the SQL query when the database should execute them before transfer.

## `write_database()`

```python
df.write_database(
    table_name="analytics.output",
    connection=connection,
    if_table_exists="append",
)
```

## Database performance principle

Do not automatically load an entire relational table just to filter most of it in Python.

Prefer pushing relationally natural work into SQL when appropriate:

```sql
SELECT id, amount, date
FROM transactions
WHERE date >= ...
```

Then continue with Polars for transformations that belong in the application/data pipeline.

---

# 36. SQL interface

Polars includes a SQL interface.

## DataFrame `.sql()`

For queries against the current frame:

```python
result = df.sql("""
    SELECT
        region,
        SUM(revenue) AS revenue
    FROM self
    GROUP BY region
""")
```

## `pl.SQLContext`

Useful when querying multiple frames.

Conceptual pattern:

```python
ctx = pl.SQLContext(
    customers=customers,
    orders=orders,
)

result = ctx.execute("""
    SELECT
        c.customer_id,
        SUM(o.amount) AS total
    FROM customers c
    JOIN orders o
      ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
""")
```

Expressions remain the most idiomatic native API for Polars pipelines, but SQL can be useful for:

- migration from SQL-heavy workflows;
- exploratory relational queries;
- teams that already think relationally;
- complex ad hoc joins/aggregations.

---

# 37. Interoperability

## pandas → Polars

```python
df = pl.from_pandas(pdf)
```

## Polars → pandas

```python
pdf = df.to_pandas()
```

## NumPy → Polars

```python
df = pl.from_numpy(array)
```

## Polars → NumPy

```python
array = df.to_numpy()
```

Series:

```python
arr = df["value"].to_numpy()
```

## Arrow → Polars

```python
df = pl.from_arrow(table)
```

## Polars → Arrow

```python
table = df.to_arrow()
```

## Dictionaries

Rows as dictionaries:

```python
records = df.to_dicts()
```

Columns as dictionary:

```python
mapping = df.to_dict()
```

## Python rows

```python
rows = df.rows()
```

Named dictionaries:

```python
rows = df.rows(named=True)
```

Use Python-object conversion at application boundaries; avoid it as the main transformation strategy.

---

# 38. Python UDFs and when to avoid them

Polars performs best when logic remains inside native expressions.

## `map_elements()`

```python
df.with_columns(
    pl.col("x").map_elements(
        custom_python_function
    )
)
```

This is a **fallback**, not the Polars equivalent of writing arbitrary vectorized expressions. The function receives individual Python values; it typically prevents native engine optimization of the function's internals. When using it, specify `return_dtype=...` when possible so the output schema is predictable.

```python
df.with_columns(
    label=pl.col("sample_code").map_elements(
        decode_custom_code,
        return_dtype=pl.String,
    )
)
```

Null values are skipped by default for this method; account for that if the Python function must see them.

This executes Python code per element and is usually much slower than a native expression.

Instead of:

```python
pl.col("x").map_elements(
    lambda x: x * 2
)
```

use:

```python
pl.col("x") * 2
```

Instead of:

```python
pl.col("name").map_elements(
    lambda x: x.upper()
)
```

use:

```python
pl.col("name").str.to_uppercase()
```

Instead of list Python loops:

```python
pl.col("values").map_elements(...)
```

consider:

```python
pl.col("values").list.eval(...)
```

## `map_rows()`

Row-wise Python UDF:

```python
df.map_rows(function)
```

Use only when a computation genuinely cannot be expressed through native column expressions.

Unlike `map_elements()` (one selected column's values), `map_rows()` passes a **tuple of values from a row**. It is especially expensive because it converts row data into Python objects and may lose column-name information. A native expression such as `(pl.col("x") ** 2 + pl.col("y") ** 2).sqrt()` is normally preferable for a vector magnitude.

## `map_batches()`

Apply a custom function to batches rather than individual elements.

This can be useful for integrating vectorized external libraries, but it introduces an optimization boundary. Use native expressions first when possible.

It differs from per-element mapping by passing a **batch/Series** to the function, which can apply a vectorized routine (for example, a specialized scientific NumPy function). The routine still needs to return the correct shape and dtype for its context. Batch size and number of calls can vary, particularly in lazy execution; do not rely on receiving the entire dataset in one call.

## NumPy ufuncs

Many NumPy universal functions can operate with Polars expressions/Series depending on the operation.

Even then, native Polars expressions are generally the first option when an equivalent exists.

---

# 39. Pipelines with `pipe`

## `pipe()`

Apply a function that takes a frame and returns another object/frame.

```python
def clean_names(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col("name")
        .str.strip_chars()
        .str.to_lowercase()
    )

result = df.pipe(clean_names)
```

The call above is conceptually `clean_names(df)`; `pipe()` simply places a Python function into a fluent transformation chain. The function can accept extra arguments via `df.pipe(func, arg1, option=...)`. A `pipe` is not itself a special optimizer operation—whether it remains lazy depends on what the function does with its `LazyFrame` argument.

Chain functions:

```python
result = (
    df
    .pipe(clean_names)
    .pipe(validate_ids)
    .pipe(add_features)
)
```

Lazy pipeline:

```python
def clean(lf: pl.LazyFrame) -> pl.LazyFrame:
    return (
        lf
        .filter(pl.col("id").is_not_null())
        .with_columns(
            amount=pl.col("amount").cast(
                pl.Float64,
                strict=False,
            )
        )
    )

result = (
    pl.scan_parquet("data.parquet")
    .pipe(clean)
    .collect()
)
```

## `pipe_with_schema()`

Lazy-specific functionality that allows transformations using resolved schema information during planning.

Use for advanced schema-dependent lazy transformations.

---

# 40. Iteration and Python conversion

Polars is columnar. Python row iteration should not be the default.

## `iter_rows()`

```python
for row in df.iter_rows():
    ...
```

Named:

```python
for row in df.iter_rows(named=True):
    ...
```

Use at API/application boundaries, not for DataFrame transformation.

## `iter_columns()`

```python
for series in df.iter_columns():
    ...
```

## `rows()`

Materialize all rows:

```python
rows = df.rows()
```

## Why row iteration is expensive

Converting columnar data into Python tuples/dicts:

- allocates many Python objects;
- crosses the Python/native boundary;
- gives up vectorized/parallel execution;
- increases memory overhead.

---

# 41. Testing Polars code

Polars provides testing helpers.

Typical imports:

```python
from polars.testing import (
    assert_frame_equal,
    assert_series_equal,
)
```

## `assert_frame_equal()`

```python
assert_frame_equal(
    actual,
    expected,
)
```

Useful for ETL/unit tests.

## `assert_series_equal()`

```python
assert_series_equal(
    actual_series,
    expected_series,
)
```

## Useful test dimensions

Test:

- values;
- column names;
- column order;
- row order where relevant;
- dtypes;
- null behavior;
- duplicates;
- sorting invariants.

For floating-point scientific calculations, consider numerical tolerance rather than exact equality of every bit. For example:

```python
assert_frame_equal(
    actual,
    expected,
    check_exact=False,
    rel_tol=1e-6,
    abs_tol=1e-9,
)
```

This still checks the structure and values, but allows small numeric rounding differences. For discrete IDs, category codes, or financial reconciliation invariants, exact checks may be more appropriate.

Example:

```python
def test_transform():
    source = pl.DataFrame(
        {
            "amount": [10.0, None],
        }
    )

    expected = pl.DataFrame(
        {
            "amount": [10.0, 0.0],
        }
    )

    actual = source.with_columns(
        pl.col("amount").fill_null(0)
    )

    assert_frame_equal(
        actual,
        expected,
    )
```

---

# 42. Common ETL patterns

## Pattern 1: normalize schema

```python
def normalize_schema(
    df: pl.DataFrame,
) -> pl.DataFrame:
    return df.with_columns(
        pl.col("id").cast(pl.Int64),
        pl.col("amount").cast(
            pl.Float64,
            strict=False,
        ),
        pl.col("date").cast(pl.Date),
    )
```

## Pattern 2: validate foreign keys using anti join

Invalid:

```python
invalid = data.join(
    dimension.select("hierarchy_id"),
    on="hierarchy_id",
    how="anti",
)
```

Valid:

```python
valid = data.join(
    dimension.select("hierarchy_id"),
    on="hierarchy_id",
    how="semi",
)
```

## Pattern 3: detect duplicates

```python
duplicate_mask = data.is_duplicated()
```

Or define key-based duplicate rows:

```python
keys = [
    "hierarchy_id",
    "stage",
    "measure_type",
    "month_date",
    "currency",
]

duplicates = (
    data
    .group_by(keys)
    .len()
    .filter(pl.col("len") > 1)
)
```

## Pattern 4: deduplicate

```python
data = data.unique(
    subset=keys,
    keep="last",
)
```

## Pattern 5: partition outputs

```python
parts = data.partition_by(
    "measure_type",
    as_dict=True,
)
```

## Pattern 6: clean all numeric fields

```python
data = data.with_columns(
    cs.numeric()
    .fill_null(0)
)
```

## Pattern 7: trim every string field

```python
data = data.with_columns(
    cs.string().str.strip_chars()
)
```

## Pattern 8: create normalized month

```python
data = data.with_columns(
    process_month=(
        pl.col("date")
        .dt.truncate("1mo")
    )
)
```

## Pattern 9: reusable lazy ETL pipeline

```python
def transform(
    lf: pl.LazyFrame,
) -> pl.LazyFrame:
    return (
        lf
        .filter(
            pl.col("transaction_id").is_not_null()
        )
        .with_columns(
            amount=(
                pl.col("amount")
                .cast(pl.Float64, strict=False)
                .fill_null(0)
            ),
            month=(
                pl.col("transaction_date")
                .dt.truncate("1mo")
            ),
        )
        .unique(
            subset=["transaction_id"],
            keep="last",
        )
    )

result = (
    pl.scan_parquet("transactions.parquet")
    .pipe(transform)
    .collect()
)
```

## Pattern 10: validation result object

A pipeline can keep valid and rejected data separate:

```python
valid = data.join(
    dimension,
    on="id",
    how="semi",
)

rejected = data.join(
    dimension,
    on="id",
    how="anti",
)
```

This is often clearer than filtering and discarding invalid records silently.

---

# 43. Pandas → Polars translation reference

| Task | pandas | Polars |
|---|---|---|
| Create DataFrame | `pd.DataFrame(...)` | `pl.DataFrame(...)` |
| Read CSV | `pd.read_csv()` | `pl.read_csv()` |
| Lazy CSV | n/a | `pl.scan_csv()` |
| Read Parquet | `pd.read_parquet()` | `pl.read_parquet()` |
| Lazy Parquet | n/a | `pl.scan_parquet()` |
| Select columns | `df[["a", "b"]]` | `df.select("a", "b")` |
| Add/replace column | `df["x"] = ...` | `df.with_columns(x=...)` |
| Assign columns | `df.assign(...)` | `df.with_columns(...)` |
| Filter | `df[df["x"] > 0]` | `df.filter(pl.col("x") > 0)` |
| Query | `df.query(...)` | `df.filter(...)` |
| Sort | `sort_values()` | `sort()` |
| Group | `groupby()` | `group_by()` |
| Aggregate | `.agg()` | `.agg()` |
| Group transform | `groupby().transform()` | `.over()` |
| Merge | `merge()` | `join()` |
| Asof merge | `merge_asof()` | `join_asof()` |
| Non-equi join | custom/merge logic | `join_where()` |
| `isin` | `.isin()` | `.is_in()` |
| `between` | `.between()` | `.is_between()` |
| Drop columns | `.drop()` | `.drop()` |
| Rename | `.rename()` | `.rename()` |
| Missing check | `.isna()` | `.is_null()` |
| Drop missing | `.dropna()` | `.drop_nulls()` |
| Fill missing | `.fillna()` | `.fill_null()` |
| NaN handling | often same missing API | explicit `.is_nan()`, `.fill_nan()` |
| Cast | `.astype()` | `.cast()` |
| Duplicates mask | `.duplicated()` | `.is_duplicated()` |
| Remove duplicates | `.drop_duplicates()` | `.unique()` |
| Unique values | `.unique()` | `.unique()` |
| N unique | `.nunique()` | `.n_unique()` |
| Value counts | `.value_counts()` | `.value_counts()` |
| Shift | `.shift()` | `.shift()` |
| Diff | `.diff()` | `.diff()` |
| Percent change | `.pct_change()` | `.pct_change()` |
| Rank | `.rank()` | `.rank()` |
| Cumsum | `.cumsum()` | `.cum_sum()` |
| Cummax | `.cummax()` | `.cum_max()` |
| Rolling mean | `.rolling().mean()` | `.rolling_mean()` |
| Explode | `.explode()` | `.explode()` |
| Pivot | `.pivot()` | `.pivot()` |
| Pivot table | `.pivot_table()` | `.pivot(..., aggregate_function=...)` |
| Melt | `.melt()` | `.unpivot()` |
| String namespace | `.str` | `.str` |
| Datetime namespace | `.dt` | `.dt` |
| Concatenate | `pd.concat()` | `pl.concat()` |
| Row index | central abstraction | explicit column if needed |
| Apply element UDF | `.apply()` / `.map()` | prefer expressions; fallback `.map_elements()` |
| Row apply | `.apply(axis=1)` | expressions / horizontal functions |
| SQL | external/various | DataFrame SQL / `SQLContext` |
| Lazy execution | not central | `LazyFrame` |
| Execute lazy query | n/a | `.collect()` |
| Query plan | n/a | `.explain()` |
| Stream to file | n/a | `.sink_*()` |

---

# 44. Common pandas habits to unlearn

## 1. Reaching for `apply` too early

Pandas:

```python
df["x"] = df["x"].apply(
    lambda x: x * 2
)
```

Polars:

```python
df = df.with_columns(
    pl.col("x") * 2
)
```

## 2. Row-wise `axis=1`

Pandas:

```python
df["profit"] = df.apply(
    lambda row: row["revenue"] - row["cost"],
    axis=1,
)
```

Polars:

```python
df = df.with_columns(
    profit=(
        pl.col("revenue")
        - pl.col("cost")
    )
)
```

## 3. Using Python loops for column operations

Avoid:

```python
for row in df.iter_rows():
    ...
```

Prefer expressions.

## 4. Depending on implicit index alignment

Polars favors:

- explicit columns;
- explicit join keys;
- explicit ordering.

## 5. Mutating one column at a time

Instead of:

```python
df["a"] = ...
df["b"] = ...
df["c"] = ...
```

prefer:

```python
df = df.with_columns(
    a=...,
    b=...,
    c=...,
)
```

## 6. Reading everything eagerly

Instead of:

```python
df = pl.read_parquet("large.parquet")
```

consider:

```python
lf = pl.scan_parquet("large.parquet")
```

and collect only after the query is assembled.

## 7. Collecting repeatedly

Avoid:

```python
a = lf.filter(...).collect()
b = a.lazy().with_columns(...).collect()
c = b.lazy().group_by(...).agg(...).collect()
```

Prefer:

```python
result = (
    lf
    .filter(...)
    .with_columns(...)
    .group_by(...)
    .agg(...)
    .collect()
)
```

## 8. Converting to Python objects in the middle of the pipeline

Avoid frequent:

```python
to_dicts()
rows()
iter_rows()
```

unless crossing an application/API boundary.

---

# 45. High-value method reference

This section is a compact reference grouped by object/namespace.

## DataFrame / LazyFrame transformation

```text
select()
select_seq()
with_columns()
with_columns_seq()
filter()
remove()
sort()
rename()
drop()
cast()
match_to_schema()
explode()
unnest()
pivot()
unpivot()
unique()
drop_nulls()
drop_nans()
fill_null()
fill_nan()
interpolate()
interpolate_by()
with_row_index()
```

## Row selection / inspection

```text
head()
tail()
first()
last()
limit()
slice()
gather()
gather_every()
sample()
top_k()
bottom_k()
reverse()
```

## Grouping / windows

```text
group_by()
group_by_dynamic()
rolling()
agg()
over()
```

## Joining / combining

```text
join()
join_asof()
join_where()
merge_sorted()
vstack()
hstack()
extend()
pl.concat()
```

## Schema / metadata

```text
columns
dtypes
schema
shape
height
width
collect_schema()
estimated_size()
```

## Lazy execution

```text
lazy()
collect()
collect_schema()
collect_batches()
explain()
show_graph()
profile()
inspect()
cache()
serialize()
```

## Lazy sinks

```text
sink_csv()
sink_parquet()
sink_ipc()
sink_ndjson()
sink_delta()
sink_iceberg()
```

## Core expressions

```text
pl.col()
pl.lit()
pl.all()
pl.exclude()
alias()
cast()
filter()
sort()
sort_by()
```

## Boolean expressions

```text
is_null()
is_not_null()
is_nan()
is_not_nan()
is_finite()
is_infinite()
is_in()
is_between()
```

## Conditional

```text
pl.when()
then()
otherwise()
pl.coalesce()
```

## Aggregation

```text
sum()
mean()
median()
min()
max()
std()
var()
quantile()
product()
count()
pl.len()
n_unique()
approx_n_unique()
unique()
value_counts()
mode()
first()
last()
```

## Sequence/order analytics

```text
shift()
diff()
pct_change()
rank()
cum_sum()
cum_prod()
cum_min()
cum_max()
cum_count()
arg_sort()
arg_min()
arg_max()
```

## Rolling

```text
rolling_sum()
rolling_mean()
rolling_min()
rolling_max()
rolling_std()
rolling_var()
rolling_median()
rolling_quantile()
```

## Numeric

```text
abs()
round()
floor()
ceil()
sqrt()
exp()
log()
pow()
clip()
sign()
dot()
```

## String namespace

```text
str.to_uppercase()
str.to_lowercase()
str.strip_chars()
str.strip_chars_start()
str.strip_chars_end()
str.starts_with()
str.ends_with()
str.contains()
str.replace()
str.replace_all()
str.extract()
str.extract_all()
str.split()
str.split_exact()
str.slice()
str.head()
str.tail()
str.len_chars()
str.len_bytes()
str.strptime()
str.json_decode()
```

## Datetime namespace

```text
dt.year()
dt.month()
dt.day()
dt.week()
dt.weekday()
dt.ordinal_day()
dt.quarter()
dt.hour()
dt.minute()
dt.second()
dt.millisecond()
dt.microsecond()
dt.nanosecond()
dt.date()
dt.time()
dt.strftime()
dt.truncate()
dt.round()
dt.offset_by()
dt.month_start()
dt.month_end()
dt.convert_time_zone()
dt.replace_time_zone()
dt.total_days()
dt.total_hours()
dt.total_minutes()
dt.total_seconds()
```

## List namespace

```text
list.len()
list.get()
list.first()
list.last()
list.slice()
list.head()
list.tail()
list.sum()
list.mean()
list.min()
list.max()
list.contains()
list.unique()
list.sort()
list.reverse()
list.join()
list.eval()
list.set_difference()
list.set_intersection()
list.set_union()
list.set_symmetric_difference()
```

## Array namespace

```text
arr.get()
arr.first()
arr.last()
arr.sum()
arr.mean()
arr.min()
arr.max()
arr.unique()
arr.sort()
arr.reverse()
arr.dot()
```

## Struct namespace

```text
struct.field()
struct.rename_fields()
df.unnest()
pl.struct()
```

## Horizontal functions

```text
pl.sum_horizontal()
pl.mean_horizontal()
pl.min_horizontal()
pl.max_horizontal()
pl.any_horizontal()
pl.all_horizontal()
pl.concat_str()
pl.concat_list()
pl.fold()
pl.reduce()
```

## Selectors

```text
cs.numeric()
cs.integer()
cs.float()
cs.string()
cs.boolean()
cs.temporal()
cs.date()
cs.datetime()
cs.duration()
cs.categorical()
cs.starts_with()
cs.ends_with()
cs.contains()
cs.matches()
```

## Constructors / conversion

```text
pl.DataFrame()
pl.Series()
pl.from_dict()
pl.from_dicts()
pl.from_records()
pl.from_numpy()
pl.from_pandas()
pl.from_arrow()
df.to_dict()
df.to_dicts()
df.to_numpy()
df.to_pandas()
df.to_arrow()
```

## I/O

```text
pl.read_csv()
pl.scan_csv()

pl.read_parquet()
pl.scan_parquet()

pl.read_ipc()
pl.scan_ipc()

pl.read_ndjson()
pl.scan_ndjson()

pl.read_json()
pl.read_excel()
pl.read_avro()

pl.read_database()
pl.read_database_uri()

df.write_csv()
df.write_parquet()
df.write_ipc()
df.write_ndjson()
df.write_json()
df.write_excel()
df.write_database()
```

---

# Additional Practice Examples

## Example: data cleaning

```python
result = (
    df
    .with_columns(
        cs.string().str.strip_chars(),
        amount=(
            pl.col("amount")
            .cast(pl.Float64, strict=False)
            .fill_null(0)
        ),
        date=(
            pl.col("date")
            .str.strptime(
                pl.Date,
                "%Y-%m-%d",
                strict=False,
            )
        ),
    )
    .filter(
        pl.col("id").is_not_null()
    )
    .unique(
        subset=["id", "date"],
        keep="last",
    )
)
```

## Example: dimensional validation

```python
valid_ids = dimension.select("id").unique()

valid = facts.join(
    valid_ids,
    on="id",
    how="semi",
)

invalid = facts.join(
    valid_ids,
    on="id",
    how="anti",
)
```

## Example: grouped statistics

```python
summary = (
    df
    .group_by(
        "region",
        "product",
    )
    .agg(
        rows=pl.len(),
        customers=pl.col("customer_id").n_unique(),
        total_sales=pl.col("sales").sum(),
        mean_sales=pl.col("sales").mean(),
        median_sales=pl.col("sales").median(),
        p95_sales=pl.col("sales").quantile(0.95),
        min_sales=pl.col("sales").min(),
        max_sales=pl.col("sales").max(),
    )
    .sort(
        "total_sales",
        descending=True,
    )
)
```

## Example: grouped ranking

```python
ranked = (
    df
    .with_columns(
        region_rank=(
            pl.col("sales")
            .rank(
                method="dense",
                descending=True,
            )
            .over("region")
        )
    )
)
```

## Example: time-series features

```python
features = (
    df
    .sort(["customer_id", "month"])
    .with_columns(
        previous_amount=(
            pl.col("amount")
            .shift(1)
            .over("customer_id")
        ),
        amount_change=(
            pl.col("amount")
            .diff()
            .over("customer_id")
        ),
        growth_rate=(
            pl.col("amount")
            .pct_change()
            .over("customer_id")
        ),
        cumulative_amount=(
            pl.col("amount")
            .cum_sum()
            .over("customer_id")
        ),
    )
)
```

## Example: lazy analytics pipeline

```python
result = (
    pl.scan_parquet("transactions/*.parquet")

    .filter(
        pl.col("transaction_date")
        >= pl.date(2026, 1, 1)
    )

    .select(
        "customer_id",
        "transaction_date",
        "quantity",
        "unit_price",
        "status",
    )

    .filter(
        pl.col("status") == "complete"
    )

    .with_columns(
        revenue=(
            pl.col("quantity")
            * pl.col("unit_price")
        ),
        month=(
            pl.col("transaction_date")
            .dt.truncate("1mo")
        ),
    )

    .group_by(
        "customer_id",
        "month",
    )

    .agg(
        revenue=pl.col("revenue").sum(),
        transactions=pl.len(),
    )

    .sort(
        ["customer_id", "month"]
    )

    .collect()
)
```

## Example: list parsing

```python
result = (
    df
    .with_columns(
        tags=(
            pl.col("tags")
            .str.split(",")
            .list.eval(
                pl.element()
                .str.strip_chars()
                .str.to_lowercase()
            )
        )
    )
    .explode("tags")
)
```

## Example: wide numeric transformation

```python
result = df.with_columns(
    (
        cs.numeric()
        - cs.numeric().mean()
    )
)
```

For transformations requiring per-column standardization, build expressions per selected column or use expression expansion carefully so each column is standardized against its own statistics.

## Example: reusable expression factory

```python
def zscore(column: str) -> pl.Expr:
    x = pl.col(column)

    return (
        (x - x.mean())
        / x.std()
    ).alias(
        f"{column}_zscore"
    )

result = df.with_columns(
    zscore("height"),
    zscore("weight"),
)
```

## Example: SQL-like validation rules

```python
result = df.with_columns(
    is_valid=(
        pl.col("id").is_not_null()
        & pl.col("amount").is_not_null()
        & (pl.col("amount") >= 0)
        & pl.col("currency").is_in(
            ["USD", "CAD", "EUR"]
        )
    )
)
```

## Example: preserve rejected rows with reason

```python
validated = df.with_columns(
    rejection_reason=(
        pl.when(pl.col("id").is_null())
        .then(pl.lit("missing_id"))

        .when(pl.col("amount").is_null())
        .then(pl.lit("missing_amount"))

        .when(pl.col("amount") < 0)
        .then(pl.lit("negative_amount"))

        .when(
            ~pl.col("currency").is_in(
                ["USD", "CAD", "EUR"]
            )
        )
        .then(pl.lit("invalid_currency"))

        .otherwise(None)
    )
)

valid = validated.filter(
    pl.col("rejection_reason").is_null()
)

rejected = validated.filter(
    pl.col("rejection_reason").is_not_null()
)
```

## Example: environmental sensor observations

Imagine irregularly spaced temperature readings from several stations. The goal is to remove non-finite values, interpolate short gaps **within each station**, and compute a trailing mean of each station's readings.

```python
observations = pl.DataFrame({
    "station": ["A", "A", "A", "B", "B", "B"],
    "hour": [0, 1, 4, 0, 2, 3],
    "temperature": [10.0, None, 22.0, 5.0, 9.0, None],
})

result = (
    observations
    .sort(["station", "hour"])
    .with_columns(
        clean_temperature=(
            pl.when(pl.col("temperature").is_finite())
            .then(pl.col("temperature"))
            .otherwise(None)
        )
    )
    .with_columns(
        estimated_temperature=(
            pl.col("clean_temperature")
            .interpolate_by("hour")
            .over("station")
        )
    )
    .with_columns(
        recent_mean=(
            pl.col("estimated_temperature")
            .rolling_mean(window_size=2, min_samples=1)
            .over("station")
        )
    )
)
```

| station | hour | temperature | estimated_temperature | recent_mean |
|---|---:|---:|---:|---:|
| A | 0 | 10.0 | 10.0 | 10.0 |
| A | 1 | null | 13.0 | 11.5 |
| A | 4 | 22.0 | 22.0 | 17.5 |
| B | 0 | 5.0 | 5.0 | 5.0 |
| B | 2 | 9.0 | 9.0 | 7.0 |
| B | 3 | null | null | 9.0 |

The missing reading at station A's hour 1 is one quarter of the way between hours 0 and 4, so it is estimated as `13.0`. The last station B reading remains null because there is no later observation to interpolate toward. The trailing mean then uses the previous two observations where available, ignoring null readings.

## Example: experimental results by condition

```python
trials = pl.DataFrame({
    "condition": ["control", "treated", "control", "treated"],
    "response": [2.0, 4.0, 6.0, 8.0],
})

summary = trials.group_by("condition").agg(
    sample_size=pl.len(),
    mean_response=pl.col("response").mean(),
    sample_variance=pl.col("response").var(),
)

annotated = trials.with_columns(
    condition_mean=pl.col("response").mean().over("condition"),
    deviation=(
        pl.col("response")
        - pl.col("response").mean().over("condition")
    ),
)
```

`summary` has **two rows**—one per experimental condition—while `annotated` retains **all four observations**. This is a practical difference between aggregation and a window transform in experimental analysis.

---

# Final syntax map

The syntax patterns below cover a large percentage of practical Polars code:

```python
# select
df.select(
    "id",
    pl.col("amount"),
)

# add or replace
df.with_columns(
    amount=...,
    category=...,
)

# filter
df.filter(
    condition
)

# conditional
pl.when(condition)
.then(value)
.otherwise(value)

# aggregate
df.group_by(keys).agg(
    metric=expr.agg_method()
)

# window
expr.agg_method().over(keys)

# join
df.join(
    other,
    on=keys,
    how="left",
)

# reshape
df.pivot(...)
df.unpivot(...)
df.explode(...)
df.unnest(...)

# nested
pl.col("x").list...
pl.col("x").arr...
pl.col("x").struct...

# strings
pl.col("x").str...

# datetime
pl.col("x").dt...

# lazy
(
    pl.scan_parquet(...)
    .filter(...)
    .select(...)
    .with_columns(...)
    .group_by(...)
    .agg(...)
    .collect()
)
```

---

# Recommended Reference Hierarchy

When solving a Polars problem, check for a solution in this order:

1. direct expression/operator;
2. expression namespace (`str`, `dt`, `list`, `arr`, `struct`);
3. selector/expression expansion;
4. `group_by` / `over`;
5. join/reshape operation;
6. horizontal function;
7. lazy-plan transformation;
8. batch UDF;
9. element/row Python UDF only when native expressions cannot represent the operation.

This keeps transformations inside the Polars engine and preserves optimization opportunities.
