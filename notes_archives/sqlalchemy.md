# SQLAlchemy

**Reference style:** SQLAlchemy class/function/method → what it does, with Core, ORM, execution, Result, relationship, SQL, schema, inspection, async, typing, and practical examples.

**Primary syntax:** modern SQLAlchemy **2.x** (`select(...)`, `Session.execute()` / `Session.scalars()`, typed declarative mappings). The original guide specifically focused on 2.1.x; older `session.query()` / `Query` are **legacy**.

**DB support:** compilation and capabilities vary by dialect (e.g., PostgreSQL/SQLite/MySQL/SQL Server); not every expression is available on every backend.

> **Mental model:** A *SQL statement/expression*, an *ORM object*, a *session*, and a *result object* are different types with different method families. Understanding the object type is central to readable SQLAlchemy code.

## Table of Contents

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

## 1. SELECT — basic construction

```text
select()                    construct SELECT statement
.where()                    WHERE condition
.filter()                   ORM-friendly synonym for where()
.filter_by()                filter using keyword attribute names
.order_by()                 ORDER BY
.group_by()                 GROUP BY
.having()                   HAVING
.distinct()                 SELECT DISTINCT
.limit()                    LIMIT
.offset()                   OFFSET
.slice()                    LIMIT + OFFSET using slice semantics
```

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

## 2. SELECT — choosing columns

```text
select(col1, col2)           select specific columns
.add_columns()               add output columns
.with_only_columns()         replace selected columns
.selected_columns            inspect selected columns
.label()                     label scalar expression
```

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

**Caution:** `select(Transaction).add_columns(Transaction.keyid)` selects both the entity and a redundant extra scalar column.

## 3. Filtering operators

Primarily methods of `ColumnElement` / ORM mapped instrumented attributes.

```text
==                           equality
!=                           inequality
>                            greater than
>=                           greater than/equal
<                            less than
<=                           less than/equal
.in_()                       SQL IN
.not_in()                    SQL NOT IN
.between()                   SQL BETWEEN
.is_()                       SQL IS
.is_not()                    SQL IS NOT
.is_distinct_from()          SQL IS DISTINCT FROM
.is_not_distinct_from()      SQL IS NOT DISTINCT FROM
```

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

## 4. Boolean expressions

```text
and_()                      SQL AND
or_()                       SQL OR
not_()                      SQL NOT
&                           AND for expressions
|                           OR for expressions
~                           NOT for expressions
true()                      SQL TRUE
false()                     SQL FALSE
```

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

## 5. String operators

```text
.like()                     SQL LIKE
.ilike()                    case-insensitive LIKE
.not_like()                 NOT LIKE
.not_ilike()                NOT ILIKE
.contains()                 contains substring
.startswith()               starts with
.endswith()                 ends with
.regexp_match()             regex matching
.regexp_replace()           regex replacement
```

```python
User.name.like('Mir%')
User.name.ilike('%abc%')
User.code.startswith('CB_')
```

Literal `_` and `%` have SQL wildcard meaning in `LIKE`; use escaping when matching literal pattern characters. Regex support is dialect-dependent.

## 6. NULL handling

```text
.is_(None)                  IS NULL
.is_not(None)               IS NOT NULL
null()                      literal SQL NULL
nulls_first()               NULLS FIRST
nulls_last()                NULLS LAST
func.coalesce()             first non-null value
```

```python
select(func.coalesce(Transaction.value, 0))
```

## 7. JOINs

```text
.join()                     INNER JOIN
.outerjoin()                LEFT OUTER JOIN
.join_from()                specify explicit left side
.outerjoin_from()           explicit left side + outer join
.select_from()              explicitly establish FROM clause
```

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

## 8. Relationship-based joins

```text
.join(Model.relationship)       join using relationship configuration
.outerjoin(Model.relationship)  outer join using relationship
.of_type()                      relationship against alias/subtype
.and_()                         add conditions to relationship join
```

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

## 9. Aliases

```text
.alias()                     SQL alias
aliased()                    ORM entity alias
.subquery()                  SELECT → named subquery
.cte()                       SELECT → CTE
.lateral()                   LATERAL subquery
```

Core:

```python
tx = transaction_table.alias('tx')
```

ORM:

```python
Tx = aliased(Transaction)
```

## 10. Subqueries

