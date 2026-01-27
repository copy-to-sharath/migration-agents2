#!/bin/bash

echo "========================================================================"
echo "JCL Parser AST Analysis - Extraction Summary"
echo "========================================================================"
echo

# Initialize counters
total_jobs=0
total_programs=0
total_datasets=0
total_gdg=0
total_errors=0
files_with_jobs=0
files_with_programs=0
files_with_datasets=0
files_with_errors=0

# Create summary file
summary_file="ast_output/extraction_summary.txt"
echo "JCL Parser - Extraction Summary Report" > "$summary_file"
echo "Generated: $(date)" >> "$summary_file"
echo "======================================" >> "$summary_file"
echo >> "$summary_file"

# Process each AST file
for ast_file in ast_output/*.ast; do
    if [ -f "$ast_file" ]; then
        basename_file=$(basename "$ast_file")
        jcl_name="${basename_file%.ast}"
        
        # Count occurrences
        jobs=$(grep -c "job_statement" "$ast_file" 2>/dev/null || echo 0)
        programs=$(grep -c "program_name" "$ast_file" 2>/dev/null || echo 0)
        datasets=$(grep -c "dataset_name" "$ast_file" 2>/dev/null || echo 0)
        gdg=$(grep -c "gdg_dataset" "$ast_file" 2>/dev/null || echo 0)
        errors=$(grep -c "ERROR" "$ast_file" 2>/dev/null || echo 0)
        
        # Extract actual values
        job_names=$(grep -A1 "job_statement" "$ast_file" | grep "name \[" | sed 's/.*name \[[^]]*\] - \[[^]]*\]))//' | head -5)
        program_values=$(grep "program_name \[" "$ast_file" | sed 's/.*program_name \[[^]]*\] - \[[^]]*\]))//' | head -5)
        dataset_values=$(grep "dataset_name \[" "$ast_file" | sed 's/.*dataset_name \[[^]]*\] - \[[^]]*\]))//' | head -5)
        
        # Update totals
        total_jobs=$((total_jobs + jobs))
        total_programs=$((total_programs + programs))
        total_datasets=$((total_datasets + datasets))
        total_gdg=$((total_gdg + gdg))
        total_errors=$((total_errors + errors))
        
        # Update file counts
        if [ $jobs -gt 0 ]; then files_with_jobs=$((files_with_jobs + 1)); fi
        if [ $programs -gt 0 ]; then files_with_programs=$((files_with_programs + 1)); fi
        if [ $datasets -gt 0 ]; then files_with_datasets=$((files_with_datasets + 1)); fi
        if [ $errors -gt 0 ]; then files_with_errors=$((files_with_errors + 1)); fi
        
        # Display results for files with content
        if [ $jobs -gt 0 ] || [ $programs -gt 0 ] || [ $datasets -gt 0 ]; then
            echo "📄 $jcl_name:"
            if [ $jobs -gt 0 ]; then
                echo "  📋 Jobs: $jobs"
            fi
            if [ $programs -gt 0 ]; then
                echo "  🔧 Programs: $programs"
            fi
            if [ $datasets -gt 0 ]; then
                echo "  💾 Datasets: $datasets (GDG: $gdg)"
            fi
            if [ $errors -gt 0 ]; then
                echo "  ⚠️  Parse errors: $errors"
            else
                echo "  ✅ No parse errors"
            fi
            echo
            
            # Write to summary file
            echo "File: $jcl_name" >> "$summary_file"
            echo "  Jobs: $jobs, Programs: $programs, Datasets: $datasets, GDG: $gdg, Errors: $errors" >> "$summary_file"
        fi
    fi
done

# Display summary
echo "========================================================================"
echo "EXTRACTION TOTALS"
echo "========================================================================"
echo
echo "📊 Element Counts:"
echo "  📋 Total Job Statements: $total_jobs (in $files_with_jobs files)"
echo "  🔧 Total Program Names: $total_programs (in $files_with_programs files)"
echo "  💾 Total Dataset Names: $total_datasets (in $files_with_datasets files)"
echo "     Including GDG datasets: $total_gdg"
echo "  ⚠️  Total Parse Errors: $total_errors (in $files_with_errors files)"
echo

# Calculate success metrics
total_files=$(ls -1 ast_output/*.ast 2>/dev/null | wc -l)
perfect_files=$((files_with_jobs - files_with_errors))

echo "📈 Success Metrics:"
echo "  Total AST files: $total_files"
echo "  Files with successful extraction: $files_with_jobs"
echo "  Files with no parse errors: $perfect_files"
echo "  Extraction success rate: $((files_with_jobs * 100 / total_files))%"
echo

# Write summary totals
echo >> "$summary_file"
echo "TOTALS:" >> "$summary_file"
echo "  Jobs: $total_jobs" >> "$summary_file"
echo "  Programs: $total_programs" >> "$summary_file"
echo "  Datasets: $total_datasets" >> "$summary_file"
echo "  GDG Datasets: $total_gdg" >> "$summary_file"
echo "  Parse Errors: $total_errors" >> "$summary_file"

echo "📊 Full report saved to: $summary_file"
echo "✨ Analysis complete!"