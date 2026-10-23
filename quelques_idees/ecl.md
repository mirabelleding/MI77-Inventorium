```
ECLModelling
    │
    ▼
InputsBuilder
.build()
    │
    │   ┌── data: pd.DataFrame
    └───├── PortfolioParams
        ├── FLACurve
        └── ScenarioWeights
                │
                ▼
            Casacade
            .calculate() ───▶ RRMCalculator ──▶ RRMResults ──┐
                                    │                        │
                                    ▼                        │
                              SIRCalculator ──▶ SIRResults ──┤
                                    │                        │
                                    ▼                        │
                              FLACalculator ──▶ FLAResults ──┤
                                    │                        │
                                    ▼                        │
                              ECLCalculator ──▶ ECLResults ──┤
                                                             │
                                                             │
                                                             ▼
                                                     ModellingResults
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