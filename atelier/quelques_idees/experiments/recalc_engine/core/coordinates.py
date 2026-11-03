from __future__ import annotations

from datetime import date
from typing import NamedTuple

from recalc_engine.sources.definitions import HierarchyLevel


class CalcCoordinate(NamedTuple):
    entity_id: int
    hierarchy_level: HierarchyLevel
    currency_code: str
    month_date: date
    stage: str
