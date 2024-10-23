# Makefile

# Variables
PROJECT_ROOT := $(PWD)
PYCACHE_DIR := $(PROJECT_ROOT)/__pycache__
ENV_FILE := .env

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  dev       - Run the development server with centralized __pycache__"
	@echo "  clean     - Remove all __pycache__ directories"
	@echo "  install   - Install project dependencies"
	@echo "  test      - Run tests"
	@echo "  format    - Format code using black and isort"
	@echo "  lint      - Lint code using flake8"
	@echo "  docs      - Build documentation"

# Run development server
.PHONY: dev
dev:
	@echo "Starting development server..."
	PYTHONPYCACHEPREFIX=$(PYCACHE_DIR) poetry run dev

# Clean __pycache__ directories
.PHONY: clean
clean:
	@echo "Removing all __pycache__ directories..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Removing centralized __pycache__ directory..."
	rm -rf $(PYCACHE_DIR)

# Install dependencies
.PHONY: install
install:
	@echo "Installing dependencies..."
	poetry install

# Run tests
.PHONY: test
test:
	@echo "Running tests..."
	poetry run pytest

# Format code
.PHONY: format
format:
	@echo "Formatting code with black and isort..."
	poetry run black .
	poetry run isort .

# Lint code
.PHONY: lint
lint:
	@echo "Linting code with flake8..."
	poetry run flake8 .

# Build documentation
.PHONY: docs
docs:
	@echo "Building documentation..."
	poetry run mkdocs build
