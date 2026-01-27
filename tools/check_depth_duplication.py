#!/usr/bin/env python3
"""
Check if nodes appear as targets across multiple depth levels.
Target nodes should only appear at their shortest depth.
"""
import os
from pathlib import Path
from collections import defaultdict

# Get all depth directories
depth_dir = Path("generated/graphs/by_depth")
depths = sorted([d for d in depth_dir.iterdir() if d.is_dir() and d.name.startswith("depth_")])

# Extract target nodes from each depth
depth_targets = {}
for depth_path in depths:
    depth_name = depth_path.name
    targets = set()
    
    for dot_file in depth_path.glob("*.dot"):
        # Extract target node (part before "_from_")
        filename = dot_file.stem
        if "_from_" in filename:
            target = filename.split("_from_")[0]
            targets.add(target)
    
    depth_targets[depth_name] = targets
    print(f"{depth_name}: {len(targets)} unique target nodes")

print("\n" + "="*80)
print("CHECKING FOR DUPLICATES ACROSS DEPTHS")
print("="*80)

# Check for duplicates
all_seen = set()
duplicates_found = False

for depth_name in sorted(depth_targets.keys()):
    targets = depth_targets[depth_name]
    
    # Find targets that were already seen in earlier depths
    duplicates = targets & all_seen
    
    if duplicates:
        duplicates_found = True
        print(f"\n❌ {depth_name}: Found {len(duplicates)} nodes that already appeared in earlier depths:")
        for dup in sorted(list(duplicates)[:10]):  # Show first 10
            # Find which earlier depth(s) it appeared in
            earlier_depths = []
            for earlier_depth in sorted(depth_targets.keys()):
                if earlier_depth == depth_name:
                    break
                if dup in depth_targets[earlier_depth]:
                    earlier_depths.append(earlier_depth)
            print(f"   - {dup} (also in: {', '.join(earlier_depths)})")
        if len(duplicates) > 10:
            print(f"   ... and {len(duplicates) - 10} more")
    else:
        print(f"✓ {depth_name}: No duplicates with earlier depths")
    
    all_seen.update(targets)

if not duplicates_found:
    print("\n" + "="*80)
    print("✓ SUCCESS: No target nodes appear in multiple depth levels!")
    print("="*80)
else:
    print("\n" + "="*80)
    print("❌ ISSUE: Some nodes appear as targets in multiple depth levels")
    print("="*80)
