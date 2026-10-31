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

`ExecutionPlan` Class Structure
```
ExecutionPlan
.plan
   └── tuple[CalcPlan]
                ├── calculator: type[BaseCalc]
                └── scope
                    ├── entity_id
                    ├── currency_code
                    ├── month_date
                    └── stage
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
        ...
```
---
```python
# core/transaction.py
@dataclass
class Transaction:
    transaction_id: str | UUID
    transaction_type: str | None = None
    process_month: date | None = None
    data: pd.DataFrame | None = None

```
---
```python
#calculations/base.py
class BaseCalc(ABC):
    def __init__(self, scope, working_data):
        self.scope = scope
        self._working_data = working_data

    @property
    def data(self):
        ...

    @abstractmethod
    def calculate(self):
        ...

```
```python
# actual calculators
class CalcB(BaseCalc):
    TIGGER_MEASURE = {measure_1: (0, table_1), measure_2: (-1, table_2)} # handle mth offset
    CASADE_DEPENDENCY= {(CalcA, 0),(CalcC, -1)} #handle mth off-set

    OUTPUT_MEASURE ={}
    TARGET_TABLE = {}

   def calculate():
    ....

```
---
```python
#core/plan.py
class Scope(NamedTuple):
    entity_id: int
    currency_code: str
    month_date: date
    stage: str


@dataclass(frozen=True)
class CalcPlan:
    calculator: type[BaseCalc]
    scope: tuple[int, str, date]


@dataclass
class ExecutionPlan:
    plan: tuple[CalcPlan]

    def __iter__(self) -> Iterator[CalcPlan]:
        return iter(self.plan)

    def __len__(self) -> int:
        return len(self.plan)

    def __getitem__(
        self,
        calculator: type[BaseCalc]
    ) -> tuple[Scope, ...]:
        return tuple(
            item.scope
            for item in self.plan
            if item.calculator is calculator
        )
#------------ or also support str retrieval
    def __getitem__(
        self,
        key: type[BaseCalc] | str,
    ) -> tuple[Scope, ...]:
        return tuple(
            item.scope
            for item in self.plan
            if (
                item.calculator.__name__ == key
                if isinstance(key, str)
                else item.calculator is key
            )
        )

```
---
```python
class Pipeline:
  PIPE = [CalcA, CalcB,...]

  def compile() -> ExecutionPlan:

  def execute() -> RecalcResults:
     #iter through ExecutionPlan , fetch supplementary data and run the Calcs
```
---
```python
@dataclass
class RecalcResults:
    table_1: pd.DataFrame()
    table_2: pd.DataFrame()
    table_3: pd.DataFrame()
```