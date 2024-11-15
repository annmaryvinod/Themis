# Themis

An Agentic AI system for legal assistance

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Configure Environment Variables](#configure-environment-variables)
  - [Initialize the Database](#initialize-the-database)
  - [Development Server](#development-server)
  - [Testing the API](#testing-the-api)
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

## Features

- RESTful API built with FastAPI
- Document embedding using Hugging Face models
- PDF text extraction and processing
- Database integration with PostgreSQL
- Linting and code formatting with `black`, `isort`, and `flake8`
- Pre-commit hooks for enforcing code style
- Configurable settings using Pydantic
- Automated testing with `pytest`

## Prerequisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/docs/) for dependency management
- PostgreSQL database
- Hugging Face API token
- Optional: Docker and Docker Compose for containerization

## Installation

### Clone the Repository

```bash
git clone git@github.com:annmaryvinod/Themis.git
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

### Activate the Virtual Environment

After installing the dependencies, activate the virtual environment by entering the Poetry shell:

```bash
poetry shell
```

This will spawn a new shell within the virtual environment, where you can run the application and manage dependencies.

## Running the Application

### Configure Environment Variables

Before running the application, you need to set up your environment variables. Create a `.env` file in the `configs/` directory or use the provided example:

```bash
cp configs/.env.example configs/.env.local
```

Edit the `configs/.env.local` file and provide the necessary configuration, including your database URL and Hugging Face API token.

### Initialize the Database

Ensure your PostgreSQL database is running. To set up the database schema, apply migrations by running:

```bash
make migrate-up
```

To rollback migrations, use:

```bash
make migrate-down
```

### Development Server

To run the development server with auto-reload and centralized `__pycache__`, use the `dev` command in the `Makefile`:

```bash
make dev
```

This will start the FastAPI application on `http://127.0.0.1:8000`.

Alternatively, if you haven't activated the Poetry shell, you can run the development server directly using:

```bash
poetry run dev
```

### Testing the API

You can test the API by navigating to `http://127.0.0.1:8000/docs` in your web browser. This will bring up the interactive Swagger UI documentation where you can interact with the API endpoints.

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
│   ├── config
│   ├── main.py
│   ├── routers
│   ├── utils
│   ├── models
│   ├── services
│   ├── store
│   └── schemas
├── configs
├── tests
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
    - **`base.py`**: Base configuration model.
    - **`logging.py`**: Logging configuration.
    - **`settings.py`**: Pydantic settings configuration using environment variables.
  - **`main.py`**: Entry point of the FastAPI application. Includes the API router and health check endpoint.
  - **`routers/`**: Contains API route definitions using FastAPI's `APIRouter`.
    - **`embedding.py`**: Routes related to embedding operations.
  - **`utils/`**: Utility modules for tasks like text extraction and splitting.
  - **`models/`**: Data models, typically database models or Pydantic models representing the data.
  - **`services/`**: Business logic layer, contains code that interacts with models and performs operations.
  - **`store/`**: Database connection and pooling.
  - **`schemas/`**: Pydantic schemas used for request validation and response serialization.
- **`configs/`**: Contains configuration files such as environment variable files (`.env`) for different environments (development, production, etc.).
- **`tests/`**: Contains test cases for the application.
- **`Makefile`**: Provides common commands to manage and run the application easily.
- **`pyproject.toml`**: Configuration file for the project, including dependencies and tool settings.
- **`README.md`**: Project documentation.
- **`LICENSE`**: License file for the project.

### Where to Keep What

- **Configuration Files**: Place all your configuration files (like `.env` files) in the `configs/` directory.
- **API Routes**: Define your API endpoints in the `app/routers/` directory. Each resource can have its own file (e.g., `embedding.py` for embedding-related endpoints).
- **Models**: Place your data models in the `app/models/` directory.
- **Schemas**: Pydantic schemas for data validation and serialization go into the `app/schemas/` directory.
- **Services**: Business logic and interactions with the models are placed in the `app/services/` directory.
- **Utilities**: Any utility functions or modules should be placed in the `app/utils/` directory.
- **Database Connections**: Database pooling and connection management are in the `app/store/` directory.
- **Scripts**: Any standalone scripts or utilities should be placed in the `app/scripts/` directory.
- **Tests**: Keep your test files in the `tests/` directory. It's a good practice to mirror the structure of the `app/` directory for your tests.

## Environment Variables

The application uses environment variables for configuration. These can be set in `.env` files located in the `configs/` directory.

Example `configs/.env.local`:

```ini
# configs/.env.local
HOST=127.0.0.1
PORT=8000
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/themis_db
HUGGINGFACEHUB_API_TOKEN=your-huggingface-api-token
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

Every time you make a commit, pre-commit will run these tools and ensure that your code adheres to the specified code style.

Alternatively, you can run the pre-commit hooks manually:

```bash
poetry run pre-commit run --all-files
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