```text
.subquery()                  SELECT → FROM-able subquery
.scalar_subquery()           SELECT → scalar SQL expression
.exists()                    SELECT → EXISTS expression
```

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

## 11. EXISTS

```text
exists()                     construct EXISTS
.exists()                    convert SELECT to EXISTS
```

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

## 12. Set operations

```text
union()                      SQL UNION
union_all()                  SQL UNION ALL
intersect()                  SQL INTERSECT
intersect_all()              INTERSECT ALL
except_()                    SQL EXCEPT
except_all()                 EXCEPT ALL
```

```python
stmt = select(TableA.id).union_all(
    select(TableB.id)
)
```

Such compound SELECTs produce `CompoundSelect` constructs. Backend support varies for `INTERSECT ALL` and `EXCEPT ALL`.

## 13. CTEs

```text
.cte()                       create Common Table Expression
.add_cte()                   attach CTE to statement
```

```python
active_tx = (
    select(Transaction)
    .where(Transaction.is_processed == 0)
    .cte('active_tx')
)
stmt = select(active_tx)
```

A CTE can make multi-stage query plans much easier to read.

## 14. Recursive CTEs

```text
.cte(recursive=True)         recursive CTE
.union_all()                 recursive branch
```

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

## 15. CASE expressions

```text
case()                       SQL CASE WHEN
```

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

## 16. SQL functions

```text
func.xxx()                   call SQL function
func.count()                 COUNT
func.sum()                   SUM
func.avg()                   AVG
func.min()                   MIN
func.max()                   MAX
func.coalesce()              COALESCE
func.lower()                 LOWER
func.upper()                 UPPER
func.now()                   current timestamp
func.current_date()          current date
func.row_number()            ROW_NUMBER
func.rank()                  RANK
func.dense_rank()            DENSE_RANK
```

`func` supports user-defined/vendor database functions, not just a fixed catalog:

```python
func.some_database_function(...)
```

## 17. Aggregation

```text
func.count()                 count rows/values
func.sum()                   sum
func.avg()                   average
func.min()                   minimum
func.max()                   maximum
.group_by()                  group rows
.having()                    filter aggregated groups
```

```python
stmt = (
    select(
        Transaction.stage,
        func.count().label('count'),
    )
    .group_by(Transaction.stage)
)
```

## 18. Labels

```text
.label()                     SQL AS alias
```

```python
select(
    func.sum(Transaction.value).label('total_value')
)
```

Then a returned row may expose:

```python
row.total_value
```

## 19. CAST / type coercion

```text
cast()                       SQL CAST
type_coerce()                change SQLAlchemy type interpretation
                             without necessarily emitting CAST
try_cast()                   TRY_CAST where supported
```

```python
cast(Transaction.value, Numeric)
```

```text
cast()                       changes SQL expression
type_coerce()                changes SQLAlchemy's type handling
```

`try_cast()` support is dialect-specific.

## 20. Literal expressions

```text
literal()                    bound literal value
literal_column()             literal SQL column expression
text()                       raw textual SQL
column()                     lightweight column expression
table()                      lightweight table construct
bindparam()                  explicit bind parameter
```

```python
literal(10)
literal_column('CURRENT_TIMESTAMP')
text('stage = 1')
bindparam('transaction_id')
```

**Safety:** `text()` and `literal_column()` can embed raw SQL. Never interpolate untrusted input directly; use bound parameters.

## 21. `text()` — raw SQL escape hatch

```text
text()                       textual SQL statement
.bindparams()                bind values
.columns()                   describe returned columns
```

```python
stmt = text('''
    SELECT *
    FROM transactions
    WHERE keyid > :keyid
''').bindparams(keyid=100)
```

Useful when the SQL is clearer than the equivalent expression tree.

## 22. INSERT

```text
insert()                     construct INSERT
.values()                    specify inserted values
.returning()                 RETURNING clause
.from_select()               INSERT ... SELECT
.inline()                    inline INSERT behavior
```

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

## 23. UPDATE

```text
update()                     construct UPDATE
.where()                     choose rows
.values()                    set values
.returning()                 return updated values
```

```python
stmt = (
    update(Transaction)
    .where(Transaction.uuid == tx_id)
    .values(is_processed=True)
)
```

## 24. DELETE

```text
delete()                     construct DELETE
.where()                     choose rows
.returning()                 return deleted values
```

