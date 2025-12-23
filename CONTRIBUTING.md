# Contributing to LBO Model Generator

Thank you for your interest in contributing to the LBO Model Generator! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Maintain professional standards

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/lbo-model-generator/issues)
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs. actual behavior
   - Python version and environment details
   - Relevant error messages or logs

### Suggesting Features

1. Check if the feature has already been suggested
2. Open an issue describing:
   - The feature and its use case
   - Why it would be valuable
   - Potential implementation approach (if you have ideas)

### Pull Requests

1. **Fork the repository** and create a feature branch
2. **Follow coding standards**:
   - Use type hints for all functions
   - Follow PEP 8 style guide
   - Keep functions focused and under 100 lines when possible
   - Add docstrings to all public functions
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Ensure all tests pass**: `pytest`
6. **Format code**: `black src/ tests/`
7. **Lint code**: `flake8 src/ tests/`
8. Submit the PR with a clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/lbo-model-generator.git
cd lbo-model-generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

## Code Style

- **Line length**: 100 characters (Black default)
- **Type hints**: Required for all function parameters and return values
- **Docstrings**: Use Google-style docstrings
- **Naming**: 
  - Functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

## Testing

- Write unit tests for new features
- Aim for >80% code coverage
- Run tests: `pytest`
- Run with coverage: `pytest --cov=src --cov-report=html`

## Project Structure

- `src/` - Source code modules
- `tests/` - Test suite
- `docs/` - Documentation
- `examples/` - Example configurations
- `output/` - Generated files (gitignored)

## Commit Messages

Use clear, descriptive commit messages:
- Start with a verb (Add, Fix, Update, Refactor, etc.)
- Keep first line under 50 characters
- Add detailed description if needed

Example:
```
Refactor: Extract debt validation into helper methods

- Split _validate_debt_schedule into 7 helper methods
- Reduce function from 182 to 60 lines
- Improve testability and maintainability
```

## Questions?

Feel free to open an issue for any questions about contributing!

