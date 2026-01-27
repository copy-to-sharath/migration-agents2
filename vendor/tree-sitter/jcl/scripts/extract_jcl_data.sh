#!/bin/bash

# JCL Data Extraction Tool
# Simple bash script to extract job, program, and dataset information from JCL files

usage() {
    echo "Usage: $0 <jcl_file> [output_format]"
    echo "  jcl_file: Path to JCL file to analyze"
    echo "  output_format: json|text|csv (default: text)"
    echo ""
    echo "Examples:"
    echo "  $0 examples/READCARD.jcl"
    echo "  $0 examples/READCARD.jcl json"
    echo "  $0 examples/READCARD.jcl csv > output.csv"
    exit 1
}

extract_names_from_ast() {
    local ast_content="$1"
    local pattern="$2"
    local jcl_file="$3"
    
    # Extract positions and then get actual text from JCL file
    echo "$ast_content" | grep "$pattern" | while read -r line; do
        if [[ $line =~ \[([0-9]+),\ ([0-9]+)\]\ -\ \[([0-9]+),\ ([0-9]+)\] ]]; then
            start_line=${BASH_REMATCH[1]}
            start_col=${BASH_REMATCH[2]}
            end_line=${BASH_REMATCH[3]}
            end_col=${BASH_REMATCH[4]}
            
            # Extract text (adding 1 to line numbers as sed is 1-based)
            actual_line=$((start_line + 1))
            text=$(sed -n "${actual_line}p" "$jcl_file" | cut -c$((start_col + 1))-$((end_col)))
            echo "$text"
        fi
    done
}

# Check arguments
if [ $# -lt 1 ]; then
    usage
fi

JCL_FILE="$1"
OUTPUT_FORMAT="${2:-text}"

if [ ! -f "$JCL_FILE" ]; then
    echo "Error: File '$JCL_FILE' not found"
    exit 1
fi

# Parse the JCL file
AST_OUTPUT=$(npx tree-sitter parse "$JCL_FILE" 2>&1)

# Extract job names
JOB_NAMES=()
while IFS= read -r line; do
    if [ -n "$line" ]; then
        JOB_NAMES+=("$line")
    fi
done < <(echo "$AST_OUTPUT" | grep -A1 "job_statement" | grep "name \[" | sed 's/.*name \[[0-9]*, [0-9]*\] - \[[0-9]*, [0-9]*\])//' | sed 's/^[ \t]*//')

# Extract program names
PROGRAM_NAMES=()
while IFS= read -r line; do
    if [ -n "$line" ]; then
        PROGRAM_NAMES+=("$line")
    fi
done < <(extract_names_from_ast "$AST_OUTPUT" "program_name" "$JCL_FILE")

# Extract dataset names
DATASET_NAMES=()
while IFS= read -r line; do
    if [ -n "$line" ]; then
        DATASET_NAMES+=("$line")
    fi
done < <(extract_names_from_ast "$AST_OUTPUT" "dataset_name" "$JCL_FILE")

# Extract GDG datasets
GDG_DATASETS=()
while IFS= read -r line; do
    if [ -n "$line" ]; then
        GDG_DATASETS+=("$line")
    fi
done < <(extract_names_from_ast "$AST_OUTPUT" "gdg_dataset" "$JCL_FILE")

# Count errors
ERROR_COUNT=$(echo "$AST_OUTPUT" | grep -c "ERROR" || echo 0)

# Output based on format
case $OUTPUT_FORMAT in
    json)
        echo "{"
        echo "  \"file\": \"$JCL_FILE\","
        echo "  \"jobs\": ["
        for i in "${!JOB_NAMES[@]}"; do
            if [ $i -eq $((${#JOB_NAMES[@]} - 1)) ]; then
                echo "    \"${JOB_NAMES[$i]}\""
            else
                echo "    \"${JOB_NAMES[$i]}\","
            fi
        done
        echo "  ],"
        echo "  \"programs\": ["
        for i in "${!PROGRAM_NAMES[@]}"; do
            if [ $i -eq $((${#PROGRAM_NAMES[@]} - 1)) ]; then
                echo "    \"${PROGRAM_NAMES[$i]}\""
            else
                echo "    \"${PROGRAM_NAMES[$i]}\","
            fi
        done
        echo "  ],"
        echo "  \"datasets\": ["
        for i in "${!DATASET_NAMES[@]}"; do
            if [ $i -eq $((${#DATASET_NAMES[@]} - 1)) ]; then
                echo "    \"${DATASET_NAMES[$i]}\""
            else
                echo "    \"${DATASET_NAMES[$i]}\","
            fi
        done
        echo "  ],"
        echo "  \"gdg_datasets\": ["
        for i in "${!GDG_DATASETS[@]}"; do
            if [ $i -eq $((${#GDG_DATASETS[@]} - 1)) ]; then
                echo "    \"${GDG_DATASETS[$i]}\""
            else
                echo "    \"${GDG_DATASETS[$i]}\","
            fi
        done
        echo "  ],"
        echo "  \"parse_errors\": $ERROR_COUNT"
        echo "}"
        ;;
        
    csv)
        echo "Type,Value"
        for job in "${JOB_NAMES[@]}"; do
            echo "JOB,$job"
        done
        for prog in "${PROGRAM_NAMES[@]}"; do
            echo "PROGRAM,$prog"
        done
        for ds in "${DATASET_NAMES[@]}"; do
            echo "DATASET,$ds"
        done
        for gdg in "${GDG_DATASETS[@]}"; do
            echo "GDG_DATASET,$gdg"
        done
        ;;
        
    text|*)
        echo "==================== JCL Data Extraction ===================="
        echo "File: $JCL_FILE"
        echo ""
        
        if [ ${#JOB_NAMES[@]} -gt 0 ]; then
            echo "📋 Jobs (${#JOB_NAMES[@]}):"
            for job in "${JOB_NAMES[@]}"; do
                echo "  - $job"
            done
            echo ""
        fi
        
        if [ ${#PROGRAM_NAMES[@]} -gt 0 ]; then
            echo "🔧 Programs (${#PROGRAM_NAMES[@]}):"
            for prog in "${PROGRAM_NAMES[@]}"; do
                echo "  - $prog"
            done
            echo ""
        fi
        
        if [ ${#DATASET_NAMES[@]} -gt 0 ]; then
            echo "💾 Datasets (${#DATASET_NAMES[@]}):"
            for ds in "${DATASET_NAMES[@]}"; do
                echo "  - $ds"
            done
            echo ""
        fi
        
        if [ ${#GDG_DATASETS[@]} -gt 0 ]; then
            echo "📁 GDG Datasets (${#GDG_DATASETS[@]}):"
            for gdg in "${GDG_DATASETS[@]}"; do
                echo "  - $gdg"
            done
            echo ""
        fi
        
        if [ $ERROR_COUNT -gt 0 ]; then
            echo "⚠️  Parse errors: $ERROR_COUNT"
        else
            echo "✅ No parse errors"
        fi
        echo "=============================================================="
        ;;
esac