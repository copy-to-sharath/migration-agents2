from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Iterable

import pyarrow as pa
import pyarrow.parquet as pq


def write_parquet(
    output_root: Path,
    table_name: str,
    rows: Iterable[dict],
    partition_cols: list[str],
    file_prefix: str | None = None,
) -> None:
    """Write rows to a partitioned parquet dataset.
    
    Args:
        output_root: Root directory for parquet files
        table_name: Name of the table (becomes subdirectory)
        rows: Iterable of row dictionaries
        partition_cols: Columns to partition by (must include run_id, artifact_version)
        file_prefix: Optional prefix for output file (default: table_name).
                     Use unique prefixes when multiple writers may create files
                     in the same partition to avoid overwriting.
    """
    if "run_id" not in partition_cols or "artifact_version" not in partition_cols:
        raise ValueError("partition_cols must include run_id and artifact_version")
    rows_list = list(rows)
    if not rows_list:
        return
    table = pa.Table.from_pylist(rows_list)
    base_path = output_root / table_name
    base_path.mkdir(parents=True, exist_ok=True)
    prefix = file_prefix or table_name
    pq.write_to_dataset(
        table,
        root_path=str(base_path),
        partition_cols=partition_cols,
        basename_template=f"{prefix}-{{i}}.parquet",
        use_dictionary=True,
        compression="zstd",
    )


def dataclass_rows(items: Iterable[object]) -> Iterable[dict]:
    for item in items:
        yield asdict(item)
