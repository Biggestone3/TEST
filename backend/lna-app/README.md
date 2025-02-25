# LNA Backend

## Local Development Setup

### Prerequisites

- Python 3.13 or higher
- Poetry (Python package manager)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd backend/lna-app
```

2. Install Poetry (if not already installed):
Follow the [Poetry installation guide](https://python-poetry.org/docs/#installation) to install Poetry on your system.

3. Install dependencies:
```bash
poetry install
```

### Running the Application

1. Activate the poetry environment:
For details, see the [Poetry documentation on environment activation](https://python-poetry.org/docs/managing-environments/#bash-csh-zsh)

   a. On macOS/Linux:
   ```bash
   cd backend/lna-app
   eval $(poetry env activate)
   ```

2. Start the development server:

**On macOS/Linux:**
```bash
uvicorn lna_app.main:app --reload
```

**On Windows:**
```bash
python -m uvicorn lna_app.main:app --reload
```

The application will be available at `http://localhost:8000`

### Running Tests

To run the tests:
```bash
python -W all -m unittest discover -v tests
```

The `-W all` flag enables all warnings, which helps catch potential issues early in development.