# AI Project Skeleton - Agent Instructions

## Project Overview
This is a reusable Python project skeleton built with Python 3.12,
uv, Pydantic Settings, and HTTPX.

## Project Structure
- `src/ai_project_skeleton/`: Application source code.
- `tests/`: Automated tests.
- `config.py`: Environment-based application configuration.
- `client.py`: Asynchronous HTTP client with retries and timeouts.

## Development Rules
- Use Python 3.12 or newer.
- Follow the src-layout structure.
- Use type hints for functions and methods.
- Use Pydantic Settings for configuration.
- Never hardcode API keys, passwords, or secrets.
- Use asynchronous HTTP requests with HTTPX.
- Write tests using pytest and mocked HTTP transports.
- Keep functions small and readable.

## Quality Checks
Run these commands before committing:

- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run pytest -v`

## Testing Rules
- Test successful requests.
- Test retry behavior and exhausted retries.
- Test timeout and HTTP error handling.
- Do not depend on external APIs during tests.

## Git Rules
- Never commit `.env` files or secrets.
- Keep `.env.example` updated when configuration changes.