# Test Documentation for Spaced Repetition API

## Overview

This document describes the comprehensive test suite for the Spaced Repetition API, which includes unit tests, integration tests, and performance tests.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py                 # Test configuration and fixtures
├── requirements.txt            # Test dependencies
├── run_tests.py               # Test runner script
├── unit/                      # Unit tests
│   ├── test_commands.py       # Command tests
│   ├── test_command_handlers.py # Command handler tests
│   ├── test_entities.py       # Entity tests
│   ├── test_events.py         # Event tests
│   ├── test_queries.py        # Query tests
│   └── test_value_objects.py  # Value object tests
├── integration/               # Integration tests
│   ├── test_api_endpoints.py  # API endpoint tests
│   ├── test_cqrs_mediator.py  # CQRS mediator tests
│   └── test_database_operations.py # Database operation tests
├── performance/               # Performance tests
│   └── test_performance.py    # Performance and memory tests
└── utils/                     # Test utilities
    └── test_helpers.py        # Test helpers and factories
```

## Test Categories

### Unit Tests

Unit tests focus on testing individual components in isolation:

- **Value Objects**: Test validation, business logic, and immutability
- **Entities**: Test business rules, state changes, and domain events
- **Commands**: Test command structure and validation
- **Queries**: Test query structure and parameters
- **Command Handlers**: Test business logic execution with mocked dependencies

### Integration Tests

Integration tests verify that components work together correctly:

- **API Endpoints**: Test HTTP endpoints with real request/response cycles
- **Database Operations**: Test CRUD operations with real database
- **CQRS Mediator**: Test command/query routing and handler execution

### Performance Tests

Performance tests ensure the system meets performance requirements:

- **API Response Times**: Test endpoint response times under load
- **Concurrent Requests**: Test system behavior under concurrent load
- **Memory Usage**: Test memory consumption patterns
- **Domain Operations**: Test performance of domain operations

## Running Tests

### Using the Test Runner

```bash
# Run all tests
python tests/run_tests.py

# Run specific test types
python tests/run_tests.py --type unit
python tests/run_tests.py --type integration
python tests/run_tests.py --type performance

# Run with additional checks
python tests/run_tests.py --lint --type-check

# Run without coverage
python tests/run_tests.py --no-coverage
```

### Using Make

```bash
# Install dependencies
make install-deps

# Run all tests
make test

# Run specific test categories
make test-unit
make test-integration
make test-performance

# Run with linting and type checking
make test-all

# Generate coverage report
make coverage
```

### Using pytest directly

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test files
pytest tests/unit/test_entities.py

# Run tests matching a pattern
pytest tests/ -k "test_word"

# Run tests with specific markers
pytest tests/ -m "not slow"
```

## Test Configuration

### pytest.ini

The `pytest.ini` file contains test configuration:

- Test discovery patterns
- Coverage settings
- Async test support
- Custom markers

### conftest.py

The `conftest.py` file provides:

- Database fixtures for testing
- Mock repositories
- Test data factories
- Common test utilities

## Test Fixtures

### Database Fixtures

- `test_db`: In-memory SQLite database for testing
- `client`: FastAPI test client with database override

### Entity Fixtures

- `sample_word`: Sample Word entity
- `sample_user_progress`: Sample UserProgress entity
- `sample_study_session`: Sample StudySession entity

### Value Object Fixtures

- `sample_quality_values`: Various Quality values
- `sample_difficulty_levels`: Various DifficultyLevel values
- `sample_frequency_ranks`: Various FrequencyRank values

### Mock Fixtures

- `mock_word_repository`: Mock word repository
- `mock_user_progress_repository`: Mock user progress repository
- `mock_study_session_repository`: Mock study session repository

## Test Utilities

### TestDataFactory

Factory class for creating test data:

```python
# Create test entities
word = TestDataFactory.create_word(word_id=1, word="hello")
progress = TestDataFactory.create_user_progress(user_id="user123")
session = TestDataFactory.create_study_session(word_id=1)
```

### TestAssertions

Custom assertions for domain objects:

```python
# Assert entity equality
TestAssertions.assert_word_equal(actual_word, expected_word)
TestAssertions.assert_user_progress_equal(actual_progress, expected_progress)
```

### Mock Repositories

Mock implementations for testing:

```python
# Use mock repositories in tests
mock_repo = MockWordRepository()
word = await mock_repo.find_by_id(WordId(1))
```

## Coverage Requirements

The test suite aims for:

- **Minimum 80% code coverage**
- **100% coverage for critical business logic**
- **Comprehensive edge case testing**

Coverage reports are generated in HTML format in the `htmlcov/` directory.

## Continuous Integration

### GitHub Actions

The `.github/workflows/test.yml` file defines CI/CD pipeline:

- Runs on Python 3.9, 3.10, and 3.11
- Includes linting and type checking
- Runs unit and integration tests
- Performance tests run only on main branch
- Uploads coverage to Codecov

### Local CI Simulation

```bash
# Run CI pipeline locally
make test-ci
```

## Best Practices

### Writing Tests

1. **Arrange-Act-Assert**: Structure tests clearly
2. **Descriptive Names**: Use clear, descriptive test names
3. **Single Responsibility**: Each test should test one thing
4. **Independent Tests**: Tests should not depend on each other
5. **Mock External Dependencies**: Use mocks for external services

### Test Data

1. **Use Factories**: Create test data using factory methods
2. **Minimal Data**: Use only necessary data for each test
3. **Realistic Data**: Use realistic test data when possible
4. **Edge Cases**: Test boundary conditions and edge cases

### Performance Testing

1. **Realistic Loads**: Test with realistic load patterns
2. **Baseline Metrics**: Establish performance baselines
3. **Monitor Trends**: Track performance over time
4. **Resource Usage**: Monitor memory and CPU usage

## Troubleshooting

### Common Issues

1. **Database Connection**: Ensure test database is properly configured
2. **Async Tests**: Use `@pytest.mark.asyncio` for async tests
3. **Import Errors**: Check Python path and module structure
4. **Fixture Scope**: Understand fixture scopes (function, class, module, session)

### Debug Mode

```bash
# Run tests with debugging
make debug

# Run specific test with debugging
pytest tests/unit/test_entities.py::TestWord::test_valid_word_creation -v -s --pdb
```

## Contributing

When adding new tests:

1. Follow existing naming conventions
2. Add appropriate test markers
3. Update this documentation if needed
4. Ensure tests pass in CI/CD pipeline
5. Maintain or improve coverage metrics
