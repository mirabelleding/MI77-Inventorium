# Atelier
A collection of abstractions, experiments, and evolving designs.

## MI77-Utils
*Some reusable Python utilities by MI77-LAB.*

### Installation
From GitHub:
```bash
pip install git+https://github.com/mirabelleding/atelier.git
```
Local installation in editable mode:
```bash
git clone https://github.com/mirabelleding/atelier.git
cd atelier
pip install -e .
```

### Usage
`inspect_object()`<br>
Inspect the structure, attributes, methods, and inheritance of Python classes and instances.
```python
from mi77_utils.essentials import inspect_object

inspect_object(SomeClass, display=True)
inspect_object(some_instance, display=True)
```

`perf_profile()`<br>
Measure the execution time, CPU time, and memory usage of a Python code block.
```python
from mi77_utils.essentials import perf_profile

with perf_profile():
  run_some_code()
```

`df_to_sql()`<br>
Generate a SQL file for INSERT statements from a pandas or Polars DataFrame.
```python
from mi77_utils.sql_scripts import df_to_sql

df_to_sql(df=some_df,
          target_table="schemaname.tablename",
          file_name="output_file_name")
```

## Quelques Idées

A collection of software creations and architectural designs.

<hr>

<p align="center">
  <sub><i><span style="color: #999999;">Where ideas become abstractions, and abstractions become code.</span></i></sub>
</p>