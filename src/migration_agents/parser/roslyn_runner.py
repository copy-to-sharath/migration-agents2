from __future__ import annotations

import json
import subprocess
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path

import pyarrow.dataset as ds


@dataclass(frozen=True)
class RoslynResult:
    symbols: list[dict]
    calls: list[dict]
    conditions: list[dict]
    constants: list[dict]
    data_access: list[dict]


def run_roslyn(
    command: list[str],
    file_path: Path,
    timeout_sec: int,
    use_parquet: bool = True,
) -> RoslynResult:
    """
    Contract: command writes a JSON file to stdout with keys:
    symbols, calls, conditions, constants, data_access.
    """
    if use_parquet:
        parquet_dir = Path(tempfile.mkdtemp(prefix="roslyn_parquet_"))
        cmd = [*command, "--format", "parquet", "--output", str(parquet_dir), str(file_path)]
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=timeout_sec)
        try:
            payload = _load_parquet_payload(parquet_dir)
            return payload
        except (FileNotFoundError, ValueError) as exc:
            # Fall back to JSON mode below.
            print(f"roslyn_parquet_load_failed: {exc}", flush=True)
    output_file = Path(tempfile.gettempdir()) / f"roslyn_{uuid.uuid4().hex}.json"
    result = subprocess.run(
        [*command, "--output", str(output_file), str(file_path)],
        check=True,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
    )
    payload: dict
    try:
        with output_file.open("r", encoding="utf-8") as f:
            payload = json.load(f)
    except FileNotFoundError:
        payload = json.loads(result.stdout)
    finally:
        try:
            output_file.unlink(missing_ok=True)
        except OSError as exc:
            print(f"roslyn_json_cleanup_failed: {exc}", flush=True)
    symbols = payload.get("symbols", payload.get("Symbols", []))
    calls = payload.get("calls", payload.get("Calls", []))
    conditions = payload.get("conditions", payload.get("Conditions", []))
    constants = payload.get("constants", payload.get("Constants", []))
    data_access = payload.get("data_access", payload.get("DataAccess", []))
    return RoslynResult(
        symbols=symbols,
        calls=calls,
        conditions=conditions,
        constants=constants,
        data_access=data_access,
    )


def _load_parquet_payload(parquet_dir: Path) -> RoslynResult:
    latest_file = parquet_dir / "LATEST_RUN"
    if latest_file.exists():
        run_id = latest_file.read_text(encoding="utf-8").strip()
    else:
        runs = sorted(p.name for p in parquet_dir.iterdir() if p.is_dir())
        if not runs:
            raise FileNotFoundError("No parquet runs found")
        run_id = runs[-1]
    # Roslyn outputs to stage_1, not step_2
    base = parquet_dir / run_id / "stage_1"

    def _read_table(name: str) -> list[dict]:
        table_dir = base / name
        if not table_dir.exists():
            return []
        try:
            table = ds.dataset(table_dir, format="parquet").to_table()
            return table.to_pylist()
        except Exception as exc:  # noqa: BLE001
            print(f"roslyn_parquet_read_failed table={name} error={exc}", flush=True)
            return []

    return RoslynResult(
        symbols=_read_table("symbols"),
        calls=_read_table("calls"),
        conditions=_read_table("conditions"),
        constants=_read_table("constants"),
        data_access=_read_table("data_access"),
    )


def load_roslyn_parquet(parquet_root: Path, run_id: str | None = None) -> RoslynResult:
    if run_id:
        base = parquet_root / run_id / "stage_1"
    else:
        latest_file = parquet_root / "LATEST_RUN"
        if latest_file.exists():
            run_id = latest_file.read_text(encoding="utf-8").strip()
        else:
            runs = sorted(p.name for p in parquet_root.iterdir() if p.is_dir())
            if not runs:
                raise FileNotFoundError(f"No runs found under {parquet_root}")
            run_id = runs[-1]
        # Roslyn outputs to stage_1, not step_2
        base = parquet_root / run_id / "stage_1"

    def _read_table(name: str) -> list[dict]:
        table_dir = base / name
        if not table_dir.exists():
            return []
        table = ds.dataset(table_dir, format="parquet").to_table()
        return table.to_pylist()

    return RoslynResult(
        symbols=_read_table("symbols"),
        calls=_read_table("calls"),
        conditions=_read_table("conditions"),
        constants=_read_table("constants"),
        data_access=_read_table("data_access"),
    )
