from __future__ import annotations

from collections.abc import Iterator

import pandas as pd
from recalc_engine.calcs.base import BaseCalc
from recalc_engine.core.plans import CalcCoordinate, CalcPlan, ExecutionPlan
from recalc_engine.core.transaction import Transaction
from recalc_engine.sources.definitions import (
    HIERARCHY_LEVEL_TABLES,
    TRANSACTION_TYPES_LANDING_MAPPING,
)
from recalc_engine.sources.dims import load_hierarchy_def


class PipeCompiler:

    def __init__(
        self,
        transaction: Transaction,
        calc_pipe: tuple[type[BaseCalc], ...],
    ):
        self.transaction = transaction
        self.calc_pipe = calc_pipe
        self.planned = {}

    def compile(self) -> ExecutionPlan:
        self.planned = {}
        return ExecutionPlan(tuple(self._plan_execution()))

    def _plan_execution(self) -> Iterator[CalcPlan]:
        for calc in self.calc_pipe:
            output_level = next(
                level
                for level, tables in HIERARCHY_LEVEL_TABLES.items()
                if calc.OUTPUT_MEASURES[1] in tables
            )

            coordinates = dict.fromkeys(
                (
                    self._resolve_hierarchy_level(entity_id)
                    if source_table not in HIERARCHY_LEVEL_TABLES[output_level]
                    else entity_id,
                    output_level,
                    currency_code,
                    (pd.Period(month_date, freq="M") + offset).to_timestamp().date(),
                    stage,
                )
                for entity_id, source_table, currency_code, month_date, stage, offset
                in self._get_triggered_coordinates(calc)
            )

            if coordinates:
                scope = tuple(CalcCoordinate(*coord) for coord in coordinates)
                self.planned[calc.OUTPUT_MEASURES] = scope
                yield CalcPlan(calc, scope)

    def _get_triggered_coordinates(
        self,
        calc: type[BaseCalc],
    ) -> Iterator:
        landing_table = TRANSACTION_TYPES_LANDING_MAPPING[self.transaction.type_]

        for spec in calc.INPUT_MEASURES.values():
            if spec.source_calculator is None and spec.source_table == landing_table:
                source_level = next(
                    level
                    for level, tables in HIERARCHY_LEVEL_TABLES.items()
                    if spec.source_table in tables
                )

                data = self.transaction.data.loc[
                    lambda df: df["measure_type_code"].eq(spec.measure_type_code)
                ]

                if self.transaction.type_ in ("model", "sum_cpp"):
                    data = self._filter_model_acl_data(calc, data)

                for row in data.to_dict("records"):
                    yield (
                        row[source_level],
                        spec.source_table,
                        row["currency_code"],
                        row["month_date"],
                        row["stage"],
                        -spec.mth_offset,
                    )

            elif spec.source_calculator is not None:
                for coordinate in self.planned.get(
                    spec.source_calculator.OUTPUT_MEASURES, ()
                ):
                    yield (
                        coordinate.entity_id,
                        spec.source_table,
                        coordinate.currency_code,
                        coordinate.month_date,
                        coordinate.stage,
                        -spec.mth_offset,
                    )

    @staticmethod
    def _resolve_hierarchy_level(entity_id: int) -> int:
        return load_hierarchy_def().set_index("keyid").at[
            entity_id, "hierarchy_group_id"
        ]

    @staticmethod
    def _filter_model_acl_data(
        calc: type[BaseCalc],
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        return data     # TODO