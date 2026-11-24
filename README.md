# AI Project Skeleton

A reusable Python project template built with Python 3.12, uv, Pydantic Settings, and HTTPX.

## Features

- Clean `src`-based project structure.
- Environment-based configuration using Pydantic Settings.
- Asynchronous HTTP requests using HTTPX.
- Automatic retries for temporary network and server errors.
- Configurable request timeouts.
- Automated testing with pytest.
- Code quality checks using Ruff and pre-commit.

## Requirements

- Python 3.12+
- uv

## Installation

Clone the repository and navigate into the project directory.

Install dependencies:

```powershell
uv sync --dev
```

## Configuration

Copy `.env.example` to `.env` and update the values as required.

Available settings:

| Variable | Purpose |
|---|---|
| APP_BASE_URL | API base URL |
| APP_API_KEY | Optional API key |
| APP_TIMEOUT_SECONDS | Request timeout |
| APP_MAX_RETRIES | Maximum retry attempts |
| APP_RETRY_BACKOFF_SECONDS | Initial retry delay |

Never commit `.env` or actual API credentials.

## Running Tests

```powershell
uv run pytest -v
```

## Code Quality

```powershell
uv run ruff check .
uv run ruff format --check .
```

## Pre-commit

Install Git hooks:

```powershell
uv run pre-commit install
```

Run all checks manually:

```powershell
uv run pre-commit run --all-files
```

## Project Structure

```text
ai-project-skeleton/
├── AGENTS.md
├── .env.example
├── .pre-commit-config.yaml
├── README.md
├── pyproject.toml
├── uv.lock
├── src/
│   └── ai_project_skeleton/
│       ├── __init__.py
│       ├── config.py
│       └── client.py
└── tests/
```

## License

For educational and project development purposes.
