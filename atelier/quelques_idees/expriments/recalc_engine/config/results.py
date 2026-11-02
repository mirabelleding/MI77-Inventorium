from __future__ import annotations

from dataclasses import dataclass, field, fields

import pandas as pd
from recalc_engine.calcs.base import BaseCalc


@dataclass
class RecalcResults:
    table_r_1: pd.DataFrame = field(default_factory=pd.DataFrame)
    table_r_2: pd.DataFrame = field(default_factory=pd.DataFrame)
    table_r_3: pd.DataFrame = field(default_factory=pd.DataFrame)

    def collect(
        self,
        calculator: type[BaseCalc],
        outputs: pd.DataFrame,
    ) -> None:
        table = calculator.OUTPUT_MEASURES[1]

        setattr(
            self,
            table,
            pd.concat(
                (getattr(self, table), outputs),
                ignore_index=True,
            ),
        )

    @classmethod
    def consolidate(cls, *results: RecalcResults) -> RecalcResults:
        return cls(**{
            f.name: pd.concat(
                (getattr(result, f.name) for result in results),
                ignore_index=True,
            )
            for f in fields(cls)
        })