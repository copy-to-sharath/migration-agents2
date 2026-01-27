#!/usr/bin/env python3
"""
JCL Data Extractor - Practical tool for extracting job, program, and dataset information from JCL files

This tool demonstrates how to use the tree-sitter JCL parser to extract:
- Job names from JOB statements
- Program names from EXEC statements  
- Dataset names from DD statements (including GDG datasets)
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict

class JCLExtractor:
    """Extract job, program, and dataset information from JCL files"""
    
    def __init__(self):
        # Updated pattern to better capture job names from job_statement nodes
        self.job_pattern = re.compile(r'\(job_statement.*?\(name \[(\d+), (\d+)\] - \[(\d+), (\d+)\]\)', re.DOTALL)
        self.program_pattern = re.compile(r'\(program_name \[(\d+), (\d+)\] - \[(\d+), (\d+)\]\)', re.MULTILINE)
        self.dataset_pattern = re.compile(r'\(dataset_name \[(\d+), (\d+)\] - \[(\d+), (\d+)\]\)', re.MULTILINE)
        self.gdg_pattern = re.compile(r'\(gdg_dataset \[(\d+), (\d+)\] - \[(\d+), (\d+)\]\)', re.MULTILINE)
        
    def parse_jcl_file(self, jcl_path: str) -> str:
        """Parse a JCL file using tree-sitter and return the AST"""
        try:
            result = subprocess.run(
                ['npx', 'tree-sitter', 'parse', jcl_path],
                capture_output=True,
                text=True
            )
            return result.stdout
        except Exception as e:
            print(f"Error parsing {jcl_path}: {e}")
            return ""
    def extract_text_from_position(self, jcl_content: List[str], 
                                  start_line: int, start_col: int, 
                                  end_line: int, end_col: int) -> str:
        """Extract actual text from JCL file based on position coordinates"""
        if start_line == end_line:
            # Single line
            return jcl_content[start_line][start_col:end_col]
        else:
            # Multi-line (shouldn't happen for names, but handle it)
            text = jcl_content[start_line][start_col:]
            for line_num in range(start_line + 1, end_line):
                text += jcl_content[line_num]
            text += jcl_content[end_line][:end_col]
            return text
    def extract_job_names(self, ast: str, jcl_content: List[str]) -> List[str]:
        """Extract job names from the AST"""
        job_names = []
        for match in self.job_pattern.finditer(ast):
            start_line = int(match.group(1))
            start_col = int(match.group(2))
            end_line = int(match.group(3))
            end_col = int(match.group(4))
            
            job_name = self.extract_text_from_position(
                jcl_content, start_line, start_col, end_line, end_col
            )
            job_names.append(job_name)
        return job_names
    def extract_program_names(self, ast: str, jcl_content: List[str]) -> List[str]:
        """Extract program names from EXEC statements"""
        program_names = []
        for match in self.program_pattern.finditer(ast):
            start_line = int(match.group(1))
            start_col = int(match.group(2))
            end_line = int(match.group(3))
            end_col = int(match.group(4))
            
            program_name = self.extract_text_from_position(
                jcl_content, start_line, start_col, end_line, end_col
            )
            program_names.append(program_name)
        return program_names
    def extract_dataset_names(self, ast: str, jcl_content: List[str]) -> Dict[str, List[str]]:
        """Extract dataset names including GDG datasets"""
        datasets = {
            'regular': [],
            'gdg': [],
            'temporary': [],
            'referback': []
        }
        # Extract regular dataset names
        for match in self.dataset_pattern.finditer(ast):
            start_line = int(match.group(1))
            start_col = int(match.group(2))
            end_line = int(match.group(3))
            end_col = int(match.group(4))
            
            dataset_name = self.extract_text_from_position(
                jcl_content, start_line, start_col, end_line, end_col
            )
            # Categorize dataset type
            if dataset_name.startswith('&&'):
                datasets['temporary'].append(dataset_name)
            elif dataset_name.startswith('*.'):
                datasets['referback'].append(dataset_name)
            else:
                datasets['regular'].append(dataset_name)
        # Extract GDG datasets
        for match in self.gdg_pattern.finditer(ast):
            start_line = int(match.group(1))
            start_col = int(match.group(2))
            end_line = int(match.group(3))
            end_col = int(match.group(4))
            
            gdg_dataset = self.extract_text_from_position(
                jcl_content, start_line, start_col, end_line, end_col
            )
            datasets['gdg'].append(gdg_dataset)
        return datasets
    def extract_from_file(self, jcl_path: str) -> Dict:
        """Extract all information from a single JCL file"""
        # Read the JCL content
        with open(jcl_path, 'r') as f:
            jcl_content = f.readlines()
        # Parse the file to get AST
        ast = self.parse_jcl_file(jcl_path)
        if not ast:
            return {
                'file': jcl_path,
                'error': 'Failed to parse file',
                'jobs': [],
                'programs': [],
                'datasets': {}
            }
        # Extract data
        jobs = self.extract_job_names(ast, jcl_content)
        programs = self.extract_program_names(ast, jcl_content)
        datasets = self.extract_dataset_names(ast, jcl_content)
        return {
            'file': os.path.basename(jcl_path),
            'jobs': jobs,
            'programs': programs,
            'datasets': datasets,
            'extraction_summary': {
                'total_jobs': len(jobs),
                'total_programs': len(programs),
                'total_datasets': sum(len(v) for v in datasets.values()),
                'dataset_breakdown': {
                    'regular': len(datasets['regular']),
                    'gdg': len(datasets['gdg']),
                    'temporary': len(datasets['temporary']),
                    'referback': len(datasets['referback'])
                }
            }
        }
    
    def extract_from_directory(self, directory: str) -> List[Dict]:
        """Extract information from all JCL files in a directory"""
        results = []
        jcl_patterns = ['*.jcl', '*.JCL']
        for pattern in jcl_patterns:
            for jcl_file in Path(directory).glob(pattern):
                print(f"Processing: {jcl_file}")
                result = self.extract_from_file(str(jcl_file))
                results.append(result)
        return results


def main():
    """Main function to demonstrate JCL data extraction"""
    extractor = JCLExtractor()
    
    print("=" * 80)
    print("JCL Data Extractor - Demonstration")
    print("=" * 80)
    print()
    # Example 1: Extract from a single file
    print("Example 1: Extracting from a single JCL file")
    print("-" * 40)
    sample_file = "examples/READCARD.jcl"
    if os.path.exists(sample_file):
        result = extractor.extract_from_file(sample_file)
        print(f"File: {result['file']}")
        print(f"Jobs: {result['jobs']}")
        print(f"Programs: {result['programs']}")
        print(f"Datasets:")
        for dtype, dlist in result['datasets'].items():
            if dlist:
                print(f"  {dtype}: {dlist}")
        print()
    # Example 2: Extract from all examples
    print("Example 2: Extracting from all example JCL files")
    print("-" * 40)
    
    all_results = []
    for directory in ['examples', 'examples/jcl']:
        if os.path.exists(directory):
            results = extractor.extract_from_directory(directory)
            all_results.extend(results)
    # Generate dependency report

        output_file = 'jcl_extraction_results.json'
        with open(output_file, 'w') as f:
            json.dump({
                'extraction_results': all_results,
            }, f, indent=2)
        
        print()
        print(f"Full extraction results saved to: {output_file}")
        # Save CSV for easy viewing
        csv_file = 'jcl_extraction_summary.csv'
        with open(csv_file, 'w') as f:
            f.write("File,Jobs,Programs,Regular_Datasets,GDG_Datasets,Temp_Datasets,Referback_Datasets,Parse_Errors\n")
            for result in all_results:
                jobs = ';'.join(result['jobs'])
                programs = ';'.join(result['programs'])
                regular = len(result['datasets']['regular'])
                gdg = len(result['datasets']['gdg'])
                temp = len(result['datasets']['temporary'])
                referback = len(result['datasets']['referback'])
                f.write(f"{result['file']},{jobs},{programs},{regular},{gdg},{temp},{referback},\n")
        
        print(f"CSV summary saved to: {csv_file}")
    
    print()
    print("Extraction demonstration complete!")
    print()
    print("To use this extractor in your own code:")
    print("  from jcl_extractor import JCLExtractor")
    print("  extractor = JCLExtractor()")
    print("  result = extractor.extract_from_file('your_file.jcl')")

if __name__ == '__main__':
    main()
