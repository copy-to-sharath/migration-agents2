#!/usr/bin/env python3
"""
Link ASPX event handlers to C# code-behind methods.
This creates call edges from ASPX controls to their event handlers.
"""
import duckdb
import hashlib
from pathlib import Path

con = duckdb.connect()
run_id = "run_20260120155302"
path = f'data/parquet/{run_id}/stage_1'

print('Linking ASPX event handlers to C# code-behind methods...\n')

# Load C# methods and calculate their "callee_id" if they were called by name
# callee_id format: sha256(f"{name}:0:callee")
print('1. Finding C# methods and generating potential callee IDs...')
cs_callees = con.execute(f"""
    SELECT 
        symbol_id,
        name,
        file_path as cs_file,
        line as cs_line,
        sha256(name || ':0:callee') as virtual_callee_id
    FROM read_parquet('{path}/symbols/**/*.parquet')
    WHERE kind IN ('Method', 'method') 
""").fetchdf()
print(f"Found {len(cs_callees)} C# methods.")

# Load ASPX calls
print('2. Loading ASPX event handler calls...')
aspx_calls = con.execute(f"""
    SELECT 
        caller_id,
        callee_id,
        file_path as aspx_file,
        line as aspx_line
    FROM read_parquet('{path}/calls/**/*.parquet')
    WHERE file_path LIKE '%.aspx' OR file_path LIKE '%.ascx'
""").fetchdf()
print(f"Found {len(aspx_calls)} ASPX calls.")

# Join
print('3. Matching calls to methods...')
matches = aspx_calls.merge(cs_callees, left_on='callee_id', right_on='virtual_callee_id', how='inner')

# Filter to only code-behind files
print('4. Filtering to code-behind files only...')
def is_code_behind(aspx_path: str, cs_path: str) -> bool:
    """Check if cs_path is the code-behind for aspx_path"""
    aspx_name = Path(aspx_path).stem  # e.g., "Account" from "Account.aspx"
    cs_name = Path(cs_path).name      # e.g., "Account.aspx.cs"
    
    # Check if C# file is code-behind for ASPX file
    # Patterns: Account.aspx -> Account.aspx.cs, Account.aspx.designer.cs, Account.cs
    return (
        cs_name.startswith(f"{aspx_name}.aspx.") or
        cs_name.startswith(f"{aspx_name}.ascx.") or
        cs_name.startswith(f"{aspx_name}.master.") or
        cs_name == f"{aspx_name}.cs"
    )

matches['is_code_behind'] = matches.apply(lambda row: is_code_behind(row['aspx_file'], row['cs_file']), axis=1)
filtered_matches = matches[matches['is_code_behind']]

print(f"\nFound {len(matches)} total matches (before filtering)")
print(f"Found {len(filtered_matches)} filtered links (code-behind only)")

if len(filtered_matches) > 0:
    print('\nSample Filtered Links:')
    for _, row in filtered_matches.head(10).iterrows():
        print(f"  {row['aspx_file'].split('/')[-1]}:{row['aspx_line']} -> {row['cs_file'].split('/')[-1]}:{row['cs_line']} ({row['name']})")
    
    # Export to parquet
    print('\n5. Exporting edges to parquet...')
    output_path = f'{path}/aspx_edges'
    edges_df = filtered_matches[['caller_id', 'callee_id', 'aspx_file', 'aspx_line', 'cs_file', 'cs_line', 'name']].copy()
    edges_df['from_id'] = filtered_matches['caller_id']
    edges_df['to_id'] = filtered_matches['symbol_id']
    edges_df['edge_type'] = 'aspx_event_handler'
    edges_df['run_id'] = run_id
    edges_df['artifact_version'] = 1
    
    final_export = edges_df[['from_id', 'to_id', 'edge_type', 'run_id', 'artifact_version']]
    con.execute(f"COPY final_export TO '{output_path}' (FORMAT PARQUET, PARTITION_BY (run_id, artifact_version), OVERWRITE_OR_IGNORE)")
    print(f"✓ Exported {len(final_export)} edges to {output_path}")
