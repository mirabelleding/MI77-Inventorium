# Atelier
A collection of abstractions, experiments, and evolving designs.

## MI77-Utils
*Reusable Python utilities by MI77-LAB.*
### Installation
Install directly from GitHub:
```bash
pip install git+https://github.com/mirabelleding/atelier.git
```
For local development, clone the repository and install in editable mode:
```bash
git clone https://github.com/mirabelleding/atelier.git
cd atelier
pip install -e .
```

## Usage
`inspect_object()`<br>
Inspect the structure, attributes, methods, and inheritance of Python classes and instances.
```python
from mi77_utils.inspection import inspect_object

inspect_object(SomeClass, display=True)
inspect_object(some_instance, display=True)
```
`df_to_sql()`<br>
Generate a SQL file containing batched INSERT statements from a pandas or Polars DataFrame.
```python
from mi77_utils.sql_scripts import df_to_sql

df_to_sql(df=some_df,
          target_table="schemaname.tablename",
          file_name="output_file_name")
```
<hr>

<p align="center">
  <sub><i><span style="color: #999999;">Where ideas become abstractions, and abstractions become code.</span></i></sub>
</p>