```python
stmt = (
    delete(Transaction)
    .where(Transaction.keyid < 100)
)
```

## 25. RETURNING

```text
.returning()                 return rows modified by DML
```

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

## 26. Execution

Core:

```text
Connection.execute()         execute SQL statement
Connection.scalar()          execute + return one scalar
Connection.scalars()         execute + scalar result stream
```

ORM:

```text
Session.execute()            execute statement → Result
Session.scalar()             execute → one scalar value
Session.scalars()            execute → ScalarResult
```

```python
users = session.scalars(
    select(User)
).all()
```

Legacy alternative (still exists but no longer preferred):

```python
session.query(User).all()
```

## 27. `Result` methods

```text
.all()                       all rows
.first()                     first row or None
.one()                       exactly one row; otherwise error
.one_or_none()               one row or None; error if multiple
.scalar()                    first column of first row
.scalar_one()                exactly one scalar
.scalar_one_or_none()        one scalar or None
.scalars()                   Row results → scalar objects
.mappings()                  Row results → mapping/dict-like objects
.tuples()                    typed tuple-style results
.unique()                    remove ORM duplicate entities / rows by strategy
.partitions()                consume results in batches
.fetchmany()                 fetch n rows
.fetchall()                  all rows
.keys()                      result column names
```

`Result.first()` does **not** automatically add a SQL `LIMIT 1` to the statement.

## 28. Result shape mental model

```text
execute()                    Result[Row]
scalars()                    ScalarResult[T]
mappings()                   MappingResult
tuples()                     tuple-oriented Result
```

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

## 29. `scalar()` vs `scalars()`

```text
scalar()                     one scalar result
scalars()                    stream/list of scalar results
```

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

## 30. Session — object persistence

```text
Session.add()                attach/add one object
Session.add_all()            add multiple objects
Session.merge()              merge detached state into Session
Session.delete()             mark object for deletion
```

```python
tx = Transaction(...)
session.add(tx)
```

`merge()` returns the local persistent instance; it does not necessarily attach the original detached instance.

## 31. Session — flushing / committing

```text
.flush()                     push pending SQL to DB without ending transaction
.commit()                    commit transaction
.rollback()                  roll back transaction
```

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

## 32. Session — retrieving by primary key

```text
.get()                       primary-key lookup
.get_one()                   primary-key lookup; require existence
```

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

## 33. Session — refresh / expiration

```text
.refresh()                   immediately reload object from DB
.expire()                    mark object's attributes stale
.expire_all()                expire every persistent object
```

```text
refresh()                    reload NOW
expire()                     reload NEXT TIME attribute is accessed
```

```python
session.refresh(tx)
session.expire(tx, ['status'])
```

SQLAlchemy's normal expiration rules depend on transaction boundaries and Session configuration (notably `expire_on_commit`).

## 34. Session — detaching objects

```text
.expunge()                   detach one object from Session
.expunge_all()               detach all objects
```

```text
transient
pending
persistent
deleted
detached
```

These are the major ORM object states.

## 35. Session transactions

```text
.begin()                     begin transaction
.begin_nested()              begin SAVEPOINT / nested transaction
.commit()                    COMMIT
.rollback()                  ROLLBACK
.in_transaction()            transaction active?
.in_nested_transaction()     nested transaction active?
.get_transaction()           current transaction
.get_nested_transaction()    current nested transaction
```

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

## 36. Session execution controls

```text
.execution_options()         execution behavior options (supported in newer 2.x)
.no_autoflush                temporarily disable autoflush
.autoflush                   Session autoflush configuration
.get_bind()                  retrieve Engine/Connection being used
```

```python
with session.no_autoflush:
    # populate related objects before autoflush would run
    ...
```

For version portability, `statement.execution_options(...)` and options passed to `Session.execute(...)` may be more widely supported than a session-level method.

## 37. ORM model declaration

```text
DeclarativeBase              declarative base class
Mapped[...]                  type annotation for mapped attribute
mapped_column()              map database column
relationship()               map relationship
__tablename__                database table name
__table__                    mapped Table object
__mapper__                   Mapper for class
```

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

## 38. `mapped_column()`

