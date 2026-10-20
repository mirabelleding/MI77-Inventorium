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

    def run(self) -> RecalcResults:
        transaction = Transaction(self.transaction_id)

        pipeline = Pipeline(transaction)
        pipeline.compile()

        return pipeline.execute()
```
---
```python
# core/transaction.py
class Transaction:

    def __init__(self, transaction_id):
        self.uuid = transaction_id
        self.transaction_type = ...
        self.process_month = ...
        self.data = self._get_data()

    def _get_data(self):
        stmt = ... 
        return load_df(stmt)

```
---
```python
#calculations/base.py
class Calculation(ABC):

# set or dict; for handing of cross-mth calculations
    INPUT_MEASURE_TYPES = ...   
    OUTPUT_MEASURE_TYPE = ...

    @abstractmethod
    def if_triggered(self, transaction) -> Bool:
        ...

    @abstractmethod
    def calculate(self, scopes, results):
        pass
```
```python
# actual calculators
class ExampleCalc(Calculation):

    ....

    def if_triggered(self, transaction) -> Bool:

        triggered = transaction.data[
            transaction.data["measure_type_code"]
            .isin(self.TRIGGER_MEASURE_TYPES)
        ]

        return (
            triggered[
                [
                    "key record cols..."
                ]
            ]
            .drop_duplicates()
            .reset_index(drop=True)
        )

    def calculate(self, ..) -> pd.DataFrame:
        ...
        
```
---
```python
#core/execution_plan.py
class ExecutionPlan:

    def __init__(self):
        self.calculations = {}
        self._data_requirements = []

    def add(self, calc, scopes, requirements):
        self.calculations[calc] = scopes

        if requirements is not None and not requirements.empty:
            self._data_requirements.append(requirements)

    def _evaluate_dataset(self):
        supplementary = self._get_supplementary_data()
        self._enrich_scopes(supplementary)

    def _get_supplementary_data(self):

        requirements = pd.concat(
            self._data_requirements,
            ignore_index=True,
        ).drop_duplicates()

        hierarchy_data = ...
        group_data = ...

        return hierarchy_data, group_data

    def _enrich_scopes(self, supplementary):
        ...

```
after pipeline compilations:
```
{
    CalcA(): calc_a_scopes,
    CalcB(): calc_b_scopes,
}
```
---
```python
# core/pipeline.py
class Pipeline:

    PIPE = (
        ....
    )

    def __init__(self, transaction):
        self.transaction = transaction
        self.execution_plan = None


    def compile(self):

        plan = ExecutionPlan()

        for Calc in self.PIPE:
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
        self.table_1 = pd.DataFrame()
        self.table_2 = pd.DataFrame()
        self.table_3 = pd.DataFrame()


    def append(self, target, records):  #e.g. results.append(table_1, records)

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
---
```python
# sources/tables.py
from db_reflection import ...

... = refelct(...)


```
---
```python
# sources/loaders.py
def get_hierarchy_data(...):
    stmt = ...

    return load_df(stmt)


def get_hierarchy_group_data(...):
    stmt = ...

    return load_df(stmt)

```
---
```python
# config/definitions.py

... some mapping
```