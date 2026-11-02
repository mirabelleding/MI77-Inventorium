from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from recalc_engine.config.results import RecalcResults
from recalc_engine.core.plans import ExecutionPlan
from recalc_engine.core.transaction import Transaction
from recalc_engine.demo_data.generator import generate_demo_table


@dataclass(frozen=True)
class ExecutionInputs:
    results: RecalcResults

    table_1: pd.DataFrame | None = None
    table_2: pd.DataFrame | None = None
    table_3: pd.DataFrame | None = None

    def __getattr__(self, name: str) -> pd.DataFrame:
        if name in RecalcResults.__dataclass_fields__:
            return getattr(self.results, name)
        raise AttributeError(name)

    @classmethod
    def from_plan(
        cls,
        transaction: Transaction,
        plan: ExecutionPlan,
        results: RecalcResults,
    ) -> ExecutionInputs:
        return cls.from_demo(results)    #TODO: replace

    #---------------

    @classmethod
    def from_demo(
        cls,
        results: RecalcResults,
    ) -> ExecutionInputs:
        return cls(
            results=results,
            **{
                table: generate_demo_table(table, n_rows=50,)
                for table in ("table_1", "table_2", "table_3")
            },
        )