```text
primary_key=True             primary key
nullable=False               NOT NULL
unique=True                  UNIQUE
index=True                   create index
default=                     Python-side / SQLAlchemy-side default
server_default=              database-side default
onupdate=                    Python update default
server_onupdate=             server update behavior / fetched marker
ForeignKey(...)              foreign key
```

```python
id: Mapped[int] = mapped_column(primary_key=True)
created_at: Mapped[datetime] = mapped_column(server_default=func.now())
user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
```

`server_onupdate` is not a portable instruction to generate every backend's server-side ON UPDATE syntax by itself.

## 39. Relationships

```text
relationship()               ORM relationship
back_populates=              explicit bidirectional relationship
secondary=                   many-to-many association table
cascade=                     persistence cascade rules
lazy=                        relationship loading strategy
uselist=                     scalar vs collection
viewonly=                    relationship not used for persistence
primaryjoin=                 custom join condition
secondaryjoin=               custom secondary join condition
foreign_keys=                explicitly identify FK columns
order_by=                    ordering of related collection
```

```python
class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    addresses: Mapped[list['Address']] = relationship(back_populates='user')
```

## 40. Relationship query operators

```text
.any()                       collection contains matching row
.has()                       scalar relationship matches condition
.contains()                  collection contains object
.of_type()                   relationship against alias/subclass
```

```python
select(User).where(
    User.addresses.any(
        Address.city == 'Toronto'
    )
)
```

This produces EXISTS-style filtering; `.has()` is the scalar relationship counterpart.

## 41. Relationship loading

```text
selectinload()               eager load with second SELECT
joinedload()                 eager load using JOIN
subqueryload()               eager load via subquery
lazyload()                   force lazy loading
immediateload()              immediate per-attribute SELECT
noload()                     don't load relationship (legacy/deprecated)
raiseload()                  error if lazy SQL would occur
contains_eager()             populate relationship from your own JOIN
defaultload()                continue loader path without changing strategy
```

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

`noload()` is retained to preserve the original method list; it is deprecated in recent SQLAlchemy 2.x and should not be a default strategy for new code.

## 42. Column loading controls

```text
load_only()                  load only selected columns
defer()                      defer loading column
undefer()                    explicitly load deferred column
undefer_group()              load deferred column group
with_expression()            populate mapped expression dynamically
```

```python
select(Transaction).options(
    load_only(
        Transaction.uuid,
        Transaction.keyid,
    )
)
```

Useful for large tables where only a handful of columns are required. Primary-key columns needed for ORM identity remain present.

## 43. `.options()`

```text
.options()                   attach ORM loading/query options
```

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

## 44. Global ORM filtering

```text
with_loader_criteria()       apply criteria everywhere an entity loads
```

```python
select(Transaction).options(
    with_loader_criteria(
        TransactionItem,
        TransactionItem.is_active == True,
    )
)
```

Prefer `TransactionItem.is_active.is_(True)` where appropriate; the example above retains the original expression style. Common use cases:

```text
soft deletes
tenant filtering
security scopes
effective-date filtering
active-record filtering
```

Criteria propagation and enforcement depend on loader options and your query/session design; don't treat it as a standalone security boundary without testing.

## 45. ORM aliases

```text
aliased()                    create ORM alias
```

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

## 46. SQL window functions

```text
.over()                      apply OVER clause
partition_by=                PARTITION BY
order_by=                   window ordering
rows=                       ROWS frame
range_=                     RANGE frame
```

```python
func.row_number().over(
    partition_by=Transaction.division,
    order_by=Transaction.keyid,
)
```

These are SQL equivalents for many Pandas `groupby().cumcount()`, `groupby().rank()` and `groupby().transform()` use cases. `partition_by`, `order_by`, `rows`, and `range_` are arguments to `over()`, not freestanding methods.

## 47. Useful window functions

```text
func.row_number()            ROW_NUMBER
func.rank()                  RANK
func.dense_rank()            DENSE_RANK
func.lag()                   previous row
func.lead()                  following row
func.first_value()           first window value
func.last_value()            last window value
func.sum().over()            cumulative/window sum
func.avg().over()            window average
```

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

## 48. Ordering helpers

```text
.asc()                       ascending
.desc()                      descending
.nulls_first()               NULL first
.nulls_last()                NULL last
```

```python
Transaction.keyid.desc()
Transaction.month_date.asc().nulls_last()
```

Null-ordering syntax/support can vary by dialect.

