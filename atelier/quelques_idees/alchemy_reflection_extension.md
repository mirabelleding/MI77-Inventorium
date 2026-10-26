```python
class TransactionalTable(ReflectedTable):

    def __init__(self, table: Table, database: Database):
        super().__init__(table, database)

        if "transaction_id" not in self.sa.c:
            raise ValueError(
                f"{self.sa.fullname} must contain 'transaction_id'"
            )

    def select_as_of(
        self,
        *conditions: ColumnElement[bool],
        transaction_id: str | None = None,
    ) -> Select:

        return select_as_of(
            self.sa,
            *conditions,
            transaction_id=transaction_id,
        )

    def combine_table(
        self,
        *tables: TransactionalTable,
    ) -> Subquery:

        return combine_tables(
            self.sa,
            *(table.sa for table in tables),
        )

```

```python

_EXCLUDED_KEY_COLUMNS = {
    ....
}


def select_as_of(
    table: FromClause,
    *conditions: ColumnElement[bool],
    transaction_id: str | None = None,
    transactions: Table = TRANSACTIONS
) -> Select:

    if "transaction_id" not in table.c:
        raise ValueError(
            f"{table.fullname} does not have a "
            "'transaction_id' column."
        )

    up = transactions.alias("up")

    key_columns = [
        column
        for column in table.c
        if column.name not in _EXCLUDED_KEY_COLUMNS
    ]

    latest = (
        select(
            *key_columns,
            func.max(up.c.keyid).label(
                "transaction_keyid"
            ),
        )
        .select_from(
            table.join(
                up,
                table.c.transaction_id == up.c.uuid,
            )
        )
    )

    if conditions:
        latest = latest.where(*conditions)

    if transaction_id is not None:
        cutoff_keyid = (
            select(up.c.keyid)
            .where(up.c.uuid == transaction_id)
            .scalar_subquery()
        )

        latest = latest.where(
            up.c.keyid <= cutoff_keyid
        )

    latest = (
        latest
        .group_by(*key_columns)
        .cte()
    )

    selected_transactions = (
        select(
            *[
                latest.c[column.name]
                for column in key_columns
            ],
            up.c.uuid.label("transaction_id"),
            latest.c.transaction_keyid,
        )
        .select_from(
            latest.join(
                up,
                up.c.keyid
                == latest.c.transaction_keyid,
            )
        )
        .cte()
    )

    record_match = [
        column.is_not_distinct_from(
            selected_transactions.c[column.name]
        )
        for column in key_columns
    ]

    return (
        select(table)
        .select_from(
            table.join(
                selected_transactions,
                and_(
                    *record_match,
                    table.c.transaction_id
                    == selected_transactions.c.transaction_id,
                ),
            )
        )
        .order_by(
            selected_transactions.c.transaction_keyid.desc()
        )
    )
```
```python
def combine_tables(
    *tables: Table,
) -> Subquery:

    if len(tables) < 2:
        raise ValueError(
            "At least two tables are required."
        )

    if all(
        "hierarchy_id" in table.c
        for table in tables
    ):
        hierarchy_column = "hierarchy_id"

    elif all(
        "hierarchy_group_id" in table.c
        for table in tables
    ):
        hierarchy_column = "hierarchy_group_id"

    else:
        raise ValueError(
            "All tables must be at the same hierarchy level "
            "('hierarchy_id' or 'hierarchy_group_id')."
        )

    columns = (
        hierarchy_column,
        *_DIMENSION_COLUMNS,
        "balance",
    )

    return union_all(
        *[
            select(
                *[
                    table.c[name]
                    for name in columns
                ]
            )
            for table in tables
        ]
    ).subquery("combined_tables")

```

```python
def load_pl(
    stmt_or_table: Select | FromClause,
) -> pl.DataFrame:

    if isinstance(stmt_or_table, FromClause):
        stmt_or_table = select(stmt_or_table)

    stmt = stmt_or_table.with_only_columns(
        *[
            cast(c, String).label(c.name)
            if c.name == "transaction_id"   # handling ComputeError when loading UNIQUEIDENTIFIER
            else c
            for c in stmt_or_table.selected_columns
        ],
        maintain_column_froms=True,
    )

    return pl.read_database(
        query=stmt,
        connection=Database.engine,
    )
```