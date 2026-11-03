from dataclasses import dataclass
from datetime import date
from functools import cached_property
from uuid import UUID

import pandas as pd


@dataclass
class Transaction:
    uuid: str | UUID

    def __post_init__(self):
        self.division, self.type_, self.process_month = self._get_metadata()

    def _get_metadata(self) -> tuple[str, str, date]:
        return tuple(
            demo_tx_table.set_index("uuid")
            .loc[str(self.uuid), ["division", "type", "process_mth"]]   #TODO: replace
        )

    @cached_property
    def data(self) -> pd.DataFrame:
        return _demo_data(self.uuid)    #TODO: replace


#-------- some demo table
from recalc_engine.demo_data.generator import generate_demo_table
from recalc_engine.sources.definitions import TRANSACTION_TYPES_LANDING_MAPPING

demo_tx_table = pd.DataFrame(
    {
        "uuid": ["tx_1", "tx_2", "tx_3", "tx_4"],
        "division":["IB", "IB", "CB", "CB"],
        "process_mth": [date(2026, 1, 1)] * 4,
        "type": ["model", "provision"] *2,
    }
)

def _demo_data(tx_id: str) -> pd.DataFrame:
    tx_type = demo_tx_table.set_index("uuid").at[tx_id, "type"]

    return generate_demo_table(
        TRANSACTION_TYPES_LANDING_MAPPING[tx_type],
        n_rows=5,
    ).assign(transaction_id=tx_id)
