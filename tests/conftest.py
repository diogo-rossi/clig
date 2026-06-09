import sys
import pytest
import clig.clig
from pathlib import Path

TESTS_DIR = Path(__file__).parent

if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))


@pytest.fixture(autouse=True)
def reset_singleton():
    """Automatically resets the singleton instance before every single test."""
    # Yield control to the test function
    yield
    # Clean up the instance after the test completes
    clig.clig._main_command = None
