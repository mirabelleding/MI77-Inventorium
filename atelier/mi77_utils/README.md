# MI77-Utils

A Python utility library of reusable tools and abstractions for development, computations, and interoperability, by MI77-LAB.

## Installation

```bash
pip install git+https://github.com/mirabelleding/MI77-Inventorium.git
```

*The core library has no third-party dependencies. Certain utilities may require additional packages.*

## Modules

- [Essentials](#essentials)
- [Computations](#computations)
- [Interops](#interops)

## Essentials

`introspect()`<br>
Inspect the structure, attributes, methods, inheritance, and signatures of Python classes, instances, and bound methods.

```python
from mi77_utils.essentials import introspect

introspect(SomeClass, display=True)
introspect(some_instance, display=True)
```
---

`performance_measure()`<br>
Measure the execution time, CPU time, and memory usage of a Python code block.
```python
from mi77_utils.essentials import performance_measure

with performance_measure("some optional name"):
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
Each key defines an output variable, and its value is a Python expression represented as a string.
Formulas can be supplied through keyword arguments or a mapping, but not both.

The optional `namespace` mapping exposes custom functions, modules, and constants to expressions.
```python
def some_magic():
    return "anything everything you can imagine."


Calculator(
    namespace={"some_magic": some_magic},
    creation="some_magic()",
)
```
By default, `calculate()` retains the input variables; use `output_only=True` to return only output variables.


### Supported Input Structures

| Input type | Output type |
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

#### SQL Scripts
`df_to_sql()`<br>
Generate a SQL file for `INSERT` statements from a pandas or Polars DataFrame.
```python
from mi77_utils.interops import df_to_sql

df_to_sql(df=some_df,
          target_table="schemaname.tablename",
          file_name="output_file_name")
```
---
#### MSOffice I/O

`decrypt_msoffice()` & `encrypt_msoffice()`<br>
Decrypt/Encrypt supported file types into an in-memory `BytesIO` stream; password can be passed as argument or entered through automatic prompt, with optional persistence to a specified location via `save_to`.

```python
import polars as pl

from mi77_utils.interops import decrypt_msoffice, encrypt_msoffice

pl.read_excel(decrypt_msoffice("some_locked_file.xlsx"))

encrypt_msoffice(
    "some_file.xlsx",
    password="...",
    save_to="encrypted_file.xlsx"
    )
```
**Supported file formats**

Encryption and decryption are implemented using [`msoffcrypto-tool`](https://github.com/nolze/msoffcrypto-tool); supported file formats and encryption methods subject to the underlying library.

| Format | Decryption | Encryption |
|---|---|---|
| Excel | `.xlsx`, `.xls`* | `.xlsx` |
| Word | `.docx`, `.doc` | `.docx` |
| PowerPoint | `.pptx`, `.ppt`* | `.pptx` |

*Legacy `.xls` decryption is experimental; `.ppt` support is partial and experimental. Encryption support is limited to OOXML formats and is experimental.*


<hr>
<p align="center">
  <img
    src="https://raw.githubusercontent.com/mirabelleding/mirabelleding/main/signatures/mi77_endmark.png"
    alt="MI77-LAB"
    width="100%"
  >
</p>