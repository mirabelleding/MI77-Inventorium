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
                                     ▼              │
                                   CalcA ─┐         │
                                   CalcB ─┼◀────────┘
                                   CalcC ─┤
                                    ...  ─┘
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