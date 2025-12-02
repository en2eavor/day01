#!/usr/bin/env python3
"""
Solution for day01 challenge - Santa's Naughty-or-Nice List Checker

This script performs static analysis on the check-list binary to extract
and reverse-engineer the correct password by:
1. Extracting all byte-level transformation operations
2. Extracting expected comparison values
3. Reversing the transformations to find the original input

As the requirement states: "it's pure, meticulous byte-level bookkeeping"
"""

import subprocess
import re
import sys

def extract_operations_and_comparisons(binary_path):
    """
    Extract transformation operations and comparison values from the binary.
    Returns: (operations_by_offset, comparisons)
    """
    # Disassemble the binary
    result = subprocess.run(
        ["objdump", "-M", "intel", "-d", binary_path],
        capture_output=True,
        text=True
    )
    
    lines = result.stdout.split('\n')
    
    operations = []
    comparisons = {}
    
    for line in lines:
        # Get address to filter code section
        addr_match = re.match(r'\s*([0-9a-f]+):', line)
        if addr_match:
            addr = int(addr_match.group(1), 16)
            
            # Operations are in the early part of .text section
            if 0x401000 <= addr < 0xaa4000:
                # Extract add operations
                match = re.search(r'add\s+BYTE PTR \[rbp-(0x[0-9a-f]+)\],(0x[0-9a-f]+)', line)
                if match:
                    offset = int(match.group(1), 16)
                    value = int(match.group(2), 16)
                    if 1 <= offset <= 0x100:
                        operations.append(('add', offset, value))
                    continue
                
                # Extract sub operations
                match = re.search(r'sub\s+BYTE PTR \[rbp-(0x[0-9a-f]+)\],(0x[0-9a-f]+)', line)
                if match:
                    offset = int(match.group(1), 16)
                    value = int(match.group(2), 16)
                    if 1 <= offset <= 0x100:
                        operations.append(('sub', offset, value))
        
        # Extract comparisons (later in the code)
        match = re.search(r'cmp\s+BYTE PTR \[rbp-(0x[0-9a-f]+)\],(0x[0-9a-f]+)', line)
        if match:
            offset = int(match.group(1), 16)
            value = int(match.group(2), 16)
            if 1 <= offset <= 0x100:
                comparisons[offset] = value
    
    # Group operations by offset (preserve order)
    ops_by_offset = {}
    for op, offset, value in operations:
        if offset not in ops_by_offset:
            ops_by_offset[offset] = []
        ops_by_offset[offset].append((op, value))
    
    return ops_by_offset, comparisons

def reverse_transform(ops_by_offset, comparisons):
    """
    Reverse the transformations to find the original password.
    """
    password = bytearray()
    
    for offset in sorted(comparisons.keys()):
        expected = comparisons[offset]
        
        # Start with expected value and reverse all operations
        current = expected
        if offset in ops_by_offset:
            # Reverse the operations (apply inverse in reverse order)
            for op, value in reversed(ops_by_offset[offset]):
                if op == 'add':
                    current = (current - value) & 0xFF
                else:  # sub
                    current = (current + value) & 0xFF
        
        password.append(current)
    
    return bytes(password)

def main():
    """
    Main entry point - extract and provide the password for Santa's list.
    """
    binary_path = "./check-list"
    
    # Extract operations and comparisons through static analysis
    print("Performing static analysis on check-list binary...", file=sys.stderr)
    ops_by_offset, comparisons = extract_operations_and_comparisons(binary_path)
    
    print(f"Found {sum(len(ops) for ops in ops_by_offset.values())} transformation operations", file=sys.stderr)
    print(f"Found {len(comparisons)} comparison checks", file=sys.stderr)
    
    # Reverse the transformations
    password = reverse_transform(ops_by_offset, comparisons)
    print(f"Extracted password: {len(password)} bytes", file=sys.stderr)
    
    # Output the password to stdout for piping
    sys.stdout.buffer.write(password)
    sys.stdout.buffer.flush()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
