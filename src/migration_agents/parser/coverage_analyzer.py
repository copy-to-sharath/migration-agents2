"""Parse coverage analyzer - tracks parsing effectiveness and provides improvement suggestions.

This module analyzes:
1. Parse success/failure rates by language
2. Symbol extraction coverage
3. Call resolution rates (semantic vs hash-based)
4. Provides actionable warnings for improvement
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger("migration_agents.parser.coverage")


@dataclass
class LanguageCoverage:
    """Coverage statistics for a single language."""
    language: str
    total_files: int = 0
    parsed_ok: int = 0
    parsed_error: int = 0
    skipped: int = 0
    
    # Symbol extraction
    symbols_extracted: int = 0
    classes_found: int = 0
    methods_found: int = 0
    fields_found: int = 0
    
    # Call resolution
    calls_total: int = 0
    calls_semantic_resolved: int = 0
    calls_symbol_matched: int = 0
    calls_hash_only: int = 0
    
    # Parse quality
    parse_errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    
    @property
    def parse_rate(self) -> float:
        """Percentage of files successfully parsed."""
        if self.total_files == 0:
            return 0.0
        return (self.parsed_ok / self.total_files) * 100
    
    @property
    def semantic_resolution_rate(self) -> float:
        """Percentage of calls resolved semantically."""
        if self.calls_total == 0:
            return 0.0
        return (self.calls_semantic_resolved / self.calls_total) * 100
    
    @property
    def symbol_resolution_rate(self) -> float:
        """Percentage of calls resolved to actual symbols."""
        if self.calls_total == 0:
            return 0.0
        resolved = self.calls_semantic_resolved + self.calls_symbol_matched
        return (resolved / self.calls_total) * 100


@dataclass
class CoverageReport:
    """Complete coverage report across all languages."""
    languages: dict[str, LanguageCoverage] = field(default_factory=dict)
    
    # Global stats
    total_files: int = 0
    total_parsed: int = 0
    total_errors: int = 0
    total_skipped: int = 0
    
    total_symbols: int = 0
    total_calls: int = 0
    total_resolved: int = 0
    
    # Warnings and suggestions
    critical_warnings: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    
    @property
    def overall_parse_rate(self) -> float:
        if self.total_files == 0:
            return 0.0
        return (self.total_parsed / self.total_files) * 100
    
    @property
    def overall_resolution_rate(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return (self.total_resolved / self.total_calls) * 100


def analyze_parse_audit(audit_rows: list[dict]) -> dict[str, LanguageCoverage]:
    """Analyze parse audit rows to build language coverage."""
    coverage: dict[str, LanguageCoverage] = {}
    
    for row in audit_rows:
        lang = row.get("language", "unknown")
        status = row.get("status", "unknown")
        reason = row.get("reason", "")
        file_path = row.get("file_path", "")
        
        if lang not in coverage:
            coverage[lang] = LanguageCoverage(language=lang)
        
        cov = coverage[lang]
        cov.total_files += 1
        
        if status == "ok":
            cov.parsed_ok += 1
        elif status == "error":
            cov.parsed_error += 1
            if reason:
                cov.parse_errors.append(f"{file_path}: {reason}")
        elif status == "skip":
            cov.skipped += 1
    
    return coverage


def analyze_symbols(symbol_rows: list[dict], coverage: dict[str, LanguageCoverage]) -> None:
    """Analyze symbol extraction by language."""
    for row in symbol_rows:
        file_path = row.get("file_path", "")
        kind = row.get("kind", "")
        
        # Determine language from file extension
        lang = _lang_from_path(file_path)
        if lang not in coverage:
            coverage[lang] = LanguageCoverage(language=lang)
        
        cov = coverage[lang]
        cov.symbols_extracted += 1
        
        if kind in ("class", "interface", "struct", "enum"):
            cov.classes_found += 1
        elif kind in ("method", "function", "subroutine"):
            cov.methods_found += 1
        elif kind in ("field", "property", "variable"):
            cov.fields_found += 1


def analyze_calls(call_rows: list[dict], coverage: dict[str, LanguageCoverage]) -> None:
    """Analyze call resolution effectiveness."""
    for row in call_rows:
        file_path = row.get("file_path", "")
        resolved = row.get("resolved", False)
        receiver = row.get("receiver", "")
        callee_name = row.get("callee_name", "")
        
        lang = _lang_from_path(file_path)
        if lang not in coverage:
            coverage[lang] = LanguageCoverage(language=lang)
        
        cov = coverage[lang]
        cov.calls_total += 1
        
        if resolved:
            cov.calls_semantic_resolved += 1
        elif receiver and receiver[0].isupper():
            # Likely resolved via symbol lookup
            cov.calls_symbol_matched += 1
        else:
            cov.calls_hash_only += 1


def generate_warnings(coverage: dict[str, LanguageCoverage]) -> tuple[list[str], list[str], list[str]]:
    """Generate warnings and suggestions based on coverage analysis."""
    critical: list[str] = []
    warnings: list[str] = []
    suggestions: list[str] = []
    
    for lang, cov in coverage.items():
        # Critical: High parse failure rate
        if cov.total_files > 0 and cov.parse_rate < 80:
            critical.append(
                f"⚠️  {lang}: Only {cov.parse_rate:.1f}% parse success rate "
                f"({cov.parsed_error} errors out of {cov.total_files} files)"
            )
            if cov.parse_errors:
                for err in cov.parse_errors[:3]:  # Show first 3 errors
                    critical.append(f"   └─ {err}")
        
        # Warning: Low symbol extraction
        if cov.parsed_ok > 0 and cov.symbols_extracted == 0:
            warnings.append(
                f"⚡ {lang}: {cov.parsed_ok} files parsed but 0 symbols extracted. "
                f"Check query file: config/queries/{lang}.scm"
            )
        
        # Warning: Low semantic resolution
        if cov.calls_total > 10 and cov.semantic_resolution_rate < 20:
            warnings.append(
                f"🔗 {lang}: Only {cov.semantic_resolution_rate:.1f}% semantic call resolution "
                f"({cov.calls_hash_only} calls using hash-only IDs)"
            )
            suggestions.append(
                f"   → Improve {lang} call resolution by adding receiver capture to "
                f"config/queries/{lang}.calls.scm"
            )
        
        # Suggestion: Missing type info
        if cov.calls_total > 0 and cov.classes_found == 0:
            suggestions.append(
                f"💡 {lang}: No class/type declarations found. "
                f"Add class queries to semantic_resolver.py"
            )
        
        # Suggestion: Missing field types
        if cov.calls_total > 50 and cov.fields_found < 10:
            suggestions.append(
                f"💡 {lang}: Few field declarations ({cov.fields_found}). "
                f"Field type info improves call resolution."
            )
    
    return critical, warnings, suggestions


def _lang_from_path(file_path: str) -> str:
    """Determine language from file path."""
    ext_map = {
        ".cs": "c_sharp",
        ".vb": "vbnet",
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "javascript",
        ".tsx": "typescript",
        ".java": "java",
        ".php": "php",
        ".pl": "perl",
        ".sql": "sql",
        ".html": "html",
        ".htm": "html",
        ".aspx": "html",
        ".ascx": "html",
        ".css": "css",
        ".xml": "xml",
        ".config": "xml",
        ".cbl": "cobol",
        ".cob": "cobol",
        ".jcl": "jcl",
    }
    ext = Path(file_path).suffix.lower()
    return ext_map.get(ext, "unknown")


def build_coverage_report(
    audit_rows: list[dict],
    symbol_rows: list[dict],
    call_rows: list[dict],
) -> CoverageReport:
    """Build comprehensive coverage report."""
    report = CoverageReport()
    
    # Analyze each category
    coverage = analyze_parse_audit(audit_rows)
    analyze_symbols(symbol_rows, coverage)
    analyze_calls(call_rows, coverage)
    
    report.languages = coverage
    
    # Aggregate totals
    for cov in coverage.values():
        report.total_files += cov.total_files
        report.total_parsed += cov.parsed_ok
        report.total_errors += cov.parsed_error
        report.total_skipped += cov.skipped
        report.total_symbols += cov.symbols_extracted
        report.total_calls += cov.calls_total
        report.total_resolved += cov.calls_semantic_resolved + cov.calls_symbol_matched
    
    # Generate warnings
    critical, warnings, suggestions = generate_warnings(coverage)
    report.critical_warnings = critical
    report.warnings = warnings
    report.suggestions = suggestions
    
    return report


def format_coverage_report(report: CoverageReport) -> str:
    """Format coverage report for display."""
    lines = []
    lines.append("=" * 70)
    lines.append("PARSE COVERAGE REPORT")
    lines.append("=" * 70)
    lines.append("")
    
    # Overall stats
    lines.append(f"📊 OVERALL STATISTICS")
    lines.append(f"   Files:    {report.total_parsed}/{report.total_files} parsed "
                 f"({report.overall_parse_rate:.1f}%)")
    lines.append(f"   Errors:   {report.total_errors} files failed to parse")
    lines.append(f"   Skipped:  {report.total_skipped} files (text/binary)")
    lines.append(f"   Symbols:  {report.total_symbols} extracted")
    lines.append(f"   Calls:    {report.total_resolved}/{report.total_calls} resolved "
                 f"({report.overall_resolution_rate:.1f}%)")
    lines.append("")
    
    # Per-language breakdown
    lines.append(f"📈 PER-LANGUAGE BREAKDOWN")
    lines.append("-" * 70)
    lines.append(f"{'Language':<15} {'Files':<10} {'Parse %':<10} {'Symbols':<10} "
                 f"{'Calls':<10} {'Resolved %':<10}")
    lines.append("-" * 70)
    
    for lang, cov in sorted(report.languages.items(), key=lambda x: -x[1].total_files):
        if cov.total_files == 0:
            continue
        lines.append(
            f"{lang:<15} {cov.total_files:<10} {cov.parse_rate:>6.1f}%   "
            f"{cov.symbols_extracted:<10} {cov.calls_total:<10} "
            f"{cov.symbol_resolution_rate:>6.1f}%"
        )
    lines.append("-" * 70)
    lines.append("")
    
    # Critical warnings
    if report.critical_warnings:
        lines.append("🚨 CRITICAL WARNINGS")
        for w in report.critical_warnings:
            lines.append(f"   {w}")
        lines.append("")
    
    # Warnings
    if report.warnings:
        lines.append("⚠️  WARNINGS")
        for w in report.warnings:
            lines.append(f"   {w}")
        lines.append("")
    
    # Suggestions
    if report.suggestions:
        lines.append("💡 SUGGESTIONS FOR IMPROVEMENT")
        for s in report.suggestions:
            lines.append(f"   {s}")
        lines.append("")
    
    lines.append("=" * 70)
    
    return "\n".join(lines)


def log_coverage_summary(report: CoverageReport) -> None:
    """Log coverage summary to logger."""
    LOGGER.info(
        "parse_coverage total_files=%d parsed=%d errors=%d skipped=%d "
        "parse_rate=%.1f%% symbols=%d calls=%d resolved=%d resolution_rate=%.1f%%",
        report.total_files,
        report.total_parsed,
        report.total_errors,
        report.total_skipped,
        report.overall_parse_rate,
        report.total_symbols,
        report.total_calls,
        report.total_resolved,
        report.overall_resolution_rate,
    )
    
    # Log critical warnings
    for w in report.critical_warnings:
        LOGGER.warning(w)
    
    # Log regular warnings
    for w in report.warnings:
        LOGGER.warning(w)
