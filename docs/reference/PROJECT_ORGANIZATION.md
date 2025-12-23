# Project Organization Guide

This document describes the organization and structure of the LBO Model Generator codebase, following Python best practices and industry standards.

## Directory Structure

```
lbo_model_generator/
│
├── src/                          # Core source code (Python package)
│   ├── __init__.py              # Package initialization and exports
│   ├── lbo_model_generator.py    # Core LBO model engine (~2,468 lines)
│   ├── lbo_engine.py             # Streamlit engine wrapper (~335 lines)
│   ├── lbo_input_generator.py    # CLI interface (~644 lines)
│   ├── lbo_ai_recommender.py     # AI recommendations (~200 lines)
│   ├── lbo_ai_validator.py       # AI validation (~882 lines)
│   ├── lbo_model_auditor.py      # AI auditing (~400 lines)
│   ├── lbo_consistency_helpers.py # Consistency checks (~200 lines)
│   ├── lbo_validation_enhanced.py # Enhanced validation (~400 lines)
│   ├── lbo_industry_excel.py     # Excel export (~1,754 lines)
│   ├── lbo_industry_standards.py # Formatting standards (~172 lines)
│   ├── lbo_excel_template.py     # Legacy template (~400 lines)
│   ├── lbo_excel_helpers.py      # Excel helpers (~200 lines)
│   ├── lbo_chart_improvements.py # Chart enhancements (~300 lines)
│   ├── lbo_constants.py           # Constants (~100 lines)
│   ├── lbo_exceptions.py          # Custom exceptions (~100 lines)
│   ├── lbo_validation.py          # Input validation (~200 lines)
│   └── lbo_logging.py             # Logging config (~141 lines)
│
├── streamlit_modules/            # Streamlit dashboard modules
│   ├── __init__.py               # Module exports
│   ├── app_config.py             # Configuration and session state
│   ├── app_utils.py              # Utility functions and caching
│   ├── app_visualizations.py    # Visualization functions
│   ├── app_analysis.py           # Advanced analysis functions
│   ├── app_export.py             # Export functionality
│   ├── app_performance.py        # Performance optimization
│   └── app_ui.py                 # UI helper functions
│
├── pages/                        # Streamlit pages (multi-page app)
│   ├── 1_📊_Dashboard.py        # Main dashboard
│   ├── 2_⚙️_Assumptions.py       # Input configuration
│   ├── 3_📈_Analysis.py          # Analysis and visualizations
│   └── 4_ℹ️_Help.py              # Help and documentation
│
├── tests/                        # Test suite
│   ├── test_lbo_generator.py     # Core functionality tests
│   ├── test_ai_mock.py           # Mock AI tests
│   ├── test_ai_with_key.py       # Real AI tests
│   ├── test_debt_validation.py   # Debt validation tests
│   ├── test_streamlit_modules.py # Streamlit module tests
│   └── test_improvements.py      # Improvement tests
│
├── docs/                         # Documentation
│   ├── guides/                   # User guides
│   │   ├── STREAMLIT_DASHBOARD.md
│   │   ├── INTERACTIVE_TEST_GUIDE.md
│   │   ├── QUICK_START.md
│   │   ├── USER_INSTRUCTIONS.md
│   │   └── API_KEY_SETUP.md
│   ├── reference/                # Reference documentation
│   │   ├── PROJECT_STRUCTURE_COMPLETE.md
│   │   ├── MODULE_ORGANIZATION.md
│   │   ├── INDUSTRY_STANDARDS_IMPLEMENTATION.md
│   │   ├── TEMPLATE_ENHANCEMENTS.md
│   │   └── PROJECT_ORGANIZATION.md (this file)
│   ├── development/              # Development docs
│   │   ├── PEP8_COMPLIANCE_REPORT.md
│   │   └── CODE_QUALITY.md
│   ├── analysis/                 # Analysis reports
│   ├── archive/                  # Archived documentation
│   ├── README_LBO_GENERATOR.md   # Main usage guide
│   ├── README_AI_INTEGRATION.md  # AI integration guide
│   ├── README_AI_VALIDATOR.md    # AI validator guide
│   └── AI_FEATURES_SUMMARY.md    # AI features summary
│
├── examples/                     # Example files
│   ├── lbo_input_template.json   # Input template
│   └── ai_recommendations_output.json
│
├── .streamlit/                   # Streamlit configuration
│   ├── config.toml                # UI configuration
│   ├── secrets.toml.example      # Secrets template
│   └── secrets.toml               # API keys (gitignored)
│
├── output/                       # Generated files (gitignored)
│   └── test_files/               # Test outputs
│
├── app.py                        # Streamlit entry point
├── run.py                        # CLI entry point
├── interactive_test.py           # Interactive test script
├── compare_streamlit_test.py     # Test case comparison script
│
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup script
├── pyproject.toml                # Modern Python project config
├── Makefile                      # Build automation
├── README.md                     # Main README
├── CHANGELOG.md                  # Version history
├── LICENSE                       # Apache 2.0 license
├── CONTRIBUTING.md               # Contribution guidelines
└── .gitignore                    # Git ignore rules
```

