```
ECLModelling
    │
    ▼
InputsBuilder
.build()
    ├── data
    ├── PortfolioParamLoader ──► PortfolioParams
    ├── FLACurvesLoader ───────► FLACurves
    ├── ScenarioWeights
    │
    ▼
ModellingInputs
    │
ECLModelling
.calculate()
    │
    ▼
Cascade
.execute() ─┬─ RRMCalculator ──┐
            │                  │
            ▼                  │
            ├─ SIRCalculator ──┤
            │                  │
            ▼                  │
            ├─ FLACalculator ──┤
            │                  │
            ▼                  │
            └─ ECLCalculator ──┤
                               │
                               ▼
                        ModellingResults
                            ├── RRMResults
                            ├── SIRResults
                            ├── FLAResults
                            └── ECLResults
```
```python
# API
ECLModelling(
    data=data,
    params=params,
    fla_curves=fla_curves,
    scenario_weights=scenario_weights,
)
```
---
```
ECLModellingBatch
    │
    ▼
BatchInputs
    │
ECLModellingBatch
.calculate()
    │
    ▼
BatchProcessor
.execute()
    ├── ECLModelling    # multiprocessing
    │   .calculate()
    ▼
BatchOutputsCompiler
.compile()
    │
    ▼
ModellingBatchOutputs
   ├── rrm: DataFrame
   ├── sir: DataFrame
   ├── fla: DataFrame
   └── ecl: DataFrame
```
```python
# API
ECLModellingBatch(
    data=data,
    params=params,
    fla_curves=fla_curves,
    scenario_weights=scenario_weights,
)
```

---
### Class Structures
`ModellingResults`
```
ModellingResults
│
├── rrm: RRMResults
│   ├── historical_balances
│   ├── historical_roll_rates
│   ├── roll_rates_all
│   └── forecast_balances
│
├── sir: SIRResults
│   ├── avg_sir_proportion
│   ├── initial_sir_proportion
│   ├── decay_ratio
│   ├── sir_stg1
│   ├── sir_stg2
│   └── sir_stg3
│
├── fla: FLAResults
│   ├── base_acl_rrm_balances
│   ├── base_acl_sir_forecast
│   │
│   ├── nonfli_acl_rrm_balances
│   ├── nonfli_acl_sir_forecast
│   │
│   ├── opti_acl_rrm_balances
│   ├── opti_acl_sir_forecast
│   │
│   ├── pess_acl_rrm_balances
│   ├── pess_acl_sir_forecast
│   │
│   ├── pessfront_acl_rrm_balances
│   └── pessfront_acl_sir_forecast
│
└── ecl: ECLResults
    ├── ecl_by_scenarios
    └── ecl_loss_rates
```
---
**input dataset construction**
```
select_ecl_input(transaction_id)
│
├── get_hierarchy_ids(transaction_id)
│       └── hierarchy_ids
│
├── get_lag_matrix_cte(hierarchy_ids)
│       ├── wrto_policy_bucket
│       ├── dlq_lag
│       ├── wrto_lag
│       └── rec_lag
│
└── get_hierarchy_ref_cte(hierarchy_ids, lag_matrix_cte)
        ├── hierarchy_id
        └── mth_hierarchy_id
```