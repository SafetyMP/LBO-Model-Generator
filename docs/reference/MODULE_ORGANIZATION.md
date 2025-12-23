# Module Organization Guide

## Overview

The LBO Model Generator codebase is organized into logical modules with clear responsibilities. This document describes the module structure and their relationships.

> **Note**: This document focuses on module organization. For complete project structure, see [PROJECT_STRUCTURE_COMPLETE.md](PROJECT_STRUCTURE_COMPLETE.md).

## Module Structure

### Core Modules (`src/`)

#### 1. Core Model Logic
- **`lbo_model_generator.py`** (3,256 lines)
  - **Purpose**: Core LBO model calculation engine
  - **Classes**: 
    - `LBOAssumptions` - Model input parameters
    - `LBODebtStructure` - Debt instrument configuration
    - `LBOModel` - Main model class
    - `ExcelConstants` - Excel layout constants
    - `ExcelRowFinder` - Excel row finding utilities
  - **Key Functions**:
    - `create_lbo_from_inputs()` - Factory function to create models
  - **Responsibilities**:
    - Financial statement generation (Income Statement, Balance Sheet, Cash Flow)
    - Debt schedule calculations
    - Returns analysis (IRR, MOIC)
    - Excel export (legacy and industry-standard)

#### 2. Input Handling
- **`lbo_input_generator.py`** (460+ lines)
  - **Purpose**: CLI interface and input processing
  - **Key Functions**:
    - `create_input_template()` - Generate input template
    - `load_config_from_json()` - Load configuration from JSON
    - `interactive_input()` - Interactive input collection
    - `main()` - CLI entry point
  - **Responsibilities**:
    - Command-line argument parsing
    - JSON configuration loading
    - Interactive user input
    - AI recommendation integration

#### 3. AI Integration
- **`lbo_ai_recommender.py`** (200+ lines)
  - **Purpose**: AI-powered parameter recommendations
  - **Classes**:
    - `LBORecommendations` - Recommendation data structure
    - `LBOModelAIRecommender` - AI recommender class
  - **Key Functions**:
    - `recommend_lbo_parameters()` - Get AI recommendations
  - **Responsibilities**:
    - Business description analysis
    - Parameter recommendation generation
    - Industry-specific recommendations

- **`lbo_ai_validator.py`** (882 lines)
  - **Purpose**: AI-powered validation and analysis
  - **Classes**:
    - `ValidationResult` - Validation results
    - `ScenarioAnalysis` - Scenario analysis results
    - `BenchmarkResult` - Benchmarking results
    - `LBOModelAIValidator` - AI validator class
  - **Key Functions**:
    - Model quality validation
    - Output review
    - Scenario generation
    - Natural language queries
    - Market benchmarking
    - Documentation generation
    - Error diagnosis
    - Optimization suggestions
  - **Responsibilities**:
    - Comprehensive AI-powered model validation
    - Quality assurance
    - Scenario analysis
    - User assistance

#### 4. Excel Export
- **`lbo_excel_template.py`** (Alternative Format)
  - **Purpose**: Excel template utilities for alternative export format
  - **Classes**:
    - `LBOExcelTemplate` - Template utilities class
  - **Responsibilities**:
    - Alternative Excel sheet creation
    - Formatting utilities for additional sheets
    - Used when `use_industry_standards=False`

- **`lbo_industry_standards.py`** (172 lines)
  - **Purpose**: Industry-standard formatting definitions
  - **Classes**:
    - `IndustryStandardTemplate` - Industry-standard formatting
  - **Key Features**:
    - Color coding standards (input, calculation, output cells)
    - Font standards (Calibri, sizes)
    - Border and alignment standards
    - Cell formatting methods
  - **Responsibilities**:
    - Define industry-standard formatting
    - Provide formatting utility methods
    - Column structure definitions

- **`lbo_industry_excel.py`** (691 lines)
  - **Purpose**: Industry-standard Excel export
  - **Classes**:
    - `IndustryStandardExcelExporter` - Industry-standard exporter
  - **Key Methods**:
    - `_create_cover_sheet()` - Cover page
    - `_create_summary_sheet()` - Executive summary
    - `_create_assumptions_sheet()` - Assumptions
    - `_create_income_statement_sheet()` - Income statement
    - `_create_cash_flow_sheet()` - Cash flow
    - `_create_balance_sheet()` - Balance sheet
    - `_create_debt_schedule_sheet()` - Debt schedule
    - `_create_returns_sheet()` - Returns analysis
  - **Responsibilities**:
    - Generate industry-standard Excel files
    - Apply professional formatting
    - Create navigation hyperlinks
    - Protect formula cells

