```
ECLModelling
    │
    ▼            ┌── data: pd.DataFrame
InputsBuilder ───├── PortfolioParamLoader ───▶ PortfolioParams
.build()         ├── FLACurvesLoader ───▶ FLACurves
    │            └── ScenarioWeights
    ▼
ModellingInputs
    │
    ▼
Casacade
.execute() ───▶ RRMCalculator ──┐
                        │       │
                        ▼       │
                SIRCalculator ──┤
                        │       │
                        ▼       │
                FLACalculator ──┤
                        │       │
                        ▼       │
                ECLCalculator ──┤
                                │
                                ▼
                        ModellingResults
                            ├── rrm: RRMResults
                            ├── sir: SIRResults
                            ├── fla: FLAResults
                            └── ecl: ECLResults
```
```
ECLModellingBatch
    │
    ▼
BatchInputs
    │
    ▼
BatchProcessor.execute()
    ├── ECLModelling.calculate()  # multiprocessing
    ▼
BatchOutputsCompiler
.compile()
    │
    ▼
ModellingBatchOutputs
```
---
```
get_hierarchy_ids()
       │
       ▼
get_lag_matrix_cte()
   ├── wrto_policy_bucket
   ├── dlq_lag
   ├── wrto_lag
   └── rec_lag
       │
       ▼
get_hierarchy_ref_cte()
   ├── hierarchy_id
   └── mth_hierarchy_id
       │
       ▼
select_ecl_input()
```