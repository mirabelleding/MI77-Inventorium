from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    import polars as pl


def estimate_column_memories(
    df: pl.DataFrame,
    unit: Literal["b", "kb", "mb", "gb", "tb"] = "b",
) -> dict[str, int | float]:
    return {
        col.name: col.estimated_size(unit)
        for col in df.get_columns()
    }