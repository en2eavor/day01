# Day 01 Challenge

This repository contains a reverse engineering challenge with a binary called `check-list`.

## Challenge Analysis

The `check-list` binary is a password validation program that:
1. Reads up to 1024 bytes of input from stdin
2. Applies cryptographic transformations to the input
3. Compares the transformed result against expected values
4. Outputs a success or failure message

The hint "Santa told you to check that list twice!" suggests this is a Christmas/Advent-themed challenge.

## Binary Analysis

- **Type**: ELF 64-bit executable, statically linked
- **Entry point**: Reads from stdin using syscall
- **Buffer size**: 1024 bytes (0x400)
- **Validation**: 256 byte-by-byte comparisons

## Solution Approach

The binary performs byte-level transformations (add/sub operations) on the input before comparing against expected values. To find the correct password, one would need to:

1. Extract all transformation operations in order
2. Extract all expected comparison values
3. Reverse the transformations to find the original input

## Files

- `check-list`: The challenge binary
- `solution.py`: Automated password extraction script
- `README.md`: This file

## Usage

```bash
# Run the binary with input
echo "your_password" | ./check-list

# Run the solution script
python3 solution.py
```

## Status

The challenge requires further analysis to extract the correct password by properly tracking all byte transformations in the correct execution order.
