from __future__ import annotations

from abc import ABC
from typing import ClassVar, NamedTuple

import pandas as pd
from recalc_engine.core.coordinates import CalcCoordinate
from recalc_engine.sources.definitions import HIERARCHY_LEVEL_TABLES, HierarchyLevel
from recalc_engine.sources.dims import load_hierarchy_def


class MeasureSpec(NamedTuple):
    measure_type_code: str
    source_table: str
    mth_offset: int
    source_calculator: type[BaseCalc] | None = None


class BaseCalc(ABC):

    INPUT_MEASURES: ClassVar[dict[str, MeasureSpec]]
    FORMULA: ClassVar[str]
    OUTPUT_MEASURES: ClassVar[tuple[str, str]]

    def __init__(self, scope, inputs, results):
        self.scope = scope
        self.inputs = inputs
        self.results = results

    @property
    def data(self) -> pd.DataFrame:
        pivoted = self._pivot(self._filter_eligible_data())

        data = (
            self._resolve_prev_measure_type(pivoted)
            if any(
                spec.mth_offset for spec
                in self.INPUT_MEASURES.values()
                )
            else pivoted
        )

        scope = pd.MultiIndex.from_tuples(
            (
                (getattr(s, self._input_level), s.currency_code, s.stage, name, s.month_date)
                for s in self._input_scope.itertuples(index=False)
                for name in self.INPUT_MEASURES
            ),
            names=[*data.index.names, "month_date"],
        ).unique()

        return (
            data
            .stack(future_stack=True)
            .reindex(scope)
            .unstack("month_date"))

    @property
    def _input_level(self) -> HierarchyLevel:
        levels = {
            level
            for spec in self.INPUT_MEASURES.values()
            for level, tables in HIERARCHY_LEVEL_TABLES.items()
            if spec.source_table in tables
        }

        if len(levels) != 1:
            raise NotImplementedError(
                "Mixed hierarchy-level inputs must be resolved by " \
                "individual calculators."
            )

        return levels.pop()

    @property
    def _input_scope(self) -> pd.DataFrame:
        scope = pd.DataFrame(self.scope, columns=CalcCoordinate._fields)

        if self._input_level != self.scope[0].hierarchy_level:
            scope = (
                scope
                .merge(
                    load_hierarchy_def(),
                    left_on="entity_id",
                    right_on="hierarchy_group_id",
                ).assign(entity_id=lambda df: df["keyid"])
            )

        return (
            scope.rename(columns={"entity_id": self._input_level})
            [[self._input_level, "currency_code", "stage", "month_date"]]
        )

    def _pivot(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.pivot(
            index=[
                self._input_level,
                "currency_code",
                "stage",
                "measure_type_code",
            ],
            columns="month_date",
            values="balance",
        )

    def _filter_eligible_data(self) -> pd.DataFrame:
        level = self._input_level
        scope = self._input_scope

        return (
            pd.concat(
                (
                    getattr(self.inputs, spec.source_table)
                    .loc[
                        lambda df: df["measure_type_code"].eq(spec.measure_type_code)
                    ]
                    .merge(
                        scope.assign(
                            month_date=(
                                pd.PeriodIndex(scope["month_date"], freq="M")
                                + spec.mth_offset
                            ).to_timestamp().date
                        )[[level, "currency_code", "stage", "month_date"]],
                        on=[level, "currency_code", "stage", "month_date"],
                        how="inner",
                    )
                    [[level, "currency_code", "stage",
                    "measure_type_code", "month_date", "balance"]]
                    for spec in self.INPUT_MEASURES.values()
                ),
                ignore_index=True,
            ).drop_duplicates()  # dupes will be produced w/ prev_measure_types
        )

    def _resolve_prev_measure_type(
        self,
        pivoted: pd.DataFrame,
    ) -> pd.DataFrame:
        months = pd.PeriodIndex(pivoted.columns, freq="M")

        return pd.concat(
            [
                pivoted,
                *(
                    pivoted.xs(
                        spec.measure_type_code,
                        level="measure_type_code",
                        drop_level=False,
                    )
                    .set_axis(months, axis=1)
                    .reindex(columns=months + spec.mth_offset)
                    .set_axis(pivoted.columns, axis=1)
                    .rename(
                        index={spec.measure_type_code: name},
                        level="measure_type_code",
                    )
                    for name, spec in self.INPUT_MEASURES.items()
                    if name != spec.measure_type_code
                    or spec.mth_offset != 0
                ),
            ]
        ).sort_index()

    @staticmethod
    def _aggregate_hierarchy_level(
        df: pd.DataFrame,
        input_level: HierarchyLevel,
        output_level: HierarchyLevel,
    ) -> pd.DataFrame:
        return (
            df.merge(
                load_hierarchy_def()[["keyid", output_level]],
                left_on=input_level,
                right_on="keyid",
                validate="many_to_one",
            )
            .drop(columns=[input_level, "keyid"])
            .pipe(
                lambda df: df.groupby(
                    df.columns.drop("balance").tolist(),
                    as_index=False,
                )["balance"].sum()
            )
        )

    def calculate(self) -> pd.DataFrame:
        inputs = {
            name: self.data.xs(name, level="measure_type_code").fillna(0)
            for name in self.INPUT_MEASURES
        }

        result = pd.eval(self.FORMULA, local_dict=inputs)

        scope_index = pd.MultiIndex.from_frame(self._input_scope)

        result = (
            result.stack(future_stack=True)
            .reindex(scope_index)
            .rename("balance")
            .reset_index()
            .assign(measure_type_code=self.OUTPUT_MEASURES[0])
            [
                [
                    *result.index.names,
                    "measure_type_code",
                    "month_date",
                    "balance",
                ]
            ]
        )

        output_level = next(
            level
            for level, tables in HIERARCHY_LEVEL_TABLES.items()
            if self.OUTPUT_MEASURES[1] in tables
        )

        return (
            self._aggregate_hierarchy_level(result, self._input_level, output_level)
            if self._input_level != output_level
            else result
        )