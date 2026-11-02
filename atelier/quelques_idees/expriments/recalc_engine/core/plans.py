from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from recalc_engine.calcs.base import BaseCalc
from recalc_engine.core.coordinates import CalcCoordinate


@dataclass(frozen=True)
class CalcPlan:
    calculator: type[BaseCalc]
    scope: tuple[CalcCoordinate, ...]


@dataclass
class ExecutionPlan:
    plan: tuple[CalcPlan, ...]

    def __iter__(self) -> Iterator[CalcPlan]:
        return iter(self.plan)

    def __len__(self) -> int:
        return len(self.plan)

    def __getitem__(
        self,
        calculator: type[BaseCalc]
    ) -> tuple[CalcPlan, ...]:
        return tuple(
            item.scope
            for item in self.plan
            if item.calculator is calculator
        )