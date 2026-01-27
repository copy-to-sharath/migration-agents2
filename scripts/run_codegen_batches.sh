#!/bin/bash
# Batch processing script for NopCommerce code generation
# Total slices: 33,941
# Batch size: 500
# Total batches: 68

set -e

BATCH_SIZE=500
TOTAL_SLICES=33941
BATCH_NUM=1

echo "=== Starting batch code generation ==="
echo "Total slices: $TOTAL_SLICES"
echo "Batch size: $BATCH_SIZE"

for ((i=0; i<TOTAL_SLICES; i+=BATCH_SIZE)); do
    echo ""
    echo "=== Batch $BATCH_NUM: Processing slices $i to $((i+BATCH_SIZE)) ==="
    
    # Update config with current offset
    python3 -c "
import json
with open('config/codegen.json', 'r') as f:
    config = json.load(f)
config['slice_offset'] = $i
config['max_slices'] = $BATCH_SIZE
with open('config/codegen.json', 'w') as f:
    json.dump(config, f, indent=4)
"
    
    # Run codegen
    python -m migration_agents.codegen.main --config config/codegen.json --generate-code
    
    echo "=== Batch $BATCH_NUM complete ==="
    ((BATCH_NUM++))
done

echo ""
echo "=== All batches complete! ==="
echo "Generated files:"
find generated/NopCommerce -type f -name "*.cs" | wc -l
echo "C# files"
find generated/NopCommerce -type f -name "*.feature" | wc -l
echo "Feature files"
