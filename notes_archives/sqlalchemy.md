# SQLAlchemy

**Reference style:** SQLAlchemy class/function/method → what it does, with Core, ORM, execution, Result, relationship, SQL, schema, inspection, async, typing, and practical examples.

**Primary syntax:** modern SQLAlchemy **2.x** (`select(...)`, `Session.execute()` / `Session.scalars()`, typed declarative mappings). The original guide specifically focused on 2.1.x; older `session.query()` / `Query` are **legacy**.

**DB support:** compilation and capabilities vary by dialect (e.g., PostgreSQL/SQLite/MySQL/SQL Server); not every expression is available on every backend.

> **Mental model:** A *SQL statement/expression*, an *ORM object*, a *session*, and a *result object* are different types with different method families. Understanding the object type is central to readable SQLAlchemy code.

## Table of Contents

- [Core type transitions](#core-type-transitions)
- [Example database and ORM definitions](#example-database-and-orm-definitions)
- [Return types and evaluation stages](#return-types-and-evaluation-stages)
- [Class-specific result and expression methods](#class-specific-result-and-expression-methods)

- [1. SELECT — basic construction](#1-select--basic-construction)
- [2. SELECT — choosing columns](#2-select--choosing-columns)
- [3. Filtering operators](#3-filtering-operators)
- [4. Boolean expressions](#4-boolean-expressions)
- [5. String operators](#5-string-operators)
- [6. NULL handling](#6-null-handling)
- [7. JOINs](#7-joins)
- [8. Relationship-based joins](#8-relationship-based-joins)
- [9. Aliases](#9-aliases)
- [10. Subqueries](#10-subqueries)
- [11. EXISTS](#11-exists)
- [12. Set operations](#12-set-operations)
- [13. CTEs](#13-ctes)
- [14. Recursive CTEs](#14-recursive-ctes)
- [15. CASE expressions](#15-case-expressions)
- [16. SQL functions](#16-sql-functions)
- [17. Aggregation](#17-aggregation)
- [18. Labels](#18-labels)
- [19. CAST / type coercion](#19-cast--type-coercion)
- [20. Literal expressions](#20-literal-expressions)
- [21. `text()` — raw SQL escape hatch](#21-text--raw-sql-escape-hatch)
- [22. INSERT](#22-insert)
- [23. UPDATE](#23-update)
- [24. DELETE](#24-delete)
- [25. RETURNING](#25-returning)
- [26. Execution](#26-execution)
- [27. `Result` methods](#27-result-methods)
- [28. Result shape mental model](#28-result-shape-mental-model)
- [29. `scalar()` vs `scalars()`](#29-scalar-vs-scalars)
- [30. Session — object persistence](#30-session--object-persistence)
- [31. Session — flushing / committing](#31-session--flushing--committing)
- [32. Session — retrieving by primary key](#32-session--retrieving-by-primary-key)
- [33. Session — refresh / expiration](#33-session--refresh--expiration)
- [34. Session — detaching objects](#34-session--detaching-objects)
- [35. Session transactions](#35-session-transactions)
- [36. Session execution controls](#36-session-execution-controls)
- [37. ORM model declaration](#37-orm-model-declaration)
- [38. `mapped_column()`](#38-mapped_column)
- [39. Relationships](#39-relationships)
- [40. Relationship query operators](#40-relationship-query-operators)
- [41. Relationship loading](#41-relationship-loading)
- [42. Column loading controls](#42-column-loading-controls)
- [43. `.options()`](#43-options)
- [44. Global ORM filtering](#44-global-orm-filtering)
- [45. ORM aliases](#45-orm-aliases)
- [46. SQL window functions](#46-sql-window-functions)
- [47. Useful window functions](#47-useful-window-functions)
- [48. Ordering helpers](#48-ordering-helpers)
- [49. Distinct](#49-distinct)
- [50. Tuple comparisons](#50-tuple-comparisons)
- [51. Arithmetic expressions](#51-arithmetic-expressions)
- [52. Metadata](#52-metadata)
- [53. Table](#53-table)
- [54. Table convenience methods](#54-table-convenience-methods)
- [55. Schema constraints](#55-schema-constraints)
- [56. Database reflection](#56-database-reflection)
- [57. Engine](#57-engine)
- [58. Connection](#58-connection)
- [59. Compiling SQL](#59-compiling-sql)
- [60. ORM state inspection](#60-orm-state-inspection)
- [61. Mapper inspection](#61-mapper-inspection)
- [62. ORM column expressions](#62-orm-column-expressions)
- [63. Bulk ORM INSERT](#63-bulk-orm-insert)
- [64. Bulk ORM UPDATE](#64-bulk-orm-update)
- [65. Locking](#65-locking)
- [66. Execution options](#66-execution-options)
- [67. Streaming / large query results](#67-streaming--large-query-results)
- [68. Async SQLAlchemy](#68-async-sqlalchemy)
- [69. Events](#69-events)
- [70. Dialect-specific INSERT extensions](#70-dialect-specific-insert-extensions)
- [71. SQLAlchemy classes/types worth knowing](#71-sqlalchemy-classestypes-worth-knowing)
- [72. Function annotations and choosing the correct abstraction](#72-function-annotations-and-choosing-the-correct-abstraction)
- [73. Compact SQLAlchemy vocabulary map](#73-compact-sqlalchemy-vocabulary-map)
  - [Priority list for complex transaction-processing architectures](#priority-list-for-complex-transaction-processing-architectures)
  - [Minimal import cheat sheet](#minimal-import-cheat-sheet)
- [Selectable Class Hierarchy](#selectable-class-hierarchy)
  - [Official references](#official-references)


## Core type transitions

| Python expression | Class produced | Important consequence |
|---|---|---|
| `select(User)` | `Select` | Builds a statement; does not execute it |
| `select(User).where(User.id == 1)` | `Select` | Returns another statement of the same class |
| `User.id == 1` | `BinaryExpression` | Creates SQL, not Python `True` / `False` |
| `select(User.id).subquery()` | `Subquery` | Becomes a `FROM` object; exposes `.c` |
| `select(User.id).scalar_subquery()` | `ScalarSelect` | Becomes one SQL expression; supports comparisons |
| `select(User).exists()` | `Exists` | Becomes a boolean SQL expression |
| `select(User.id).cte("ids")` | `CTE` | Named `FROM`-usable common table expression |
| `User.__table__.alias("u")` | `Alias` | Core alias of a `FromClause` |
| `aliased(User)` | `AliasedClass` | ORM-aware mapped-entity alias |
| `User.__table__.join(Address.__table__)` | `Join` | Core FROM-able join |
| `select(User).join(Address)` | `Select` | Join is composed into the SELECT |
| `union_all(select(...), select(...))` | `CompoundSelect` | Compound statement |
| `func.count()` | `count` (`FunctionElement`) | SQL function expression |
| `func.count().label("n")` | `Label` | Labeled SQL expression |
| `func.row_number().over(...)` | `Over` | Window expression |
| `insert(User)` / `update(User)` / `delete(User)` | `Insert` / `Update` / `Delete` | Executable DML statements |
| `create_engine(...)` | `Engine` | Database-connectivity façade and pool |
| `engine.connect()` | `Connection` | Synchronous database connection |
| `Connection.execute(select(...))` | `CursorResult` | Core execution result |
| `Session.execute(select(...))` | `Result` | ORM-aware execution result |
| `result.first()` | `Row` or `None` | One tuple-like row |
| `result.scalars()` | `ScalarResult` | Values from one selected position |
| `result.mappings()` | `MappingResult` | Produces `RowMapping` values |
| `Session.scalar(select(...))` | Python value or `None` | Retrieves one scalar immediately |
| `inspect(engine)` | `Inspector` | Database schema inspection |
| `inspect(User)` | `Mapper` | ORM mapping inspection |
| `inspect(user_instance)` | `InstanceState` | ORM object state inspection |

The `Result` and `Select` types in the table are API-level types. Concrete runtime implementations can be subclasses, and Python generic type hints such as `Result[tuple[User]]` do not always coincide with `type(obj).__name__`.

## Example database and ORM definitions

The following definitions establish a simple SQLite dataset for the SQLAlchemy examples. They use ordinary SQLAlchemy 2.x declarative mapping and require no external database server.

```python
from __future__ import annotations

from datetime import date, datetime
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, MetaData, Numeric, UniqueConstraint, Index,
    String, Table, and_, bindparam, case, cast, column,
    create_engine, delete, distinct, exists, false, func,
    insert, inspect, literal, literal_column, null,
    or_, select, table, text, true, try_cast, tuple_,
    type_coerce, union, union_all, update, values,
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, Session, aliased, defer,
    joinedload, load_only, mapped_column, relationship,
    selectinload, with_loader_criteria,
    column_property, query_expression,
)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    addresses: Mapped[list[Address]] = relationship(back_populates="user")

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    city: Mapped[str] = mapped_column(String)
    user: Mapped[User] = relationship(back_populates="addresses")

engine = create_engine("sqlite+pysqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([
        User(id=1, name="Ada", addresses=[
            Address(city="Toronto"), Address(city="Toronto")
        ]),
        User(id=2, name="Grace", addresses=[Address(city="Boston")]),
        User(id=3, name="Linus"),
    ])
    session.commit()
```

The pre-existing sections also use conceptual models such as `Transaction`, `TransactionItem`, and `Hierarchy`. Those model names represent mapped tables with the named attributes. The executed examples use the concrete `User` and `Address` models above.

## Return types and evaluation stages

There are three distinct meanings of “return type” in SQLAlchemy:

1. **Statement-construction type:** `type(select(User)).__name__` is `Select`.
2. **Execution-result type:** `session.execute(select(User))` implements `Result` and returns rows.
3. **Selected Python value type:** `session.scalars(select(User)).first()` returns a `User` instance or `None`.

Type annotations and runtime types can differ. For example, `Mapped[int]` specifies an integer-valued ORM attribute for type checking; `User.id` at class level is a SQLAlchemy `InstrumentedAttribute`; `user.id` on an instance is a Python `int`.


## 1. SELECT — basic construction

**Object behavior.** A `Select` is a Python statement object, not query results. Calling `.where()` generates a new `Select`; the original remains unchanged. Predicates passed to `.where()` together are combined with SQL `AND`.


**Return types** — select() / Select

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `select()` | `Select` | construct SELECT statement |
| `.where()` | `Select` | WHERE condition |
| `.filter()` | `Select` | ORM-friendly synonym for where() |
| `.filter_by()` | `Select` | filter using keyword attribute names |
| `.order_by()` | `Select` | ORDER BY |
| `.group_by()` | `Select` | GROUP BY |
| `.having()` | `Select` | HAVING |
| `.distinct()` | `Select` | SELECT DISTINCT |
| `.limit()` | `Select` | LIMIT |
| `.offset()` | `Select` | OFFSET |
| `.slice()` | `Select` | LIMIT + OFFSET using slice semantics |

```python
select(User)
select(User).where(User.id == 10)
select(User).where(
    User.division == 'CB',
    User.stage == 1,
)
select(User).order_by(User.keyid)
select(User).limit(10).offset(20)
```

`Select` methods are generally **generative**: `.where()` etc. return a new statement rather than mutating the existing one. Multiple `.where()` predicates are combined with AND.

### Example and output

```python
base = select(User)
filtered = base.where(User.id > 1)

print(type(base).__name__, type(filtered).__name__)
print(base is filtered)
print([user.name for user in Session(engine).scalars(filtered)])
```

```text
Select Select
False
['Grace', 'Linus']
```

## 2. SELECT — choosing columns

**Object behavior.** Selecting an ORM entity yields rows containing that mapped entity; selecting only columns yields row values. `.selected_columns` exposes expression objects, not retrieved database data.


**Return types** — Select / SQL column expression

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `select(col1, col2)` | `Select` | select specific columns |
| `.add_columns()` | `Select` | add output columns |
| `.with_only_columns()` | `Select` | replace selected columns |
| `.selected_columns` | `ReadOnlyColumnCollection` | inspect selected columns |
| `.label()` | `Label` | label scalar expression |

```python
stmt = select(
    Transaction.keyid,
    Transaction.transaction_type,
    Transaction.created_at,
)
```

Or:

```python
stmt = (
    select(Transaction)
    .add_columns(Transaction.keyid)
)
```

**Important:** `select(Transaction).add_columns(Transaction.keyid)` selects both the entity and a redundant extra scalar column.

### Example and output

```python
stmt = select(User.id, User.name)
print(type(stmt).__name__)
print(type(stmt.selected_columns).__name__)

with Session(engine) as session:
    print([tuple(row) for row in session.execute(stmt).all()])
```

```text
Select
ReadOnlyColumnCollection
[(1, 'Ada'), (2, 'Grace'), (3, 'Linus')]
```

## 3. Filtering operators

**Object behavior.** SQLAlchemy overloads Python comparison operators on SQL expression objects. `User.id == 1` creates a `BinaryExpression`, not a Python `bool`. Its truth value must not be used as a normal Python condition.


Primarily methods of `ColumnElement` / ORM mapped instrumented attributes.

**Return types** — ColumnElement / mapped attribute

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `==` | `BinaryExpression` | equality |
| `!=` | `BinaryExpression` | inequality |
| `>` | `BinaryExpression` | greater than |
| `>=` | `BinaryExpression` | greater than/equal |
| `<` | `BinaryExpression` | less than |
| `<=` | `BinaryExpression` | less than/equal |
| `.in_()` | `BinaryExpression` | SQL IN |
| `.not_in()` | `BinaryExpression` | SQL NOT IN |
| `.between()` | `BinaryExpression` | SQL BETWEEN |
| `.is_()` | `BinaryExpression` | SQL IS |
| `.is_not()` | `BinaryExpression` | SQL IS NOT |
| `.is_distinct_from()` | `BinaryExpression` | SQL IS DISTINCT FROM |
| `.is_not_distinct_from()` | `BinaryExpression` | SQL IS NOT DISTINCT FROM |

```python
User.id.in_([1, 2, 3])
Transaction.keyid.between(100, 500)
Transaction.value.is_(None)
Transaction.value.is_not(None)
```

```text
.is_(None)                  IS NULL
.is_not(None)               IS NOT NULL
```

### Example and output

```python
predicate = User.id.in_([1, 3])
print(type(predicate).__name__)

with Session(engine) as session:
    print(session.scalars(select(User.name).where(predicate)).all())
```

```text
BinaryExpression
['Ada', 'Linus']
```

## 4. Boolean expressions

**Object behavior.** `and_()` / `or_()` construct SQL logic. Python `and` / `or` are evaluated immediately and cannot compose SQL predicates. `not_()` may negate an operator into another binary expression, so its exact concrete class can vary.


**Return types** — SQL boolean expression

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `and_()` | `BooleanClauseList` | SQL AND |
| `or_()` | `BooleanClauseList` | SQL OR |
| `not_()` | `ColumnElement[bool] (usually unary/binary expression)` | SQL NOT |
| `&` | `ColumnElement[bool]` | AND for expressions |
| `\|` | `ColumnElement[bool]` | OR for expressions |
| `~` | `ColumnElement[bool]` | NOT for expressions |
| `true()` | `True_` | SQL TRUE |
| `false()` | `False_` | SQL FALSE |

```python
stmt = select(Transaction).where(
    and_(
        Transaction.stage == 1,
        Transaction.currency == 'CAD',
    )
)
```

Or, using implicit AND:

```python
stmt = select(Transaction).where(
    Transaction.stage == 1,
    Transaction.currency == 'CAD',
)
```

When using `&`/`|`, parenthesize every comparison due to Python precedence.

### Example and output

```python
predicate = and_(User.id >= 2, User.name != 'Ada')
print(type(predicate).__name__)

with Session(engine) as session:
    print(session.scalars(select(User.name).where(predicate)).all())
```

```text
BooleanClauseList
['Grace', 'Linus']
```

## 5. String operators

**Object behavior.** String operators normally return boolean SQL expressions. Dialects translate operations differently; `ilike()` on backends without native `ILIKE` can compile into case-normalized comparisons.


**Return types** — ColumnElement (string operators)

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.like()` | `BinaryExpression` | SQL LIKE |
| `.ilike()` | `BinaryExpression` | case-insensitive LIKE |
| `.not_like()` | `BinaryExpression` | NOT LIKE |
| `.not_ilike()` | `BinaryExpression` | NOT ILIKE |
| `.contains()` | `BinaryExpression` | contains substring |
| `.startswith()` | `BinaryExpression` | starts with |
| `.endswith()` | `BinaryExpression` | ends with |
| `.regexp_match()` | `BinaryExpression` | regex matching |
| `.regexp_replace()` | `ColumnElement (dialect-dependent)` | regex replacement |

```python
User.name.like('Mir%')
User.name.ilike('%abc%')
User.code.startswith('CB_')
```

Literal `_` and `%` have SQL wildcard meaning in `LIKE`; use escaping when matching literal pattern characters. Regex support is dialect-dependent.

### Example and output

```python
predicate = User.name.like('A%')
print(type(predicate).__name__)

with Session(engine) as session:
    print(session.scalars(select(User.name).where(predicate)).all())
```

```text
BinaryExpression
['Ada']
```

## 6. NULL handling

**Object behavior.** SQL `NULL` is not equal to ordinary values. `.is_(None)` constructs `IS NULL`; `func.coalesce()` is a SQL function expression evaluated by the database, not a Python fallback value.


**Return types** — ColumnElement / SQL function

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.is_(None)` | `BinaryExpression` | IS NULL |
| `.is_not(None)` | `BinaryExpression` | IS NOT NULL |
| `null()` | `Null` | literal SQL NULL |
| `nulls_first()` | `UnaryExpression` | NULLS FIRST |
| `nulls_last()` | `UnaryExpression` | NULLS LAST |
| `func.coalesce()` | `FunctionElement` | first non-null value |

```python
select(func.coalesce(Transaction.value, 0))
```

### Example and output

```python
expr = func.coalesce(literal(None), 42)
print(type(expr).__name__)

with Session(engine) as session:
    print(session.scalar(select(expr)))
```

```text
coalesce
42
```

The named `coalesce` subclass is a `FunctionElement`.

## 7. JOINs

**Object behavior.** The receiver determines the return type: `Select.join()` returns a new `Select`, whereas `Table.join()` returns a `Join` object, itself usable in `FROM`. Both may render `JOIN` in SQL.


**Return types** — Select

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.join()` | `Select` | INNER JOIN |
| `.outerjoin()` | `Select` | LEFT OUTER JOIN |
| `.join_from()` | `Select` | specify explicit left side |
| `.outerjoin_from()` | `Select` | explicit left side + outer join |
| `.select_from()` | `Select` | explicitly establish FROM clause |

```python
select(Transaction).join(TransactionItem)
```

Explicit condition:

```python
select(Transaction).join(
    TransactionItem,
    Transaction.uuid == TransactionItem.transaction_id,
)
```

Explicit starting point:

```python
select(TransactionItem).join_from(
    Transaction,
    TransactionItem,
)
```

`join()` without an ON clause needs an inferable FK relationship (or mapped relationship path), not merely similarly named columns.

### Example and output

```python
stmt = select(User).join(Address)
join = User.__table__.join(Address.__table__)

print(type(stmt).__name__)
print(type(join).__name__)

with Session(engine) as session:
    print([user.name for user in session.scalars(stmt)])
```

```text
Select
Join
['Ada', 'Ada', 'Grace']
```

## 8. Relationship-based joins

**Object behavior.** `User.addresses` on the mapped class is an `InstrumentedAttribute`. Its relationship comparator lets `.any()`, `.of_type()`, and `.and_()` build SQL; accessing `user.addresses` on an instance gives related objects instead.


**Return types** — ORM relationship comparator / Select

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.join(Model.relationship)` | `Select` | join using relationship configuration |
| `.outerjoin(Model.relationship)` | `Select` | outer join using relationship |
| `.of_type()` | `QueryableAttribute/PropComparator` | relationship against alias/subtype |
| `.and_()` | `PropComparator` | add conditions to relationship join |

```python
select(User).join(User.addresses)
```

Rather than manually:

```python
select(User).join(
    Address,
    User.id == Address.user_id,
)
```

Both are valid; the relationship path carries already-configured join semantics.

### Example and output

```python
stmt = select(User).join(User.addresses)
predicate = User.addresses.any(Address.city == 'Toronto')

print(type(User.addresses).__name__)
print(type(stmt).__name__)
print(type(predicate).__name__)

with Session(engine) as session:
    print([user.name for user in session.scalars(select(User).where(predicate))])
```

```text
InstrumentedAttribute
Select
Exists
['Ada']
```

## 9. Aliases

**Object behavior.** `Table.alias()` produces an `Alias`, `Select.subquery()` a `Subquery`, `Select.cte()` a `CTE`, and `Select.lateral()` a `Lateral`. These are `FROM`-usable objects; `aliased(User)` is instead an ORM `AliasedClass`.


**Return types** — FromClause / Select / ORM

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.alias()` | `Alias (Table/FromClause)` | SQL alias |
| `aliased()` | `AliasedClass (ORM alias)` | ORM entity alias |
| `.subquery()` | `Subquery` | SELECT → named subquery |
| `.cte()` | `CTE` | SELECT → CTE |
| `.lateral()` | `Lateral` | LATERAL subquery |

Core:

```python
tx = transaction_table.alias('tx')
```

ORM:

```python
Tx = aliased(Transaction)
```

### Example and output

```python
core_alias = User.__table__.alias('u')
orm_alias = aliased(User)
subq = select(User.id).subquery('ids')
cte = select(User.id).cte('ids')

print(type(core_alias).__name__)
print(type(orm_alias).__name__)
print(type(subq).__name__)
print(type(cte).__name__)
```

```text
Alias
AliasedClass
Subquery
CTE
```

## 10. Subqueries

**Object behavior.** A `Subquery` is a `FROM` source with a `.c` column collection; a `ScalarSelect` is a column expression usable in comparisons. They are not interchangeable despite originating from the same `Select`.


**Return types** — Select

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.subquery()` | `Subquery` | SELECT → FROM-able subquery |
| `.scalar_subquery()` | `ScalarSelect` | SELECT → scalar SQL expression |
| `.exists()` | `Exists` | SELECT → EXISTS expression |

```python
subq = (
    select(TransactionItem.transaction_id)
    .where(TransactionItem.stage == 1)
    .subquery()
)
```

Scalar:

```python
max_keyid = (
    select(func.max(Transaction.keyid))
    .scalar_subquery()
)

stmt = select(Transaction).where(
    Transaction.keyid == max_keyid
)
```

**Distinction:** a `Subquery` is a FROM-clause object; a `ScalarSelect` is usable like a SQL value/expression.

### Example and output

```python
stmt = select(User.id)
from_source = stmt.subquery()
scalar_expression = stmt.limit(1).scalar_subquery()

print(type(stmt).__name__)
print(type(from_source).__name__)
print(type(scalar_expression).__name__)
print(type(from_source.c.id).__name__)
```

```text
Select
Subquery
ScalarSelect
Column
```

A one-column `select(User.id)` may also be passed directly to `User.id.in_(...)`. This retains the `Select` as a subselect and does not require `.subquery()`.

## 11. EXISTS

**Object behavior.** An `Exists` is a boolean SQL expression, so it fits naturally in `.where()`. It does not return a Python `bool` until you execute an appropriate SQL query that evaluates it.


**Return types** — Select / sqlalchemy.exists

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `exists()` | `Exists` | construct EXISTS |
| `.exists()` | `Exists` | convert SELECT to EXISTS |

```python
stmt = select(Transaction).where(
    exists().where(
        TransactionItem.transaction_id == Transaction.uuid
    )
)
```

Or:

```python
item_exists = (
    select(TransactionItem)
    .where(
        TransactionItem.transaction_id == Transaction.uuid
    )
    .exists()
)
```

### Example and output

```python
expr = select(Address.id).where(Address.user_id == User.id).exists()
print(type(expr).__name__)

with Session(engine) as session:
    print(session.scalars(select(User.name).where(expr)).all())
```

```text
Exists
['Ada', 'Grace']
```

## 12. Set operations

**Object behavior.** Set operations return `CompoundSelect`. Ordinary `UNION` removes duplicate rows; `UNION ALL` retains them. Each branch must have compatible result column shapes.


**Return types** — Select / SQL set operation

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `union()` | `CompoundSelect` | SQL UNION |
| `union_all()` | `CompoundSelect` | SQL UNION ALL |
| `intersect()` | `CompoundSelect` | SQL INTERSECT |
| `intersect_all()` | `CompoundSelect` | INTERSECT ALL |
| `except_()` | `CompoundSelect` | SQL EXCEPT |
| `except_all()` | `CompoundSelect` | EXCEPT ALL |

```python
stmt = select(TableA.id).union_all(
    select(TableB.id)
)
```

Such compound SELECTs produce `CompoundSelect` constructs. Backend support varies for `INTERSECT ALL` and `EXCEPT ALL`.

### Example and output

```python
stmt = union_all(select(literal(1)), select(literal(2)))
print(type(stmt).__name__)

with engine.connect() as conn:
    print([row[0] for row in conn.execute(stmt)])
```

```text
CompoundSelect
[1, 2]
```

## 13. CTEs

**Object behavior.** A CTE is a named selectable embedded in the SQL statement. Creating it does not execute SQL or store rows in Python.


**Return types** — Select / statement

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.cte()` | `CTE` | create Common Table Expression |
| `.add_cte()` | `Select or another statement type (generative)` | attach CTE to statement |

```python
active_tx = (
    select(Transaction)
    .where(Transaction.is_processed == 0)
    .cte('active_tx')
)
stmt = select(active_tx)
```

A CTE can make multi-stage query plans much easier to read.

### Example and output

```python
selected = select(User.id, User.name).where(User.id <= 2)
cte = selected.cte('active_users')
stmt = select(cte.c.name)

print(type(cte).__name__, type(stmt).__name__)

with engine.connect() as conn:
    print(conn.execute(stmt).scalars().all())
```

```text
CTE Select
['Ada', 'Grace']
```

## 14. Recursive CTEs

**Object behavior.** The recursive branch is joined with a seed using a `CTE` method. The result remains a `CTE`, which can then be selected from using `.c`.


**Return types** — CTE

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.cte(recursive=True)` | `CTE` | recursive CTE |
| `.union_all()` | `CTE (when called on recursive CTE)` | recursive branch |

Useful for hierarchy trees, parent-child relationships, graphs and organization structures.

```python
seed = select(Hierarchy.id, Hierarchy.parent_id).where(Hierarchy.id == root_id)
tree = seed.cte('tree', recursive=True)
tree = tree.union_all(
    select(Hierarchy.id, Hierarchy.parent_id).join(
        tree, Hierarchy.parent_id == tree.c.id
    )
)
stmt = select(tree)
```

### Example and output

```python
seed = select(literal(1).label('n'))
series = seed.cte('series', recursive=True)
series = series.union_all(select(series.c.n + 1).where(series.c.n < 3))

print(type(series).__name__)

with engine.connect() as conn:
    print(conn.execute(select(series.c.n)).scalars().all())
```

```text
CTE
[1, 2, 3]
```

## 15. CASE expressions

**Object behavior.** `case()` creates a `Case`, a SQL value expression. The database evaluates each `WHEN` branch when executing the enclosing statement.


**Return types** — sqlalchemy.case

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `case()` | `Case` | SQL CASE WHEN |

```python
case(
    (Transaction.stage == 1, 'S1'),
    (Transaction.stage == 2, 'S2'),
    else_='S3',
)
```

SQL equivalent:

```sql
CASE
    WHEN stage = 1 THEN 'S1'
    WHEN stage = 2 THEN 'S2'
    ELSE 'S3'
END
```

Approximately SQL's answer to a Pandas/NumPy `np.select(...)`.

### Example and output

```python
category = case((User.id == 1, 'first'), else_='other')
print(type(category).__name__)

with Session(engine) as session:
    print([tuple(row) for row in session.execute(select(User.name, category))])
```

```text
Case
[('Ada', 'first'), ('Grace', 'other'), ('Linus', 'other')]
```

## 16. SQL functions

**Object behavior.** `func` dynamically constructs SQL function expressions. Specific built-in functions may be specialized `GenericFunction` subclasses; arbitrary names usually construct `Function`. A function expression is not its returned SQL value.


**Return types** — sqlalchemy.func

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `func.xxx()` | `Function / specialized GenericFunction` | call SQL function |
| `func.count()` | `FunctionElement (often a specialized subclass)` | COUNT |
| `func.sum()` | `FunctionElement (often a specialized subclass)` | SUM |
| `func.avg()` | `FunctionElement (often a specialized subclass)` | AVG |
| `func.min()` | `FunctionElement (often a specialized subclass)` | MIN |
| `func.max()` | `FunctionElement (often a specialized subclass)` | MAX |
| `func.coalesce()` | `FunctionElement (often a specialized subclass)` | COALESCE |
| `func.lower()` | `FunctionElement (often a specialized subclass)` | LOWER |
| `func.upper()` | `FunctionElement (often a specialized subclass)` | UPPER |
| `func.now()` | `FunctionElement (often a specialized subclass)` | current timestamp |
| `func.current_date()` | `FunctionElement (often a specialized subclass)` | current date |
| `func.row_number()` | `FunctionElement (often a specialized subclass)` | ROW_NUMBER |
| `func.rank()` | `FunctionElement (often a specialized subclass)` | RANK |
| `func.dense_rank()` | `FunctionElement (often a specialized subclass)` | DENSE_RANK |

`func` supports user-defined/vendor database functions, not just a fixed catalog:

```python
func.some_database_function(...)
```

### Example and output

```python
expr = func.count(User.id)
print(type(expr).__name__)

with Session(engine) as session:
    print(session.scalar(select(expr)))
```

```text
count
3
```

`count` is a concrete `FunctionElement` subclass. An arbitrary database function such as `func.custom_operation()` typically produces `Function`.

## 17. Aggregation

**Object behavior.** `func.count()` constructs a SQL expression object even before execution. Grouped query results are ordinary `Row` objects (or mappings/scalars after filtering), not Python groupby objects.


**Return types** — func / Select

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `func.count()` | `count (FunctionElement)` | count rows/values |
| `func.sum()` | `FunctionElement` | sum |
| `func.avg()` | `FunctionElement` | average |
| `func.min()` | `FunctionElement` | minimum |
| `func.max()` | `FunctionElement` | maximum |
| `.group_by()` | `Select` | group rows |
| `.having()` | `Select` | filter aggregated groups |

```python
stmt = (
    select(
        Transaction.stage,
        func.count().label('count'),
    )
    .group_by(Transaction.stage)
)
```

### Example and output

```python
stmt = select(Address.city, func.count().label('n')).group_by(Address.city)

with engine.connect() as conn:
    print([tuple(row) for row in conn.execute(stmt).all()])
```

```text
[('Boston', 1), ('Toronto', 2)]
```

`group_by()` modifies a SQL statement; the groups are returned as `Row` values after execution.

## 18. Labels

**Object behavior.** `.label()` produces `Label` (`AS` in SQL). It is still an expression, not a Python string. Its name can be used to retrieve a selected value from a result row.


**Return types** — ColumnElement

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.label()` | `Label` | SQL AS alias |

```python
select(
    func.sum(Transaction.value).label('total_value')
)
```

Then a returned row may expose:

```python
row.total_value
```

### Example and output

```python
expr = func.count().label('number_of_users')
print(type(expr).__name__)

with Session(engine) as session:
    row = session.execute(select(expr).select_from(User)).one()
    print(row.number_of_users)
```

```text
Label
3
```

## 19. CAST / type coercion

**Object behavior.** `cast()` emits SQL CAST and changes SQLAlchemy type handling. `type_coerce()` changes the expression type interpretation without necessarily changing SQL text. `try_cast()` is not universally supported by database dialects.


**Return types** — SQL expression constructor

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `cast()` | `Cast` | SQL CAST |
| `type_coerce()` | `TypeCoerce` | change SQLAlchemy type interpretation without necessarily emitting CAST |
| `try_cast()` | `TryCast` | TRY_CAST where supported |

```python
cast(Transaction.value, Numeric)
```

```text
cast()                       changes SQL expression
type_coerce()                changes SQLAlchemy's type handling
```

`try_cast()` support is dialect-specific.

### Example and output

```python
print(type(cast(User.id, String)).__name__)
print(type(type_coerce(User.id, String)).__name__)
print(type(try_cast(User.id, String)).__name__)
```

```text
Cast
TypeCoerce
TryCast
```

The last line only constructs an expression. Executing `try_cast()` requires a dialect that supports it.

## 20. Literal expressions

**Object behavior.** `literal(10)` is a bound parameter expression (`BindParameter`), while `literal_column("10")` is raw SQL text treated as a column expression. Use bound values for untrusted data.


**Return types** — SQL expression constructor

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `literal()` | `BindParameter` | bound literal value |
| `literal_column()` | `ColumnClause` | literal SQL column expression |
| `text()` | `TextClause` | raw textual SQL |
| `column()` | `ColumnClause` | lightweight column expression |
| `table()` | `TableClause` | lightweight table construct |
| `bindparam()` | `BindParameter` | explicit bind parameter |

```python
literal(10)
literal_column('CURRENT_TIMESTAMP')
text('stage = 1')
bindparam('transaction_id')
```

**Safety:** `text()` and `literal_column()` can embed raw SQL. Never interpolate untrusted input directly; use bound parameters.

### Example and output

```python
print(type(literal(10)).__name__)
print(type(literal_column('CURRENT_TIMESTAMP')).__name__)
print(type(text('SELECT 1')).__name__)
print(type(column('id')).__name__)
print(type(table('users', column('id'))).__name__)
print(type(bindparam('id')).__name__)
```

```text
BindParameter
ColumnClause
TextClause
ColumnClause
TableClause
BindParameter
```

## 21. `text()` — raw SQL escape hatch

**Object behavior.** `text("SELECT ...")` gives a `TextClause`. Adding typed `.columns(...)` converts it to `TextualSelect`, which is a SELECT-like structure and supports operations such as `.subquery()`.


**Return types** — TextClause

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `text()` | `TextClause` | textual SQL statement |
| `.bindparams()` | `TextClause` | bind values |
| `.columns()` | `TextualSelect` | describe returned columns |

```python
stmt = text('''
    SELECT *
    FROM transactions
    WHERE keyid > :keyid
''').bindparams(keyid=100)
```

Useful when the SQL is clearer than the equivalent expression tree.

### Example and output

```python
statement = text('SELECT :value AS amount').bindparams(value=15)
typed = statement.columns(amount=Integer)

print(type(statement).__name__, type(typed).__name__)

with engine.connect() as conn:
    print(conn.execute(typed).scalar_one())
```

```text
TextClause TextualSelect
15
```

## 22. INSERT

**Object behavior.** `insert()` produces an `Insert` statement. `.values()`, `.returning()`, and `.from_select()` remain statements; only executing them contacts the database.


**Return types** — Insert

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `insert()` | `Insert` | construct INSERT |
| `.values()` | `Insert` | specify inserted values |
| `.returning()` | `Insert` | RETURNING clause |
| `.from_select()` | `Insert` | INSERT ... SELECT |
| `.inline()` | `Insert` | inline INSERT behavior |

```python
stmt = insert(Transaction).values(
    keyid=100,
    transaction_type='model_upload',
)
```

Multiple rows:

```python
session.execute(
    insert(Transaction),
    [
        {'keyid': 100},
        {'keyid': 101},
        {'keyid': 102},
    ],
)
```

`insert()`, `update()`, and `delete()` form the Core DML API. `RETURNING` is dialect-dependent.

### Example and output

```python
stmt = insert(User).values(id=4, name='New')
print(type(stmt).__name__)
print(type(stmt.returning(User.id)).__name__)
```

```text
Insert
Insert
```

No database row is inserted until the statement executes.

## 23. UPDATE

**Object behavior.** `update()` produces `Update`. A filter without an index might affect many rows, but the Python return type remains a statement until execution.


**Return types** — Update

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `update()` | `Update` | construct UPDATE |
| `.where()` | `Update` | choose rows |
| `.values()` | `Update` | set values |
| `.returning()` | `Update` | return updated values |

```python
stmt = (
    update(Transaction)
    .where(Transaction.uuid == tx_id)
    .values(is_processed=True)
)
```

### Example and output

```python
stmt = update(User).where(User.id == 1).values(name='Updated')
print(type(stmt).__name__)
print(type(stmt.returning(User.id)).__name__)
```

```text
Update
Update
```

## 24. DELETE

**Object behavior.** `delete()` produces `Delete`. The table and WHERE criteria determine affected rows; committing a transaction is a separate step.


**Return types** — Delete

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `delete()` | `Delete` | construct DELETE |
| `.where()` | `Delete` | choose rows |
| `.returning()` | `Delete` | return deleted values |

```python
stmt = (
    delete(Transaction)
    .where(Transaction.keyid < 100)
)
```

### Example and output

```python
stmt = delete(User).where(User.id == 3)
print(type(stmt).__name__)
print(type(stmt.returning(User.id)).__name__)
```

```text
Delete
Delete
```

## 25. RETURNING

**Object behavior.** `returning()` is a generative method on INSERT/UPDATE/DELETE; it preserves the DML statement kind. When executed on a supporting backend, the result contains returned rows.


**Return types** — DML statement

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.returning()` | `Insert / Update / Delete (same statement kind)` | return rows modified by DML |

```python
stmt = (
    insert(Transaction)
    .values(keyid=100, transaction_type='model_upload')
    .returning(
        Transaction.uuid,
        Transaction.keyid,
    )
)
```

Useful when the database generates IDs, UUIDs, timestamps, sequence numbers and default values. Check dialect support.

### Example and output

```python
stmt = insert(User).values(id=4, name='New').returning(User.id)
print(type(stmt).__name__)

with engine.begin() as conn:
    print(conn.execute(stmt).scalar_one())
```

```text
Insert
4
```

Executing the INSERT adds ID `4`; executing it again without a database reset violates the unique primary key.

## 26. Execution

**Object behavior.** Execution moves from a SQL expression object to an execution result object. `Session.execute()` exposes ORM-aware results; `Connection.execute()` produces Core cursor results. Calling `.scalar()` directly returns a Python value rather than a result iterator.


Core:

**Return types** — Connection / Session

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `Connection.execute()` | `CursorResult` | execute SQL statement |
| `Connection.scalar()` | `Python scalar or None` | execute + return one scalar |
| `Connection.scalars()` | `ScalarResult` | execute + scalar result stream |

ORM:

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `Session.execute()` | `Result` (commonly `ChunkedIteratorResult`) | Execute ORM/Core statement |
| `Session.scalar()` | `Python scalar or None` | Execute and return first-column value |
| `Session.scalars()` | `ScalarResult` | Execute and return scalar-filtering stream |

```python
users = session.scalars(
    select(User)
).all()
```

Legacy alternative (still exists but no longer preferred):

```python
session.query(User).all()
```

### Example and output

```python
with engine.connect() as conn:
    result = conn.execute(select(User.__table__.c.id))
    print(type(result).__name__)
    print(type(result.scalars()).__name__)

with Session(engine) as session:
    result = session.execute(select(User))
    print(type(result).__name__)
    print(type(session.scalars(select(User))).__name__)
```

```text
CursorResult
ScalarResult
ChunkedIteratorResult
ScalarResult
```

`ChunkedIteratorResult` is a common ORM implementation class; program against the `Result` interface rather than relying on that concrete implementation name.

## 27. `Result` methods

**Object behavior.** `Result` is an iterator-like database result abstraction. `.all()` materializes rows; `.scalars()` changes the *view* to the first selected element per row; `.mappings()` changes it to `RowMapping`. `Result.tuples()` is deprecated as of SQLAlchemy 2.1 and does not create plain Python tuple objects at runtime.


**Return types** — Result

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.all()` | `Sequence[Row]` | all rows |
| `.first()` | `Row or None` | first row or None |
| `.one()` | `Row` | exactly one row; otherwise error |
| `.one_or_none()` | `Row or None` | one row or None; error if multiple |
| `.scalar()` | `Python scalar or None` | first column of first row |
| `.scalar_one()` | `Python scalar` | exactly one scalar |
| `.scalar_one_or_none()` | `Python scalar or None` | one scalar or None |
| `.scalars()` | `ScalarResult` | Row results → scalar objects |
| `.mappings()` | `MappingResult` | Row results → mapping/dict-like objects |
| `.tuples()` | `Result (same object at runtime)` | typed tuple-style results |
| `.unique()` | `Result` | remove ORM duplicate entities / rows by strategy |
| `.partitions()` | `Iterator[list[Row]]` | consume results in batches |
| `.fetchmany()` | `Sequence[Row]` | fetch n rows |
| `.fetchall()` | `Sequence[Row]` | all rows |
| `.keys()` | `RMKeyView` | result column names |

`Result.first()` does **not** automatically add a SQL `LIMIT 1` to the statement.

### Example and output

```python
with Session(engine) as session:
    result = session.execute(select(User.id, User.name))
    print(type(result).__name__)
    print(type(result.first()).__name__)

    values = session.execute(select(User.id)).scalars().all()
    print(values)

    mappings = session.execute(select(User.id, User.name)).mappings().all()
    print(type(mappings[0]).__name__)
    print(dict(mappings[0]))
```

```text
ChunkedIteratorResult
Row
[1, 2, 3]
RowMapping
{'id': 1, 'name': 'Ada'}
```

A consumed `Result` cannot be reread. Use a new execution to obtain a fresh result.

## 28. Result shape mental model

**Object behavior.** `Row` behaves like a tuple but is a SQLAlchemy class. `RowMapping` provides mapping semantics through `.mappings()` or `row._mapping`. ORM `select(User)` results contain `User` instances *inside* `Row` objects until `.scalars()` removes the row layer.


**Return types** — Result family

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `execute()` | `Result / CursorResult` | Result[Row] |
| `scalars()` | `ScalarResult` | ScalarResult[T] |
| `mappings()` | `MappingResult` | MappingResult |
| `tuples()` | `Result (typing view; deprecated in 2.1)` | tuple-oriented Result |

```python
result = session.execute(
    select(User.id, User.name)
)
rows = result.all()
```

Returns row objects. But:

```python
users = session.scalars(select(User)).all()
```

returns:

```text
[User, User, User, ...]
```

### Example and output

```python
with Session(engine) as session:
    row = session.execute(select(User.id, User.name)).first()
    print(type(row).__name__)
    print(tuple(row))
    print(type(row._mapping).__name__)
    print(dict(row._mapping))
```

```text
Row
(1, 'Ada')
RowMapping
{'id': 1, 'name': 'Ada'}
```

## 29. `scalar()` vs `scalars()`

**Object behavior.** `Session.scalar(stmt)` and `Result.scalar()` return one value (or `None`); `Session.scalars(stmt)` and `Result.scalars()` return a `ScalarResult` object that may yield multiple values.


**Return types** — Session / Result

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `scalar()` | `Python scalar or None` | one scalar result |
| `scalars()` | `ScalarResult` | stream/list of scalar results |

```python
count = session.scalar(
    select(func.count(Transaction.id))
)
```

Versus:

```python
transactions = session.scalars(
    select(Transaction)
).all()
```

### Example and output

```python
with Session(engine) as session:
    value = session.scalar(select(func.count(User.id)))
    stream = session.scalars(select(User.name))
    print(value, type(value).__name__)
    print(type(stream).__name__, stream.all())
```

```text
3 int
ScalarResult ['Ada', 'Grace', 'Linus']
```

## 30. Session — object persistence

**Object behavior.** `Session.add()` mutates Session state and returns `None`. `Session.merge(obj)` instead returns a managed model instance, which may be different from the source object.


**Return types** — Session

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `Session.add()` | `None` | attach/add one object |
| `Session.add_all()` | `None` | add multiple objects |
| `Session.merge()` | `Mapped model instance` | merge detached state into Session |
| `Session.delete()` | `None` | mark object for deletion |

```python
tx = Transaction(...)
session.add(tx)
```

`merge()` returns the local persistent instance; it does not necessarily attach the original detached instance.

### Example and output

```python
with Session(engine) as session:
    user = User(id=99, name='Temporary')
    print(session.add(user))
    print(inspect(user).pending)
    session.rollback()
```

```text
None
True
```

`session.merge(detached_user)` returns a managed `User`, unlike `session.add(...)`.

## 31. Session — flushing / committing

**Object behavior.** `flush()` emits pending SQL in the current transaction; `commit()` finalizes the transaction. All of these Session methods return `None`.


**Return types** — Session

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.flush()` | `None` | push pending SQL to DB without ending transaction |
| `.commit()` | `None` | commit transaction |
| `.rollback()` | `None` | roll back transaction |

```text
flush()                      synchronize ORM → database transaction
commit()                     permanently commit transaction
```

A flush issues pending INSERT/UPDATE/DELETE according to ORM unit-of-work ordering, but changes can still be rolled back.

```python
session.add(tx)
session.flush()  # generated PK may now be populated
session.commit()
```

### Example and output

```python
with Session(engine) as session:
    user = User(name='New')
    session.add(user)
    print(session.flush())
    print(user.id is not None)
    print(session.rollback())
```

```text
None
True
None
```

The `flush()` assigned a primary key inside the transaction; `rollback()` undoes the insert.

## 32. Session — retrieving by primary key

**Object behavior.** `Session.get()` looks up a mapped entity by primary key and may use the identity map without executing SQL. `Session.get_one()` raises `NoResultFound` if absent.


**Return types** — Session

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.get()` | `Mapped model instance or None` | primary-key lookup |
| `.get_one()` | `Mapped model instance` | primary-key lookup; require existence |

```python
tx = session.get(Transaction, tx_id)
```

Prefer for PK lookups over:

```python
session.scalars(
    select(Transaction).where(Transaction.id == tx_id)
).first()
```

`get()` can use the Session's identity map and may avoid issuing SQL when the object is already loaded and unexpired.

### Example and output

```python
with Session(engine) as session:
    user = session.get(User, 1)
    missing = session.get(User, 500)
    print(type(user).__name__, user.name)
    print(missing)
```

```text
User Ada
None
```

## 33. Session — refresh / expiration

**Object behavior.** `refresh()` performs an immediate reload while `expire()` marks an object for lazy reload. Both operate on ORM state and return `None`.


**Return types** — Session

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.refresh()` | `None` | immediately reload object from DB |
| `.expire()` | `None` | mark object's attributes stale |
| `.expire_all()` | `None` | expire every persistent object |

```text
refresh()                    reload NOW
expire()                     reload NEXT TIME attribute is accessed
```

```python
session.refresh(tx)
session.expire(tx, ['status'])
```

SQLAlchemy's normal expiration rules depend on transaction boundaries and Session configuration (notably `expire_on_commit`).

### Example and output

```python
with Session(engine) as session:
    user = session.get(User, 1)
    print(session.expire(user, ['name']))
    print('name' in inspect(user).expired_attributes)
    print(session.refresh(user))
    print(user.name)
```

```text
None
True
None
Ada
```

## 34. Session — detaching objects

**Object behavior.** Detaching an ORM object affects its Session association. It does not delete the corresponding database row. Unloaded attributes on detached objects may not be accessible without another Session.


**Return types** — Session

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.expunge()` | `None` | detach one object from Session |
| `.expunge_all()` | `None` | detach all objects |

```text
transient
pending
persistent
deleted
detached
```

These are the major ORM object states.

### Example and output

```python
with Session(engine) as session:
    user = session.get(User, 1)
    print(inspect(user).persistent)
    session.expunge(user)
    print(inspect(user).detached)
```

```text
True
True
```

## 35. Session transactions

**Object behavior.** `Session.begin()` and `begin_nested()` give `SessionTransaction` context managers. `Session.in_transaction()` returns a Python `bool`; it does not inspect database transaction content.


**Return types** — Session

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.begin()` | `SessionTransaction` | begin transaction |
| `.begin_nested()` | `SessionTransaction` | begin SAVEPOINT / nested transaction |
| `.commit()` | `None` | COMMIT |
| `.rollback()` | `None` | ROLLBACK |
| `.in_transaction()` | `bool` | transaction active? |
| `.in_nested_transaction()` | `bool` | nested transaction active? |
| `.get_transaction()` | `SessionTransaction or None` | current transaction |
| `.get_nested_transaction()` | `SessionTransaction or None` | current nested transaction |

```python
with Session(engine) as session:
    with session.begin():
        ...
```

Or:

```python
with Session(engine) as session, session.begin():
    ...
```

### Example and output

```python
with Session(engine) as session:
    print(session.in_transaction())
    with session.begin():
        print(type(session.get_transaction()).__name__)
        print(session.in_transaction())
    print(session.in_transaction())
```

```text
False
SessionTransaction
True
False
```

## 36. Session execution controls

**Object behavior.** In SQLAlchemy 2.1, `execution_options` is a **Session constructor parameter**, not a general `Session.execution_options()` method. `Session.get_bind()` returns the `Engine` or `Connection` used to execute SQL.


**Return types** — Session configuration / property

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `execution_options=` | `Configuration dictionary / option on Session(...) (2.1+)` | Default execution behavior for a Session |
| `.no_autoflush` | `Context manager` | temporarily disable autoflush |
| `.autoflush` | `bool (attribute)` | Session autoflush configuration |
| `.get_bind()` | `Engine or Connection` | retrieve Engine/Connection being used |

```python
with session.no_autoflush:
    # populate related objects before autoflush would run
    ...
```

In SQLAlchemy 2.1, `Session(execution_options={...})` configures options at session construction. Statements may use `.execution_options(...)`, and `Session.execute(..., execution_options={...})` provides per-execution overrides.

### Example and output

```python
with Session(engine, autoflush=False) as session:
    print(session.autoflush)
    print(type(session.get_bind()).__name__)
```

```text
False
Engine
```

In SQLAlchemy 2.1, session-wide options are set with `Session(engine, execution_options={...})`. They are not set using `session.execution_options(...)`.

## 37. ORM model declaration

**Object behavior.** `Mapped[T]` is a typing form, not a runtime field object. `mapped_column()` constructs declarative column configuration; after mapping, accessing the attribute on the model class yields an `InstrumentedAttribute`.


**Return types** — ORM declarative definition

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `DeclarativeBase` | `Class (user-defined subclass of DeclarativeBase)` | declarative base class |
| `Mapped[...]` | `Type annotation, not a constructor` | type annotation for mapped attribute |
| `mapped_column()` | `MappedColumn` | map database column |
| `relationship()` | `RelationshipProperty; mapped attribute becomes InstrumentedAttribute` | map relationship |
| `__tablename__` | `str (attribute)` | database table name |
| `__table__` | `Table (attribute)` | mapped Table object |
| `__mapper__` | `Mapper (attribute)` | Mapper for class |

```python
class Transaction(Base):
    __tablename__ = 'transaction'
    id: Mapped[int] = mapped_column(primary_key=True)
```

Typical imports:

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass
```

### Example and output

```python
print(type(User.__table__).__name__)
print(type(User.__mapper__).__name__)
print(type(User.name).__name__)
print(type(User(id=10, name='X').name).__name__)
```

```text
Table
Mapper
InstrumentedAttribute
str
```

## 38. `mapped_column()`

**Object behavior.** `mapped_column()` constructs a `MappedColumn` (used during declarative mapping). Flags such as `nullable`, `unique`, and `index` are keyword arguments, not methods with return values.


**Return types** — mapped_column arguments

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `primary_key=True` | `Configuration argument` | primary key |
| `nullable=False` | `Configuration argument` | NOT NULL |
| `unique=True` | `Configuration argument` | UNIQUE |
| `index=True` | `Configuration argument` | create index |
| `default=` | `Configuration argument` | Python-side / SQLAlchemy-side default |
| `server_default=` | `Configuration argument` | database-side default |
| `onupdate=` | `Configuration argument` | Python update default |
| `server_onupdate=` | `Configuration argument` | server update behavior / fetched marker |
| `ForeignKey(...)` | `ForeignKey` | foreign key |

```python
id: Mapped[int] = mapped_column(primary_key=True)
created_at: Mapped[datetime] = mapped_column(server_default=func.now())
user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
```

`server_onupdate` is not a portable instruction to generate every backend's server-side ON UPDATE syntax by itself.

### Example and output

```python
field = mapped_column(Integer, primary_key=True)
print(type(field).__name__)
print(type(User.__table__.c.id).__name__)
```

```text
MappedColumn
Column
```

The first is a declarative-mapping construct; the second is the actual schema `Column`.

## 39. Relationships

**Object behavior.** `relationship()` configures a `RelationshipProperty`. After class mapping, the class exposes an `InstrumentedAttribute`; an instance relationship typically yields a mapped instance or a collection, depending on `uselist`.


**Return types** — relationship arguments

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `relationship()` | `RelationshipProperty / InstrumentedAttribute` | ORM relationship |
| `back_populates=` | `Configuration argument` | explicit bidirectional relationship |
| `secondary=` | `Configuration argument` | many-to-many association table |
| `cascade=` | `Configuration argument` | persistence cascade rules |
| `lazy=` | `Configuration argument` | relationship loading strategy |
| `uselist=` | `Configuration argument` | scalar vs collection |
| `viewonly=` | `Configuration argument` | relationship not used for persistence |
| `primaryjoin=` | `Configuration argument` | custom join condition |
| `secondaryjoin=` | `Configuration argument` | custom secondary join condition |
| `foreign_keys=` | `Configuration argument` | explicitly identify FK columns |
| `order_by=` | `Configuration argument` | ordering of related collection |

```python
class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    addresses: Mapped[list['Address']] = relationship(back_populates='user')
```

### Example and output

```python
print(type(User.addresses).__name__)

with Session(engine) as session:
    user = session.get(User, 1)
    print(type(user.addresses).__name__)
    print([address.city for address in user.addresses])
```

```text
InstrumentedAttribute
InstrumentedList
['Toronto', 'Toronto']
```

## 40. Relationship query operators

**Object behavior.** Relationship `.any()` and `.has()` construct correlated EXISTS predicates. They are SQL expressions, not booleans produced by inspecting loaded collections in Python.


**Return types** — RelationshipProperty comparator

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.any()` | `Exists` | collection contains matching row |
| `.has()` | `Exists` | scalar relationship matches condition |
| `.contains()` | `BinaryExpression` | collection contains object |
| `.of_type()` | `QueryableAttribute` | relationship against alias/subclass |

```python
select(User).where(
    User.addresses.any(
        Address.city == 'Toronto'
    )
)
```

This produces EXISTS-style filtering; `.has()` is the scalar relationship counterpart.

### Example and output

```python
predicate = User.addresses.any(Address.city == 'Toronto')
print(type(predicate).__name__)

with Session(engine) as session:
    print(session.scalars(select(User.name).where(predicate)).all())
```

```text
Exists
['Ada']
```

## 41. Relationship loading

**Object behavior.** Loader helpers return `Load` options, which modify how an ORM statement executes; they do not fetch data by themselves. With joined eager-loading collections, `.unique()` is normally required on the result.


**Return types** — ORM loader strategy

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `selectinload()` | `Load` | eager load with second SELECT |
| `joinedload()` | `Load` | eager load using JOIN |
| `subqueryload()` | `Load` | eager load via subquery |
| `lazyload()` | `Load` | force lazy loading |
| `immediateload()` | `Load` | immediate per-attribute SELECT |
| `noload()` | `Load (deprecated)` | don't load relationship (legacy/deprecated) |
| `raiseload()` | `Load` | error if lazy SQL would occur |
| `contains_eager()` | `Load` | populate relationship from your own JOIN |
| `defaultload()` | `Load` | continue loader path without changing strategy |

`selectinload()` is generally a straightforward eager strategy for collections (one-to-many), while `joinedload()` often works well for many-to-one relationships.

```python
stmt = select(User).options(selectinload(User.addresses))
users = session.scalars(stmt).all()
```

**Important:** if using `joinedload()` for a collection, ORM results normally need `.unique()`:

```python
users = session.scalars(
    select(User).options(joinedload(User.addresses))
).unique().all()
```

`noload()` is deprecated in recent SQLAlchemy 2.x and should not be the default for new code.

### Example and output

```python
option = selectinload(User.addresses)
stmt = select(User).options(option)
print(type(option).__name__, type(stmt).__name__)

with Session(engine) as session:
    print([(u.name, len(u.addresses)) for u in session.scalars(stmt)])
```

```text
Load Select
[('Ada', 2), ('Grace', 1), ('Linus', 0)]
```

## 42. Column loading controls

**Object behavior.** Column loader functions return `Load` options. They affect fetched ORM attributes, not the class of the enclosing `Select`.


**Return types** — ORM column loader strategy

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `load_only()` | `Load` | load only selected columns |
| `defer()` | `Load` | defer loading column |
| `undefer()` | `Load` | explicitly load deferred column |
| `undefer_group()` | `Load` | load deferred column group |
| `with_expression()` | `Load` | populate mapped expression dynamically |

```python
select(Transaction).options(
    load_only(
        Transaction.uuid,
        Transaction.keyid,
    )
)
```

Useful for large tables where only a handful of columns are required. Primary-key columns needed for ORM identity remain present.

### Example and output

```python
option = load_only(User.id, User.name)
print(type(option).__name__)
print(type(select(User).options(option)).__name__)
```

```text
Load
Select
```

## 43. `.options()`

**Object behavior.** `Select.options()` returns another `Select`. Loader options change ORM loading behavior but do not transform the query into a Result.


**Return types** — Select

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.options()` | `Select (generative)` | attach ORM loading/query options |

```python
stmt = (
    select(Transaction)
    .options(
        selectinload(Transaction.items),
        load_only(
            Transaction.uuid,
            Transaction.keyid,
        ),
    )
)
```

Loader options are part of SQLAlchemy's ORM `Load` system.

### Example and output

```python
base = select(User)
configured = base.options(selectinload(User.addresses))
print(type(configured).__name__)
print(base is configured)
```

```text
Select
False
```

## 44. Global ORM filtering

**Object behavior.** `with_loader_criteria()` builds a `LoaderCriteriaOption`; it is attached through `.options()` and may affect applicable relationship loads.


**Return types** — ORM loader criteria

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `with_loader_criteria()` | `LoaderCriteriaOption` | apply criteria everywhere an entity loads |

```python
select(Transaction).options(
    with_loader_criteria(
        TransactionItem,
        TransactionItem.is_active == True,
    )
)
```

For SQL boolean columns, `.is_(True)` expresses `IS TRUE` explicitly. Common use cases:

```text
soft deletes
tenant filtering
security scopes
effective-date filtering
active-record filtering
```

Criteria propagation and enforcement depend on loader options and your query/session design; don't treat it as a standalone security boundary without testing.

### Example and output

```python
option = with_loader_criteria(Address, Address.city == 'Toronto')
print(type(option).__name__)
```

```text
LoaderCriteriaOption
```

## 45. ORM aliases

**Object behavior.** `aliased(User)` produces an ORM `AliasedClass`, which is distinct from a Core `Alias`. It preserves model-oriented attribute access for joins and filters.


**Return types** — sqlalchemy.orm.aliased

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `aliased()` | `AliasedClass` | create ORM alias |

```python
Parent = aliased(Hierarchy)
Child = aliased(Hierarchy)
stmt = (
    select(Parent, Child)
    .join(
        Child,
        Child.parent_id == Parent.id,
    )
)
```

Useful for self-joins and repeated use of one mapped entity in a statement.

### Example and output

```python
Parent = aliased(User)
print(type(Parent).__name__)
print(type(Parent.id).__name__)
print(type(select(Parent)).__name__)
```

```text
AliasedClass
InstrumentedAttribute
Select
```

## 46. SQL window functions

**Object behavior.** `.over()` returns `Over`, a SQL expression representing a window operation. Its `partition_by`, `order_by`, and frame parameters are arguments, not methods.


**Return types** — FunctionElement.over()

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.over()` | `Over` | apply OVER clause |
| `partition_by=` | `Argument: expression(s)` | PARTITION BY |
| `order_by=` | `Argument: expression(s)` | window ordering |
| `rows=` | `Argument: 2-tuple` | ROWS frame |
| `range_=` | `Argument: 2-tuple` | RANGE frame |

```python
func.row_number().over(
    partition_by=Transaction.division,
    order_by=Transaction.keyid,
)
```

These are SQL equivalents for many Pandas `groupby().cumcount()`, `groupby().rank()` and `groupby().transform()` use cases. `partition_by`, `order_by`, `rows`, and `range_` are arguments to `over()`, not freestanding methods.

### Example and output

```python
expr = func.row_number().over(order_by=User.id)
print(type(expr).__name__)

with Session(engine) as session:
    print([tuple(row) for row in session.execute(select(User.name, expr))])
```

```text
Over
[('Ada', 1), ('Grace', 2), ('Linus', 3)]
```

## 47. Useful window functions

**Object behavior.** `func.lag(...)` creates a function expression; `.over(...)` produces `Over`. `LAG` accesses the previous row in the window ordering, not necessarily the prior calendar period.


**Return types** — SQL function / Over

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `func.row_number()` | `FunctionElement` | ROW_NUMBER |
| `func.rank()` | `FunctionElement` | RANK |
| `func.dense_rank()` | `FunctionElement` | DENSE_RANK |
| `func.lag()` | `FunctionElement` | previous row |
| `func.lead()` | `FunctionElement` | following row |
| `func.first_value()` | `FunctionElement` | first window value |
| `func.last_value()` | `FunctionElement` | last window value |
| `func.sum().over()` | `Over` | cumulative/window sum |
| `func.avg().over()` | `Over` | window average |

For month-dependent calculations:

```python
func.lag(Transaction.value).over(
    partition_by=[
        Transaction.hierarchy_id,
        Transaction.measure_type,
    ],
    order_by=Transaction.month_date,
)
```

A `lag()` observes the previous **row** in the ordered partition; to require the **previous calendar month**, gaps in the month sequence must be handled explicitly.

### Example and output

```python
previous_id = func.lag(User.id).over(order_by=User.id)
print(type(previous_id).__name__)

with Session(engine) as session:
    print([tuple(row) for row in session.execute(select(User.id, previous_id))])
```

```text
Over
[(1, None), (2, 1), (3, 2)]
```

## 48. Ordering helpers

**Object behavior.** Ordering helpers produce `UnaryExpression` objects, which you can pass to `.order_by()`. Calling `.desc()` never sorts Python data locally.


**Return types** — ColumnElement

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.asc()` | `UnaryExpression` | ascending |
| `.desc()` | `UnaryExpression` | descending |
| `.nulls_first()` | `UnaryExpression` | NULL first |
| `.nulls_last()` | `UnaryExpression` | NULL last |

```python
Transaction.keyid.desc()
Transaction.month_date.asc().nulls_last()
```

Null-ordering syntax/support can vary by dialect.

### Example and output

```python
expr = User.name.desc()
print(type(expr).__name__)

with Session(engine) as session:
    print(session.scalars(select(User.name).order_by(expr)).all())
```

```text
UnaryExpression
['Linus', 'Grace', 'Ada']
```

## 49. Distinct

**Object behavior.** `Select.distinct()` returns `Select`; `distinct(column)` produces `UnaryExpression` for use as one column argument. Their semantics and positions in the expression tree differ.


**Return types** — Select / expression

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.distinct()` | `Select` | SELECT DISTINCT |
| `distinct()` | `UnaryExpression` | DISTINCT expression |

```python
select(
    Transaction.hierarchy_id,
    Transaction.stage,
    Transaction.currency,
).distinct()
```

Useful for retrieving only the unique data-point keys your pipeline should process.

### Example and output

```python
stmt = select(Address.city).distinct()
expr = distinct(Address.city)
print(type(stmt).__name__, type(expr).__name__)

with Session(engine) as session:
    print(session.scalars(stmt.order_by(Address.city)).all())
```

```text
Select UnaryExpression
['Boston', 'Toronto']
```

## 50. Tuple comparisons

**Object behavior.** `tuple_()` constructs a SQL `Tuple` expression, often for composite `IN` comparisons. Backend support varies.


**Return types** — sqlalchemy.tuple_

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `tuple_()` | `Tuple` | SQL row/tuple expression |

```python
tuple_(
    Transaction.hierarchy_id,
    Transaction.stage,
).in_([
    (100, 1),
    (101, 2),
])
```

SQL concept:

```sql
WHERE (hierarchy_id, stage)
IN ((100, 1), (101, 2))
```

Very helpful for composite/multicolumn keys; tuple IN support differs across databases.

### Example and output

```python
expr = tuple_(User.id, User.name)
print(type(expr).__name__)

with Session(engine) as session:
    print(session.scalars(select(User.name).where(expr.in_([(1, 'Ada'), (3, 'Linus')]))).all())
```

```text
Tuple
['Ada', 'Linus']
```

## 51. Arithmetic expressions

**Object behavior.** Overloaded numeric operators produce SQL expressions (usually `BinaryExpression`). Database precision/type behavior is independent of Python arithmetic on materialized values.


**Return types** — ColumnElement

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `+` | `ColumnElement (usually BinaryExpression)` | addition |
| `-` | `ColumnElement (usually BinaryExpression)` | subtraction |
| `*` | `ColumnElement (usually BinaryExpression)` | multiplication |
| `/` | `ColumnElement (usually BinaryExpression)` | division |
| `%` | `ColumnElement (usually BinaryExpression)` | modulo |

```python
select(
    (
        Transaction.amount *
        Transaction.fx_rate
    ).label('converted_amount')
)
```

Be conscious of SQL type/precision semantics: numeric arithmetic is compiled and evaluated by the database.

### Example and output

```python
expr = User.id * 10 + 1
print(type(expr).__name__)

with Session(engine) as session:
    print(session.scalars(select(expr).order_by(User.id)).all())
```

```text
BinaryExpression
[11, 21, 31]
```

## 52. Metadata

**Object behavior.** A `MetaData` object records tables/schema structures. `create_all`, `drop_all`, and `reflect` change the database and/or metadata registry but return `None`.


**Return types** — MetaData

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `MetaData()` | `MetaData` | registry of schema objects |
| `.create_all()` | `None` | create all registered tables |
| `.drop_all()` | `None` | drop registered tables |
| `.reflect()` | `None` | load database schema into MetaData |
| `.tables` | `FacadeDict[str, Table]` | dictionary of tables |
| `.sorted_tables` | `list[Table]` | dependency-sorted Tables |

```python
metadata = MetaData()
metadata.reflect(bind=engine)
```

Do not use `create_all()` as a substitute for production schema migrations (e.g., Alembic) when existing schemas must be changed.

### Example and output

```python
metadata = MetaData()
print(type(metadata).__name__)
print(metadata.create_all(engine))
print(type(metadata.tables).__name__)
```

```text
MetaData
None
FacadeDict
```

The empty metadata registry creates no tables here.

## 53. Table

**Object behavior.** A `Table` is a schema object and also a `FromClause`. Its `.c` column collection holds `Column` objects, not data values. The corresponding ORM class attribute is usually an `InstrumentedAttribute`.


**Return types** — Table

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `Table()` | `Table` | define Core table |
| `.c` | `ReadOnlyColumnCollection` | column collection |
| `.columns` | `ReadOnlyColumnCollection` | column collection |
| `.primary_key` | `PrimaryKeyConstraint` | PK constraint |
| `.foreign_keys` | `set[ForeignKey]` | foreign-key set |
| `.constraints` | `set[Constraint]` | table constraints |
| `.indexes` | `set[Index]` | table indexes |

Core:

```python
transaction.c.keyid
```

ORM:

```python
Transaction.keyid
```

### Example and output

```python
core_table = User.__table__
print(type(core_table).__name__)
print(type(core_table.c).__name__)
print(type(core_table.c.name).__name__)
print([c.name for c in core_table.columns])
```

```text
Table
ReadOnlyColumnCollection
Column
['id', 'name']
```

## 54. Table convenience methods

**Object behavior.** A `Table.select()` produces a `Select`, whereas a `Table.join()` produces a `Join`. This is useful when selecting an abstraction/interface based on which methods the result must support.


**Return types** — Table

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `table.select()` | `Select` | SELECT table |
| `table.insert()` | `Insert` | INSERT table |
| `table.update()` | `Update` | UPDATE table |
| `table.delete()` | `Delete` | DELETE table |
| `table.join()` | `Join` | JOIN |
| `table.outerjoin()` | `Join` | LEFT OUTER JOIN |
| `table.alias()` | `Alias` | alias table |

```python
transaction_table.select().where(
    transaction_table.c.keyid > 100
)
```

### Example and output

```python
core = User.__table__
print(type(core.select()).__name__)
print(type(core.insert()).__name__)
print(type(core.update()).__name__)
print(type(core.delete()).__name__)
print(type(core.join(Address.__table__)).__name__)
```

```text
Select
Insert
Update
Delete
Join
```

## 55. Schema constraints

**Object behavior.** Constraint and Index constructors build schema metadata objects. They are not database result rows and are typically attached to Tables/MetaData before DDL execution.


**Return types** — SQL schema objects

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `PrimaryKeyConstraint()` | `PrimaryKeyConstraint` | composite/custom PK |
| `ForeignKey()` | `ForeignKey` | column-level FK |
| `ForeignKeyConstraint()` | `ForeignKeyConstraint` | table-level/composite FK |
| `UniqueConstraint()` | `UniqueConstraint` | UNIQUE constraint |
| `CheckConstraint()` | `CheckConstraint` | CHECK constraint |
| `Index()` | `Index` | database index |

```python
UniqueConstraint('keyid', 'stage', 'month_date', name='uq_tx_point')
```

### Example and output

```python
print(type(UniqueConstraint('name')).__name__)
print(type(Index('idx_user_name', User.__table__.c.name)).__name__)
print(type(ForeignKey('user.id')).__name__)
```

```text
UniqueConstraint
Index
ForeignKey
```

## 56. Database reflection

**Object behavior.** `inspect(engine)` returns an `Inspector`, distinct from inspecting a mapped ORM object or a mapped class. Inspector methods return Python lists/dicts describing schema, not SQL expression objects.


**Return types** — Inspector / reflection

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `MetaData.reflect()` | `None` | reflect many tables |
| `Table(..., autoload_with=)` | `Table` | reflect one table |
| `inspect(engine)` | `Inspector` | obtain Inspector |

| `Inspector` method | Python return type | Value |
|---|---|---|
| `get_table_names()` | `list[str]` | Table names |
| `get_view_names()` | `list[str]` | View names |
| `get_columns(table)` | `list[dict[str, Any]]` | Column metadata |
| `get_pk_constraint(table)` | `dict[str, Any]` | Primary-key metadata |
| `get_foreign_keys(table)` | `list[dict[str, Any]]` | Foreign keys |
| `get_indexes(table)` | `list[dict[str, Any]]` | Indexes |
| `get_unique_constraints(table)` | `list[dict[str, Any]]` | Unique constraints |
| `get_check_constraints(table)` | `list[dict[str, Any]]` | Check constraints |
| `get_schema_names()` | `list[str]` | Schemas |
| `has_table(table)` | `bool` | Whether the table or view exists |
| `has_index(table, index_name)` | `bool` | Whether an index exists |

```python
inspector = inspect(engine)
inspector.get_table_names()
inspector.get_columns('transaction')
```

The `Inspector` supplies backend-independent schema-introspection methods, to the extent the dialect supports each one.

### Example and output

```python
inspector = inspect(engine)
print(type(inspector).__name__)
print(type(inspector.get_table_names()).__name__)
print(type(inspector.get_columns('user')).__name__)
print(inspector.has_table('user'))
```

```text
Inspector
list
list
True
```

`get_columns()` returns dictionaries describing column names, SQL types, nullability, defaults, etc.

## 57. Engine

**Object behavior.** `create_engine()` creates an `Engine` that manages database connectivity. `engine.connect()` returns `Connection`; `engine.begin()` is a context manager that yields a `Connection` inside a transaction.


**Return types** — Engine

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `create_engine()` | `Engine` | create Engine |
| `engine.connect()` | `Connection` | obtain Connection |
| `engine.begin()` | `Context manager yielding Connection` | Connection + transaction context |
| `engine.dispose()` | `None` | dispose connection pool |

```python
with engine.connect() as conn:
    result = conn.execute(stmt)
```

Or:

```python
with engine.begin() as conn:
    conn.execute(stmt)
```

`engine.begin()` scopes both connection and transaction, committing on success and rolling back on exceptions.

### Example and output

```python
print(type(engine).__name__)
with engine.begin() as conn:
    print(type(conn).__name__)
    print(conn.scalar(select(func.count()).select_from(User.__table__)))
```

```text
Engine
Connection
3
```

## 58. Connection

**Object behavior.** `Connection.execute()` returns `CursorResult` for standard synchronous Core executions. `Connection.execution_options()` returns that same `Connection` in SQLAlchemy 2.x; setting its options is not a generative statement transformation.


**Return types** — Connection

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.execute()` | `CursorResult` | execute statement |
| `.scalar()` | `Python scalar or None` | execute and return scalar |
| `.scalars()` | `ScalarResult` | execute and return scalar stream |
| `.begin()` | `RootTransaction` | transaction |
| `.begin_nested()` | `NestedTransaction` | SAVEPOINT |
| `.commit()` | `None` | commit |
| `.rollback()` | `None` | rollback |
| `.close()` | `None` | return connection to pool |
| `.execution_options()` | `Connection (same object in 2.x)` | execution configuration |

```python
with engine.begin() as conn:
    conn.execute(insert(transaction_table), rows)
```

### Example and output

```python
with engine.connect() as conn:
    stmt = select(User.__table__.c.name).order_by(User.__table__.c.id)
    result = conn.execute(stmt)
    print(type(result).__name__)
    print(result.scalars().all())
    print(conn.execution_options(stream_results=True) is conn)
```

```text
CursorResult
['Ada', 'Grace', 'Linus']
True
```

## 59. Compiling SQL

**Object behavior.** `.compile()` gives a `Compiled` object (often a dialect-specific `SQLCompiler`). `str(compiled)` displays SQL text, while `.params` contains bound values.


**Return types** — ClauseElement

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.compile()` | `Compiled (often SQLCompiler)` | compile statement to SQL representation |

```python
print(stmt.compile())
```

Display embedded literal binds for **diagnostics**:

```python
print(
    stmt.compile(
        compile_kwargs={'literal_binds': True}
    )
)
```

Not every bound value/type supports literal rendering; don't use this compilation option as a safe substitute for parameterized SQL execution.

### Example and output

```python
stmt = select(User.id).where(User.id == 2)
compiled = stmt.compile()
print(type(compiled).__name__)
print(compiled.params)
```

```text
StrSQLCompiler
{'id_1': 2}
```

The compiler class name depends on dialect. `compiled.params` contains the Python parameter values; the SQL string contains bind markers.

## 60. ORM state inspection

**Object behavior.** `inspect(instance)` returns `InstanceState`; this is distinct from `inspect(Model)` (`Mapper`) and `inspect(engine)` (`Inspector`). The state flags themselves are Python booleans.


**Return types** — ORM instance inspection

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `inspect(obj)` | `InstanceState` | get InstanceState |
| `inspect(obj).transient` | `bool` | not in Session / DB |
| `inspect(obj).pending` | `bool` | added but not flushed |
| `inspect(obj).persistent` | `bool` | persistent in Session |
| `inspect(obj).deleted` | `bool` | marked deleted (after flush) |
| `inspect(obj).detached` | `bool` | detached |

Also:

| Property | Class / type | Meaning |
|---|---|---|
| `inspect(obj).attrs` | `ReadOnlyProperties[AttributeState]` | ORM attribute state mapping |
| `inspect(obj).attrs.name` | `AttributeState` | One mapped-attribute state |
| `inspect(obj).attrs.name.history` | `History` | Added/unchanged/deleted history |
| `inspect(obj).attrs.name.loaded_value` | Python value or `LoaderCallableStatus.NO_VALUE` | Value without triggering loading |

```python
state = inspect(tx)
print(state.persistent, state.detached)
print(state.attrs.status.history)
```

### Example and output

```python
with Session(engine) as session:
    user = session.get(User, 1)
    state = inspect(user)
    print(type(state).__name__)
    print(state.persistent, state.detached)
    print(type(state.attrs.name.history).__name__)
```

```text
InstanceState
True False
History
```

## 61. Mapper inspection

**Object behavior.** A mapped ORM class has an inspection `Mapper` with metadata about primary keys, properties, and relationships. Inspecting these does not fetch user rows.


**Return types** — ORM class inspection

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `inspect(Model)` | `Mapper` | retrieve Mapper |
| `mapper.columns` | `ColumnCollection` | mapped columns |
| `mapper.relationships` | `ReadOnlyProperties[RelationshipProperty]` | relationships |
| `mapper.primary_key` | `tuple[Column, ...]` | primary-key columns |
| `mapper.attrs` | `ReadOnlyProperties` | mapped attributes |
| `mapper.local_table` | `FromClause / Table` | underlying Table |

```python
mapper = inspect(Transaction)
columns = list(mapper.columns)
relationships = list(mapper.relationships)
```

Excellent for generic ORM access layers / serialization / dynamic query construction.

### Example and output

```python
mapper = inspect(User)
print(type(mapper).__name__)
print(type(mapper.local_table).__name__)
print([c.key for c in mapper.primary_key])
print(list(mapper.relationships.keys()))
```

```text
Mapper
Table
['id']
['addresses']
```

## 62. ORM column expressions

**Object behavior.** Column/hybrid properties define mapping descriptors or SQL expressions. An ORM instance can compute/read a Python value, whereas class-level usage may construct SQL.


**Return types** — ORM attribute mapping

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `column_property()` | `MappedSQLExpression/ColumnProperty` | SQL expression mapped as attribute |
| `query_expression()` | `MappedSQLExpression/ColumnProperty` | query-time expression attribute |
| `hybrid_property` | `hybrid_property descriptor` | Python + SQL-aware computed property |
| `hybrid_method` | `hybrid_method descriptor` | Python + SQL-aware method |

Conceptual example:

```python
from sqlalchemy.ext.hybrid import hybrid_property

class User(Base):
    # ... id, first_name and last_name mappings ...

    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
```

Instance access:

```python
user.full_name
```

Potential SQL expression use:

```python
select(User).where(
    User.full_name == '...'
)
```

A `hybrid_property` may need a separate `.expression` implementation if its Python expression and intended SQL expression differ.

### Example and output

```python
expr = column_property(User.__table__.c.id + 10)
print(type(expr).__name__)
print(type(query_expression()).__name__)
```

```text
MappedSQLExpression
MappedSQLExpression
```

A hybrid property behaves differently on instances versus mapped classes; its SQL-side expression must be valid when used inside a query.

## 63. Bulk ORM INSERT

**Object behavior.** `Session.execute(insert(Model), list_of_dicts)` performs ORM bulk INSERT. With `RETURNING` it can yield returned rows/objects; otherwise a result may carry little row data. The call does not itself commit.


**Return types** — Session

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `Session.execute(insert(...), rows)` | `Result (typically; driver and RETURNING determine rows)` | bulk INSERT |

```python
session.execute(
    insert(Transaction),
    records,
)
```

```python
records = [
    {'keyid': 1, 'stage': 1},
    {'keyid': 2, 'stage': 2},
]
```

Useful for ingestion without instantiating large numbers of ORM objects. `Session.execute(insert(ORMModel), rows)` uses modern ORM bulk insert behavior (parameter keys generally refer to mapped attribute names).

### Example and output

```python
with Session(engine) as session:
    result = session.execute(insert(User), [{'id': 90, 'name': 'X'}])
    print(type(result).__name__)
    session.rollback()
```

```text
IteratorResult
```

Concrete result implementations can vary with execution mode. Here no ORM object is loaded into the identity map.

## 64. Bulk ORM UPDATE

**Object behavior.** `Session.execute(update(Model), rows)` can perform bulk UPDATE-by-primary-key when multiple parameter dictionaries include primary keys. This differs from a single set-based SQL UPDATE.


**Return types** — Session

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `Session.execute(update(...), params)` | `Result (typically; driver and RETURNING determine rows)` | bulk UPDATE |

Set-based update:

```python
session.execute(
    update(Transaction)
    .where(Transaction.is_processed == False)
    .values(is_processed=True)
)
```

There is also bulk UPDATE **by primary key** when using `Session.execute(update(Model), list_of_dicts_with_pks)`, with different semantics from one set-based UPDATE. Use `is_(False)` in new code where appropriate.

### Example and output

```python
stmt = update(User).where(User.id == 1).values(name='Changed')
print(type(stmt).__name__)

with Session(engine) as session:
    result = session.execute(stmt)
    print(result.rowcount)
    session.rollback()
```

```text
Update
1
```

`rowcount` is commonly available on cursor-backed results, but behavior varies by statement and driver.

## 65. Locking

**Object behavior.** `.with_for_update()` returns a `Select`; lock semantics are database-specific and only apply when the statement executes.


**Return types** — Select

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.with_for_update()` | `Select` | SELECT ... FOR UPDATE |

```python
stmt = (
    select(Transaction)
    .where(Transaction.is_processed == False)
    .with_for_update()
)
```

Potential options, depending on backend:

```text
nowait
read
skip_locked
of
```

Useful when multiple workers could claim the same queue rows, but actual concurrency and lock behavior are database-specific.

### Example and output

```python
stmt = select(User).with_for_update(nowait=True)
print(type(stmt).__name__)
```

```text
Select
```

Constructing the statement is portable; support for `NOWAIT` at execution is database-specific.

## 66. Execution options

**Object behavior.** `.execution_options()` on an SQL statement returns a new statement of the same kind. On `Connection`, it changes options on the connection and returns that connection.


**Return types** — Executable statement

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.execution_options()` | `Select (generative; other executable statement kind preserved)` | statement execution behavior |

Some ORM execution option concepts:

```text
populate_existing           reload existing ORM identities
autoflush                   control pre-query autoflush
yield_per                    process large results incrementally
```

```python
stmt = select(Transaction).execution_options(yield_per=1000)
```

### Example and output

```python
stmt = select(User).execution_options(populate_existing=True)
print(type(stmt).__name__)
print(stmt.get_execution_options()['populate_existing'])
```

```text
Select
True
```

## 67. Streaming / large query results

**Object behavior.** `Result.partitions(n)` yields Python lists, one batch at a time. It does not return an `itertools.batched` iterator of tuples, and server-side buffering depends on driver/options.


**Return types** — Result / Connection

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `yield_per` | `Argument (int), not a function` | fetch ORM objects incrementally |
| `Result.partitions()` | `Iterator[list[Row]] or Iterator[list[T]]` | consume groups of result rows |
| `Connection.execution_options()` | `Connection (same object)` | stream-related controls |

```python
stmt = select(Transaction).execution_options(yield_per=1000)
for batch in session.scalars(stmt).partitions(1000):
    process(batch)
```

Useful when query results are too large to materialize at once. Check driver/database streaming behavior and avoid eager-loading configurations incompatible with your batch strategy.

### Example and output

```python
with Session(engine) as session:
    stmt = select(User.name).order_by(User.id)
    parts = session.scalars(stmt).partitions(2)
    print(list(parts))
```

```text
[['Ada', 'Grace'], ['Linus']]
```

`partitions()` returns an iterator of **lists**, rather than fixed-size tuples.

## 68. Async SQLAlchemy

**Object behavior.** `AsyncSession.execute()` and `.scalars()` are awaitable and produce synchronous-style `Result`/`ScalarResult` objects after awaiting. `.stream()` and `.stream_scalars()` instead produce `AsyncResult`/`AsyncScalarResult` after awaiting.


**Return types** — Async API

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `create_async_engine()` | `AsyncEngine` | async Engine |
| `AsyncSession` | `AsyncSession instance` | async ORM Session |
| `AsyncSession.execute()` | `Coroutine[Result]` | async execute |
| `AsyncSession.scalar()` | `Coroutine[scalar or None]` | async scalar |
| `AsyncSession.scalars()` | `Coroutine[ScalarResult]` | async scalar result |
| `AsyncSession.stream()` | `Coroutine[AsyncResult]` | stream async result |
| `AsyncSession.stream_scalars()` | `Coroutine[AsyncScalarResult]` | stream scalar values |
| `AsyncSession.flush()` | `Coroutine[None]` | async flush |
| `AsyncSession.commit()` | `Coroutine[None]` | async commit |
| `AsyncSession.rollback()` | `Coroutine[None]` | async rollback |
| `AsyncSession.refresh()` | `Coroutine[None]` | async refresh |

```python
async with AsyncSession(async_engine) as session:
    items = (await session.scalars(select(Transaction))).all()
    await session.commit()
```

Some SQLAlchemy 2.1 installations may require the `sqlalchemy[asyncio]` extra for the `greenlet` dependency. Async support also needs an appropriate async database dialect/driver.

### Example and output

```python
async def fetch_names(async_session):
    result = await async_session.execute(select(User.name))
    print(type(result).__name__)
    print(result.scalars().all())

async def stream_names(async_session):
    result = await async_session.stream(select(User.name))
    print(type(result).__name__)
    return [name async for name in result.scalars()]
```

For a typical ORM query, awaited `execute()` produces a `Result` (often `ChunkedIteratorResult`), whereas awaited `stream()` produces `AsyncResult`. These functions require an async engine and async database driver.

## 69. Events

**Object behavior.** `event.listen()` registers a listener and returns `None`. `@event.listens_for(...)` returns the decorated Python function; registration itself is a side effect.


**Return types** — SQLAlchemy events

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `event.listen()` | `None` | attach event listener |
| `event.listens_for()` | `Function (original decorated callable)` | decorator form |

Event names worth recognizing:

```text
before_insert
after_insert
before_update
after_update
before_delete
after_delete
before_flush
after_flush
before_commit
after_commit
checkout
checkin
before_execute
after_execute
```

```python
@event.listens_for(Session, 'before_flush')
def check_pending(session, flush_context, instances):
    ...
```

Which events are legal depends on their target (Mapper, Session, Engine/Connection, pool). Mapper-level flush events have restrictions; they aren't general-purpose replacements for Session/pipeline logic.

### Example and output

```python
from sqlalchemy import event

def before_execute(conn, clauseelement, multiparams, params, execution_options):
    pass

print(event.listen(engine, 'before_execute', before_execute))
event.remove(engine, 'before_execute', before_execute)
```

```text
None
```

## 70. Dialect-specific INSERT extensions

**Object behavior.** PostgreSQL/SQLite `on_conflict_*` methods and MySQL `on_duplicate_key_update()` belong to dialect-specific `Insert` subclasses. They preserve the dialect-specific Insert type.


PostgreSQL/SQLite-specific upsert constructs support:

**Return types** — Dialect-specific Insert

| API / attribute | Produced Python class / type | Operation |
|---|---|---|
| `.on_conflict_do_nothing()` | `Dialect-specific Insert` | INSERT ... ON CONFLICT DO NOTHING |
| `.on_conflict_do_update()` | `Dialect-specific Insert` | UPSERT |

MySQL-family alternative:

| Method | Python return class | Operation |
|---|---|---|
| `.on_duplicate_key_update()` | MySQL-specific `Insert` | `ON DUPLICATE KEY UPDATE` |

These are **dialect-specific Insert methods**, not guaranteed methods on every generic `sqlalchemy.insert()` statement.

```python
from sqlalchemy.dialects.postgresql import insert as pg_insert

stmt = pg_insert(Transaction).values(keyid=10)
stmt = stmt.on_conflict_do_nothing(index_elements=['keyid'])
```

### Example and output

```python
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

stmt = sqlite_insert(User).values(id=1, name='Ada')
stmt = stmt.on_conflict_do_nothing(index_elements=['id'])
print(type(stmt).__name__)
```

```text
Insert
```

The runtime class name is `Insert`, but this is the SQLite-specific `Insert` subclass rather than the generic Core `Insert`.

## 71. SQLAlchemy classes/types worth knowing

SQL expression side:

```text
ClauseElement
    very broad base for SQL expression objects

ColumnElement
    something usable as a SQL value/expression

Column
    real schema column

InstrumentedAttribute
    ORM mapped class attribute
```

FROM/query side:

```text
Selectable
    broad category of things participating in SELECT structures

FromClause
    object directly usable in a FROM clause

Table
    real table; a FromClause

Alias
    aliased FROM object

Subquery
    SELECT wrapped as FROM object

Join
    JOIN expression; a FromClause
```

SELECT statements:

```text
SelectBase
    base for SELECT-like statements

Select
    normal SELECT

CompoundSelect
    UNION / INTERSECT / EXCEPT

TextualSelect
    textual SELECT with column information
```

A core theme: `Table` / `Alias` / `Subquery` / `Join` generally represent FROM-able SQL constructs; `Select` is a SELECT statement; `ColumnElement` represents a SQL expression/value.

## 72. Function annotations and choosing the correct abstraction

If a function accepts these FROM-able objects:

```text
Table
Alias
Subquery
Join
```

Then `FromClause` is often the meaningful annotation:

```python
def something(source: FromClause):
    ...
```

> Give me something usable in SQL `FROM`.

If it expects:

```text
Select
CompoundSelect
```

`SelectBase` is conceptually relevant:

```python
def something(stmt: SelectBase):
    ...
```

> Give me SELECT-like statement behavior.

For an actual ordinary SELECT:

```python
def something(stmt: Select):
    ...
```

> Give me an actual `Select` statement.

Broader:

```python
def something(selectable: Selectable):
    ...
```

> Give me an object from a wider family of selectable SQL constructs.

**Type-system distinction:** `Selectable` is deliberately broad; it does *not* promise every method available on either `FromClause` or `Select`. Choose the narrowest type matching the operations you call.

Illustrative imports (availability/import paths can vary across minor versions):

```python
from sqlalchemy.sql.selectable import FromClause, SelectBase, Selectable
from sqlalchemy.sql import Select
```

## 73. Compact SQLAlchemy vocabulary map

```text
QUERY
select()                    build SELECT
.where()                    filtering
.filter_by()                filtering by ORM attributes
.order_by()                 sorting
.group_by()                 grouping
.having()                   aggregate filtering
.distinct()                 unique rows
.limit() / .offset()        pagination

CONDITIONS
.in_()                      membership
.between()                  range
.is_() / .is_not()          NULL/identity
.like() / .ilike()          pattern matching
and_() / or_() / not_()    boolean logic

JOINS
.join()                     inner join
.outerjoin()                left join
.join_from()                explicit source
.select_from()              explicit FROM

RESHAPING QUERY STRUCTURE
.alias()                    alias
.subquery()                 SELECT → FROM object
.scalar_subquery()          SELECT → scalar expression
.cte()                      CTE
.exists()                   EXISTS
.lateral()                  LATERAL

SET OPERATIONS
.union()
.union_all()
.intersect()
.except_()

EXPRESSIONS
case()                      CASE WHEN
cast()                      CAST
func.xxx()                  SQL function
.label()                    AS alias
tuple_()                    tuple expression
literal()                   literal value
bindparam()                 bind parameter
text()                      raw SQL

WRITE
insert()                    INSERT
update()                    UPDATE
delete()                    DELETE
.values()                   data to write
.returning()                return changed rows

EXECUTE
Session.execute()           execute → rows
Session.scalars()           execute → ORM/scalar objects
Session.scalar()            execute → one scalar
Result.all()                all results
Result.first()              first
Result.one()                exactly one
Result.one_or_none()        zero or one
Result.scalars()            unwrap first column
Result.mappings()           dict-like rows
Result.unique()             unique ORM identities

SESSION
.add()                      stage object
.add_all()                  stage objects
.merge()                    merge detached object
.delete()                   mark deleted
.flush()                    send SQL
.commit()                   commit
.rollback()                 rollback
.get()                      lookup by PK
.refresh()                  reload now
.expire()                   reload on next access
.expunge()                  detach

ORM
Mapped[]                    mapped type
mapped_column()             column
relationship()              relationship
selectinload()              eager second SELECT
joinedload()                eager JOIN
load_only()                 selected columns
defer()                     delayed column
raiseload()                 prevent accidental lazy query

SCHEMA
MetaData()                  schema registry
Table()                     table
Column()                    column
ForeignKey()                FK
Index()                     index
create_all()                create schema
reflect()                   inspect existing schema

INSPECTION
inspect()                   inspect ORM/schema object
Inspector.get_table_names()
Inspector.get_columns()
Inspector.get_foreign_keys()
Inspector.get_indexes()

TRANSACTIONS
.begin()
.begin_nested()
.commit()
.rollback()

DEBUGGING
.compile()                  render generated SQL
```

### Frequently composed SQL and ORM interfaces

```text
select()
.where()
.join()
.join_from()
.select_from()
.in_()
.between()
.exists()
.distinct()
.group_by()
.subquery()
.scalar_subquery()
.cte()
case()
func()
tuple_()
insert()
update()
delete()
.returning()
Session.execute()
Session.scalars()
Session.scalar()
Session.get()
Result.scalar_one()
Result.scalar_one_or_none()
Result.mappings()
aliased()
selectinload()
load_only()
inspect()
Table.c
FromClause
Selectable
Select
SelectBase
CompoundSelect
```

**Type-system implication:** know whether you are passing around a `Table`, `FromClause`, `Select`, `Subquery`, ORM entity, `Session` or `Result`. This is key to clean repository and transaction-engine APIs.

### Minimal import cheat sheet

```python
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey, Index,
    select, insert, update, delete,
    and_, or_, not_, exists, case, cast,
    text, literal, literal_column, bindparam, tuple_,
    func, inspect, create_engine,
    union, union_all, intersect, except_,
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship,
    Session, aliased, selectinload, joinedload,
    load_only, defer, raiseload, with_loader_criteria,
    column_property, query_expression,
)
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import event
```

## Selectable Class Hierarchy

The hierarchy below summarizes the **principal SQLAlchemy Core selectable interfaces**. A number of classes also use additional mixins and multiple inheritance; the diagram highlights the relationships most useful for choosing APIs and annotations rather than reproducing every runtime MRO.
```
ReturnsRows
│
└── Selectable
    │
    ├───────────────────────────────────────────────────────────────┐
    │                                                               │
    ▼                                                               ▼
FromClause                                                     SelectBase
"can appear in FROM"                                           "a SELECT statement"
    │                                                               │
    │                                                               ├── TextualSelect
    │                                                               │      text(...).columns(...)
    │                                                               │
    │                                                               └── GenerativeSelect
    │                                                                      │
    │                                                                      ├── Select
    │                                                                      │      select(...)
    │                                                                      │
    │                                                                      └── CompoundSelect
    │                                                                             union(...)
    │                                                                             union_all(...)
    │                                                                             intersect(...)
    │                                                                             except_(...)
    │
    ├── Join
    │      table1.join(table2)
    │
    └── NamedFromClause
           │
           ├── TableClause
           │      │
           │      └── Table
           │
           │          table(...)     → TableClause
           │          Table(...)     → Table
           │
           │
           ├── AliasedReturnsRows
           │      │
           │      ├── Subquery
           │      │      select(...).subquery()
           │      │
           │      ├── CTE
           │      │      select(...).cte()
           │      │
           │      └── FromClauseAlias
           │             │
           │             ├── Alias
           │             │      table.alias()
           │             │
           │             ├── TableSample
           │             │      table.tablesample(...)
           │             │
           │             └── Lateral
           │                    select(...).lateral()
           │
           └── LateralFromClause
                  │
                  ├── Values
                  │      values(...)
                  │
                  ├── Lateral
                  │      [multiple inheritance]
                  │
                  └── TableValuedAlias
                         func.some_func().table_valued(...)
```

### Official SQLAlchemy reference documentation

- [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/21/)
- [Core SQL expression language](https://docs.sqlalchemy.org/en/21/core/expression_api.html)
- [Select and other selectable constructs](https://docs.sqlalchemy.org/en/21/core/selectable.html)
- [DML](https://docs.sqlalchemy.org/en/21/core/dml.html)
- [ORM querying guide](https://docs.sqlalchemy.org/en/21/orm/queryguide/)
- [ORM relationship loading](https://docs.sqlalchemy.org/en/21/orm/queryguide/relationships.html)
- [Session API](https://docs.sqlalchemy.org/en/21/orm/session_api.html)
- [ORM object state](https://docs.sqlalchemy.org/en/21/orm/session_state_management.html)
- [Reflection and Inspector](https://docs.sqlalchemy.org/en/21/core/reflection.html)
- [SQLAlchemy 2.0 migration notes](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)


## Class-specific result and expression methods

### Concrete type compared with API type

```python
stmt = select(User)
print(type(stmt).__name__)

with Session(engine) as session:
    result = session.execute(stmt)
    row = result.first()
    print(type(result).__name__)
    print(type(row).__name__)
    print(type(row[0]).__name__)
```

```text
Select
ChunkedIteratorResult
Row
User
```

`Result` is the general interface; a `ChunkedIteratorResult` is a common concrete implementation for ORM execution. `Row` describes the result container. `User` describes a selected object inside it.

### `Row`, `RowMapping`, `ScalarResult`, and normal Python containers

| Operation | Return value type | Important distinction |
|---|---|---|
| `session.execute(select(User))` | `Result` | Iterates over `Row` objects |
| `.first()` | `Row[tuple[User]]` or `None` conceptually | A row containing the ORM entity |
| `.all()` | `Sequence[Row]` | Materializes all rows |
| `.scalars()` | `ScalarResult[User]` | Filters to one selected entry per row |
| `.scalars().first()` | `User` or `None` | Single mapped instance |
| `.scalars().all()` | `Sequence[User]` | Materializes mapped objects |
| `.mappings()` | `MappingResult` | Iterator-style mapping filter |
| `.mappings().first()` | `RowMapping` or `None` | Mapping view of a row |
| `dict(row._mapping)` | `dict` | Explicitly materialized Python dictionary |
| `tuple(row)` | `tuple` | Explicitly converted Python tuple |
| `.partitions(100)` | `Iterator[list[Row]]` | Chunked row lists |
| `.scalars().partitions(100)` | `Iterator[list[T]]` | Chunked scalar lists |
| `Session.get(User, id)` | `User` or `None` | Entity lookup by primary key |

`Result.first()` and `Result.scalar()` consume the first result and close the result set; `.all()` consumes the remainder. To retrieve multiple independent representations, execute the statement again or intentionally materialize the data.

### `Table`, `TableClause`, and ORM class attributes

```python
print(type(User).__name__)
print(type(User.__table__).__name__)
print(type(User.__table__.c.id).__name__)
print(type(User.id).__name__)
print(type(table('example', column('id'))).__name__)
```

```text
DeclarativeAttributeIntercept
Table
Column
InstrumentedAttribute
TableClause
```

The exact metaclass name printed for a mapped class is an implementation detail and may differ between SQLAlchemy versions. `User` is a user-defined ORM mapped class; `User.__table__` is the Core `Table`; `User.id` is an ORM instrumented class attribute.

### `FromClause` versus `SelectBase`

| Interface | Common implementations | Core responsibility |
|---|---|---|
| `FromClause` | `Table`, `TableClause`, `Alias`, `Join`, `Subquery`, `CTE`, `Lateral`, `Values`, `TableValuedAlias` | Supplies FROM-clause semantics and exported columns |
| `SelectBase` | `Select`, `CompoundSelect`, `TextualSelect` | Supplies SELECT-statement semantics |
| `ColumnElement` | `Column`, `ColumnClause`, `BinaryExpression`, `Label`, `ScalarSelect`, `Case`, `Cast`, `BindParameter`, `Over`, `Exists` | Supplies expression/value semantics |
| `Executable` | `Select`, `Insert`, `Update`, `Delete`, `TextClause`, and others | Can be executed by a Connection/Session |
| `ReturnsRows` | `Select`, `Join`, `Table`, `Subquery`, and others | Participates in row-producing SQL structures |

The categories overlap through inheritance, but they do not promise identical methods. For instance, a `Select` can be converted to a `Subquery`, which can then expose `.c` through `FromClause`; a `ScalarSelect` instead participates in expression comparisons.

### Table-valued and column-valued SQL functions

Some database functions produce rows rather than a single scalar. SQLAlchemy provides distinct object types for these uses.

| Operation | Produced class | Meaning |
|---|---|---|
| `func.some_function(...)` | `Function` / `FunctionElement` | Function expression |
| `.table_valued('col1', 'col2')` | `TableValuedAlias` | FROM-able function result with named columns |
| `.column_valued()` | `TableValuedColumn` | Column-valued function expression |
| `.scalar_table_valued('field')` | `ScalarFunctionColumn` | Scalar field from table-valued function |
| `values(column('x', Integer))` | `Values` | Literal rowset expression |
| `values(...).data([(1,), (2,)])` | `Values` | Add inline rows to a rowset |

```python
rowset = values(column('x', Integer)).data([(1,), (2,)])
function_rows = func.json_each('[10, 20]').table_valued('key', 'value')

print(type(rowset).__name__)
print(type(function_rows).__name__)
print(type(function_rows.c.value).__name__)
```

```text
Values
TableValuedAlias
ColumnClause
```

Database-specific functions such as SQLite `json_each` and PostgreSQL `generate_series` require supported backends.

### Result objects compared with NumPy, Pandas, and Polars

Core SQLAlchemy returns `Row` / `RowMapping` / Python scalar values, not a Pandas or Polars DataFrame. Conversion into a DataFrame is an additional application-level operation.

```python
with engine.connect() as conn:
    rows = conn.execute(select(User.__table__.c.id, User.__table__.c.name))
    records = [dict(row) for row in rows.mappings()]
    print(records)
```

```text
[{'id': 1, 'name': 'Ada'}, {'id': 2, 'name': 'Grace'}, {'id': 3, 'name': 'Linus'}]
```

`pandas.read_sql(statement, connection)` and `polars.read_database(query=..., connection=...)` are external-library conveniences; they do not change the native return type of `Connection.execute()`.

### Additional official references

- [SQLAlchemy 2.1 — SELECT and selectable objects](https://docs.sqlalchemy.org/en/21/core/selectable.html)
- [SQLAlchemy 2.1 — SQL functions and table-valued functions](https://docs.sqlalchemy.org/en/21/core/functions.html)
- [SQLAlchemy 2.1 — Result / CursorResult / ScalarResult](https://docs.sqlalchemy.org/en/21/core/connections.html#sqlalchemy.engine.Result)
- [SQLAlchemy 2.1 — Session API](https://docs.sqlalchemy.org/en/21/orm/session_api.html)
- [SQLAlchemy 2.1 — Change notes](https://docs.sqlalchemy.org/en/21/changelog/migration_21.html)