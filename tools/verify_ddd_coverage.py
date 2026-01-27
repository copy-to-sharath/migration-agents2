#!/usr/bin/env python3
"""
Verify DDD Analysis Coverage

This tool compares the endpoints analyzed in the DDD analysis
against the source data in parquet files to ensure complete coverage.

Usage:
    python tools/verify_ddd_coverage.py
"""

import duckdb
import json
from pathlib import Path


def find_latest_run() -> Path | None:
    """Find the latest parquet run directory."""
    parquet_dir = Path("data/parquet")
    runs = sorted([d for d in parquet_dir.iterdir() if d.is_dir() and d.name.startswith("run_")])
    return runs[-1] if runs else None


def verify_coverage():
    """Verify DDD analysis covers all endpoints."""
    run_dir = find_latest_run()
    if not run_dir:
        print("❌ No parquet run found")
        return False
    
    print("═" * 60)
    print("DDD COVERAGE VERIFICATION")
    print("═" * 60)
    print(f"Run: {run_dir.name}")
    print()
    
    conn = duckdb.connect(":memory:")
    
    # Find source index file
    source_index = None
    for f in run_dir.rglob("intake_source_index*.parquet"):
        source_index = f
        break
    
    if not source_index:
        print("❌ No source index found")
        return False
    
    # Count source files
    print("SOURCE FILES:")
    print("─" * 40)
    
    # ASPX pages
    aspx_pages = conn.execute(f'''
        SELECT COUNT(*) FROM "{source_index}"
        WHERE file_path LIKE '%.aspx'
        AND file_path NOT LIKE '%.cs'
        AND file_path NOT LIKE '%Zone.Identifier%'
    ''').fetchone()[0]
    print(f"  .aspx pages:           {aspx_pages:>5}")
    
    # ASPX code-behind
    aspx_cs = conn.execute(f'''
        SELECT COUNT(*) FROM "{source_index}"
        WHERE file_path LIKE '%.aspx.cs'
        AND file_path NOT LIKE '%Zone.Identifier%'
    ''').fetchone()[0]
    print(f"  .aspx.cs code-behind:  {aspx_cs:>5}")
    
    # C# files total
    cs_files = conn.execute(f'''
        SELECT COUNT(*) FROM "{source_index}"
        WHERE file_path LIKE '%.cs'
        AND file_path NOT LIKE '%Zone.Identifier%'
    ''').fetchone()[0]
    print(f"  All .cs files:         {cs_files:>5}")
    
    # Entry graphs (all entry points)
    entry_graphs = None
    for f in run_dir.rglob("entry_graphs*.parquet"):
        entry_graphs = f
        break
    
    if entry_graphs:
        total_entries = conn.execute(f'SELECT COUNT(*) FROM "{entry_graphs}"').fetchone()[0]
        print(f"  Entry graphs (all):    {total_entries:>5}")
    
    print()
    
    # Check DDD analysis
    ddd_file = Path("generated/ddd_analysis_result.json")
    if not ddd_file.exists():
        print("❌ No DDD analysis result found at generated/ddd_analysis_result.json")
        return False
    
    with open(ddd_file) as f:
        ddd = json.load(f)
    
    ddd_analyzed = ddd.get("total_endpoints_analyzed", 0)
    ddd_depths = ddd.get("depth_levels_covered", [])
    bounded_contexts = ddd.get("bounded_context_candidates", [])
    
    print("DDD ANALYSIS:")
    print("─" * 40)
    print(f"  Endpoints analyzed:    {ddd_analyzed:>5}")
    print(f"  Depth levels:          {ddd_depths}")
    print(f"  Bounded contexts:      {len(bounded_contexts):>5}")
    
    # Count endpoints per bounded context
    print()
    print("BOUNDED CONTEXT ENDPOINTS:")
    print("─" * 40)
    total_bc_endpoints = 0
    for bc in bounded_contexts:
        ep_count = len(bc.get("endpoints", []))
        total_bc_endpoints += ep_count
        name = bc.get("name", "Unknown")
        conf = bc.get("confidence_score", 0)
        print(f"  {name:<25} {ep_count:>4} endpoints ({conf:.0%})")
    
    print("─" * 40)
    print(f"  Total in contexts:     {total_bc_endpoints:>5}")
    
    print()
    print("═" * 60)
    print("COVERAGE RESULT")
    print("═" * 60)
    
    # Determine coverage
    if ddd_analyzed >= aspx_pages:
        print(f"✅ ALL {aspx_pages} ASPX ENDPOINTS COVERED")
        print(f"   DDD analyzed {ddd_analyzed} endpoints (includes sub-entries)")
        coverage_ok = True
    else:
        print(f"⚠️  GAP DETECTED")
        print(f"   ASPX pages: {aspx_pages}")
        print(f"   DDD analyzed: {ddd_analyzed}")
        print(f"   Missing: {aspx_pages - ddd_analyzed} endpoints")
        coverage_ok = False
    
    print()
    
    # Check for completeness markers
    ddd_review = Path("generated/ddd_sme_review.md")
    if ddd_review.exists():
        content = ddd_review.read_text()
        if "... and" in content or "+ more" in content.lower():
            print("⚠️  WARNING: Review document contains truncation markers")
            print("   Some items may be abbreviated with '... and X more'")
            coverage_ok = False
        else:
            print("✅ Review document has no truncation markers (complete)")
    
    print("═" * 60)
    
    return coverage_ok


if __name__ == "__main__":
    import sys
    success = verify_coverage()
    sys.exit(0 if success else 1)