## 49. Distinct

```text
.distinct()                  SELECT DISTINCT
distinct()                   DISTINCT expression
```

```python
select(
    Transaction.hierarchy_id,
    Transaction.stage,
    Transaction.currency,
).distinct()
```

Useful for retrieving only the unique data-point keys your pipeline should process.

## 50. Tuple comparisons

```text
tuple_()                     SQL row/tuple expression
```

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

## 51. Arithmetic expressions

```text
+                           addition
-                           subtraction
*                           multiplication
/                           division
%                           modulo
```

```python
select(
    (
        Transaction.amount *
        Transaction.fx_rate
    ).label('converted_amount')
)
```

Be conscious of SQL type/precision semantics: numeric arithmetic is compiled and evaluated by the database.

## 52. Metadata

```text
MetaData()                   registry of schema objects
.create_all()                create all registered tables
.drop_all()                  drop registered tables
.reflect()                   load database schema into MetaData
.tables                      dictionary of tables
.sorted_tables               dependency-sorted Tables
```

```python
metadata = MetaData()
metadata.reflect(bind=engine)
```

Do not use `create_all()` as a substitute for production schema migrations (e.g., Alembic) when existing schemas must be changed.

## 53. Table

```text
Table()                      define Core table
.c                           column collection
.columns                     column collection
.primary_key                 PK constraint
.foreign_keys                foreign-key set
.constraints                 table constraints
.indexes                     table indexes
```

Core:

```python
transaction.c.keyid
```

ORM:

```python
Transaction.keyid
```

## 54. Table convenience methods

```text
table.select()               SELECT table
table.insert()               INSERT table
table.update()               UPDATE table
table.delete()               DELETE table
table.join()                 JOIN
table.outerjoin()            LEFT OUTER JOIN
table.alias()                alias table
```

```python
transaction_table.select().where(
    transaction_table.c.keyid > 100
)
```

## 55. Schema constraints

```text
PrimaryKeyConstraint()       composite/custom PK
ForeignKey()                 column-level FK
ForeignKeyConstraint()       table-level/composite FK
UniqueConstraint()           UNIQUE constraint
CheckConstraint()            CHECK constraint
Index()                      database index
```

```python
UniqueConstraint('keyid', 'stage', 'month_date', name='uq_tx_point')
```

## 56. Database reflection

```text
MetaData.reflect()           reflect many tables
Table(..., autoload_with=)   reflect one table
inspect(engine)              obtain Inspector
```

```text
Inspector.get_table_names()          tables
Inspector.get_view_names()           views
Inspector.get_columns()              columns
Inspector.get_pk_constraint()        primary key
Inspector.get_foreign_keys()         foreign keys
Inspector.get_indexes()              indexes
Inspector.get_unique_constraints()   unique constraints
Inspector.get_check_constraints()    check constraints
Inspector.get_schema_names()         schemas
Inspector.has_table()                does object exist?
Inspector.has_index()                does index exist?
```

```python
inspector = inspect(engine)
inspector.get_table_names()
inspector.get_columns('transaction')
```

The `Inspector` supplies backend-independent schema-introspection methods, to the extent the dialect supports each one.

## 57. Engine

```text
create_engine()              create Engine
engine.connect()             obtain Connection
engine.begin()               Connection + transaction context
engine.dispose()             dispose connection pool
```

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

## 58. Connection

```text
.execute()                   execute statement
.scalar()                    execute and return scalar
.scalars()                   execute and return scalar stream
.begin()                     transaction
.begin_nested()              SAVEPOINT
.commit()                    commit
.rollback()                  rollback
.close()                     return connection to pool
.execution_options()         execution configuration
```

```python
with engine.begin() as conn:
    conn.execute(insert(transaction_table), rows)
```

## 59. Compiling SQL

```text
.compile()                   compile statement to SQL representation
```

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

## 60. ORM state inspection

```text
inspect(obj)                 get InstanceState
inspect(obj).transient       not in Session / DB
inspect(obj).pending         added but not flushed
inspect(obj).persistent      persistent in Session
inspect(obj).deleted         marked deleted (after flush)
inspect(obj).detached        detached
```

Also:

```text
inspect(obj).attrs           mapped attribute states
inspect(obj).attrs.name.history
                            change history for one mapped attribute
inspect(obj).attrs.name.loaded_value
                            loaded value for one attribute
```

