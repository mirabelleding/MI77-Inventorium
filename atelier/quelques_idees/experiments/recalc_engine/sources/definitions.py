from typing import Literal

type HierarchyLevel = Literal[
    "hierarchy_id",
    "hierarchy_group_id",
]

HIERARCHY_LEVEL_TABLES: dict[HierarchyLevel, list[str]] = {
    "hierarchy_id": ["table_1", "table_2", "table_r_1", "table_r_2",],
    "hierarchy_group_id": ["table_3", "table_r_3"],
}

TRANSACTION_TYPES_LANDING_MAPPING: dict[str, str] = {
    "model": "table_1",
    "sum_cpp": "table_2",
    "provision":"table_3",
}

# TODO: replace