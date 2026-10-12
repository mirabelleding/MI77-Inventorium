# loader.py
from pathlib import Path

import pandas as pd


def load_hierarchy(path: str | Path) -> pd.DataFrame:
    return pd.read_excel(path)


def load_stage_measure(path: str | Path) -> pd.DataFrame:
    return pd.read_excel(path)


def load_data_workbook(
    path: str | Path,
) -> dict[str, pd.DataFrame]:
    return pd.read_excel(
        path,
        sheet_name=None,
    )

# dims.py
from dataclasses import dataclass

import pandas as pd


@dataclass
class Dimensions:
    hierarchy_id_dim: pd.DataFrame
    hierarchy_group_dim: pd.DataFrame
    stage_measure_dim: pd.DataFrame


def build_dimensions(
    hierarchy_raw: pd.DataFrame,
    stage_measure_raw: pd.DataFrame,
) -> Dimensions:

    return Dimensions(
        hierarchy_id_dim=_build_hierarchy_id_dim(
            hierarchy_raw
        ),
        hierarchy_group_dim=_build_hierarchy_group_dim(
            hierarchy_raw
        ),
        stage_measure_dim=_build_stage_measure_dim(
            stage_measure_raw
        ),
    )


def _build_hierarchy_id_dim(
    df: pd.DataFrame,
) -> pd.DataFrame:
    ...


def _build_hierarchy_group_dim(
    df: pd.DataFrame,
) -> pd.DataFrame:
    ...


def _build_stage_measure_dim(
    df: pd.DataFrame,
) -> pd.DataFrame:
    ...


# data_pipe.py
from dataclasses import dataclass

import pandas as pd

from .dims import Dimensions


@dataclass
class DataPipeResult:
    datasets: dict[str, pd.DataFrame]
    rejected: pd.DataFrame
    process_months: list[pd.Timestamp]

def process_data(
    sheets: dict[str, pd.DataFrame],
    dims: Dimensions,
    max_process_month: str | pd.Timestamp | None = None,
) -> DataPipeResult:

    process_months = _resolve_process_months(
        sheets,
        max_process_month=max_process_month,
    )

    sheets = _trim_process_months(
        sheets,
        process_months,
    )

    df = _combine_sheets(sheets)

    df = _normalize_data(df)

    rejected = []

    df, invalid = _validate_hierarchy(
        df,
        dims,
    )
    rejected.append(invalid)

    df, invalid = _validate_stage_measure(
        df,
        dims,
    )
    rejected.append(invalid)

    df = _deduplicate(df)

    df = _transform_data(
        df,
        dims,
    )

    datasets = _build_output_datasets(
        df,
        dims,
    )

    rejected_df = pd.concat(
        rejected,
        ignore_index=True,
    )

    return DataPipeResult(
        datasets=datasets,
        rejected=rejected_df,
        process_months=process_months,
    )


def _validate_hierarchy(
    df: pd.DataFrame,
    dims: Dimensions,
) -> tuple[pd.DataFrame, pd.DataFrame]:

    valid_mask = ...

    valid = df.loc[valid_mask].copy()
    rejected = df.loc[~valid_mask].copy()

    rejected["rejection_reason"] = (
        "Hierarchy not found in dimension"
    )

    return valid, rejected


def _validate_stage_measure(
    df: pd.DataFrame,
    dims: Dimensions,
) -> tuple[pd.DataFrame, pd.DataFrame]:

    valid_mask = ...

    valid = df.loc[valid_mask].copy()
    rejected = df.loc[~valid_mask].copy()

    rejected["rejection_reason"] = (
        "Stage/measure combination not found in dimension"
    )

    return valid, rejected


def _resolve_process_months(
    sheets: dict[str, pd.DataFrame],
    max_process_month=None,
) -> list[pd.Timestamp]:
    ...


def _trim_process_months(
    sheets: dict[str, pd.DataFrame],
    process_months: list[pd.Timestamp],
) -> dict[str, pd.DataFrame]:
    ...



# xlsx_writer.py
from pathlib import Path

import pandas as pd

from .dims import Dimensions

def add_control_sheet(
    writer: pd.ExcelWriter,
    df: pd.DataFrame,
) -> None:
    ...

def _write_workbook(
    df: pd.DataFrame,
    path: Path,
) -> None:

    with pd.ExcelWriter(path) as writer:

        df.to_excel(
            writer,
            sheet_name="Data",
            index=False,
        )

        add_control_sheet(
            writer,
            df,
        )

def _append_process_months(
    df: pd.DataFrame,
    process_months: list[pd.Timestamp],
) -> pd.DataFrame:

    df = df.copy()

    for month in process_months:
        df[month] = ...

    return df


def write_dimensions(
    dims: Dimensions,
    process_months: list[pd.Timestamp],
    output_dir: str | Path,
) -> None:

    output_dir = Path(output_dir)

    hierarchy_id = _append_process_months(
        dims.hierarchy_id_dim,
        process_months,
    )

    hierarchy_group = _append_process_months(
        dims.hierarchy_group_dim,
        process_months,
    )

    stage_measure = _append_process_months(
        dims.stage_measure_dim,
        process_months,
    )

    _write_workbook(
        hierarchy_id,
        output_dir / "hierarchy_id_dim.xlsx",
    )

    _write_workbook(
        hierarchy_group,
        output_dir / "hierarchy_group_dim.xlsx",
    )

    _write_workbook(
        stage_measure,
        output_dir / "stage_measure_dim.xlsx",
    )

def write_rejected(
    rejected: pd.DataFrame,
    output_dir: str | Path,
) -> None:

    if rejected.empty:
        return

    _write_workbook(
        rejected,
        Path(output_dir) / "rejected_records.xlsx",
    )


# migrator.py

