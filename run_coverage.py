def run_coverage_main():
    import pytest
    pytest.main(["--cov=etl", "--cov-report=term-missing", "tests/"])