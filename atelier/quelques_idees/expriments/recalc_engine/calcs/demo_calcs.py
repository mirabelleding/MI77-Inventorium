from typing import ClassVar

import pandas as pd
from recalc_engine.sources.dims import load_hierarchy_def

from .base import BaseCalc, MeasureSpec


class CalcA(BaseCalc):  # have a mth offset

    INPUT_MEASURES: ClassVar= {
        "measure_1": MeasureSpec("measure_1", "table_1", 0),
        "measure_1_prev": MeasureSpec("measure_1", "table_1", -1),
        "measure_2": MeasureSpec("measure_2", "table_1", 0),
    }

    FORMULA: ClassVar = "measure_1 - measure_1_prev + measure_2"

    OUTPUT_MEASURES: ClassVar = ("measure_a", "table_r_1")


class CalcB(BaseCalc):  # from different tables

    INPUT_MEASURES: ClassVar= {
        "measure_3": MeasureSpec("measure_3", "table_1", 0),
        "measure_4": MeasureSpec("measure_4", "table_2", 0),
    }

    FORMULA = "measure_3 + measure_4"

    OUTPUT_MEASURES = ("measure_b", "table_r_1")


class CalcC(BaseCalc):  # having a dependent calculator

    INPUT_MEASURES: ClassVar= {
        "measure_5": MeasureSpec("measure_1", "table_2", 0),
        "measure_a": MeasureSpec("measure_a", "table_r_1", 0, CalcA),
        "measure_b": MeasureSpec("measure_b", "table_r_1", 0, CalcB),
    }

    FORMULA = "measure_5 - measure_b + measure_a"

    OUTPUT_MEASURES = ("measure_c", "table_r_2")


class CalcD(BaseCalc):  # group_level normal

    INPUT_MEASURES: ClassVar= {
        "measure_5": MeasureSpec("measure_5", "table_3", 0),
        "measure_6": MeasureSpec("measure_6", "table_3", 0),
    }

    FORMULA = "measure_5 + measure_6"

    OUTPUT_MEASURES = ("measure_d", "table_r_3")


class CalcE(BaseCalc):  # i/o diff level

    INPUT_MEASURES: ClassVar= {
        "measure_1": MeasureSpec("measure_1", "table_1", 0),
        "measure_2": MeasureSpec("measure_2", "table_1", 0),
        "measure_3": MeasureSpec("measure_3", "table_1", 0),
    }

    FORMULA = "measure_1 + measure_2 + measure_3"

    OUTPUT_MEASURES = ("measure_e", "table_r_3")
