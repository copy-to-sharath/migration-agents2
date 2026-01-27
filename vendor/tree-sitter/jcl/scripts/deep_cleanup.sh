#!/bin/bash

# Deep cleanup script for tree-sitter-jcl project
# Removes redundant test files and scripts

echo "======================================"
echo "Deep Cleanup - Removing Redundant Files"
echo "======================================"
echo

# Track what we remove
removed_count=0

# 1. Remove redundant JavaScript test files
echo "🔍 Analyzing JavaScript files..."

# parse_all_examples.js - redundant, functionality replaced by bash script
if [ -f "parse_all_examples.js" ]; then
    echo "  ❌ Removing parse_all_examples.js (replaced by scripts/parse_examples.sh)"
    rm -f parse_all_examples.js
    ((removed_count++))
fi

# test/validate_all_jcl.js - redundant validation script
if [ -f "test/validate_all_jcl.js" ]; then
    echo "  ❌ Removing test/validate_all_jcl.js (validation integrated in main tests)"
    rm -f test/validate_all_jcl.js
    ((removed_count++))
fi

# test/real_jcl.test.js - basic pattern matching, not using tree-sitter
if [ -f "test/real_jcl.test.js" ]; then
    echo "  ❌ Removing test/real_jcl.test.js (basic regex tests, not tree-sitter)"
    rm -f test/real_jcl.test.js
    ((removed_count++))
fi

# 2. Remove redundant Python analysis scripts
echo
echo "🔍 Analyzing Python scripts..."

# analyze_extraction.py - old analysis script, replaced by jcl_extractor.py
if [ -f "analyze_extraction.py" ]; then
    echo "  ❌ Removing analyze_extraction.py (functionality in jcl_extractor.py)"
    rm -f analyze_extraction.py
    ((removed_count++))
fi

# create_extraction_report.py - old report generator, integrated in jcl_extractor.py
if [ -f "create_extraction_report.py" ]; then
    echo "  ❌ Removing create_extraction_report.py (reporting in jcl_extractor.py)"
    rm -f create_extraction_report.py
    ((removed_count++))
fi

# 3. Remove generated output files
echo
echo "🔍 Checking for generated output files..."

if [ -f "jcl_extraction_results.json" ]; then
    echo "  ❌ Removing jcl_extraction_results.json (generated output)"
    rm -f jcl_extraction_results.json
    ((removed_count++))
fi

if [ -f "jcl_extraction_summary.csv" ]; then
    echo "  ❌ Removing jcl_extraction_summary.csv (generated output)"
    rm -f jcl_extraction_summary.csv
    ((removed_count++))
fi

# 4. Clean up old cleanup scripts
echo
echo "🔍 Consolidating cleanup scripts..."

if [ -f "cleanup_project.sh" ]; then
    echo "  ❌ Removing cleanup_project.sh (replaced by this script)"
    rm -f cleanup_project.sh
    ((removed_count++))
fi

# 5. Remove empty directories
echo
echo "🔍 Removing empty directories..."

# Remove ast_output if empty
if [ -d "ast_output" ] && [ -z "$(ls -A ast_output)" ]; then
    echo "  ❌ Removing empty ast_output directory"
    rmdir ast_output
    ((removed_count++))
fi

# 6. Keep only essential files
echo
echo "📋 Essential files being kept:"
echo "  ✅ grammar.js - Core parser grammar"
echo "  ✅ package.json - Node configuration"
echo "  ✅ jcl_extractor.py - Main extraction tool"
echo "  ✅ test/corpus/*.txt - Tree-sitter test cases"
echo "  ✅ test/basic.test.js - Core parser tests"
echo "  ✅ scripts/*.sh - Utility scripts"
echo "  ✅ examples/jcl/*.jcl - JCL samples"
echo "  ✅ *.md - Documentation"

# 7. Final report
echo
echo "======================================"
echo "📊 Cleanup Summary"
echo "======================================"
echo "  Files removed: $removed_count"
echo

# Show remaining structure
echo "📁 Remaining project structure:"
echo "  Core files: $(find . -name "*.js" -not -path "./node_modules/*" -not -path "./src/*" | wc -l) JavaScript"
echo "  Python tools: $(find . -name "*.py" -not -path "./bindings/*" | wc -l) Python"
echo "  Test corpus: $(find test/corpus -name "*.txt" | wc -l) test files"
echo "  Bash scripts: $(find scripts -name "*.sh" 2>/dev/null | wc -l) scripts"
echo "  Documentation: $(find . -name "*.md" | wc -l) markdown files"
echo "  JCL examples: $(find examples -name "*.jcl" -o -name "*.JCL" | wc -l) samples"

echo
echo "✨ Deep cleanup complete!"
echo
echo "Next steps:"
echo "  1. Run 'npx tree-sitter test' to verify parser tests"
echo "  2. Run 'python3 jcl_extractor.py' to test extraction"
echo "  3. The project is now minimal and focused"