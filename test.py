#!/usr/bin/env python3.9
"""
Runs all tests under the test/ folder in the current directory.
"""

import pytest
import sys

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", "-s", "test/"]))
