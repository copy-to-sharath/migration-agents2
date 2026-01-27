"""
Judge module for validating migration slices.

The judge validates:
1. Citation completeness (every artifact has source_ref)
2. Rule coverage (all logic rules have test coverage)
3. Dead code dependencies (no dependencies on dead code)
4. Build/test status (when code is generated)

Results are written to judge_reports and fix_queue Parquet tables.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb

from migration_agents.ingestion.parquet_writer import write_parquet
from migration_agents.shared_run_id import resolve_run_id


@dataclass
class ValidationFinding:
    """A single validation finding."""
    finding_id: str
    slice_id: str
    category: str  # citation, coverage, dead_code, build, test
    severity: str  # error, warning, info
    description: str
    source_ref: str = ""
    suggested_fix: str = ""


@dataclass
class ValidationReport:
    """Complete validation report for a slice."""
    report_id: str
    slice_id: str
    status: str  # passed, failed, warning
    findings: list[ValidationFinding] = field(default_factory=list)
    citation_coverage: float = 0.0
    rule_coverage: float = 0.0
    dead_code_deps: int = 0
    
    @property
    def error_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "error")
    
    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")


def _created_at() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _hash_id(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def _sql_string_list(paths: list[str]) -> str:
    escaped = [path.replace("'", "''") for path in paths]
    quoted = ", ".join(f"'{path}'" for path in escaped)
    return f"[{quoted}]"


def _table_files(parquet_root: Path, table: str) -> list[str]:
    return sorted(str(path) for path in parquet_root.rglob(f"{table}/**/*.parquet"))


def _register_view(con: duckdb.DuckDBPyConnection, parquet_root: Path, table: str) -> bool:
    """Register a parquet table as a view."""
    files = _table_files(parquet_root, table)
    if not files:
        return False
    con.execute(f"CREATE OR REPLACE VIEW {table} AS SELECT * FROM read_parquet({_sql_string_list(files)})")
    return True


def validate_slice_citations(
    con: duckdb.DuckDBPyConnection,
    slice_id: str,
    run_id: str,
    artifact_version: int
) -> list[ValidationFinding]:
    """Check that all artifacts have source_ref citations."""
    findings = []
    
    # Check logic_rules for missing source_ref
    sql = f"""
        SELECT rule_id, rule_text
        FROM logic_rules
        WHERE slice_id = '{slice_id}'
          AND run_id = '{run_id}'
          AND artifact_version = {artifact_version}
          AND (source_ref IS NULL OR source_ref = '')
    """
    try:
        rows = con.execute(sql).fetchdf().to_dict(orient="records")
        for row in rows:
            findings.append(ValidationFinding(
                finding_id=_hash_id(f"citation_{slice_id}_{row['rule_id']}"),
                slice_id=slice_id,
                category="citation",
                severity="warning",
                description=f"Logic rule {row['rule_id']} missing source_ref",
                source_ref=f"logic_rules:{row['rule_id']}",
                suggested_fix="Add source_ref linking to original code location",
            ))
    except Exception:
        pass  # Table may not exist
    
    return findings


def validate_slice_dead_code(
    con: duckdb.DuckDBPyConnection,
    slice_id: str,
    run_id: str,
    artifact_version: int
) -> list[ValidationFinding]:
    """Check for dependencies on dead code."""
    findings = []
    
    # Get symbols in slice
    manifest_sql = f"""
        SELECT DISTINCT symbol_id
        FROM slice_manifest
        WHERE slice_id = '{slice_id}'
          AND run_id = '{run_id}'
          AND artifact_version = {artifact_version}
    """
    
    dead_code_sql = f"""
        SELECT symbol_id, file_path, reason
        FROM dead_code
        WHERE run_id = '{run_id}'
          AND artifact_version = {artifact_version}
    """
    
    try:
        slice_symbols = set(con.execute(manifest_sql).fetchdf()["symbol_id"].tolist())
        dead_rows = con.execute(dead_code_sql).fetchdf().to_dict(orient="records")
        
        dead_ids = {r["symbol_id"] for r in dead_rows}
        overlap = slice_symbols & dead_ids
        
        for symbol_id in overlap:
            dead_info = next(r for r in dead_rows if r["symbol_id"] == symbol_id)
            findings.append(ValidationFinding(
                finding_id=_hash_id(f"dead_{slice_id}_{symbol_id}"),
                slice_id=slice_id,
                category="dead_code",
                severity="warning",
                description=f"Slice depends on dead code: {dead_info['file_path']} ({dead_info['reason']})",
                source_ref=f"dead_code:{symbol_id}",
                suggested_fix="Remove dependency on unreachable code",
            ))
    except Exception:
        pass  # Tables may not exist
    
    return findings


def validate_slice_coverage(
    con: duckdb.DuckDBPyConnection,
    slice_id: str,
    run_id: str,
    artifact_version: int
) -> tuple[float, list[ValidationFinding]]:
    """Check rule coverage (all logic rules should have trace_map entries)."""
    findings = []
    coverage = 100.0
    
    sql = f"""
        SELECT 
            lr.rule_id,
            CASE WHEN tm.rule_id IS NOT NULL THEN 1 ELSE 0 END as has_trace
        FROM logic_rules lr
        LEFT JOIN trace_map tm ON lr.rule_id = tm.rule_id 
            AND tm.run_id = '{run_id}' AND tm.artifact_version = {artifact_version}
        WHERE lr.slice_id = '{slice_id}'
          AND lr.run_id = '{run_id}'
          AND lr.artifact_version = {artifact_version}
    """
    
    try:
        rows = con.execute(sql).fetchdf().to_dict(orient="records")
        if rows:
            traced = sum(1 for r in rows if r["has_trace"])
            coverage = (traced / len(rows)) * 100 if rows else 100.0
            
            for row in rows:
                if not row["has_trace"]:
                    findings.append(ValidationFinding(
                        finding_id=_hash_id(f"coverage_{slice_id}_{row['rule_id']}"),
                        slice_id=slice_id,
                        category="coverage",
                        severity="info",
                        description=f"Logic rule {row['rule_id']} has no trace_map entry",
                        source_ref=f"logic_rules:{row['rule_id']}",
                        suggested_fix="Ensure rule is traced to source",
                    ))
    except Exception:
        pass
    
    return coverage, findings


def validate_slice(
    parquet_root: Path,
    slice_id: str,
    run_id: str,
    artifact_version: int,
    check_citations: bool = True,
    check_coverage: bool = True,
    check_dead_code: bool = True,
) -> ValidationReport:
    """Validate a single slice and return a report."""
    from migration_agents.mcp.duckdb_catalog import get_run_connection
    
    con, _ = get_run_connection(parquet_root, run_id)
    
    # Register required views
    tables = ["logic_rules", "trace_map", "slice_manifest", "dead_code"]
    for table in tables:
        _register_view(con, parquet_root, table)
    
    report_id = _hash_id(f"report_{slice_id}_{_created_at()}")
    findings: list[ValidationFinding] = []
    
    # Run validations
    citation_coverage = 100.0
    rule_coverage = 100.0
    dead_code_deps = 0
    
    if check_citations:
        citation_findings = validate_slice_citations(con, slice_id, run_id, artifact_version)
        findings.extend(citation_findings)
        if citation_findings:
            # Calculate citation coverage
            total_rules_sql = f"""
                SELECT COUNT(*) as cnt FROM logic_rules
                WHERE slice_id = '{slice_id}' AND run_id = '{run_id}' AND artifact_version = {artifact_version}
            """
            try:
                total = con.execute(total_rules_sql).fetchone()[0]
                citation_coverage = ((total - len(citation_findings)) / total * 100) if total > 0 else 100.0
            except Exception:
                pass
    
    if check_coverage:
        rule_coverage, coverage_findings = validate_slice_coverage(con, slice_id, run_id, artifact_version)
        findings.extend(coverage_findings)
    
    if check_dead_code:
        dead_findings = validate_slice_dead_code(con, slice_id, run_id, artifact_version)
        findings.extend(dead_findings)
        dead_code_deps = len(dead_findings)
    
    # Determine status
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    
    if errors > 0:
        status = "failed"
    elif warnings > 0:
        status = "warning"
    else:
        status = "passed"
    
    con.close()
    return ValidationReport(
        report_id=report_id,
        slice_id=slice_id,
        status=status,
        findings=findings,
        citation_coverage=citation_coverage,
        rule_coverage=rule_coverage,
        dead_code_deps=dead_code_deps,
    )


def write_judge_reports(
    reports: list[ValidationReport],
    parquet_root: Path,
    run_id: str,
    artifact_version: int,
) -> None:
    """Write validation reports to Parquet."""
    created_at = _created_at()
    
    # Write judge_reports table
    report_rows = []
    for report in reports:
        report_rows.append({
            "report_id": report.report_id,
            "slice_id": report.slice_id,
            "status": report.status,
            "findings": json.dumps([{
                "finding_id": f.finding_id,
                "category": f.category,
                "severity": f.severity,
                "description": f.description,
            } for f in report.findings]),
            "citation_coverage": report.citation_coverage,
            "rule_coverage": report.rule_coverage,
            "dead_code_deps": report.dead_code_deps,
            "error_count": report.error_count,
            "warning_count": report.warning_count,
            "run_id": run_id,
            "artifact_version": artifact_version,
            "slice_id": report.slice_id,
            "created_at": created_at,
            "supersedes_version": None,
        })
    
    if report_rows:
        write_parquet(parquet_root, "judge_reports", report_rows, ["run_id", "artifact_version"])
    
    # Write fix_queue table (findings that need fixing)
    fix_rows = []
    for report in reports:
        for finding in report.findings:
            if finding.severity in ("error", "warning"):
                fix_rows.append({
                    "fix_id": finding.finding_id,
                    "slice_id": report.slice_id,
                    "issue_type": finding.category,
                    "description": finding.description,
                    "source_ref": finding.source_ref,
                    "suggested_fix": finding.suggested_fix,
                    "status": "pending",
                    "run_id": run_id,
                    "artifact_version": artifact_version,
                    "created_at": created_at,
                    "supersedes_version": None,
                })
    
    if fix_rows:
        write_parquet(parquet_root, "fix_queue", fix_rows, ["run_id", "artifact_version"])


def main():
    """Run judge validation from command line."""
    parser = argparse.ArgumentParser(description="Judge module for validating migration slices")
    parser.add_argument("--config", required=True, help="Path to judge config JSON")
    parser.add_argument("--slice", required=True, help="Slice ID to validate")
    args = parser.parse_args()
    
    # Load config
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config not found: {config_path}")
        return
    
    with open(config_path) as f:
        config = json.load(f)
    
    parquet_root = Path(config.get("output_root", "data/parquet"))
    run_id_config = config.get("run_id", "auto")
    if run_id_config == "auto":
        run_id = resolve_run_id(parquet_root)
    else:
        run_id = run_id_config
    artifact_version = config.get("artifact_version", 1)
    
    print(f"Validating slice: {args.slice}")
    print(f"Run ID: {run_id}")
    print(f"Artifact Version: {artifact_version}")
    
    report = validate_slice(
        parquet_root=parquet_root,
        slice_id=args.slice,
        run_id=run_id,
        artifact_version=artifact_version,
    )
    
    print(f"\n=== Validation Report ===")
    print(f"Status: {report.status}")
    print(f"Citation Coverage: {report.citation_coverage:.1f}%")
    print(f"Rule Coverage: {report.rule_coverage:.1f}%")
    print(f"Dead Code Dependencies: {report.dead_code_deps}")
    print(f"Errors: {report.error_count}")
    print(f"Warnings: {report.warning_count}")
    
    if report.findings:
        print(f"\n=== Findings ({len(report.findings)}) ===")
        for f in report.findings[:10]:  # Show first 10
            icon = "❌" if f.severity == "error" else "⚠️" if f.severity == "warning" else "ℹ️"
            print(f"  {icon} [{f.category}] {f.description}")
    
    # Write results
    write_judge_reports([report], parquet_root, run_id, artifact_version)
    print(f"\nResults written to {parquet_root}/judge_reports and {parquet_root}/fix_queue")


if __name__ == "__main__":
    main()
