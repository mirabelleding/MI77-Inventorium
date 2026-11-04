from datetime import date, datetime
from pathlib import Path

import pandas as pd
import polars as pl


def df_to_sql(
    df: pd.DataFrame | pl.DataFrame,
    target_table: str,
    file_name: str,
    batch_size: int = 1000,
) -> None:
    """
    Generate a SQL file containing INSERT statements from a pandas DataFrame.
    Column names are taken directly from the DataFrame.
    Statements are batched to comply with SQL Server's 1,000-row limit for
    INSERT ... VALUES. The generated script uses the GO batch separator.
    """
    def sql_value(v):
        if pd.isna(v):
            return "NULL"

        if isinstance(v, (pd.Timestamp, datetime, date)):
            return f"'{v:%Y-%m-%d}'"

        if isinstance(v, str):
            return "'" + v.replace("'", "''") + "'"

        return str(v)

    cols = list(df.columns)
    column_names = ",\n    ".join(cols)

    insert_header = (
        f"INSERT INTO {target_table} (\n"
        f"    {column_names}\n"
        f")\nVALUES\n"
    )

    sql_parts = []

    for start in range(0, len(df), batch_size):
        if isinstance(df, pd.DataFrame):
            rows = df.iloc[start:start + batch_size].itertuples(
                index=False, name=None
            )
        else:
            rows = df.slice(start, batch_size).iter_rows()

        values = [
            f"({', '.join(sql_value(v) for v in row)})"
            for row in rows
        ]

        sql_parts.append(
            insert_header
            + ",\n".join(values)
            + "\nGO\n"
        )

    Path(f"{file_name}.sql").write_text(
        "\n\n".join(sql_parts),
        encoding="utf-8",
    )