#### 5. Utilities
- **`lbo_constants.py`**
  - **Purpose**: Centralized constants
  - **Classes**:
    - `LBOConstants` - All model constants
  - **Key Constants**:
    - Financial ratios and percentages
    - Days outstanding defaults
    - Multiples defaults
    - Years and periods
    - Excel export settings
    - AI configuration
  - **Responsibilities**:
    - Store all magic numbers
    - Provide default values
    - Centralize configuration

- **`lbo_exceptions.py`**
  - **Purpose**: Custom exception classes
  - **Classes**:
    - `LBOError` - Base exception
    - `LBOValidationError` - Validation errors
    - `LBOConfigurationError` - Configuration errors
    - `LBOCalculationError` - Calculation errors
    - `LBOAIServiceError` - AI service errors
    - `LBOExcelExportError` - Excel export errors
  - **Responsibilities**:
    - Provide specific error types
    - Improve error handling
    - Better error messages

- **`lbo_validation.py`**
  - **Purpose**: Input validation utilities
  - **Key Functions**:
    - `validate_output_path()` - Validate file paths
    - `sanitize_filename()` - Sanitize filenames
    - `validate_api_key()` - Validate API keys
    - `validate_json_input()` - Validate JSON configs
    - `validate_numeric_input()` - Validate numbers
    - `validate_percentage_input()` - Validate percentages
  - **Responsibilities**:
    - Input validation
    - Path sanitization
    - Type checking

## Module Dependencies

```
lbo_model_generator.py (Core)
├── lbo_constants.py
├── lbo_exceptions.py
├── lbo_excel_template.py (legacy)
├── lbo_industry_standards.py
└── lbo_industry_excel.py

lbo_input_generator.py (CLI)
├── lbo_model_generator.py
├── lbo_exceptions.py
├── lbo_validation.py
└── lbo_ai_recommender.py (optional)

lbo_ai_recommender.py (AI)
├── lbo_exceptions.py
└── lbo_validation.py

lbo_ai_validator.py (AI)
├── lbo_exceptions.py
└── lbo_validation.py

lbo_industry_excel.py (Excel)
└── lbo_industry_standards.py
```

## Import Strategy

All modules use a consistent import strategy:

```python
# Handle both package and direct imports
try:
    from .module_name import ClassName
except ImportError:
    from module_name import ClassName
```

This allows:
- Package imports: `from lbo_model_generator import LBOModel`
- Direct imports: `from lbo_model_generator.src.lbo_model_generator import LBOModel`
- Testing: Direct module imports in test files

## Module Responsibilities Summary

| Module | Primary Responsibility | Lines | Dependencies |
|--------|----------------------|-------|--------------|
| `lbo_model_generator.py` | Core model calculations | 3,256 | Constants, Exceptions, Excel |
| `lbo_input_generator.py` | CLI and input handling | 460+ | Model, Validation, AI |
| `lbo_ai_recommender.py` | AI recommendations | 200+ | Exceptions, Validation |
| `lbo_ai_validator.py` | AI validation | 882 | Exceptions, Validation |
| `lbo_industry_excel.py` | Industry Excel export | 691 | Industry Standards |
| `lbo_industry_standards.py` | Formatting standards | 172 | None |
| `lbo_excel_template.py` | Alternative Excel utilities | 500+ | None |
| `lbo_constants.py` | Constants | 100+ | None |
| `lbo_exceptions.py` | Exceptions | 50+ | None |
| `lbo_validation.py` | Validation utilities | 200+ | Exceptions, Constants |

## Best Practices

1. **Separation of Concerns**: Each module has a single, clear responsibility
2. **Dependency Management**: Modules only import what they need
3. **Error Handling**: Use custom exceptions for better error messages
4. **Constants**: All magic numbers in `lbo_constants.py`
5. **Validation**: Input validation in dedicated module
6. **Format Options**: Industry-standard format (default) and alternative format available

## Future Organization Considerations

If the codebase grows, consider organizing into subdirectories:

```
src/
├── core/
│   ├── model.py
│   └── assumptions.py
├── excel/
│   ├── legacy_template.py
│   ├── industry_standards.py
│   └── industry_excel.py
├── ai/
│   ├── recommender.py
│   └── validator.py
├── utils/
│   ├── constants.py
│   ├── exceptions.py
│   └── validation.py
└── cli/
    └── input_generator.py
```

However, the current flat structure is appropriate for the current codebase size.

