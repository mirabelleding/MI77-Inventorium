```
RecalcEngine
        │
        ▼
   Transaction
        │
        ▼
     Pipeline
   compile() → ExecutionPlan
        │          │
    execute()   ◀──┘
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
│   ├── transaction.py
│   ├── pipeline.py
│
├── calculations/
│   ├── base.py
│   ├── …
│   └── ...
│
├── sources/
│   └── tables.py
│
└── config/
    └── results.py
    └── functions to retrieve data
```
x = RecalcEngine(transaction_id)
