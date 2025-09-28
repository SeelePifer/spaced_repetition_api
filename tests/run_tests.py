"""
Test runner and configuration scripts
"""
#!/usr/bin/env python3
"""
Test runner for the Spaced Repetition API
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(test_type: str = "all", coverage: bool = True, verbose: bool = True):
    """Run tests with specified configuration"""
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add verbose flag
    if verbose:
        cmd.append("-v")
    
    # Add coverage if requested
    if coverage:
        cmd.extend([
            "--cov=src",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-fail-under=80"
        ])
    
    # Add test type specific options
    if test_type == "unit":
        cmd.extend(["-m", "not integration and not slow"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "performance":
        cmd.extend(["-m", "slow"])
    elif test_type == "fast":
        cmd.extend(["-m", "not slow"])
    
    # Add test directory
    cmd.append("tests/")
    
    print(f"Running command: {' '.join(cmd)}")
    
    # Run tests
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    return result.returncode


def run_linting():
    """Run code linting"""
    print("Running code linting...")
    
    # Check if flake8 is available
    try:
        result = subprocess.run(["python", "-m", "flake8", "src/", "tests/"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Linting passed")
        else:
            print("❌ Linting failed:")
            print(result.stdout)
            print(result.stderr)
        return result.returncode
    except FileNotFoundError:
        print("⚠️  flake8 not found, skipping linting")
        return 0


def run_type_checking():
    """Run type checking with mypy"""
    print("Running type checking...")
    
    try:
        result = subprocess.run(["python", "-m", "mypy", "src/"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Type checking passed")
        else:
            print("❌ Type checking failed:")
            print(result.stdout)
            print(result.stderr)
        return result.returncode
    except FileNotFoundError:
        print("⚠️  mypy not found, skipping type checking")
        return 0


def install_test_dependencies():
    """Install test dependencies"""
    print("Installing test dependencies...")
    
    test_requirements = Path(__file__).parent / "requirements.txt"
    if test_requirements.exists():
        result = subprocess.run([
            "python", "-m", "pip", "install", "-r", str(test_requirements)
        ])
        return result.returncode
    else:
        print("⚠️  Test requirements file not found")
        return 0


def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description="Test runner for Spaced Repetition API")
    parser.add_argument(
        "--type", 
        choices=["all", "unit", "integration", "performance", "fast"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--no-coverage", 
        action="store_true",
        help="Skip coverage reporting"
    )
    parser.add_argument(
        "--quiet", 
        action="store_true",
        help="Run tests quietly"
    )
    parser.add_argument(
        "--lint", 
        action="store_true",
        help="Run linting"
    )
    parser.add_argument(
        "--type-check", 
        action="store_true",
        help="Run type checking"
    )
    parser.add_argument(
        "--install-deps", 
        action="store_true",
        help="Install test dependencies"
    )
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        install_test_dependencies()
    
    # Run linting if requested
    if args.lint:
        lint_result = run_linting()
        if lint_result != 0:
            print("❌ Linting failed, stopping")
            return lint_result
    
    # Run type checking if requested
    if args.type_check:
        type_result = run_type_checking()
        if type_result != 0:
            print("❌ Type checking failed, stopping")
            return type_result
    
    # Run tests
    test_result = run_tests(
        test_type=args.type,
        coverage=not args.no_coverage,
        verbose=not args.quiet
    )
    
    if test_result == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
    
    return test_result


if __name__ == "__main__":
    sys.exit(main())
