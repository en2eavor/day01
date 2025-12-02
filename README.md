# Day 01 Challenge - Santa's Naughty-or-Nice List

This repository contains a reverse engineering challenge themed around Santa's legendary Naughty-or-Nice list. As the challenge states: **"it's pure, meticulous byte-level bookkeeping"** - there's no magic, just careful static analysis.

## Challenge Description

Every year, Santa maintains the legendary Naughty-or-Nice list through pure byte-level bookkeeping. Your job is to:
- Apply every tiny change exactly
- Confirm the final list matches perfectly
- Check it once, check it twice (as Santa requires)

## The Binary: `check-list`

The `check-list` binary is Santa's validation program that:
1. Reads up to 1024 bytes of input from stdin (the "list")
2. Applies meticulous byte-level transformations (add/sub operations)
3. Performs 256 byte-by-byte comparisons against expected values
4. Outputs success or failure message

### Binary Details

- **Type**: ELF 64-bit executable, statically linked
- **Entry point**: 0x401000
- **Buffer**: 1024 bytes (0x400) at [rbp-0x400]
- **Validation**: 256 byte comparisons at offsets [rbp-0x1] to [rbp-0x100]

### Success/Failure Messages

```
✓ Correct: you checked it twice, and it shows!
✗ Wrong: Santa told you to check that list twice!
```

## Solution Approach

The challenge is solved through **static analysis** - examining the binary without execution:

1. **Extract Transformations**: Use `objdump` to disassemble and find all `add`/`sub` operations on bytes
2. **Extract Comparisons**: Find all `cmp` instructions that check the final values
3. **Reverse Engineer**: Work backwards from expected values through transformations
4. **Validate**: The original input, when transformed, must match exactly

As the hint says: _"even a simple objdump | grep goes a long way"_

## Files

- `check-list`: The challenge binary (Santa's validator)
- `solution.py`: Automated static analysis and password extraction script
- `test_challenge.py`: Test suite to validate the binary
- `README.md`: This documentation

## Usage

```bash
# Test the binary with wrong input
echo "wrong" | ./check-list
# Output: 🚫 Wrong: Santa told you to check that list twice!

# Run the solution script to extract the correct password
python3 solution.py | ./check-list
# Output: ✅ Correct: you checked it twice, and it shows!

# Run tests
python3 test_challenge.py
```

## Technical Details

The binary performs these operations:
1. Reads input into buffer at `[rbp-0x400]`
2. Applies hundreds of thousands of byte-level transformations
3. Compares each of 256 bytes against hardcoded expected values
4. All transformations must be reversed to find the original "naughty-or-nice list"

## The "Check It Twice" Requirement

Santa's requirement to "check that list twice" refers to:
- **First check**: Extract all operations through static analysis
- **Second check**: Verify the transformations are reversed correctly
- **Perfection required**: Not even a single incorrect byte is tolerated
