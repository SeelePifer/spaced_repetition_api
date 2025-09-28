# Makefile for Spaced Repetition API Tests

.PHONY: help test test-unit test-integration test-performance test-fast lint type-check install-deps clean coverage

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-deps: ## Install test dependencies
	python -m pip install -r tests/requirements.txt

test: ## Run all tests with coverage
	python tests/run_tests.py --type all

test-unit: ## Run unit tests only
	python tests/run_tests.py --type unit

test-integration: ## Run integration tests only
	python tests/run_tests.py --type integration

test-performance: ## Run performance tests only
	python tests/run_tests.py --type performance

test-fast: ## Run fast tests (exclude performance tests)
	python tests/run_tests.py --type fast

lint: ## Run code linting
	python tests/run_tests.py --lint

type-check: ## Run type checking
	python tests/run_tests.py --type-check

coverage: ## Generate coverage report
	python tests/run_tests.py --type all
	@echo "Coverage report generated in htmlcov/"

clean: ## Clean test artifacts
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test-ci: ## Run tests for CI/CD pipeline
	python tests/run_tests.py --type fast --lint --type-check

test-all: ## Run all tests including performance
	python tests/run_tests.py --type all --lint --type-check

# Development helpers
dev-setup: install-deps ## Setup development environment
	@echo "Development environment setup complete!"

watch: ## Run tests in watch mode
	python -m pytest-watch tests/

debug: ## Run tests with debugging
	python -m pytest tests/ -v -s --pdb

# Database testing
test-db: ## Run database-specific tests
	python -m pytest tests/integration/test_database_operations.py -v

# API testing
test-api: ## Run API-specific tests
	python -m pytest tests/integration/test_api_endpoints.py -v

# Domain testing
test-domain: ## Run domain-specific tests
	python -m pytest tests/unit/test_entities.py tests/unit/test_value_objects.py tests/unit/test_events.py -v

# Application testing
test-app: ## Run application-specific tests
	python -m pytest tests/unit/test_commands.py tests/unit/test_queries.py tests/unit/test_command_handlers.py -v
