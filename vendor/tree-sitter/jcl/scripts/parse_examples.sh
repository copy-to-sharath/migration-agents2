#!/bin/bash

# Create output directory
mkdir -p ast_output

echo "========================================================================"
echo "JCL Parser - Processing All Example Files"
echo "========================================================================"
echo

# Counter variables
total=0
success=0
failed=0

# Process each JCL file
for file in examples/*.jcl examples/*.JCL examples/jcl/*.jcl examples/jcl/*.JCL; do
    if [ -f "$file" ]; then
        basename_file=$(basename "$file")
        output_file="ast_output/${basename_file%.*}.ast"
        
        echo "Processing: $basename_file"
        
        # Parse the file and save output
        if npx tree-sitter parse "$file" > "$output_file" 2>&1; then
            echo "  ✅ Parsed successfully"
            ((success++))
            
            # Extract some basic info
            jobs=$(grep -o "job_statement" "$output_file" | wc -l)
            progs=$(grep -o "program_name" "$output_file" | wc -l)
            datasets=$(grep -o "dataset_name\|gdg_dataset" "$output_file" | wc -l)
            errors=$(grep -o "ERROR" "$output_file" | wc -l)
            
            if [ $jobs -gt 0 ]; then
                echo "  📋 Jobs found: $jobs"
            fi
            if [ $progs -gt 0 ]; then
                echo "  🔧 Programs found: $progs"
            fi
            if [ $datasets -gt 0 ]; then
                echo "  💾 Datasets found: $datasets"
            fi
            if [ $errors -gt 0 ]; then
                echo "  ⚠️  Errors in AST: $errors"
            fi
        else
            echo "  ❌ Failed to parse"
            ((failed++))
        fi
        
        echo "  📁 AST saved to: $output_file"
        echo
        ((total++))
    fi
done

echo "========================================================================"
echo "PARSING SUMMARY"
echo "========================================================================"
echo
echo "Total files processed: $total"
echo "✅ Successfully parsed: $success"
echo "❌ Failed to parse: $failed"
echo
echo "📊 AST files saved to: ast_output/"
echo
echo "✨ Processing complete!"