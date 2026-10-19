```
   RecalcEngine
        │
        ▼
   Transaction
        │
        ▼
     Pipeline
    .compile() ──▶ ExecutionPlan
    .execute() ◀────────┘
        │
        ▼
 Calculations
        │
        ▼
 RecalcResults
   ├── table_a: DataFrame
   ├── table_b: DataFrame
   └── table_c: DataFrame
```

```
recalc_engine/
│
├── recalc.py             
│
├── core/
│   ├── __init__.py
│   ├── transaction.py             
│   ├── pipeline.py                 
│   ├── execution_plan.py           
│   └── results.py                  
│
├── calculations/
│   ├── base.py
│   ├── ...
│   └── ...
│
├── sources/
│   ├── tables.py             
│   └── loaders.py 
│
└── config/
    └── definitions.py
```
RecalcEngine(transaction_id)


---
```python
# recalc.py
from .core.transaction import Transaction
from .core.pipeline import Pipeline


class RecalcEngine:

    def __init__(self, transaction_id):
        self.transaction_id = transaction_id

    def run(self):
        transaction = Transaction(self.transaction_id)

        pipeline = Pipeline(transaction)
        pipeline.compile()

        return pipeline.execute()
```
---
```python
# core/transaction.py
from sqlalchemy import select

from your_db_package import load_df
from ..sources.tables import TRANSACTION_TABLE


class Transaction:

    def __init__(self, transaction_id):
        self.id = transaction_id

        self.data = self._get_data()

        self.transaction_type = ...
        self.process_mode = ...
        self.process_month = ...

    def _get_data(self):
        stmt = (
            select(TRANSACTION_TABLE)
            .where(
                TRANSACTION_TABLE.c.transaction_id
                == self.id
            )
        )

        return load_df(stmt)
```
---
```python
#calculations/base.py
from abc import ABC, abstractmethod


class Calculation(ABC):

    INPUT_MEASURE_TYPES = set()
    OUTPUT_MEASURE_TYPE = None

    @abstractmethod
    def get_scopes(self, transaction):
        ...

    @abstractmethod
    def get_data_requirements(self, scopes):
        ...

    @abstractmethod
    def calculate(self, scopes, results):
        ...
```
```python
# actual calculators
from .base import Calculation


class ExampleCalc(Calculation):

    TRIGGER_MEASURE_TYPES = {
        "A",
        "B",
    }

    RESULT_ATTR = "example"

    def get_scopes(self, transaction):

        triggered = transaction.data[
            transaction.data["measure_type"]
            .isin(self.TRIGGER_MEASURE_TYPES)
        ]

        return (
            triggered[
                [
                    "hierarchy_id",
                    "stage",
                    "currency",
                    "month_date",
                ]
            ]
            .drop_duplicates()
            .reset_index(drop=True)
        )

    def get_data_requirements(self, scopes):
        # Example:
        # Calculation also needs historical measure C

        requirements = scopes.copy()
        requirements["measure_type"] = "C"

        return requirements

    def calculate(self, scopes, results):

        # At this point `scopes` has ALREADY been
        # enriched with supplementary data.

        # Can also consume earlier calculation results:
        previous = results.some_other_table

        records = ...

        return records
```
---
```python
#core/execution_plan.py
from ..sources.loaders import (
    get_hierarchy_data,
    get_hierarchy_group_data,
)

class ExecutionPlan:

    def __init__(self):
        self.calculations = {}
        self._data_requirements = []

    def add(self, calc, scopes, requirements):
        self.calculations[calc] = scopes

        if requirements is not None and not requirements.empty:
            self._data_requirements.append(requirements)

    def prepare(self):
        supplementary = self._get_supplementary_data()
        self._enrich_scopes(supplementary)

    def _get_supplementary_data(self):

        requirements = pd.concat(
            self._data_requirements,
            ignore_index=True,
        ).drop_duplicates()

        hierarchy_req = requirements[
            requirements["hierarchy_id"].notna()
        ]

        group_req = requirements[
            requirements["hierarchy_group_id"].notna()
        ]

        hierarchy_data = ...
        group_data = ...

        return hierarchy_data, group_data

    def _enrich_scopes(self, supplementary):
        ...
```
after compilations:
```
{
    ModelACLCalc(): model_acl_scopes,
    ImpairmentCalc(): impairment_scopes,
}
```
---
```python
# core/pipeline.py
from .execution_plan import ExecutionPlan
from .results import RecalcResults

from ..calculations.model_acl import ModelACLCalc
from ..calculations.os import OSCalc
from ..calculations.impairment import ImpairmentCalc


class Pipeline:

    CALCULATIONS = (
        ModelACLCalc,
        OSCalc,
        ImpairmentCalc,
    )

    def __init__(self, transaction):
        self.transaction = transaction
        self.execution_plan = None


    def compile(self):

        plan = ExecutionPlan()

        for Calc in self.CALCULATIONS:
            calc = Calc()

            scopes = calc.get_scopes(
                self.transaction
            )

            if scopes.empty:
                continue

            requirements = calc.get_data_requirements(
                scopes
            )

            plan.add(
                calc=calc,
                scopes=scopes,
                requirements=requirements,
            )

        plan.prepare()

        self.execution_plan = plan

        return plan

    def execute(self):

        results = RecalcResults()

        for calc, scopes in (
            self.execution_plan.calculations.items()
        ):
            records = calc.calculate(
                scopes=scopes,
                results=results,
            )

            results.add(
                calc.RESULT_ATTR,
                records,
            )

        return results
```
---
```python
# core/results.py
class RecalcResults:

    def __init__(self):
        self.ecl_result = pd.DataFrame()
        self.model_acl_output = pd.DataFrame()
        self.master_forecast = pd.DataFrame()


    def add(self, target, records):

        if records is None or records.empty:
            return

        current = getattr(self, target)

        setattr(
            self,
            target,
            pd.concat(
                [current, records],
                ignore_index=True,
            ),
        )
```
```python
# example
results.add("model_acl", records)
# updates
results.model_acl
```
---
```python
# sources/tables.py
from db_reflection import ...
TRANSACTION_TABLE = refelct(...)
......
```
---
```python
# sources/loaders.py
from sqlalchemy import select

from db_reflection import load_df

from .tables import (
    HIERARCHY_SOURCE,
    HIERARCHY_GROUP_SOURCE,
)


def get_hierarchy_data(requirements):
    stmt = (
        select(HIERARCHY_SOURCE)
        .where(...)
    )

    return load_df(stmt)


def get_hierarchy_group_data(requirements):
    stmt = (
        select(HIERARCHY_GROUP_SOURCE)
        .where(...)
    )

    return load_df(stmt)

```
---
```python
# config/definitions.py
MODEL_TYPE_MEASURES = {
    "TYPE_A": {...},
    "TYPE_B": {...},
}

TRANSACTION_TYPE_LEVEL = {
    "model_upload": "hierarchy_id",
    "group_upload": "hierarchy_group_id",
}

```