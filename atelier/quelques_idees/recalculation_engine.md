```
RecalcEngine
    │
    ▼
Transaction
    │
    ▼
Pipeline
.compile() ──▶ ExecutionPlan
    │              │
.execute()         │
    │              │
    ▼              │
  CalcA            │
  CalcB ◀──────────┘
  CalcC
   ....
    │
    ▼
ResultsCollector
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
│   ├── transaction.py
│   ├── pipeline.py
│   ├── execution_plan.py
    ├── collector.py
│   └── results.py
│
├── calculations/
│   ├── base.py
│   ├── ...
│   └── ...
│
└── config/
    └── definitions.py

```
```python
# API
RecalcEngine(transaction_id)
```

---
```python
# recalc.py
class RecalcEngine:

    def __init__(self, uuid):
        self.uuid = uuid

    def run(self) -> RecalcResults:
        self.transaction = Transaction(self.uuid)
        self.execution_plan = Pipeline(transaction).compile()

        return pipeline.execute(self.execution_plan)
```
---
```python
# core/transaction.py
class Transaction:

    def __init__(self, transaction_id):
        self.transaction_id = transaction_id
        self.transaction_type = ...
        self.process_month = ...
        self.data = self._get_data()

```
---
```python
#calculations/base.py
class Calculation(ABC):

# set or dict; for handing of cross-mth calculations
    INPUT_MEASURE_TYPES = {
        "measure_a": "...",
        "measure_b": "...",
        "beginning_measure": "...", # handling mth-offset calculations
    }
    OUTPUT_MEASURE_TYPE = {
        "measure_type": "...",
        "table": "...",
    }

    @abstractmethod
    def if_triggered(self, transaction) -> Bool:
        ...

    @abstractmethod
    def calculate(self, scopes, results):
        pass
```
```python
# actual calculators
class CalcA(Calculation):

    @property
    def is_triggered(self, transaction) -> Bool:
        ...

    def calculate(self, ..) -> pd.DataFrame:
        ...

```
---
```python
#core/execution_plan.py
class ExecutionPlan:

    def __init__(self):
        self.calculations = {}

    def _evaluate_scope(self):
        ...

    def _get_supplementary_data(self):
        ...

    def construct_dataset(self):
        ...groupby(hierarchy_id, stage).getgroup(...)

    def build(self):
        ...

"""
after pipeline compilations:
{
    CalcA(): calc_a_scopes: DataFrame,
    CalcB(): calc_b_scopes: DataFrame,
}

"""
```
---
```python
# core/pipeline.py
class Pipeline:

    PIPE = [
        CalcA,
        CalcB,
        ...
    ]

    def __init__(self, transaction):
        self.transaction = transaction

    def compile(self):
        ...
        return execution_plan

    def execute(self):
        results = RecalcResults()

        for calc, scopes in (
            self.execution_plan.calculations.items()
        ):
            records = calc.calculate(
                scopes=scopes,
                results=results,
            )
            results.append(
                calc.OUTPUT_MEASURE_TYPE["table"],
                records,
            )
        return results
```
---
```python
# core/collector.o=pt
class ResultsCollector:

    def __init__(self):
        .....
        self.result = RecalcResults()

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
```python
# core/results.py
@dataclass
class RecalcResults:
    table_1: pd.DataFrame()
    table_2: pd.DataFrame()
    table_3: pd.DataFrame()
```
---
```python
# config/definitions.py

... some mapping and table instances
```