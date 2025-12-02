#!/usr/bin/env python3
"""
Solution for day01 challenge.
The check-list binary checks if the input matches a specific password.
This script reverse-engineers and provides the correct password.
"""

import subprocess
import re
import sys

def extract_password_from_binary(binary_path):
    """
    Extract the expected password by analyzing the binary's comparison operations.
    """
    # Disassemble the binary
    result = subprocess.run(
        ["objdump", "-M", "intel", "-d", binary_path],
        capture_output=True,
        text=True
    )
    
    lines = result.stdout.split('\n')
    
    # Extract comparison values
    comparisons = {}
    for line in lines:
        match = re.search(r'cmp\s+BYTE PTR \[rbp-0x([0-9a-f]+)\],0x([0-9a-f]+)', line)
        if match:
            offset = int(match.group(1), 16)
            value = int(match.group(2), 16)
            if 1 <= offset <= 0x100:
                comparisons[offset] = value
    
    # Build password from comparisons
    password = bytearray()
    for offset in sorted(comparisons.keys()):
        password.append(comparisons[offset])
    
    return bytes(password)

def main():
    binary_path = "./check-list"
    password = extract_password_from_binary(binary_path)
    
    print(f"Extracted password ({len(password)} bytes)", file=sys.stderr)
    
    # Output the password to stdout for piping
    sys.stdout.buffer.write(password)
    sys.stdout.buffer.flush()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
