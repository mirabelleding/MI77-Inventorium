```
RecalcEngine
    │
    ▼
Transaction
    │
    ▼
RecalcQueues
    ├── ib: tuple[Transaction, ...] ─┐
    └── cb: tuple[Transaction, ...] ─┤
                                 RecalcEngine
                                 .run()
                                     │
                                     ▼
                                 Pipeline
                                 .compile() ──▶ PipeCompiler ──▶ ExecutionPlan
                                     │                               │
                                 .execute() ◀───────┬────────────────┘
                                     │              │
                                     │              ▼
                                     ├◀───── ExecutionInputs
                                     ▼           │    ├── table_1: DataFrame
                                   CalcA ─┐      │    ├── table_2: DataFrame
                                   CalcB ─┼◀─────┘    ├── table_3: DataFrame
                                   CalcC ─┤           ├── table_r_1: DataFrame
                                    ...  ─┘           └── ...
                                     │
                                     ▼
                                 RecalcResults
                                     ├── table_r_1: DataFrame
                                     ├── table_r_2: DataFrame
                                     ├── table_r_3: DataFrame
                                     └── ...
```

`ExecutionPlan` Class Structure
```
ExecutionPlan
.plan
   └── tuple[CalcPlan, ...]
                ├── calculator: type[BaseCalc]
                └── scope: tuple[CalcCoordinate, ...]
                                    ├── entity_id
                                    ├── currency_code
                                    ├── month_date
                                    └── stage
```
```python
# API
RecalcEngine(transaction_1, transaction_2,...)

recalc.transactions
recalc.queues.ib
recalc.queues.cb
recalc.results.table_a
recalc.results.table_b
...
```