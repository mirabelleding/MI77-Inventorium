```python
# batch/model.py
from __future__ import annotations

import multiprocessing as mp
from collections.abc import Sequence
from functools import partial

import pandas as pd


class ECLModellingBatch:

    def __init__(
        self,
        hierarchy_ids: Sequence[int],
        data: pd.DataFrame,
        params: pd.DataFrame,
        fla: pd.DataFrame,
        sgwt: pd.DataFrame,
    ) -> None:
        self.hierarchy_ids = hierarchy_ids
        self.data = data
        self.params = params
        self.fla = fla
        self.sgwt = sgwt

    def _load_inputs(
        self,
    ) -> tuple[tuple[pd.DataFrame, pd.DataFrame], ...]:
        data_groups = self.data.groupby("hierarchy_id")
        param_groups = self.params.groupby("hierarchy_id")

        return tuple(
            (
                data_groups.get_group(hierarchy_id),
                param_groups.get_group(hierarchy_id),
            )
            for hierarchy_id in self.hierarchy_ids
        )

    @staticmethod
    def _run_model(
        model_inputs: tuple[pd.DataFrame, pd.DataFrame],
        *,
        fla: pd.DataFrame,
        sgwt: pd.DataFrame,
    ) -> ModellingResults:
        data, params = model_inputs

        model = ECLModelling(
            data=data,
            params=params,
            fla=fla,
            sgwt=sgwt,
        )

        model.calculate()

        return model.results

    def _execute_models(self) -> dict[int, ModellingResults]:
        if not self.hierarchy_ids:
            return {}

        model = partial(
            self._run_model,
            fla=self.fla,
            sgwt=self.sgwt,
        )

        with mp.Pool(
            processes=min(
                mp.cpu_count(),
                len(self.hierarchy_ids),
            )
        ) as pool:
            results = pool.map(
                model,
                self._load_inputs(),
            )

        return dict(zip(self.hierarchy_ids, results))

    def calculate(self) -> ECLModellingOutputs:
        return ECLModellingOutputs(
            raw=self._execute_models(),
        )
```
---
```python
# batch/outputs
class ECLModellingOutputs:

    def __init__(
        self,
        raw: dict[int, ModellingResults],
    ) -> None:
        self.__raw = raw

    @property
    def historical_roll_rates(self) -> pd.DataFrame:
        pass

    @property
    def forecast_rrm(self) -> pd.DataFrame:
        pass

    @property
    def fla_rrm(self) -> pd.DataFrame:
        pass

    @property
    def ecl_final_output(self) -> pd.DataFrame:
        pass

```