## Code Organization Principles

### 1. Separation of Concerns

- **Core Logic** (`src/`): Pure business logic, no UI dependencies
- **Streamlit Modules** (`streamlit_modules/`): UI-specific logic, separated by function
- **Pages** (`pages/`): Streamlit page definitions, minimal logic
- **Tests** (`tests/`): Test files mirror source structure

### 2. Module Responsibilities

#### Core Modules (`src/`)
- **lbo_model_generator.py**: Core financial calculations
- **lbo_engine.py**: Simplified interface for Streamlit
- **lbo_input_generator.py**: CLI interface
- **lbo_ai_*.py**: AI integration modules
- **lbo_industry_*.py**: Excel export modules
- **lbo_*.py**: Utility modules (constants, exceptions, validation, logging)

#### Streamlit Modules (`streamlit_modules/`)
- **app_config.py**: Configuration, session state, API key management
- **app_utils.py**: Utility functions, caching, test case loading
- **app_visualizations.py**: All visualization functions (Plotly charts)
- **app_analysis.py**: Advanced analysis (break-even, sensitivity)
- **app_export.py**: Export functionality (Excel, PDF)
- **app_performance.py**: Performance optimization (cache management)
- **app_ui.py**: UI helper functions

#### Pages (`pages/`)
- **1_📊_Dashboard.py**: Main results display
- **2_⚙️_Assumptions.py**: Input configuration
- **3_📈_Analysis.py**: Analysis and visualizations
- **4_ℹ️_Help.py**: Help and documentation

### 3. Import Organization

Following PEP 8 import order:
1. Standard library imports
2. Related third-party imports
3. Local application/library imports

Example:
```python
# Standard library
import json
from typing import Dict, List

# Third-party
import pandas as pd
import streamlit as st

# Local
from src.lbo_engine import calculate_lbo
from streamlit_modules.app_config import initialize_session_state
```

### 4. Naming Conventions

