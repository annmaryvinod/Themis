# Themis

An Agentic AI system for legal assistance 

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Development Server](#development-server)
  - [Production Server](#production-server)
- [Project Structure](#project-structure)
  - [Directory Breakdown](#directory-breakdown)
  - [Where to Keep What](#where-to-keep-what)
- [Environment Variables](#environment-variables)
- [Linting and Code Style](#linting-and-code-style)
  - [Running Linters](#running-linters)
  - [Pre-commit Hooks](#pre-commit-hooks)
- [Testing](#testing)
- [Contributing](#contributing)
  - [Coding Guidelines](#coding-guidelines)
- [License](#license)

## Introduction

**Themis** is a FastAPI application that provides APIs for managing items and processing document embeddings using language models. The project is organized to facilitate scalability, maintainability, and collaboration.

## Features

- RESTful API built with FastAPI
- Document embedding scripts using Hugging Face models
- Database integration with PostgreSQL
- Linting and code formatting with `black`, `isort`, and `flake8`
- Pre-commit hooks for enforcing code style
- Configurable settings using Pydantic
- Automated testing with `pytest`

## Prerequisites

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/docs/) for dependency management
- PostgreSQL database
- Optional: Docker and Docker Compose for containerization

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/themis.git
cd themis
```

### Install Dependencies

We use Poetry for dependency management. If you don't have Poetry installed, install it first:

```bash
pip install poetry
```

Then, install the project dependencies:

```bash
poetry install
```

## Running the Application

### Development Server

To run the development server with auto-reload and centralized `__pycache__`, use the `dev` command in the `Makefile`:

```bash
make dev
```

This will start the FastAPI application on `http://127.0.0.1:8000`.

Alternatively, you can run the development server directly using:

```bash
poetry run dev
```

### Production Server

For production deployment, you might want to use a production-grade server like `gunicorn` along with `uvicorn` workers.

Example command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Project Structure

```plaintext
themis
├── Makefile
├── app
│   ├── scripts
│   │   └── dev.py
│   ├── config
│   │   ├── base.py
│   │   ├── logging.py
│   │   └── settings.py
│   ├── main.py
│   ├── routers
│   │   └── item.py
│   ├── models
│   │   └── item.py
│   ├── services
│   │   └── item.py
│   └── schemas
│       └── item.py
├── configs
├── tests
│   └── __init__.py
├── README.md
├── LICENSE
├── pyproject.toml
└── poetry.lock
```

### Directory Breakdown

- **`app/`**: Main application directory containing the core of the FastAPI app.
  - **`scripts/`**: Scripts related to running the application.
    - **`dev.py`**: Script to run the development server.
  - **`config/`**: Application configuration files.
    - **`settings.py`**: Pydantic settings configuration using environment variables.
    - **`logging.py`**: Logging configuration.
    - **`base.py`**: Base configuration model.
  - **`main.py`**: Entry point of the FastAPI application. Includes the API router and health check endpoint.
  - **`routers/`**: Contains API route definitions using FastAPI's `APIRouter`.
    - **`item.py`**: Routes related to item operations.
  - **`models/`**: Data models, typically database models or Pydantic models representing the data.
    - **`item.py`**: Model representing an item.
  - **`services/`**: Business logic layer, contains code that interacts with models and performs operations.
    - **`item.py`**: Service for item-related operations.
  - **`schemas/`**: Pydantic schemas used for request validation and response serialization.
    - **`item.py`**: Pydantic schemas for items.
- **`configs/`**: Contains configuration files such as environment variable files (`.env`) for different environments (development, production, etc.). Keep your environment-specific configurations here.
- **`tests/`**: Contains test cases for the application. Organize your tests mirroring the application's structure.
- **`Makefile`**: Provides common commands to manage and run the application easily.
- **`pyproject.toml`**: Configuration file for the project, including dependencies and tool settings.
- **`README.md`**: Project documentation.
- **`LICENSE`**: License file for the project.

### Where to Keep What

- **Configuration Files**: Place all your configuration files (like `.env` files) in the `configs/` directory.
- **API Routes**: Define your API endpoints in the `app/routers/` directory. Each resource can have its own file (e.g., `item.py` for item-related endpoints).
- **Models**: Place your data models in the `app/models/` directory.
- **Schemas**: Pydantic schemas for data validation and serialization go into the `app/schemas/` directory.
- **Services**: Business logic and interactions with the models are placed in the `app/services/` directory.
- **Scripts**: Any standalone scripts or utilities should be placed in the `scripts/` directory.
- **Tests**: Keep your test files in the `tests/` directory. It's a good practice to mirror the structure of the `app/` directory for your tests.

## Environment Variables

The application uses environment variables for configuration. These can be set in `.env` files located in the `configs/` directory.

Example `configs/.env.local`:

```ini
# configs/.env.local
HOST=127.0.0.1
PORT=8000
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
```

Make sure to create or update the `.env` files according to your environment (development, production, etc.).

## Linting and Code Style

We use `black` for code formatting, `isort` for import sorting, and `flake8` for linting.

### Running Linters

To format and lint the code, use the provided `Makefile` commands:

```bash
make format  # Formats the code using black and isort
make lint    # Lints the code using flake8
```

Alternatively, you can run them via Poetry:

```bash
poetry run black .
poetry run isort .
poetry run flake8 .
```

### Pre-commit Hooks

We use `pre-commit` to enforce code style before commits. Pre-commit hooks can be set up to automatically format and lint code before each commit.

First, install the pre-commit hooks:

```bash
poetry run pre-commit install
```

To set up pre-commit hooks, create a `.pre-commit-config.yaml` file in the root directory with the following content:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://gitlab.com/pycqa/flake8
    rev: 7.1.1
    hooks:
      - id: flake8
```

Now, every time you make a commit, pre-commit will run these tools and ensure that your code adheres to the specified code style.

Alternatively, you can run the pre-commit hooks manually:

```bash
poetry run pre-commit run --all-files
```

### Linting and Formatting Configuration

The configurations for `black`, `isort`, and `flake8` are specified in the `pyproject.toml` file.

Example from `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py312']
exclude = '''
/(
    \.venv
  | build
  | dist
  | \.git
  | \.mypy_cache
  | __pycache__
)/
'''

[tool.isort]
profile = "black"
line_length = 88
known_first_party = ["app"]
```

## Testing

Run the test suite using:

```bash
make test
```

Or directly with pytest:

```bash
poetry run pytest
```

## Contributing

We welcome contributions! Please follow these guidelines:

- **Code Style**: Ensure code is formatted with `black` and imports are sorted with `isort`.
- **Testing**: Write tests for new features and ensure existing tests pass.
- **Documentation**: Update documentation to reflect changes.

### Coding Guidelines

- Use meaningful variable and function names.
- Keep functions small and focused.
- Write docstrings for modules, classes, and functions.
- Follow PEP 8 style guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

