# MI77-Utils

A Python utility library of reusable tools and abstractions for development, computation, and data interoperability, by MI77-LAB.
## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Essentials](#essentials)
- [Computations](#computations)
- [Interops](#interops)

## Overview
| Module | Utilities |
| --- | --- |
| `essentials` | `introspect`, `performance_measure` |
| `computations` | `Calculator` |
| `interops.sql` | `df_to_sql` |
| `interops.excel` | `unlock_excel` |

## Installation

```bash
pip install git+https://github.com/mirabelleding/MI77-Inventorium.git
```

*The core library has no third-party dependencies. Certain utilities may require additional packages.*

## Essentials

`introspect()`<br>
Inspect the structure, attributes, methods, inheritance, and signatures of Python classes, instances, and bound methods.

```python
from mi77_utils.essentials import introspect

introspect(SomeClass, display=True)
introspect(some_instance, display=True)
```
---

`perf_profile()`<br>
Measure the execution time, CPU time, and memory usage of a Python code block.
```python
from mi77_utils.essentials import perf_profile

with perf_profile("some optional name"):
  run_some_code()
```

## Computations

## `Calculator`<br>
Evaluate named Python expressions against dictionaries, dataclasses, Pandas or Polars DataFrames, and Pandas Series indexed by variable names, with support for sequential formulas and custom namespaces.

### Defining Formulas

`Calculator` supports two equivalent constructor styles.

**Keyword Expressions**
```python
calc = Calculator(
    squared_norm="x**2 + y**2",
    norm="squared_norm**0.5",
)
```
**Formula Mapping**
```python
calc = Calculator(
    formulas={
        "squared_norm": "x**2 + y**2",
        "norm": "squared_norm**0.5",
    }
)
```
Each key defines an output variable, and its value is a Python expression represented as a string.Formulas can be supplied through keyword arguments or a mapping, but not both.

The optional `namespace` mapping exposes custom functions, modules, and constants to expressions.
```python
def some_magic():
    return "anything everything you can imagine."


Calculator(
    namespace={"some_magic": some_magic},
    creation="some_magic()",
)
```
By default, `calculate()` retains the input variables; use `output_only=True` to return only calculated outputs.


### Supported Input Structures

| Input structure | Result structure |
| --- | --- |
| `dict` of `Any` | `dict` with value types determined by the evaluated expressions|
| pandas/Polars `DataFrame` | pandas/Polars`DataFrame` |
| pandas `Series` indexed by variable names | `dict` |
| Dataclass instance | `dict` |

> *Dictionary values may be of any type, including NumPy arrays, pandas/Polars Series, or any Python object, provided the evaluated expressions support their operations.*

### Evaluation Behavior

- Expressions are evaluated using Python's `eval()` and can access built-ins such as `sum()`.
- Formulas execute in definition order, allowing later formulas to reference earlier results. Calculation dependencies are not automatically reordered or checked for cycles.
- Arithmetic and output dtypes follow the underlying input types and backend. The calculator does not cast or validate dtypes.
- Invalid expressions, undefined variables, and unsupported operations raise the underlying exceptions.
- Callers are responsible for handling nulls, array lengths, and alignment. Pandas Series generally align by index, while Polars Series operate positionally.

> **Security:** Only trusted expressions should be evaluated, as `eval()` can execute arbitrary Python code.


### Input Compatibility

```python
from dataclasses import dataclass

import numpy as np
import pandas as pd
import polars as pl

from mi77_utils.computations import Calculator


@dataclass
class XYZ:
    x: float
    y: float
    z: float


data = {
    "x": [7.7, 4.3],
    "y": [5.2, 6.5],
    "z": [9.7, 0.7],
}

scalar = {name: values[0] for name, values in data.items()}

constructors = {
    "np_array": np.array,
    "pd_series": pd.Series,
    "pl_series": pl.Series,
}

inputs = {
    **{
        name: {key: constructor(values) for key, values in data.items()}
        for name, constructor in constructors.items()
    },
    "number": scalar,
    "pd_df": pd.DataFrame(data),
    "pl_df": pl.DataFrame(data),
    "pd_series_dict": pd.Series(scalar),
    "dataclass": XYZ(**scalar),
}

calc = Calculator(
    namespace={"sqrt": np.sqrt},
    squared_norm="x**2 + y**2",
    norm="sqrt(squared_norm)",
    normalized="norm / z",
)

for name, values in inputs.items():
    display(name, calc.calculate(values))
```
## Interops

`df_to_sql()`<br>
Generate a SQL file for `INSERT` statements from a pandas or Polars DataFrame.
```python
from mi77_utils.sql_scripts import df_to_sql

df_to_sql(df=some_df,
          target_table="schemaname.tablename",
          file_name="output_file_name")
```
---

`unlock_excel()`<br>
Load a password-protected Excel file into an in-memory stream.

```python
import polars as pl

from mi77_utils.interops.excel import unlock_excel

pl.read_excel(unlock_excel("some_locked_file.xlsx"))
```
<hr>
<p align="center">
  <img
    src="https://raw.githubusercontent.com/mirabelleding/mirabelleding/main/signatures/mi77_endmark.png"
    alt="MI77-LAB"
    width="100%"
  >
</p>