- **Modules**: `snake_case` (e.g., `lbo_model_generator.py`)
- **Classes**: `PascalCase` (e.g., `LBOModel`)
- **Functions**: `snake_case` (e.g., `calculate_lbo`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_TAX_RATE`)
- **Private**: `_leading_underscore` (e.g., `_calculate_irr`)

### 5. File Organization

#### Configuration Files
- **Root level**: Project-wide configs (`setup.py`, `pyproject.toml`, `requirements.txt`)
- **`.streamlit/`**: Streamlit-specific configs
- **`docs/`**: Documentation files

#### Test Files
- Mirror source structure: `tests/test_*.py` matches `src/*.py`
- Test data: `tests/*.json` for test fixtures

#### Example Files
- Templates: `examples/lbo_input_template.json`
- Sample outputs: `examples/ai_recommendations_output.json`

## Python Best Practices

### 1. Package Structure

- **`src/`** is a proper Python package with `__init__.py`
- Exports are defined in `src/__init__.py`
- Imports use relative imports within package (`from .module import ...`)
- Absolute imports for external packages

### 2. Type Hints

- Functions include type hints for parameters and return values
- Use `typing` module for complex types (`Dict`, `List`, `Optional`, etc.)
- Example:
  ```python
  def calculate_lbo(
      entry_multiple: float,
      leverage_ratio: float,
      rev_growth: float,
      ebitda_margin: float,
  ) -> Dict[str, Any]:
      ...
  ```

### 3. Documentation

- **Docstrings**: All public functions and classes have docstrings
- **Format**: Google-style docstrings
- **Documentation files**: Markdown files in `docs/` directory
- **Inline comments**: Explain complex logic, not obvious code

### 4. Error Handling

- Custom exceptions in `src/lbo_exceptions.py`
- Specific exception types for different error categories
- Error messages are informative and actionable
- Example:
  ```python
  raise LBOCalculationError(
      f"Failed to initialize LBO model: {e}"
  ) from e
  ```

### 5. Logging

- Centralized logging configuration in `src/lbo_logging.py`
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Structured logging format
- Example:
  ```python
  logger.info("LBO model initialized successfully")
  logger.warning("Debt schedule validation warning: ...")
  ```

### 6. Testing

- Test files mirror source structure
- Test functions use `test_` prefix
- Test classes use `Test` prefix
- Use pytest fixtures for test data
- Example:
  ```python
  def test_basic_lbo_model():
      """Test basic LBO model generation."""
      ...
  ```

## Streamlit-Specific Organization

### 1. Multi-Page Structure

- Pages in `pages/` directory
- Naming convention: `{order}_{icon}_{name}.py`
- Each page has `st.set_page_config()` at top
- Pages are independent but share session state

### 2. Module Separation

- UI logic separated from business logic
- Visualization functions in `app_visualizations.py`
- Analysis functions in `app_analysis.py`
- Export functions in `app_export.py`

### 3. Session State

- Centralized in `app_config.py`
- Initialize with `initialize_session_state()`
- Access via `st.session_state`
- Keys follow naming convention: `current_results`, `current_inputs`, etc.

### 4. Caching

- Use `@st.cache_data` for expensive calculations
- Cache management UI in `app_performance.py`
- Clear cache when assumptions change significantly

## Configuration Management

### 1. Environment Variables

- API keys: `OPENAI_API_KEY`
- Loaded via `app_config.py` or `.streamlit/secrets.toml`

### 2. Streamlit Config

- `.streamlit/config.toml`: UI configuration
- `.streamlit/secrets.toml`: Sensitive data (gitignored)

### 3. Project Config

- `pyproject.toml`: Modern Python project configuration
- `setup.py`: Package setup (for compatibility)
- `requirements.txt`: Dependency list

## File Naming Conventions

### Source Files
- **Modules**: `snake_case.py` (e.g., `lbo_model_generator.py`)
- **Streamlit modules**: `app_{purpose}.py` (e.g., `app_config.py`)
- **Pages**: `{order}_{icon}_{name}.py` (e.g., `1_📊_Dashboard.py`)

### Documentation Files
- **Guides**: `{TOPIC}_GUIDE.md` (e.g., `STREAMLIT_DASHBOARD.md`)
- **Reference**: `{TOPIC}.md` (e.g., `PROJECT_ORGANIZATION.md`)
- **Development**: `docs/development/{TOPIC}.md`

### Test Files
- **Test modules**: `test_{module_name}.py` (e.g., `test_lbo_generator.py`)
- **Test data**: `{name}.json` in `tests/` directory

## Dependency Management

### 1. Core Dependencies
- Listed in `requirements.txt`
- Also in `pyproject.toml` for modern tools
- Version constraints specified

### 2. Optional Dependencies
- Streamlit: For web dashboard
- OpenAI: For AI features
- ReportLab: For PDF export

### 3. Development Dependencies
- Listed in `pyproject.toml` under `[project.optional-dependencies.dev]`
- Includes: pytest, black, flake8, mypy

## Git Organization

### 1. Ignored Files
- `.gitignore` includes:
  - Python cache files (`__pycache__/`, `*.pyc`)
  - Virtual environments (`venv/`, `env/`)
  - IDE files (`.vscode/`, `.idea/`)
  - Output files (`output/`, `*.xlsx`)
  - Secrets (`.streamlit/secrets.toml`)
  - Logs (`*.log`)

### 2. Commit Structure
- Clear commit messages
- Feature branches for major changes
- Pull requests for code review

## Best Practices Summary

1. ✅ **Modular Design**: Clear separation of concerns
2. ✅ **Type Hints**: Comprehensive type annotations
3. ✅ **Documentation**: Docstrings and markdown docs
4. ✅ **Testing**: Comprehensive test coverage
5. ✅ **Error Handling**: Custom exceptions with clear messages
6. ✅ **Logging**: Structured logging throughout
7. ✅ **Configuration**: Centralized config management
8. ✅ **Dependencies**: Clear dependency management
9. ✅ **Naming**: Consistent naming conventions
10. ✅ **Code Quality**: PEP 8 compliance, linting, formatting

## References

- [PEP 8 - Style Guide](https://pep8.org/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Project Structure Guide](PROJECT_STRUCTURE_COMPLETE.md)
- [Module Organization](MODULE_ORGANIZATION.md)

