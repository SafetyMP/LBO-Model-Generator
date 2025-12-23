#!/usr/bin/env python3
"""
Code Audit Script for LBO Model Generator

Analyzes codebase for quality issues, bugs, and improvement opportunities.
"""

import sys
import os
import json
import ast
import re
from pathlib import Path
from typing import Dict, List, Any

# Add src to path
sys.path.insert(0, 'src')

try:
    from lbo_model_auditor import LBOModelAuditor
    AUDITOR_AVAILABLE = True
except ImportError:
    AUDITOR_AVAILABLE = False
    print("Warning: LBOModelAuditor not available")


def analyze_code_quality() -> Dict[str, Any]:
    """Analyze codebase for quality issues."""
    findings = []
    
    src_dir = Path('src')
    python_files = list(src_dir.glob('*.py'))
    
    # Analyze each file
    for py_file in python_files:
        if py_file.name.startswith('__'):
            continue
            
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Check for issues
        file_findings = []
        
        # 1. Check for bare exception handlers
        bare_except_pattern = r'except\s*:|except\s+Exception\s*:'
        for i, line in enumerate(lines, 1):
            if re.search(bare_except_pattern, line):
                file_findings.append({
                    'line': i,
                    'issue': 'Bare exception handler',
                    'severity': 'medium',
                    'recommendation': 'Use specific exception types'
                })
        
        # 2. Check for missing type hints in function definitions
        func_pattern = r'def\s+(\w+)\s*\([^)]*\)\s*:'
        for i, line in enumerate(lines, 1):
            match = re.search(func_pattern, line)
            if match and '->' not in line and 'def __' not in line:
                # Check if it's a simple function (not a method with self/cls)
                if 'self' not in line and 'cls' not in line:
                    file_findings.append({
                        'line': i,
                        'issue': 'Missing return type hint',
                        'severity': 'low',
                        'recommendation': 'Add return type annotation'
                    })
        
        # 3. Check for long functions (>50 lines)
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                    if func_lines > 50:
                        file_findings.append({
                            'line': node.lineno,
                            'issue': f'Long function ({func_lines} lines)',
                            'severity': 'medium',
                            'recommendation': 'Consider breaking into smaller functions'
                        })
        except SyntaxError:
            pass
        
        # 4. Check for TODO/FIXME comments
        for i, line in enumerate(lines, 1):
            if re.search(r'TODO|FIXME|XXX|HACK', line, re.IGNORECASE):
                file_findings.append({
                    'line': i,
                    'issue': 'TODO/FIXME comment found',
                    'severity': 'low',
                    'recommendation': 'Address or remove TODO comment'
                })
        
        if file_findings:
            findings.append({
                'file': py_file.name,
                'findings': file_findings
            })
    
    return {
        'total_files': len(python_files),
        'files_with_issues': len(findings),
        'findings': findings
    }


def get_file_statistics() -> Dict[str, Any]:
    """Get codebase statistics."""
    src_dir = Path('src')
    python_files = list(src_dir.glob('*.py'))
    
    stats = {
        'total_files': len(python_files),
        'total_lines': 0,
        'largest_files': [],
        'file_sizes': {}
    }
    
    for py_file in python_files:
        with open(py_file, 'r', encoding='utf-8') as f:
            lines = len(f.readlines())
            stats['total_lines'] += lines
            stats['file_sizes'][py_file.name] = lines
    
    # Get largest files
    sorted_files = sorted(stats['file_sizes'].items(), key=lambda x: x[1], reverse=True)
    stats['largest_files'] = sorted_files[:5]
    
    return stats


def main():
    """Run code audit."""
    print('='*80)
    print('CODE AUDIT - LBO MODEL GENERATOR')
    print('='*80)
    print()
    
    # Get statistics
    print('CODEBASE STATISTICS:')
    print('-'*80)
    stats = get_file_statistics()
    print(f"Total Python files: {stats['total_files']}")
    print(f"Total lines of code: {stats['total_lines']:,}")
    print()
    print("Largest files:")
    for filename, lines in stats['largest_files']:
        print(f"  {filename}: {lines:,} lines")
    print()
    
    # Analyze code quality
    print('CODE QUALITY ANALYSIS:')
    print('-'*80)
    quality = analyze_code_quality()
    print(f"Files analyzed: {quality['total_files']}")
    print(f"Files with issues: {quality['files_with_issues']}")
    print()
    
    # Summary of findings
    total_issues = sum(len(f['findings']) for f in quality['findings'])
    print(f"Total issues found: {total_issues}")
    print()
    
    # Group by severity
    severity_counts = {'high': 0, 'medium': 0, 'low': 0}
    for file_data in quality['findings']:
        for finding in file_data['findings']:
            severity = finding.get('severity', 'low')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    print("Issues by severity:")
    for severity, count in severity_counts.items():
        print(f"  {severity.upper()}: {count}")
    print()
    
    # Show top issues
    print('TOP ISSUES BY FILE:')
    print('-'*80)
    for file_data in quality['findings'][:10]:  # Top 10 files
        print(f"\n{file_data['file']}:")
        for finding in file_data['findings'][:5]:  # Top 5 per file
            print(f"  Line {finding['line']}: [{finding['severity'].upper()}] {finding['issue']}")
            print(f"    → {finding['recommendation']}")
    
    # Save report
    report = {
        'statistics': stats,
        'quality_analysis': quality,
        'severity_counts': severity_counts
    }
    
    with open('CODE_AUDIT_REPORT.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print()
    print('='*80)
    print('✓ Code audit complete. Report saved to CODE_AUDIT_REPORT.json')
    print('='*80)


if __name__ == '__main__':
    main()

