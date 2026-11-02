import random
from collections.abc import Sequence
from datetime import date
from itertools import product

import pandas as pd

"""
Demo Table Setups:

month-range: default 2026-01-01 - 2026-03-01

hierarchy_id: default int 1-5
hierarchy_group_id: default int 1-2

stage: Stage1/2/3
--------
hierarchy_id tables:
table_1: measure 1-3
table_2: measure 4-5

table_r_1: measure_a, _b
table_r_2: measure_c,

hierarchy_group_id tables:
table_3: measure 6-10

table_r_3: measure_d, _e
"""


MAX_H_IDS = {
    "hierarchy_id": 5,
    "hierarchy_group_id": 2,
}

TABLE_SPECS = {
    "table_1": ("hierarchy_id", ("measure_1", "measure_2", "measure_3")),
    "table_2": ("hierarchy_id", ("measure_4", "measure_5")),
    "table_3": ("hierarchy_group_id", tuple(f"measure_{i}" for i in range(6, 11))),
    "table_r_1": ("hierarchy_id", ("measure_a", "measure_b")),
    "table_r_2": ("hierarchy_id", ("measure_c",)),
    "table_r_3": ("hierarchy_group_id", ("measure_e",)),
}

DEFAULT_MTH_RANGE = (date(2026, 1, 1), date(2026, 3, 1))


def generate_demo_table(
    table_name: str,
    n_rows: int,
    h_ids: Sequence[int] | None = None,
    measure_types: Sequence[str] | None = None,
    month_range: tuple[date, date] | None = None,
    months: Sequence[date] | None = None,
    stage: str | Sequence[str] = ("Stage 1", "Stage 2", "Stage 3"),
    seed: int = 7,
) -> pd.DataFrame:
    if n_rows < 0:
        raise ValueError("n_rows must be non-negative")

    if month_range is not None and months is not None:
        raise ValueError("Specify either month_range or months, not both")

    id_column, available_measures = TABLE_SPECS[table_name]

    entity_ids = (
        h_ids
        if h_ids is not None
        else range(1, MAX_H_IDS[id_column] + 1)
    )

    measures = (
        measure_types
        if measure_types is not None
        else available_measures
    )

    if not set(measures).issubset(available_measures):
        raise ValueError("measure_types contains measures not defined for this table")

    stages = (stage,) if isinstance(stage, str) else stage

    month_values = (
        pd.PeriodIndex(months, freq="M")
        if months is not None
        else pd.period_range(
            *(month_range or DEFAULT_MTH_RANGE),
            freq="M",
        )
    ).to_timestamp().date

    combinations = list(
        product(
            dict.fromkeys(entity_ids),
            dict.fromkeys(stages),
            dict.fromkeys(measures),
            dict.fromkeys(month_values),
        )
    )

    if n_rows > len(combinations):
        print(
            f"n_rows exceeds available combinations. "
            f"Generating {len(combinations)} rows instead."
        )

    rng = random.Random(f"{seed}:{table_name}")

    df = pd.DataFrame(
        (
            (*row, rng.randint(1, 20))
            for row in rng.sample(
                combinations, min(n_rows, len(combinations))
            )
        ),
        columns=[
            id_column,
            "stage",
            "measure_type_code",
            "month_date",
            "balance",
        ],
    )

    df.insert(1, "currency_code", "CAD")
    df["balance"] = df["balance"].astype(float)

    return df