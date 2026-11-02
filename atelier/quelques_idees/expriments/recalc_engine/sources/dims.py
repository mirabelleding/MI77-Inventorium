from functools import cache

import pandas as pd


@cache
def load_hierarchy_def() -> pd.DataFrame:
    return pd.DataFrame({
        "keyid": [1, 2, 3, 4, 5,],
        "hierarchy_group_id": [1, 1, 1, 2, 2]
    })