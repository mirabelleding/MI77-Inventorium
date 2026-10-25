# PEP 8: Comprehensive Python Style Guide

**A practical, example-driven reference for writing readable, consistent, maintainable Python.**

> **Scope.** This study guide explains the conventions in [PEP 8](https://peps.python.org/pep-0008/), supplements its docstring advice with [PEP 257](https://peps.python.org/pep-0257/), and adds clearly identified practical recommendations for modern Python projects. It is a learning reference, **not a verbatim reproduction** of either PEP. Examples assume modern Python 3 unless stated otherwise.
>
> **Verified:** October 22, 2026. The official PEP 8 page reviewed for this guide identifies its latest source modification as April 4, 2025.

## Contents

1. [Philosophy and decision hierarchy](#1-philosophy-and-decision-hierarchy)
2. [At-a-glance rules](#2-at-a-glance-rules)
3. [Indentation and multiline formatting](#3-indentation-and-multiline-formatting)
4. [Line length, blank lines, and files](#4-line-length-blank-lines-and-files)
5. [Imports and module organization](#5-imports-and-module-organization)
6. [Whitespace, operators, and punctuation](#6-whitespace-operators-and-punctuation)
7. [Strings, collections, and trailing commas](#7-strings-collections-and-trailing-commas)
8. [Comments and documentation](#8-comments-and-documentation)
9. [Naming conventions](#9-naming-conventions)
10. [Public APIs, class design, and inheritance](#10-public-apis-class-design-and-inheritance)
11. [Programming recommendations](#11-programming-recommendations)
12. [Type annotation style](#12-type-annotation-style)
13. [Applied examples: data processing and SQLAlchemy](#13-applied-examples-data-processing-and-sqlalchemy)
14. [PEP 8 versus modern formatting tools](#14-pep-8-versus-modern-formatting-tools)
15. [Practical Ruff configuration and commands](#15-practical-ruff-configuration-and-commands)
16. [Before-and-after refactoring examples](#16-before-and-after-refactoring-examples)
17. [Common misconceptions and edge cases](#17-common-misconceptions-and-edge-cases)
18. [Review checklist and references](#18-review-checklist-and-references)

---

## 1. Philosophy and decision hierarchy

PEP 8 is a **style guide**, not a mandatory part of Python's grammar. The interpreter rejects invalid syntax; it does not generally reject code for using a poor variable name, inconsistent quote style, or a long line.

### 1.1 Why style matters

Consistency helps a reader distinguish **what the program does** from **how the author happened to format it**. Good formatting makes nesting, related expressions, interfaces, and errors easier to spot. In large packages, consistency also reduces code-review noise.

### 1.2 Prioritize readability over mechanical compliance

When conventions conflict, use this practical decision sequence:

1. Preserve **correctness, compatibility, and behavior**.
2. Respect an established project's documented style.
3. Preserve local consistency unless making an intentional refactor.
4. Apply PEP 8's defaults where no stronger project convention exists.
5. Choose the clearer expression when following a rule literally makes the code harder to understand.

Appropriate exceptions may include generated code, public names required by a dependency, an older Python version, a file undergoing a focused bug fix, or a line that cannot be wrapped meaningfully.

### 1.3 Distinguish three different kinds of rules

| Category | Example | Meaning |
|---|---|---|
| Language requirement | Indented blocks must be syntactically valid | Python must be able to parse the code. |
| PEP 8 recommendation | Use 4 spaces per indentation level | A widely accepted convention, subject to justified exceptions. |
| Project/tool convention | Use an 88-character line length | A team or formatter setting; not PEP 8's baseline. |

**Key principle:** Be intentionally consistent rather than blindly uniform.

---

## 2. At-a-glance rules

| Topic | PEP 8 guidance | Example |
|---|---|---|
| Indentation | 4 spaces per level | `if ready:` followed by a 4-space-indented suite |
| Tabs | Prefer spaces; avoid mixing indentation methods | Four spaces, not one tab |
| Code line length | Normally at most 79 characters | Wrap expressions in parentheses |
| Comments/docstrings | Normally at most 72 characters | Wrap explanatory prose |
| Team-specific line length | Up to 99 characters may be agreed for code | A project's explicit convention |
| Top-level definitions | Separate functions/classes with 2 blank lines | Between `def a` and `class B` |
| Methods | Separate with 1 blank line | Between two methods in a class |
| Imports | Top of module; standard, third-party, local groups | Blank line between groups |
| Imports | Usually one `import module` per line | `import os` then `import sys` |
| Functions/variables | `snake_case` | `calculate_total` |
| Classes/exceptions | `CapWords` | `DatabaseClient`, `QueryError` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Modules/packages | Short lowercase names | `queries.py`, `analytics/` |
| Internal interfaces | One leading `_` | `_load_inputs` |
| Instance/class methods | `self` / `cls` | `def build(self)`, `def create(cls)` |
| Keyword arguments | No spaces around `=` | `connect(timeout=10)` |
| Annotated defaults | Spaces around `=` | `def f(x: int = 1)` |
| Annotations | Space after `:` and around `->` | `def f(x: int) -> str:` |
| `None` | Use identity | `value is None` |
| Boolean expressions | Prefer truthiness where intended | `if items:` |
| Error handling | Catch targeted exceptions | `except ValueError:` |
| Single-element tuples | Include trailing comma | `(42,)` |
| Docstrings | Triple double quotes | `"""Return the value."""` |
| Quotes for ordinary strings | Neither `'` nor `"` is universally preferred | Be consistent locally |

---

## 3. Indentation and multiline formatting

### 3.1 Use four spaces for each nested block

**Avoid** inconsistent or two-space indentation:

```python
if is_valid:
  process_data()
  save_results()
```

**Prefer**:

```python
if is_valid:
    process_data()
    save_results()
```

This applies to functions, methods, conditionals, loops, exception handlers, and context managers.

```python
def calculate_total(values: list[float]) -> float:
    total = 0.0

    for value in values:
        if value > 0:
            total += value

    return total
```

PEP 8 prefers **spaces**. Tabs are appropriate primarily when preserving consistency in legacy tab-indented files. Python disallows inconsistent mixing that makes indentation ambiguous.

### 3.2 Wrap inside parentheses, brackets, and braces

Python implicitly joins continued lines inside `()`, `[]`, and `{}`. This is usually more robust than a line-continuation backslash.

**Avoid:**

```python
result = calculate_discount(price, quantity, customer_type, promotion, region, tax_rate)
```

**Prefer:**

```python
result = calculate_discount(
    price,
    quantity,
    customer_type,
    promotion,
    region,
    tax_rate,
)
```

Both of these alignment styles are acceptable:

```python
result = combine(first_value, second_value,
                 third_value, fourth_value)
```

```python
result = combine(
    first_value,
    second_value,
    third_value,
    fourth_value,
)
```

The second format often minimizes editing effort when arguments are added later. A **hanging indent** should be visually distinct from the function body, and the first argument should not remain on the opening line when using a hanging indent.

### 3.3 Multiline function definitions

```python
def calculate_expected_loss(
    portfolio_id: int,
    process_month: str,
    scenario_weights: dict[str, float],
    include_history: bool = False,
) -> float:
    return compute_loss(
        portfolio_id,
        process_month,
        scenario_weights,
        include_history,
    )
```

The argument indentation identifies the parameter list without confusing it with executable statements in the body.

### 3.4 Multiline conditionals

**One valid style:**

```python
if (
    portfolio_id is not None
    and process_month is not None
    and include_history
):
    process_portfolio()
```

This makes the condition and its body visually separate. PEP 8 permits several conditional-continuation indentation styles; consistency is more important than selecting one particular layout.

### 3.5 Break before binary operators when it improves clarity

In new code, PEP 8 suggests placing operators at the beginning of continuation lines:

```python
total_income = (
    salary
    + bonus
    + dividend_income
    - tax_deductions
)
```

Breaking **after** binary operators is also permissible when used consistently nearby:

```python
total_income = (
    salary +
    bonus +
    dividend_income -
    tax_deductions
)
```

Choose one consistent approach locally; the first is generally clearer for long expressions.

### 3.6 Closing delimiters

Both closing-delimiter placements are permitted by PEP 8:

```python
items = [
    "alpha",
    "beta",
]
```

```python
items = [
    "alpha",
    "beta",
    ]
```

The first is common in today's formatters; PEP 8 permits either.

### 3.7 Avoid unnecessary backslashes

**Less robust:**

```python
total = subtotal + tax + shipping + \
    handling_fee
```

**Prefer:**

```python
total = (
    subtotal
    + tax
    + shipping
    + handling_fee
)
```

Modern Python also permits parenthesized multiple context managers:

```python
with (
    open(source_path, encoding="utf-8") as source,
    open(target_path, "w", encoding="utf-8") as target,
):
    target.write(source.read())
```

The parenthesized `with` syntax above requires Python 3.10 or newer; older supported codebases may need a different style.

---

## 4. Line length, blank lines, and files

### 4.1 Line lengths and exceptions

Official PEP 8 defaults:

- **79 characters** for Python code.
- **72 characters** for flowing comments and docstrings.
- A team maintaining its own code may agree on **up to 99 characters for code**, while retaining the 72-character prose convention.

Do not conflate these values with a formatter's default. Black and Ruff format at **88 characters by default**, which is a tool choice rather than the original PEP 8 line limit.

**Avoid:**

```python
filtered = [record for record in records if record["active"] and record["balance"] > minimum_balance]
```

**Prefer:**

```python
filtered = [
    record
    for record in records
    if record["active"] and record["balance"] > minimum_balance
]
```

### 4.2 Blank lines between definitions

At module level, use **two blank lines** between top-level function and class definitions:

```python
def normalize_data(data):
    return data.copy()


class DataProcessor:
    def process(self, data):
        return normalize_data(data)


def load_data():
    return []
```

Within a class, use **one blank line** between methods:

```python
class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process(self):
        return self.data.copy()

    def count(self):
        return len(self.data)
```

Inside a function, add blank lines **sparingly** to mark conceptual phases such as input validation, transformation, and output creation.

```python
def prepare_values(values: list[int]) -> list[int]:
    positives = [value for value in values if value > 0]

    unique_values = set(positives)

    return sorted(unique_values)
```

The examples show visible blank-line rules. Markdown rendering does not always preserve spacing well outside fenced code blocks.

### 4.3 File encoding and text conventions

Use **UTF-8** for Python source files. Ordinary Python 3 source does not need a `# -*- coding: utf-8 -*-` declaration. Public libraries with global audiences often use ASCII-compatible identifiers, although Unicode identifiers are legal in Python.

Prefer names such as `customer_name` rather than ambiguous symbols or visually confusable letters.

Avoid trailing spaces at the ends of lines, and terminate text files with a newline as a sensible cross-tool practice. The final-newline convention is a common tooling practice, not a separately enumerated rule in PEP 8.

---

## 5. Imports and module organization

### 5.1 Import each module separately

**Avoid:**

```python
import os, sys, json
```

**Prefer:**

```python
import json
import os
import sys
```

Importing multiple names *from the same module* on one line is valid:

```python
from pathlib import Path, PurePath
```

### 5.2 Group imports into three categories

1. Standard-library imports.
2. Third-party dependency imports.
3. Imports from your application or package.

Separate the groups with a blank line.

```python
from pathlib import Path
from typing import Sequence

import pandas as pd
from sqlalchemy import Select, select

from my_project.core.transaction import Transaction
from my_project.queries.ecl import build_ecl_query
```

Alphabetizing imports is a widely used *tool convention*, not an explicit comprehensive sorting algorithm prescribed by PEP 8. Tools such as Ruff's import-sorting rules can enforce a predictable order.

### 5.3 Use absolute imports as a default

```python
from my_project.core.transaction import Transaction
```

Explicit relative imports are acceptable inside packages:

```python
from .transaction import Transaction
from ..config.settings import Settings
```

Absolute imports can make package boundaries more obvious; relative imports can reduce redundant prefixes in a complex package. Avoid implicit relative imports.

### 5.4 Avoid wildcard imports

**Avoid:**

```python
from sqlalchemy import *
```

**Prefer:**

```python
from sqlalchemy import MetaData, Table, select
```

Wildcard imports obscure where names come from and reduce static-analysis accuracy. Re-exporting a deliberate public API is a specialized exception.

### 5.5 Organize module metadata and future imports correctly

The file order requires extra care when using `__all__` or `from __future__`:

```python
"""Utilities for building database queries."""

from __future__ import annotations

__all__ = ["build_select", "build_filter"]

from collections.abc import Sequence

from sqlalchemy import Select, select


def build_select(columns: Sequence) -> Select:
    return select(*columns)
```

`from __future__` imports must appear before other executable module code, except for permitted module docstrings and other future imports. PEP 8 places module-level dunder metadata before ordinary imports but after future imports. This is an exception to the usual advice that imports come before module globals.

### 5.6 Imports inside functions

PEP 8's default is top-of-module imports. A local import may be justified for an optional dependency, a circular-import workaround, or an expensive dependency used only on a rare path. That exception should be intentional rather than habitual.

---

## 6. Whitespace, operators, and punctuation

### 6.1 Do not insert padding inside delimiters

**Avoid:**

```python
values = [ 1, 2, 3 ]
result = calculate( value )
setting = { "retry": 3 }
```

**Prefer:**

```python
values = [1, 2, 3]
result = calculate(value)
setting = {"retry": 3}
```

Do not put a space before `(` in a call, or before `[` in an index operation:

```python
process_data(data)
value = records[index]
```

### 6.2 Put normal spaces around assignment and comparisons

**Avoid:**

```python
total=price*quantity
if total>=minimum and status=="active":
    total+=1
```

**Prefer:**

```python
total = price * quantity
if total >= minimum and status == "active":
    total += 1
```

Normally add one space around assignment, augmented assignment, comparison, and Boolean operators. For arithmetic with mixed precedence, selective omission of spaces around high-precedence operations is permitted if it improves readability:

```python
result = x*2 - 1
```

For most projects, consistent conventional spacing is easier to maintain:

```python
result = x * 2 - 1
```

Both are compatible with the spirit of PEP 8; do not mistake the second for a mandatory universal rule.

### 6.3 Distinguish assignments from keyword arguments

```python
threshold = 0.5
process_data(limit=100, strict=True)
```

The `=` in `limit=100` and `strict=True` **does not** get surrounding spaces.

For function defaults, the correct spacing **depends on whether the parameter is annotated**:

```python
def fetch_data(limit=100, timeout=5):
    return limit, timeout
```

```python
def fetch_data(limit: int = 100, timeout: int = 5):
    return limit, timeout
```

**Avoid:**

```python
def fetch_data(limit : int=100, timeout = 5):
    return limit, timeout
```

### 6.4 Colons in slices differ from dictionary colons

Simple slices do not have spaces around the colon:

```python
items[1:5]
items[:5]
items[2:]
items[::2]
```

For more complex slice expressions, PEP 8 treats the slice colon somewhat like a low-precedence operator. Keep spacing symmetrical when operands require spaces:

```python
items[start + offset : end + offset]
items[: upper_bound(items) : step]
```

A dictionary's colon uses a space **after** it:

```python
configuration = {"limit": 10, "enabled": True}
```

**Avoid** arbitrary mixed spacing such as `items[1: 5]` or `items[1 :5]`.

### 6.5 Type annotations have their own spacing pattern

```python
count: int = 0
names: list[str] = []


def normalize(name: str) -> str:
    return name.strip().lower()
```

No space before an annotation colon, one after it, and a space on each side of `->`.

### 6.6 One statement per line

**Avoid:**

```python
x = 1; y = 2; z = 3
if is_ready: process_data()
```

**Prefer:**

```python
x = 1
y = 2
z = 3

if is_ready:
    process_data()
```

Single-line suites are sometimes legal but reduce consistency and are particularly difficult to read with multiple branches, `try` blocks, or nested statements.

### 6.7 Trailing whitespace

Delete spaces following the final visible character on a line. These are difficult to notice and can break backslash continuations or generate unnecessary diffs.

---

## 7. Strings, collections, and trailing commas

### 7.1 Single versus double quotes

PEP 8 **does not dictate** a universal quote choice for ordinary Python strings. Both are valid:

```python
message = 'Ready'
message = "Ready"
```

Choose one convention for your project. Prefer the delimiter that avoids escaping apostrophes or quote marks:

```python
message = "It's ready"
text = 'The parameter is named "timeout".'
```

Use **triple double quotes** for docstrings and normally for triple-quoted strings:

```python
query = """
SELECT portfolio_id, balance
FROM portfolios
WHERE is_active = TRUE
"""
```

### 7.2 Trailing commas for multiline constructs

```python
measure_types = [
    "RM",
    "SER",
    "FLA",
    "ECL",
]
```

```python
configuration = {
    "currency": "CAD",
    "process_month": "2026-10",
    "retries": 3,
}
```

Trailing commas are usually optional, but in multiline lists, dictionaries, calls, and import lists they make future edits cleaner.

### 7.3 Singleton tuples require a comma

```python
one_item = (42,)
not_a_tuple = (42)
```

`one_item` is a tuple; `not_a_tuple` is an integer. The comma, not the parentheses, makes the tuple. PEP 8 recommends parentheses for clarity.

### 7.4 Avoid awkward closing-line commas

**Avoid:**

```python
items = ["a", "b",]
```

**Prefer:**

```python
items = ["a", "b"]
```

Or use the expandable multiline form:

```python
items = [
    "a",
    "b",
]
```

---
## 8. Comments and documentation

### 8.1 The purpose of comments

Good comments explain **why** a decision was made or clarify a non-obvious requirement. They should not repeat an operation that the code already expresses clearly. Keep them accurate as the program evolves.

**Unhelpful:**

```python
count += 1  # Increase count by one.
```

**Potentially helpful:**

```python
count += 1  # Include the final partial billing period.
```

Avoid comments that become false when a function changes. Prefer clear naming and smaller functions when those choices eliminate the need for an explanation.

### 8.2 Block comments

When block comments are useful, align them with the code they explain, and begin each line with `# `:

```python
def calculate_adjustment(amount: float) -> float:
    # Legacy contracts apply the original rate throughout renewal.
    # Repricing occurs only when a new contract is issued.
    return amount * 0.95
```

Write complete, readable sentences where practical. Separate paragraphs of a block comment with a line containing just `#`.

### 8.3 Inline comments

An inline comment should generally have **at least two spaces** between the code and `#`, followed by one space after `#`:

```python
value = value + 1  # Account for the inclusive upper bound.
```

Use inline comments sparingly. Excessive comments can be a symptom of unclear structure.

### 8.4 Docstrings are different from comments

A docstring is a string literal that begins a module, class, function, or method body and is available via `__doc__`. A `#` comment is not part of that object's `__doc__`.

```python
def calculate_average(values: list[float]) -> float:
    """Return the arithmetic mean of the supplied values."""
    return sum(values) / len(values)
```

```python
print(calculate_average.__doc__)
```

PEP 8 recommends docstrings for public modules, functions, classes, and methods; PEP 257 gives the fuller docstring conventions. Non-public helpers do not necessarily need a full docstring, but their behavior should still be understandable. **These are documentation conventions, not requirements that every internal function must contain extra prose.**

### 8.5 One-line docstrings

Use triple double quotes, a concise command-style summary, and a closing period:

```python
def load_portfolios() -> list[str]:
    """Return the identifiers of active portfolios."""
    return ["A", "B"]
```

### 8.6 Multiline docstrings

Put a summary first, then a blank line, then details. The final triple quote belongs on its own line:

```python
def calculate_ecl(
    exposure: float,
    probability: float,
    loss_given_default: float,
) -> float:
    """Calculate expected credit loss for one exposure.

    Multiply exposure by the probability of default and loss
    given default. All inputs must be non-negative.

    Raise ValueError when any input is negative.
    """
    if min(exposure, probability, loss_given_default) < 0:
        raise ValueError("Inputs must be non-negative")

    return exposure * probability * loss_given_default
```

The example's behavior and validation agree with its documentation. Avoid a docstring that merely duplicates the function name, argument list, or type annotations.

### 8.7 Docstring details from PEP 257

- Use `"""triple double quotes"""`.
- For a one-line docstring, keep opening and closing quotes on the same line.
- For a multiline docstring, leave a blank line after the summary.
- Document meaningful parameters, outputs, exceptions, side effects, and constraints when applicable.
- Separate a class docstring from its first method with a blank line.
- Consider how other developers will discover public behavior through `help()` or IDE inspection.

A team can choose NumPy-style or Google-style structured docstrings, but those markup formats are **not prescribed by PEP 8 or PEP 257**.

---

## 9. Naming conventions

Names communicate both an object's role and its intended visibility. Naming style is not interchangeable with object semantics: a class and a function should not be named identically just because both can be called.

### 9.1 Naming reference

| Construct | Convention | Good example | Poor example |
|---|---|---|---|
| Module file | Short lowercase; `_` if useful | `query_builder.py` | `QueryBuilder.py` |
| Package directory | Short lowercase; avoid `_` if practical | `queries/` | `QueryModules/` |
| Function | `snake_case` | `calculate_loss()` | `CalculateLoss()` |
| Method | `snake_case` | `load_inputs()` | `loadInputs()` |
| Variable | `snake_case` | `portfolio_ids` | `portfolioIds` |
| Class | `CapWords` | `PortfolioLoader` | `portfolio_loader` |
| Error exception | `CapWords` + `Error` | `MissingDataError` | `missing_data` |
| Constant | `UPPER_SNAKE_CASE` | `DEFAULT_TIMEOUT` | `DefaultTimeout` |
| Internal function | Leading `_` | `_fetch_records()` | `__fetch_records__()` |
| Instance method parameter | `self` | `def load(self)` | `def load(this)` |
| Class method parameter | `cls` | `def create(cls)` | `def create(klass)` |
| Reserved keyword conflict | Trailing `_` | `class_` | `clss` |
| Type variable (traditional) | Short CapWords | `T`, `KeyT` | `my_type_variable` |
| Standard special method | Existing `__name__` form | `__init__` | Invented `__load_data__` |

PEP 8 permits existing historical naming conventions when keeping a stable API matters. An isolated naming change can break imports, callers, reflection code, and serialization.

### 9.2 Package and module names

Recommended package structure:

```text
my_project/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── transaction.py
│   └── pipeline.py
├── queries/
│   ├── __init__.py
│   ├── common.py
│   └── ecl.py
└── calculations/
    ├── __init__.py
    └── expected_loss.py
```

`queries`, `core`, and `calculations` use simple lowercase package names. `expected_loss.py` is a readable lowercase module with underscores.

**Note:** PEP 8 does not specify how to split an application's architecture into files or directories. The tree above is an illustrative design, not a required layout.

### 9.3 Function names describe actions

```python
def fetch_transactions():
    ...


def compile_results():
    ...


def calculate_expected_loss():
    ...
```

Choose a descriptive verb when the function performs an operation. A returned property or query object may justify a noun-like name when that reads better in the public API; semantics matter more than a rigid grammatical rule.

### 9.4 Variable names convey content and units

```python
portfolio_ids = [101, 102, 103]
process_month = "2026-10"
exposure_amount = 500_000.0
```

Avoid one-letter identifiers except for conventional, clearly local uses such as short loop indices or mathematical formulas. Specifically avoid lowercase `l`, uppercase `O`, and uppercase `I` as single-character variables; they can look like `1` or `0`.

```python
for index, portfolio_id in enumerate(portfolio_ids):
    print(index, portfolio_id)
```

### 9.5 Class names: CapWords

```python
class Transaction:
    pass


class RecalculationEngine:
    pass


class SQLQueryBuilder:
    pass
```

PEP 8 generally prefers retaining all-capital acronyms in a CapWords identifier: for example, `HTTPServerError` rather than `HttpServerError`. Stable library names may follow other conventions.

### 9.6 Exception names

Use an `Error` suffix for exceptions representing errors:

```python
class TransactionNotFoundError(Exception):
    pass


class InvalidConfigurationError(ValueError):
    pass
```

Exceptions used only as flow-control signals need not have that suffix. Inherit ordinary custom exceptions from `Exception` or an appropriate subclass, rather than directly from `BaseException`.

### 9.7 Constants

```python
MAX_RETRIES = 3
DEFAULT_CURRENCY = "CAD"
SUPPORTED_MEASURE_TYPES = ("RM", "SER", "FLA", "ECL")
```

Uppercase signals that the value is *intended* to be treated as constant. Python generally does not enforce immutability of the referenced object.

### 9.8 `self` and `cls`

```python
class Transaction:
    def __init__(self, transaction_id: str):
        self.transaction_id = transaction_id

    def identifier(self) -> str:
        return self.transaction_id

    @classmethod
    def from_string(cls, transaction_id: str) -> "Transaction":
        return cls(transaction_id)
```

`self` and `cls` are conventional parameter names, not language keywords. The `@staticmethod` decorator does not require either argument.

### 9.9 Leading and trailing underscores

| Form | Meaning | Example |
|---|---|---|
| `name` | Ordinary public name by default | `client.connect()` |
| `_name` | Internal/non-public convention | `client._session` |
| `name_` | Avoid keyword collision | `class_` |
| `__name` inside a class | Triggers name mangling | `self.__cache` |
| `__name__` | Reserved family for special names | `__init__`, `__repr__` |

**Single leading underscore** is a convention; it does not prevent access:

```python
class Client:
    def __init__(self):
        self._session = object()
```

**Double leading underscore** activates class-based name mangling:

```python
class Base:
    def __init__(self):
        self.__cache = {}


base = Base()
print(base._Base__cache)
```

The access is deliberately shown to emphasize that name mangling is **not true data privacy**. Use it mainly to reduce accidental clashes in extensible inheritance hierarchies; do not automatically make every internal attribute double-underscored.

Never invent names such as `__calculate__` to make methods appear special. Implement an actual documented special method only when its semantics apply.

### 9.10 Type variables and newer syntax

Traditional generic declarations often use short, recognizable names:

```python
from typing import TypeVar

T = TypeVar("T")
KeyT = TypeVar("KeyT")
```

Python 3.12 introduced type-parameter syntax such as `class Box[T]:`, where `T` is still a conventional type parameter. The **syntax** comes from Python's typing evolution, whereas PEP 8 primarily addresses naming style.

---

## 10. Public APIs, class design, and inheritance

### 10.1 Treat public names as compatibility commitments

A public function or attribute is something you expect library users to rely on. Renaming it is a change to the public API, even when only its spelling changes.

```python
class QueryBuilder:
    def __init__(self, table):
        self.table = table

    def build(self):
        return self.table.select()

    def _validate_table(self):
        return self.table is not None
```

`build()` is publicly named; `_validate_table()` is marked non-public. A library may document stricter access contracts independently of naming.

### 10.2 Declare intentionally exported names

```python
__all__ = ["QueryBuilder", "build_query"]
```

`__all__` explicitly lists the names a module exports when wildcard-imported, and it helps signal the intended public surface. An empty `__all__` declares no wildcard-exported names.

**Important nuance:** `__all__` is **not an access-control feature**. Users can still import other accessible names directly, and documented APIs can exist without `__all__`.

### 10.3 Prefer simple public attributes when appropriate

Rather than writing getters and setters automatically:

```python
class Portfolio:
    def __init__(self, portfolio_id: int):
        self.portfolio_id = portfolio_id
```

If validation later becomes necessary, a property can preserve the same caller syntax:

```python
class Portfolio:
    def __init__(self, portfolio_id: int):
        self.portfolio_id = portfolio_id

    @property
    def portfolio_id(self) -> int:
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Portfolio ID must be positive")
        self._portfolio_id = value
```

Avoid surprising, expensive computation or major side effects from a property that *looks* like cheap attribute access.

### 10.4 Design for inheritance deliberately

Before exposing a member, decide whether it is:

- **Public:** part of the supported client-facing API.
- **Subclass-facing:** intended for subclasses to override or reuse.
- **Internal:** an implementation detail with no stability guarantee.

Use a single leading underscore for ordinary internals. Double leading underscores can help protect base-class implementation names against accidental collisions with subclass attributes, but complicate introspection and debugging.

```python
class BaseProcessor:
    def process(self, data):
        normalized = self._normalize(data)
        return self._calculate(normalized)

    def _normalize(self, data):
        return data

    def _calculate(self, data):
        raise NotImplementedError


class SumProcessor(BaseProcessor):
    def _calculate(self, data):
        return sum(data)
```

Here, `_calculate()` is clearly intended as an extension hook even though it is non-public to unrelated consumers. Actual subclass contracts should be documented for a public framework.

---

## 11. Programming recommendations

This section goes beyond typography. PEP 8 also addresses idiomatic programming patterns that make code more reliable or expressive.

### 11.1 Compare `None` by identity

**Avoid:**

```python
if result == None:
    handle_missing()
```

**Prefer:**

```python
if result is None:
    handle_missing()
```

Use `is not None` for the opposite condition:

```python
if result is not None:
    process(result)
```

Do not accidentally replace an explicit `None` test with a truthiness test when `0`, `False`, `""`, or `[]` are valid non-`None` values.

```python
limit = 0

if limit is not None:
    apply_limit(limit)
```

### 11.2 Prefer ordinary Boolean conditions

**Avoid:**

```python
if is_enabled == True:
    activate()
```

**Prefer:**

```python
if is_enabled:
    activate()
```

```python
if not is_enabled:
    deactivate()
```

**Nuance:** `value is True` is a different, stricter identity test than `if value:`. If a public interface genuinely requires the exact `True` singleton, that semantic requirement can justify an identity check. Do not simplify it without considering behavior.

### 11.3 Prefer truthiness for ordinary empty sequences

**Avoid:**

```python
if len(records) > 0:
    process(records)
```

**Prefer:**

```python
if records:
    process(records)
```

For an empty sequence:

```python
if not records:
    return []
```

**Important exception:** NumPy arrays and pandas DataFrames have different or ambiguous truth-value behavior. For those objects, explicitly test `.empty`, `.size`, `.any()`, or `.all()` according to your intent. `if dataframe:` is not the correct generalized replacement.

### 11.4 Use `isinstance` for polymorphic type checks

**Avoid:**

```python
if type(value) is list:
    process(value)
```

**Prefer when subclasses are acceptable:**

```python
if isinstance(value, list):
    process(value)
```

`isinstance` respects subclass relationships. If a true **exact-type** comparison is a deliberate requirement, direct type comparison has different semantics and may be appropriate.

### 11.5 Prefer `startswith` and `endswith`

**Avoid:**

```python
if filename[-3:] == ".py":
    process(filename)
```

**Prefer:**

```python
if filename.endswith(".py"):
    process(filename)
```

```python
if key.startswith("ecl_"):
    process(key)
```

These methods communicate the intent directly and avoid manual slice-length calculations.

### 11.6 Define named functions with `def`, not assigned lambdas

**Avoid:**

```python
calculate_tax = lambda amount: amount * 0.13
```

**Prefer:**

```python
def calculate_tax(amount: float) -> float:
    return amount * 0.13
```

Named `def` functions offer clearer tracebacks and introspection. Lambdas remain appropriate for small callbacks or expressions where an inline function is itself the intended argument:

```python
sorted(people, key=lambda person: person.age)
```

### 11.7 Catch specific exceptions

**Avoid:**

```python
try:
    count = int(raw_count)
except:
    count = 0
```

**Prefer:**

```python
try:
    count = int(raw_count)
except ValueError:
    count = 0
```

A bare `except:` also catches `KeyboardInterrupt` and `SystemExit`. Catching `Exception` is preferable when intentionally handling conventional application failures without intercepting those process-control exceptions. The narrowest suitable exception is normally best.

### 11.8 Keep `try` blocks narrow; use `else` when helpful

**Less safe:**

```python
try:
    value = records[key]
    return transform(value)
except KeyError:
    return None
```

The handler could accidentally conceal a `KeyError` raised **inside `transform()`**.

**Prefer:**

```python
try:
    value = records[key]
except KeyError:
    return None
else:
    return transform(value)
```

The `else` branch runs only when the lookup succeeds. This isolates the operation whose `KeyError` you actually mean to catch.

### 11.9 Preserve exception context thoughtfully

```python
def parse_identifier(raw: str) -> int:
    try:
        return int(raw)
    except ValueError as exc:
        raise InvalidIdentifierError(raw) from exc
```

Use `raise NewError(...) from exc` when replacing one exception while preserving the cause. Use `from None` only when intentionally suppressing the visible cause and when the new exception carries the information the caller needs.

### 11.10 Use context managers for resource lifetime

**Avoid:**

```python
file = open(path, encoding="utf-8")
content = file.read()
file.close()
```

**Prefer:**

```python
with open(path, encoding="utf-8") as file:
    content = file.read()
```

This ensures orderly cleanup even if an exception occurs. Context-manager methods should communicate their purpose; avoid hiding complex unrelated behavior behind a surprising `with object:` syntax.

### 11.11 Be consistent with return paths

**Avoid ambiguous implicit returns:**

```python
def sqrt_if_valid(value: float) -> float | None:
    if value >= 0:
        return value ** 0.5
```

**Prefer explicit `None` for this optional-result function:**

```python
def sqrt_if_valid(value: float) -> float | None:
    if value < 0:
        return None
    return value ** 0.5
```

When a function returns a meaningful value on some paths, make its other return outcomes explicit. A procedure that always returns `None` does not need an explicit `return None` at every exit.

### 11.12 Do not suppress exceptions through `finally`

**Avoid:**

```python
def get_result():
    try:
        raise ValueError("Failed")
    finally:
        return 42
```

The return from `finally` hides the active exception.

**Prefer:**

```python
def get_result():
    try:
        return calculate_result()
    finally:
        release_resources()
```

The `finally` suite performs cleanup but does not replace the result or suppress the failure.

### 11.13 Choose portable string concatenation patterns

For many string fragments, especially inside loops, accumulate fragments and then join:

```python
parts = []
for record in records:
    parts.append(str(record))

output = "".join(parts)
```

Avoid building large strings by repeatedly depending on a particular Python implementation's optimization of `+=`. `join` communicates the accumulation pattern clearly.

### 11.14 Rich comparisons

For custom classes supporting ordering, ensure the ordering operations behave consistently. PEP 8 recommends considering the full set of six rich comparisons (`==`, `!=`, `<`, `<=`, `>`, `>=`) rather than counting on every consumer to infer them. `functools.total_ordering` can generate missing methods from a smaller definition.

```python
from functools import total_ordering


@total_ordering
class Priority:
    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Priority):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, Priority):
            return NotImplemented
        return self.value < other.value
```

This is a standard-library convenience, not a blanket instruction that every custom class must implement ordering. When comparing across incompatible types, returning `NotImplemented` allows Python's comparison machinery to handle the case.

---
## 12. Type annotation style

PEP 8 describes **formatting conventions** for type annotations. Type-hint meanings and typing-system design are covered primarily by PEP 484, PEP 526, and newer typing PEPs. Type hints are not mandatory just because PEP 8 specifies how to format them.

### 12.1 Annotate function inputs and outputs clearly

```python
def fetch_transactions(
    transaction_ids: list[str],
    include_archived: bool = False,
) -> dict[str, float]:
    return {transaction_id: 0.0 for transaction_id in transaction_ids}
```

Spacing rules:

- Write `parameter: Type`, not `parameter:Type` or `parameter : Type`.
- Write `) -> ReturnType:`, with spaces around the arrow.
- Use `parameter: Type = default` when an annotated parameter has a default.
- Write ordinary keyword arguments as `name=value` without spaces around `=`.

### 12.2 Annotate variables and attributes

```python
portfolio_id: int = 101
portfolio_names: list[str] = []


class Transaction:
    transaction_type: str

    def __init__(self, transaction_id: str):
        self.transaction_id: str = transaction_id
```

A variable annotation does not by itself enforce type checking during ordinary execution.

### 12.3 Optional results

```python
def find_portfolio(
    portfolio_id: int,
) -> dict[str, str] | None:
    if portfolio_id <= 0:
        return None
    return {"id": str(portfolio_id)}
```

The `T | None` spelling requires Python 3.10 or newer. For earlier Python compatibility, use `Optional[T]` or relevant postponed-evaluation strategies as appropriate. This is a *version compatibility consideration*, not a PEP 8 whitespace rule.

### 12.4 Collections, mappings, and interfaces

```python
from collections.abc import Iterable, Mapping, Sequence


def normalize_scores(scores: Sequence[float]) -> list[float]:
    return [score / 100 for score in scores]


def sum_measurements(values: Iterable[float]) -> float:
    return sum(values)


def read_currency(record: Mapping[str, str]) -> str:
    return record["currency"]
```

Whether to accept `Sequence`, `Iterable`, `Mapping`, or a concrete `list` depends on the API's behavioral requirements. Choosing the most appropriate abstraction is a typing/design decision rather than a rule imposed by PEP 8.

### 12.5 Distinguish `None` defaults from required values

```python
def calculate_discount(
    amount: float,
    rate: float | None = None,
) -> float:
    if rate is None:
        rate = 0.05
    return amount * rate
```

The annotation reflects the admitted `None` default. This is more accurate than claiming `rate: float = None` without an explicit reason or type-checking convention.

### 12.6 Annotations are not docstrings

```python
def convert_amount(amount: float, currency: str) -> float:
    return amount * exchange_rates[currency]
```

The signature describes input and output *types*. It does not tell the caller what exchange-rate convention is used, whether the function mutates state, or what exceptions can occur. Add documentation where these behavioral details are part of the public contract.

---

## 13. Applied examples: data processing and SQLAlchemy

The following demonstrate readable formatting in the kinds of chained and query-building code common in data engineering. They are **applications** of PEP 8 ideas, not additional rules found in PEP 8.

### 13.1 Readable pandas method chains

**Harder to scan:**

```python
result=df[df["active"]==True].groupby("portfolio_id")["balance"].sum().reset_index().sort_values("balance",ascending=False)
```

**Prefer:**

```python
result = (
    df.loc[df["active"]]
    .groupby("portfolio_id", as_index=False)["balance"]
    .sum()
    .sort_values("balance", ascending=False)
)
```

This exposes the pipeline's selection, aggregation, and ordering phases. It also avoids `== True` when the `active` column is already Boolean. In pandas, nullable Boolean values may require a deliberate policy for missing data.

### 13.2 Multiline SQLAlchemy query expressions

```python
from sqlalchemy import Select, select
from sqlalchemy.sql.schema import Table


def build_portfolio_query(table: Table) -> Select:
    return (
        select(
            table.c.portfolio_id,
            table.c.balance,
        )
        .where(table.c.is_active.is_(True))
        .order_by(table.c.portfolio_id)
    )
```

The nested structure makes it easy to distinguish selected columns, filters, and ordering. Some query builders also prefer breaking the method chain after the leading `select(...)`, as shown here.

### 13.3 Scalar subquery expressions

```python
from sqlalchemy import func, select


latest_month = (
    select(func.max(process_table.c.process_month))
    .scalar_subquery()
)

statement = select(results_table).where(
    results_table.c.process_month == latest_month
)
```

The local name describes the role of the expression, while indentation separates the subquery from the enclosing selection. A scalar subquery is a **SQL expression**, not a Python scalar fetched from a database. Query semantics are governed by SQLAlchemy, not PEP 8.

### 13.4 Long transformations and keyword arguments

```python
output = transform_results(
    input_data=transactions,
    process_month=process_month,
    hierarchy_ids=hierarchy_ids,
    include_historical_values=True,
)
```

This avoids a long horizontal call and gives each input a stable place in code reviews.

### 13.5 Naming a general query module

```text
queries/
├── __init__.py
├── common.py
├── ecl.py
└── transactions.py
```

All names are stylistically reasonable. Whether a general-purpose module should be named `common.py`, `shared.py`, or `builders.py` depends on its responsibilities rather than a PEP 8 prescription. Favor a name that accurately describes the content; `common.py` is not automatically superior.

### 13.6 One coherent class example

```python
from collections.abc import Sequence


class TransactionCompiler:
    DEFAULT_BATCH_SIZE = 100

    def __init__(self, transaction_ids: Sequence[str]):
        self.transaction_ids = list(transaction_ids)

    def compile(self, batch_size: int = DEFAULT_BATCH_SIZE):
        if batch_size <= 0:
            raise ValueError("Batch size must be positive")

        return [
            self.transaction_ids[index : index + batch_size]
            for index in range(0, len(self.transaction_ids), batch_size)
        ]
```

The example combines CapWords classes, uppercase constants, snake_case names, meaningful whitespace, specific exceptions, and a compact list comprehension.

---

## 14. PEP 8 versus modern formatting tools

### 14.1 PEP 8 is guidance; a formatter is an implementation

PEP 8 describes human-readable conventions. A formatter such as **Black** or **Ruff's formatter** makes specific layout decisions automatically. A linter such as **Ruff** checks many potential style and correctness problems; its formatter is a different capability.

| Dimension | PEP 8 | Black / Ruff formatter |
|---|---|---|
| Nature | Written style recommendations | Automated code rewriting |
| Typical code width | 79, with some agreed exceptions | 88 by default |
| String quote style | Neither single nor double quotes universally required | Often normalizes to double quotes by default |
| Multiline calls | Multiple acceptable layouts | Uses consistent chosen layouts |
| Imports | Groups and discourages wildcard imports | Sorting generally needs a linter/import tool |
| Naming | Gives conventions | Formatter does not generally rename identifiers |
| Program design | Includes selected idioms | Formatter does not fix architectural or logical design |

An 88-character project is not necessarily poorly styled; it simply chooses a widespread modern formatting convention rather than PEP 8's original 79-character baseline.

### 14.2 Formatters do not validate all semantics

They generally cannot determine whether:

- `calculate_ecl` is a meaningful public function name.
- A class has a coherent public API.
- `None` is a legitimate value in a business domain.
- An exception is too general for the intended error contract.
- A DataFrame's truthiness is well-defined.
- A comment accurately describes its neighboring code.

Use type checking, tests, review, and thoughtful design alongside formatting.

### 14.3 Avoid using two competing formatters on every save

Black and Ruff's formatter are designed to be largely compatible, but their output is not guaranteed to be byte-for-byte identical in every case. For a given repository, choose **one primary formatter** and configure other tools to avoid contradictory rules.

### 14.4 Line length is a policy decision

A practical approach:

- **79 characters:** close to the PEP 8 default.
- **88 characters:** widespread Black/Ruff default, often a useful compromise.
- **99 characters or fewer:** PEP 8 explicitly permits team consensus to extend code line length within this bound, while retaining the shorter comments/docstrings convention.

For lines that contain lengthy identifiers, URLs, strings, or unbreakable tokens, a formatter or linter may still be unable to achieve the configured width without harming readability.

---

## 15. Practical Ruff configuration and commands

Ruff can provide both a linter and a formatter using one tool. The following is an **example setup** for a project that wants a PEP 8-like 79-character limit. It is not a required or official PEP 8 configuration.

### 15.1 Install and run

```bash
python -m pip install ruff

ruff check .
ruff format .
ruff format --check .
ruff check --fix .
```

`ruff check .` reports lint issues; `ruff format .` rewrites formatting; `ruff format --check .` reports files that would need formatting without rewriting them; `ruff check --fix .` applies eligible lint fixes. Always review automatic changes in version control.

### 15.2 Example `pyproject.toml`

```toml
[tool.ruff]
line-length = 79
indent-width = 4
target-version = "py311"

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

**Customize** `target-version` to the oldest Python version your application supports. The example's `py311` is illustrative, not a recommendation to target Python 3.11 in every project. The selected lint families check a useful subset of error, Pyflakes, and import-sorting rules; they do **not** claim exhaustive PEP 8 enforcement.

### 15.3 Why not turn on every rule without review?

Some lint rules are stylistic, some catch likely bugs, and some conflict with formatters. For example, strict line-length linting may flag otherwise acceptable long string literals or generated expressions. Enable additional rule sets deliberately and adjust exceptions at the project level when needed.

### 15.4 A practical editing workflow

1. Write code with meaningful names and simple control flow.
2. Run the formatter to normalize punctuation, whitespace, and wrapping.
3. Run the linter to detect additional issues such as unused imports.
4. Run type checking and tests when appropriate.
5. Review the final diff for behavior, interface stability, and maintainability.

### 15.5 Beyond PEP 8: useful tools

| Tool | Typical purpose |
|---|---|
| Ruff linter | Style, import, and selected correctness checks |
| Ruff formatter | Automatic code layout |
| Black | Opinionated automatic code layout |
| mypy or Pyright | Static type analysis |
| pytest | Automated testing |
| pre-commit | Repeatable checks before a commit |

A project need not install every listed tool. Choose a coherent workflow with minimal overlap.

---

## 16. Before-and-after refactoring examples

These examples illustrate multiple conventions together. The **before** examples are intentionally poorly styled; the **after** examples prioritize clarity without changing the intended logic.

### Example A: inconsistent naming, spacing, and imports

**Before**

```python
import os,sys
DEFAULTLIMIT=20

def GetItems(Items,minimum=0):
  result=[]
  for I in Items:
    if I>=minimum:result.append(I)
  return result[:DEFAULTLIMIT]
```

**After**

```python
import os
import sys

DEFAULT_LIMIT = 20


def get_items(items, minimum=0):
    result = []
    for item in items:
        if item >= minimum:
            result.append(item)
    return result[:DEFAULT_LIMIT]
```

Note that `os` and `sys` are not actually used by this snippet. A linter may suggest **deleting** them, which is better than merely splitting them onto separate lines. They are retained here only to show the import-layout correction.

### Example B: unnecessary Boolean comparison and complex return

**Before**

```python
def filter_records(records,enabled=True):
    if enabled==True:return [x for x in records if x["active"]==True]
    else:return records
```

**After**

```python
def filter_records(records, enabled=True):
    if enabled:
        return [record for record in records if record["active"]]
    return records
```

The meaning is preserved when `enabled` and `record["active"]` represent ordinary truth-valued flags. The longer form also avoids an unnecessary `else` following an unconditional `return`.

### Example C: broad exception handling

**Before**

```python
def parse_balance(row):
    try:
        return float(row["balance"])
    except:
        return 0.0
```

**After**

```python
def parse_balance(row):
    try:
        raw_balance = row["balance"]
    except KeyError:
        return 0.0

    try:
        return float(raw_balance)
    except (TypeError, ValueError):
        return 0.0
```

The second version states which failures should result in the fallback. The choice to treat missing or invalid values as zero is a **domain decision**, not something dictated by PEP 8.

### Example D: complicated function call

**Before**

```python
output=calculate(data,params,scenario_weights,process_month,include_history=True,raise_on_missing=False)
```

**After**

```python
output = calculate(
    data,
    params,
    scenario_weights,
    process_month,
    include_history=True,
    raise_on_missing=False,
)
```

### Example E: splitting a calculation into visible stages

**Before**

```python
def calculate_final_amount(price,tax,discount,shipping):return (price-price*discount)*(1+tax)+shipping
```

**After**

```python
def calculate_final_amount(
    price: float,
    tax: float,
    discount: float,
    shipping: float,
) -> float:
    discounted_price = price * (1 - discount)
    taxed_price = discounted_price * (1 + tax)
    return taxed_price + shipping
```

The intermediate variables improve comprehension; **introducing them is a readability choice**, not an explicit PEP 8 mandate.

---

## 17. Common misconceptions and edge cases

### Q1. Does PEP 8 require every line to be at most 79 characters?

No. **79** is the default recommendation for code. PEP 8 allows a team to agree on up to **99** characters for code, and readability or unavoidable tokens can justify localized exceptions.

### Q2. Is Black's 88-character default an official PEP 8 limit?

No. It is a formatter policy chosen to balance readability and compactness. It is widely used but distinct from PEP 8's default.

### Q3. Does PEP 8 require double quotes for every string?

No. Ordinary strings may use single or double quotes consistently. Triple double quotes are recommended for docstrings.

### Q4. Is `snake_case` mandatory for every object?

No. Functions and variables normally use `snake_case`; classes use `CapWords`; constants use `UPPER_SNAKE_CASE`; special methods use their documented `__dunder__` names.

### Q5. Does a leading underscore make an attribute private?

No. `_attribute` is an intentional non-public signal. `__attribute` within a class triggers name mangling, but even that is not an access-control boundary.

### Q6. Is `if not values:` always better than `if len(values) == 0:`?

For ordinary lists, tuples, and strings, it usually reads better. For NumPy/pandas objects, truthiness may be ambiguous or mean something different. Choose a condition suited to the object's API.

### Q7. Is `is None` the same as `not value`?

No. `is None` distinguishes the singleton `None`, whereas `not value` is true for many false-like values such as `0`, `""`, and `[]`.

### Q8. Is `from .module import name` a PEP 8 violation?

No. Absolute imports are recommended by default, but **explicit relative imports** are a supported alternative.

### Q9. Does every function need a return annotation?

No. PEP 8 governs formatting if annotations are present; it does not force universal annotation. A team's type-checking policy may require more annotations.

### Q10. Does following PEP 8 guarantee good architecture?

No. A perfectly formatted module may still have overly coupled classes, unclear responsibility boundaries, hidden state, poor exception handling, or incorrect SQL.

### Q11. Do all PEP 8 recommendations apply uniformly to legacy code?

No. Preserving compatibility and local consistency may be more important. Style-only edits should not silently change external APIs.

### Q12. Is a formatter equivalent to a linter?

No. A formatter rewrites layout; a linter analyzes selected rules and potential defects. Ruff includes **both**, invoked with different commands.

### Q13. Does using a type annotation perform runtime validation?

No. Python ordinarily records annotations but does not automatically check argument or return types at runtime. Additional tools or logic are needed for validation.

### Q14. Should you always remove `else` following `return`?

Not as an absolute rule. Removing it often reduces indentation, but retaining it may be helpful to emphasize symmetrical branches. Judge readability in context.

### Q15. Should you rewrite a public API solely to make its name PEP 8-compliant?

Not without weighing breakage. PEP 8 explicitly places compatibility and project context above mechanical stylistic consistency.

---

## 18. Review checklist and references

### 18.1 Quick pre-commit checklist

**Layout**

- [ ] Four spaces per normal indentation level.
- [ ] Long expressions wrapped clearly, preferably within delimiters.
- [ ] Appropriate blank lines around definitions and between logical phases.
- [ ] No trailing whitespace or gratuitous line continuations.
- [ ] Line-width policy matches the project's documented rules.

**Imports**

- [ ] Imports grouped by standard library, third-party, and local code.
- [ ] No unexplained wildcard imports or unused imports.
- [ ] Explicit absolute or relative imports are sensible for the package.
- [ ] Future imports and module metadata are ordered correctly.

**Naming and interfaces**

- [ ] Functions, variables, classes, constants, and modules use suitable styles.
- [ ] `self` and `cls` follow the standard conventions.
- [ ] Internal names and stable public interfaces are clearly differentiated.
- [ ] Existing public names are not changed unintentionally.

**Expressions and control flow**

- [ ] Whitespace around operators and annotations is consistent.
- [ ] `None` uses identity comparisons.
- [ ] Boolean and collection tests express the intended semantics.
- [ ] Exceptions are caught as narrowly as practical.
- [ ] Return paths are understandable and exception behavior is preserved.
- [ ] Resource cleanup uses context managers or equivalent safe handling.

**Documentation and tooling**

- [ ] Comments explain meaningful decisions rather than obvious operations.
- [ ] Public APIs are documented where useful.
- [ ] The chosen formatter and linter have been run.
- [ ] Tests and static analysis have been run where appropriate.

### 18.2 Compact memory aid

```text
4 spaces                  normal indentation
79 / 72 characters        code / prose default limits
2 / 1 blank lines         top-level definitions / methods
snake_case                functions, methods, variables
CapWords                  classes and exception classes
UPPER_SNAKE_CASE          module-level constants
_name                     non-public convention
name_                     reserved keyword avoidance
__name__                  only documented special names
self / cls                instance / class method parameters
x is None                 singleton comparison
if items:                 ordinary collection truthiness
except SpecificError:     targeted error handling
func(limit=10)            keyword argument spacing
def f(x: int = 10)         annotated default spacing
def f(x: int) -> str:      annotation spacing
(value,)                  singleton tuple
```

### 18.3 Primary references

1. **PEP 8 — Style Guide for Python Code:** https://peps.python.org/pep-0008/
2. **PEP 257 — Docstring Conventions:** https://peps.python.org/pep-0257/
3. **PEP 484 — Type Hints:** https://peps.python.org/pep-0484/
4. **PEP 526 — Syntax for Variable Annotations:** https://peps.python.org/pep-0526/
5. **Ruff Formatter documentation:** https://docs.astral.sh/ruff/formatter/
6. **Ruff configuration documentation:** https://docs.astral.sh/ruff/configuration/
7. **Black code style documentation:** https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html

### 18.4 How to use this guide

For quick daily work, consult the **at-a-glance rules** and **review checklist**. For design questions, review **naming**, **public interfaces**, and **programming recommendations**. If a formatting choice is disputed, consult the linked PEP 8 text and the repository's documented convention before changing working code.

---

*End of study guide.*
