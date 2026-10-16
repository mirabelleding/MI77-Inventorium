# Polars — Comprehensive Study Notes

A detailed reference for Python Polars covering the expression system, DataFrame and LazyFrame operations, data types, selectors, joins, aggregation, reshaping, strings, datetimes, nested data, missing values, time series, I/O, SQL, interoperability, testing, lazy execution, optimization, and pandas-to-Polars translation patterns.

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

```python
gross = pl.col("price") * pl.col("quantity")
net = gross - pl.col("discount")

df.with_columns(
    gross=gross,
    net=net,
)
```

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

Add or replace columns.

```python
df = df.with_columns(
    revenue=pl.col("price") * pl.col("quantity")
)
```

Multiple columns:

```python
df = df.with_columns(
    revenue=pl.col("price") * pl.col("quantity"),
    margin=pl.col("revenue") - pl.col("cost"),
    year=pl.col("date").dt.year(),
)
```

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

## `with_columns_seq()`

Sequential counterpart to `with_columns()` for cheap expressions.

```python
df.with_columns_seq(
    pl.col("a").cast(pl.Int64),
    pl.col("b").cast(pl.Int64),
)
```

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

---

# 10. Sorting and row selection

## `sort()`

```python
df.sort("amount")
```

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

---

# 13. Missing values and NaN

Polars distinguishes **null** from **NaN**.

- `null`: missing data.
- `NaN`: IEEE floating-point "not a number".

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

Useful for ordered numeric/time-series data.

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

## `sign()`

```python
pl.col("x").sign()
```

## `dot()`

Dot product:

```python
pl.col("a").dot(pl.col("b"))
```

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

## `var()`

```python
pl.col("amount").var()
```

## `quantile()`

```python
pl.col("amount").quantile(0.95)
```

## `product()`

```python
pl.col("factor").product()
```

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

## `approx_n_unique()`

Approximate cardinality:

```python
pl.col("customer_id").approx_n_unique()
```

Useful for very large datasets when exact cardinality is unnecessary.

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

## Covariance

```python
df.select(
    pl.cov("x", "y")
)
```

---

# 16. GroupBy

## Basic `group_by()`

```python
df.group_by("region").agg(
    pl.col("sales").sum()
)
```

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

## `arg_sort()`

Return row indices that would sort a column:

```python
pl.col("score").arg_sort()
```

## `arg_unique()`

Return indices of first unique values:

```python
pl.col("category").arg_unique()
```

---

# 19. Joins

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

Conceptually useful cases:

```text
1:1
1:m
m:1
m:m
```

Use validation when join-key uniqueness is an invariant.

## `join_asof()`

Match nearest ordered key rather than exact equality.

```python
trades.join_asof(
    quotes,
    on="timestamp",
    strategy="backward",
)
```

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

## `merge_sorted()`

Merge two already-sorted DataFrames using a sorted key.

Useful when data is known to be sorted and you want to preserve/merge sorted structure.

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

## `hstack()`

```python
df.hstack(
    [
        pl.Series("new_a", [1, 2, 3]),
        pl.Series("new_b", [4, 5, 6]),
    ]
)
```

## `extend()`

Append rows from another DataFrame in-place-like fashion where the API allows.

This can be useful for repeated extension scenarios but should be used intentionally; for many frames, a single `pl.concat(...)` is often clearer.

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

Literal behavior can be requested where appropriate.

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

This can produce a struct that can then be unnested.

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

## `round()`

Round to nearest temporal interval:

```python
pl.col("timestamp").dt.round("15m")
```

## `offset_by()`

Calendar-aware offsets:

```python
pl.col("date").dt.offset_by("1mo")
pl.col("date").dt.offset_by("-3mo")
pl.col("date").dt.offset_by("1y")
```

## Month boundaries

Methods such as month start/end helpers may be useful for period normalization where supported.

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

Useful concepts:

```text
difference
intersection
union
symmetric difference
```

## `list.eval()`

Apply an expression to each element in each list.

```python
pl.col("values").list.eval(
    pl.element() * 2
)
```

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

Use `Array` for fixed-size vector-like data where the fixed width is part of the schema.

Use `List` for variable-length sequences.

---

# 26. Struct expressions

A `Struct` is a nested record with named fields.

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

## Rename fields

Struct namespace provides field-renaming capabilities where appropriate.

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

## `pl.Categorical`

Useful for repeated string-like category values.

```python
df.with_columns(
    pl.col("category").cast(pl.Categorical)
)
```

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

## Categorical vs Enum

`Categorical`:

- categories can be discovered from data;
- useful for repeated categories where set is not necessarily fixed beforehand.

`Enum`:

- allowed values are explicitly defined;
- useful when category domain is known;
- invalid values can be treated as schema/data errors depending on conversion settings.

---

# 28. Horizontal operations

Horizontal functions operate across columns for each row.

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

## `pl.reduce()`

Reduce expressions without manually supplying an initial accumulator.

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

## Lag within entity

```python
df = (
    df
    .sort(["customer_id", "date"])
    .with_columns(
        previous_amount=(
            pl.col("amount")
            .shift(1)
            .over("customer_id")
        )
    )
)
```

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

- creates regular time windows/buckets.

`rolling`:

- creates windows relative to observations/index positions.

Use the one matching the temporal semantics of the problem.

---

# 31. LazyFrame

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

## `collect()`

Materialize:

```python
result = lf.collect()
```

## `collect_schema()`

Resolve output schema:

```python
schema = lf.collect_schema()
```

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

## Join optimization

The optimizer can reason about join ordering/strategies under supported scenarios.

## `explain()`

Inspect query plan:

```python
print(lf.explain())
```

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

## `pl.read_database_uri()`

Read through a connection URI where supported:

```python
df = pl.read_database_uri(
    query="SELECT id, amount FROM transactions",
    uri=uri,
)
```

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

## `map_batches()`

Apply a custom function to batches rather than individual elements.

This can be useful for integrating vectorized external libraries, but it introduces an optimization boundary. Use native expressions first when possible.

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
dt.date()
dt.time()
dt.strftime()
dt.truncate()
dt.round()
dt.offset_by()
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
```

## Struct namespace

```text
struct.field()
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
