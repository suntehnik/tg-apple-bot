#!/usr/bin/env python3
"""
Script to run all tests for the Telegram Food Tracking Bot.
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and print its output."""
    print(f"\n=== {description} ===\n")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               text=True, capture_output=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    """Run all tests."""
    print("\n=== Running Telegram Food Tracking Bot Tests ===\n")
    
    # Get project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Check if Python modules are installed
    try:
        import pytest
        pytest_available = True
    except ImportError:
        pytest_available = False
        print("⚠️  pytest module not available. Some tests may not run.")
    
    # Run basic structure test
    structure_test_success = run_command(
        "python example_structure.py", 
        "Checking Project Structure"
    )
    
    # Run the demo test
    demo_test_success = run_command(
        "python run_openai_test.py", 
        "Running OpenAI Vision API Demo Test"
    )
    
    # Run integration test
    integration_test_success = run_command(
        "python tests/integration_test_openai.py", 
        "Running OpenAI Vision API Integration Test"
    )
    
    # Run pytest tests if available
    pytest_success = True
    if pytest_available:
        pytest_success = run_command(
            "python -m pytest -v tests/test_config.py tests/test_dto.py", 
            "Running pytest Tests"
        )
    
    # Print summary
    print("\n=== Test Summary ===\n")
    print(f"Structure Test:    {'✓' if structure_test_success else '✗'}")
    print(f"Demo Test:         {'✓' if demo_test_success else '✗'}")
    print(f"Integration Test:  {'✓' if integration_test_success else '✗'}")
    if pytest_available:
        print(f"pytest Tests:      {'✓' if pytest_success else '✗'}")
    else:
        print("pytest Tests:      ⚠️  Not run (pytest not available)")
    
    # Overall status
    all_success = structure_test_success and demo_test_success and integration_test_success
    if pytest_available:
        all_success = all_success and pytest_success
    
    print(f"\nOverall Status:    {'✓ All tests passed' if all_success else '✗ Some tests failed'}")
    
    # Return exit code
    return 0 if all_success else 1

if __name__ == "__main__":
    sys.exit(main())