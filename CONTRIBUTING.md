# Contributing to Engli

Thank you for your interest in contributing to Engli!

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/engli.git`
3. Create a virtual environment: `python3 -m venv .venv`
4. Activate it: `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
5. Install with dev dependencies: `pip install -e ".[dev]"`
6. Run tests: `pytest`

## Code Style

- Use type hints
- Follow PEP 8
- Format with Black: `black src/ tests/`
- Lint with Ruff: `ruff check src/ tests/`
- Type check with mypy: `mypy src/`

## Testing

- Write tests for new features
- Run the full test suite before submitting PRs
- Ensure all tests pass: `pytest`

## Submitting Changes

1. Create a branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Add tests
4. Run tests and ensure they pass
5. Commit with a clear message
6. Push to your fork
7. Open a pull request

## Documentation

Update documentation for any user-facing changes.

## Questions

Open an issue for questions or discussion.
