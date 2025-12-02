#!/usr/bin/env python3
"""
Test suite for the day01 check-list challenge
"""

import subprocess
import sys

def test_binary_exists():
    """Test that the binary exists and is executable"""
    import os
    assert os.path.exists("./check-list"), "Binary check-list not found"
    assert os.access("./check-list", os.X_OK), "Binary is not executable"
    print("✓ Binary exists and is executable")

def test_binary_runs():
    """Test that the binary runs without crashing"""
    try:
        result = subprocess.run(
            ["./check-list"],
            input=b"test\n",
            capture_output=True,
            timeout=5
        )
        assert result.returncode in [0, 1], "Binary crashed or returned unexpected code"
        print("✓ Binary runs without crashing")
        return True
    except subprocess.TimeoutExpired:
        print("✗ Binary timed out")
        raise AssertionError("Binary timed out")
    except Exception as e:
        raise AssertionError(f"Binary execution failed: {e}")

def test_wrong_password():
    """Test that wrong password is rejected"""
    result = subprocess.run(
        ["./check-list"],
        input=b"wrong_password\n",
        capture_output=True
    )
    assert result.returncode != 0, "Binary should reject wrong password"
    assert b"Wrong" in result.stdout or b"Wrong" in result.stderr, "Expected 'Wrong' message"
    print("✓ Wrong password is correctly rejected")

def test_empty_input():
    """Test handling of empty input"""
    result = subprocess.run(
        ["./check-list"],
        input=b"",
        capture_output=True,
        timeout=5
    )
    # Should handle gracefully
    print(f"✓ Empty input handled (exit code: {result.returncode})")

def main():
    """Run all tests"""
    print("Running day01 challenge tests...\n")
    
    tests = [
        test_binary_exists,
        test_binary_runs,
        test_wrong_password,
        test_empty_input
    ]
    
    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
    
    print(f"\n{passed}/{len(tests)} tests passed")
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    sys.exit(main())
