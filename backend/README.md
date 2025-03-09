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

From the root directory:

```
# Run ruff on all packages
poetry run ruff .

# Run type checking
poetry run pyre check

# Run pre-commit hooks
poetry run pre-commit run --all-files
```

## Project Structure

Each package is independently deployable and has its own version, dependencies, and release cycle. However, they can also reference each other as local dependencies when needed. 