```python
state = inspect(tx)
print(state.persistent, state.detached)
print(state.attrs.status.history)
```

## 61. Mapper inspection

```text
inspect(Model)               retrieve Mapper
mapper.columns               mapped columns
mapper.relationships         relationships
mapper.primary_key           primary-key columns
mapper.attrs                 mapped attributes
mapper.local_table           underlying Table
```

```python
mapper = inspect(Transaction)
columns = list(mapper.columns)
relationships = list(mapper.relationships)
```

Excellent for generic ORM access layers / serialization / dynamic query construction.

## 62. ORM column expressions

```text
column_property()            SQL expression mapped as attribute
query_expression()           query-time expression attribute
hybrid_property              Python + SQL-aware computed property
hybrid_method                Python + SQL-aware method
```

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

## 63. Bulk ORM INSERT

```text
Session.execute(insert(...), rows)
                            bulk INSERT
```

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

## 64. Bulk ORM UPDATE

```text
Session.execute(update(...), params)
                            bulk UPDATE
```

Set-based update:

```python
session.execute(
    update(Transaction)
    .where(Transaction.is_processed == False)
    .values(is_processed=True)
)
```

There is also bulk UPDATE **by primary key** when using `Session.execute(update(Model), list_of_dicts_with_pks)`, with different semantics from one set-based UPDATE. Use `is_(False)` in new code where appropriate.

## 65. Locking

```text
.with_for_update()           SELECT ... FOR UPDATE
```

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

## 66. Execution options

```text
.execution_options()         statement execution behavior
```

Some ORM execution option concepts:

```text
populate_existing           reload existing ORM identities
autoflush                   control pre-query autoflush
yield_per                    process large results incrementally
```

```python
stmt = select(Transaction).execution_options(yield_per=1000)
```

## 67. Streaming / large query results

```text
yield_per                    fetch ORM objects incrementally
Result.partitions()          consume groups of result rows
Connection.execution_options()
                            stream-related controls
```

```python
stmt = select(Transaction).execution_options(yield_per=1000)
for batch in session.scalars(stmt).partitions(1000):
    process(batch)
```

Useful when query results are too large to materialize at once. Check driver/database streaming behavior and avoid eager-loading configurations incompatible with your batch strategy.

## 68. Async SQLAlchemy

```text
create_async_engine()        async Engine
AsyncSession                 async ORM Session
AsyncSession.execute()       async execute
AsyncSession.scalar()        async scalar
AsyncSession.scalars()       async scalar result
AsyncSession.stream()        stream async result
AsyncSession.stream_scalars()
                            stream scalar values
AsyncSession.flush()         async flush
AsyncSession.commit()        async commit
AsyncSession.rollback()      async rollback
AsyncSession.refresh()       async refresh
```

```python
async with AsyncSession(async_engine) as session:
    items = (await session.scalars(select(Transaction))).all()
    await session.commit()
```

Some SQLAlchemy 2.1 installations may require the `sqlalchemy[asyncio]` extra for the `greenlet` dependency. Async support also needs an appropriate async database dialect/driver.

## 69. Events

```text
event.listen()               attach event listener
event.listens_for()          decorator form
```

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

## 70. Dialect-specific INSERT extensions

PostgreSQL/SQLite-specific upsert constructs support:

```text
.on_conflict_do_nothing()    INSERT ... ON CONFLICT DO NOTHING
.on_conflict_do_update()     UPSERT
```

MySQL-family alternative:

```text
.on_duplicate_key_update()
```

These are **dialect-specific Insert methods**, not guaranteed methods on every generic `sqlalchemy.insert()` statement.

```python
from sqlalchemy.dialects.postgresql import insert as pg_insert

stmt = pg_insert(Transaction).values(keyid=10)
stmt = stmt.on_conflict_do_nothing(index_elements=['keyid'])
```

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

**Important qualification:** `Selectable` is deliberately broad; it does *not* promise every method available on either `FromClause` or `Select`. Choose the narrowest type matching the operations you call.

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

### Priority list for complex transaction-processing architectures

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

**Architectural lesson:** know whether you are passing around a `Table`, `FromClause`, `Select`, `Subquery`, ORM entity, `Session` or `Result`. This is key to clean repository and transaction-engine APIs.

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

### Official references

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
