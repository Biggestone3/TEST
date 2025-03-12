# LNA Backend

This is the backend monorepo for the LNA project, containing multiple Python packages:

- `lna-app`: FastAPI application
- `lna-db`: Database models and utilities
- `lna-crawlers`: Data crawling services

## Development Setup

This monorepo uses Poetry for dependency management. Each package has its own dependencies, but common development tools are defined at the root level.

### Installation

1. Install Poetry if you haven't already: https://python-poetry.org/docs/#installation

2. Install the development dependencies for the entire project:
   ```
   cd backend
   poetry install
   ```

3. Install package-specific dependencies:
   ```
   cd lna-app
   poetry install
   
   cd ../lna-db
   poetry install
   
   cd ../lna-crawlers
   poetry install
   ```

### Development Workflow

- Use the root Poetry environment for running linters, type checkers, and other development tools.
- Use package-specific environments when working on a single package.

### Running Code Quality Tools

**Important:** All these commands must be run from the **backend root directory**, not from individual package directories.

```
# Run ruff linter and formatter
poetry run ruff check .
poetry run ruff format .

# Run type checking with pyright
poetry run pyright

# Run pre-commit hooks (if configured)
poetry run pre-commit run --all-files
```

Note: Pre-commit hooks require a `.pre-commit-config.yaml` file in the backend directory. If you encounter an error saying this file is not found, make sure you are in the correct directory or check if the file exists.

## Project Structure

Each package is independently deployable and has its own version, dependencies, and release cycle. However, they can also reference each other as local dependencies when needed. 