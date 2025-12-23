# LBO Model Generator

A comprehensive Python tool for generating professional Leveraged Buyout (LBO) financial models with AI-powered recommendations, validation, and analysis.

## Features

- **Complete LBO Modeling**: Generate Income Statement, Balance Sheet, Cash Flow Statement, Debt Schedule, and Returns Analysis
- **Excel Export**: Professional Excel output with interactive formulas and multiple sheets
- **AI Integration**: 10 AI-powered features including validation, scenario analysis, benchmarking, and natural language queries
- **Interactive Models**: Excel models with formulas that recalculate when inputs change
- **Scenario Analysis**: High/Base/Low case scenarios with sensitivity analysis
- **Market Benchmarking**: Compare your model against industry standards

## Quick Start

### Installation

```bash
# Clone or download the repository
cd lbo_model_generator

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key (optional, for AI features)
export OPENAI_API_KEY='your-api-key-here'
```

### Interactive Test (Recommended for First-Time Users)

```bash
# Run interactive test with minimal input - AI fills in the rest
python3 interactive_test.py
```

This tool allows you to:
- Provide minimal company information
- Let AI generate missing details
- Test the LBO model generator easily
- Get AI-powered recommendations

See [Interactive Test Guide](docs/guides/INTERACTIVE_TEST_GUIDE.md) for detailed instructions.

### Basic Usage

```bash
# Generate a template
python run.py --template

# Generate model from JSON
python run.py --input examples/lbo_input_template.json --output output/my_model.xlsx

# Interactive mode
python run.py --interactive

# AI-powered recommendations
python run.py --ai-description "SaaS software company with $10M revenue" --ai-industry "Software"
```

## Code Overview

### Architecture

The LBO Model Generator follows a modular architecture with clear separation of concerns:

- **Core Model Engine**: Financial calculations and statement generation
- **AI Integration Layer**: OpenAI-powered recommendations and validation
- **Excel Export Layer**: Industry-standard Excel file generation
- **Input/Output Layer**: CLI, JSON parsing, and interactive interfaces
- **Utilities Layer**: Constants, exceptions, validation, and helpers

### Module Structure

The codebase consists of **18 source modules** (~8,400 lines) organized into functional categories:

#### Core Modules

**`lbo_model_generator.py`** (~2,468 lines)
- **Purpose**: Core LBO model calculation engine
- **Key Classes**:
  - `LBOAssumptions` - Model input parameters (dataclass)
  - `LBODebtStructure` - Debt instrument configuration
  - `LBOModel` - Main model class with all financial calculations
- **Responsibilities**:
  - Income Statement, Balance Sheet, Cash Flow Statement generation
  - Debt schedule calculations with cash flow sweep
  - Returns analysis (IRR, MOIC calculations)
  - Financial statement reconciliation and validation
  - Target-based calibration (exit debt, FCF conversion, growth rates)

**`lbo_input_generator.py`** (~644 lines)
- **Purpose**: CLI interface and input processing
- **Key Functions**:
  - `create_input_template()` - Generate JSON input template
  - `load_config_from_json()` - Load configuration from JSON
  - `interactive_input()` - Interactive user input collection
  - `main()` - CLI entry point with argparse
- **Responsibilities**:
  - Command-line argument parsing
  - JSON configuration loading and validation
  - Interactive user input with AI assistance
  - Error handling and AI-powered diagnosis

#### AI Integration Modules

**`lbo_ai_recommender.py`** (~200 lines)
- **Purpose**: AI-powered parameter recommendations
- **Key Classes**:
  - `LBOModelAIRecommender` - AI recommender class
- **Key Functions**:
  - `recommend_lbo_parameters()` - Get AI recommendations from business description
- **Features**:
  - Business description analysis
  - Industry-specific parameter recommendations
  - Confidence scoring

**`lbo_ai_validator.py`** (~882 lines)
- **Purpose**: Comprehensive AI-powered validation and analysis
- **Key Classes**:
  - `LBOModelAIValidator` - AI validator class
  - `ValidationResult`, `ScenarioAnalysis`, `BenchmarkResult` - Result dataclasses
- **Features**:
  1. Model quality validation
  2. Excel output review
  3. Scenario generation (High/Base/Low)
  4. Natural language queries
  5. Market benchmarking
  6. Documentation generation
  7. Error diagnosis
  8. Optimization suggestions

**`lbo_model_auditor.py`** (~400+ lines)
- **Purpose**: AI-powered code and model auditing
- **Features**:
  - Code quality analysis
  - Model consistency checks
  - Chart structure validation
  - Test case alignment verification

**`lbo_consistency_helpers.py`** (~200+ lines)
- **Purpose**: Financial statement consistency validation
- **Features**:
  - Cross-statement reconciliation checks
  - Balance sheet balancing verification
  - Cash flow reconciliation

#### Excel Export Modules

**`lbo_industry_excel.py`** (~1,754 lines)
- **Purpose**: Industry-standard Excel export
- **Key Classes**:
  - `IndustryStandardExcelExporter` - Main exporter class
- **Key Methods**:
  - `_create_cover_sheet()` - Professional cover page
  - `_create_summary_sheet()` - Executive summary
  - `_create_assumptions_sheet()` - Assumptions with formatting
  - `_create_income_statement_sheet()` - Income statement
  - `_create_balance_sheet()` - Balance sheet
  - `_create_cash_flow_sheet()` - Cash flow statement
  - `_create_debt_schedule_sheet()` - Debt schedule
  - `_create_returns_sheet()` - Returns analysis with sensitivity tables
  - `_create_sources_uses_sheet()` - Sources & Uses table
  - `_create_sensitivity_charts()` - Dynamic sensitivity charts
- **Features**:
  - Industry-standard formatting (color coding, fonts, borders)
  - Interactive formulas that recalculate
  - Navigation hyperlinks between sheets
  - Protected formula cells
  - Professional charts and visualizations

**`lbo_industry_standards.py`** (~172 lines)
- **Purpose**: Industry-standard formatting definitions
- **Key Classes**:
  - `IndustryStandardTemplate` - Formatting standards
- **Features**:
  - Color coding (input cells: blue, calculation: black, output: green)
  - Font standards (Calibri, specific sizes)
  - Border and alignment standards
  - Cell formatting utility methods

**`lbo_excel_template.py`** (~400+ lines)
- **Purpose**: Alternative Excel template format (legacy)
- **Key Classes**:
  - `LBOExcelTemplate` - Alternative template utilities
- **Note**: Used when `use_industry_standards=False`

**`lbo_excel_helpers.py`** (~200+ lines)
- **Purpose**: Excel formatting helper utilities
- **Key Classes**:
  - `ExcelFormattingHelper` - Reusable formatting methods
- **Features**:
  - Standardized cell formatting
  - Chart creation helpers
  - Sheet navigation utilities

**`lbo_chart_improvements.py`** (~300+ lines)
- **Purpose**: Enhanced chart creation and validation
- **Key Classes**:
  - `ChartStructureImprover` - Chart enhancement utilities
- **Features**:
  - Dynamic chart data references
  - Chart structure validation
  - Chart formatting improvements

#### Utility Modules

**`lbo_constants.py`** (~100 lines)
- **Purpose**: Centralized constants
- **Key Classes**:
  - `LBOConstants` - All model constants
- **Includes**:
  - Financial ratios and percentages
  - Days outstanding defaults
  - Multiples defaults
  - Excel export settings
  - AI configuration

**`lbo_exceptions.py`** (~100 lines)
- **Purpose**: Custom exception classes
- **Key Classes**:
  - `LBOError` - Base exception
  - `LBOValidationError` - Validation errors
  - `LBOConfigurationError` - Configuration errors
  - `LBOCalculationError` - Calculation errors
  - `LBOAIServiceError` - AI service errors
  - `LBOExcelExportError` - Excel export errors

**`lbo_validation.py`** (~200+ lines)
- **Purpose**: Input validation
- **Features**:
  - Assumption validation
  - Debt structure validation
  - Financial constraint checking

**`lbo_validation_enhanced.py`** (~400+ lines)
- **Purpose**: Enhanced validation with detailed reporting
- **Key Classes**:
  - `EnhancedLBOValidator` - Advanced validator
- **Features**:
  - Comprehensive validation rules
  - Detailed validation reports
  - Cross-field validation

**`lbo_logging.py`** (~141 lines)
- **Purpose**: Centralized logging configuration
- **Features**:
  - Configurable log levels
  - File and console handlers
  - Structured logging format

### Key Design Patterns

1. **Factory Pattern**: `create_lbo_from_inputs()` creates models from dictionaries
2. **Strategy Pattern**: Multiple Excel export formats (industry-standard vs. legacy)
3. **Template Method**: Consistent sheet creation across Excel exporter
4. **Helper Methods**: Extensive refactoring into focused helper functions (99+ helper methods)
5. **Dataclasses**: Type-safe configuration with `LBOAssumptions`, `LBODebtStructure`

### Code Quality

- **Total Lines**: ~8,400 lines of source code
- **Functions Refactored**: 51 large functions broken into smaller, focused methods
- **Helper Methods Created**: 99+ helper methods for improved maintainability
- **Code Reduction**: ~1,744 lines reduced through refactoring
- **Quality Score**: ~94% (based on comprehensive audit)
- **Type Hints**: Comprehensive type annotations throughout
- **Error Handling**: Custom exceptions with detailed error messages
- **Logging**: Structured logging with configurable levels

### Data Flow

```
User Input (JSON/CLI/Interactive)
    ↓
lbo_input_generator.py (Parse & Validate)
    ↓
LBOAssumptions + LBODebtStructure
    ↓
LBOModel (Financial Calculations)
    ↓
Financial Statements (Income, Balance, Cash Flow, Debt)
    ↓
IndustryStandardExcelExporter (Excel Generation)
    ↓
Excel File (.xlsx)
```

## Project Structure

```
lbo_model_generator/
├── src/                          # Source code modules (~8,400 lines)
│   ├── lbo_model_generator.py    # Core LBO model logic (~2,468 lines)
│   ├── lbo_input_generator.py    # CLI and input handling (~644 lines)
│   ├── lbo_ai_recommender.py     # AI recommendations (~200 lines)
│   ├── lbo_ai_validator.py       # AI validation and analysis (~882 lines)
│   ├── lbo_model_auditor.py      # AI-powered auditing (~400 lines)
│   ├── lbo_consistency_helpers.py # Consistency validation (~200 lines)
│   ├── lbo_validation_enhanced.py # Enhanced validation (~400 lines)
│   ├── lbo_industry_excel.py      # Industry-standard Excel export (~1,754 lines)
│   ├── lbo_industry_standards.py  # Industry-standard formatting (~172 lines)
│   ├── lbo_excel_template.py     # Legacy Excel template (~400 lines)
│   ├── lbo_excel_helpers.py      # Excel formatting helpers (~200 lines)
│   ├── lbo_chart_improvements.py  # Chart enhancements (~300 lines)
│   ├── lbo_constants.py           # Centralized constants (~100 lines)
│   ├── lbo_exceptions.py         # Custom exceptions (~100 lines)
│   ├── lbo_validation.py          # Input validation (~200 lines)
│   └── lbo_logging.py             # Logging configuration (~141 lines)
├── tests/                        # Test suite
│   ├── test_lbo_generator.py     # Core functionality tests
│   ├── test_ai_mock.py           # Mock AI tests
│   ├── test_ai_with_key.py       # Real AI tests
│   ├── test_debt_validation.py  # Debt validation tests
│   └── test_improvements.py      # Improvement tests
├── docs/                          # Documentation
│   ├── README_LBO_GENERATOR.md   # Main usage guide
│   ├── README_AI_INTEGRATION.md  # AI integration
│   ├── README_AI_VALIDATOR.md    # AI validator
│   ├── AI_FEATURES_SUMMARY.md    # AI features
│   ├── guides/                    # User guides
│   └── reference/                 # Reference docs
├── examples/                      # Example files
│   ├── lbo_input_template.json
│   └── ai_recommendations_output.json
├── output/                        # Generated files (gitignored)
├── requirements.txt               # Dependencies
├── run.py                         # Main entry point
├── interactive_test.py            # Interactive test script
└── README.md                      # This file
```

See [Complete Project Structure](docs/reference/PROJECT_STRUCTURE_COMPLETE.md) and [Module Organization](docs/reference/MODULE_ORGANIZATION.md) for detailed information.

## Documentation

### Main Guides
- **[LBO Generator Guide](docs/README_LBO_GENERATOR.md)** - Main usage guide
- **[AI Integration](docs/README_AI_INTEGRATION.md)** - AI recommendations setup
- **[AI Validator](docs/README_AI_VALIDATOR.md)** - AI validation features
- **[AI Features Summary](docs/AI_FEATURES_SUMMARY.md)** - Complete AI features list

### User Guides
- **[Interactive Test Guide](docs/guides/INTERACTIVE_TEST_GUIDE.md)** - Interactive testing instructions
- **[Quick Start Guide](docs/guides/QUICK_START.md)** - Quick start instructions
- **[User Instructions](docs/guides/USER_INSTRUCTIONS.md)** - Detailed user instructions
- **[API Key Setup](docs/guides/API_KEY_SETUP.md)** - OpenAI API key configuration

### Reference Documentation
- **[Industry Standards Implementation](docs/reference/INDUSTRY_STANDARDS_IMPLEMENTATION.md)** - Industry-standard Excel formatting
- **[Complete Project Structure](docs/reference/PROJECT_STRUCTURE_COMPLETE.md)** - Comprehensive project organization
- **[Module Organization](docs/reference/MODULE_ORGANIZATION.md)** - Module structure and dependencies
- **[Template Enhancements](docs/reference/TEMPLATE_ENHANCEMENTS.md)** - Excel template improvements
- **[Codebase Review](CODEBASE_REVIEW.md)** - Comprehensive code review and recommendations
- **[Follow-Up Review](CODEBASE_REVIEW_FOLLOWUP.md)** - Post-improvements review (⭐ 5/5 rating)

## AI Features

The tool includes 10 AI-powered features:

1. **Model Validation** - Validate assumptions for realism
2. **Output Review** - Check Excel files for errors
3. **Scenario Generation** - Auto-generate High/Base/Low scenarios
4. **Natural Language Queries** - Ask questions about your model
5. **Market Benchmarking** - Compare against industry standards
6. **Documentation Generation** - Auto-generate model docs
7. **Error Diagnosis** - AI-powered debugging
8. **Optimization Suggestions** - Improve deal structures
9. **Prompt Enhancement** - Enhance business descriptions
10. **Real-time Guidance** - Contextual help during model building

See [AI Features Summary](docs/AI_FEATURES_SUMMARY.md) for details.

## Requirements

- Python 3.8+
- pandas
- numpy
- openpyxl
- openai (optional, for AI features)

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/SafetyMP/LBO-Model-Generator.git
cd LBO-Model-Generator

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

## Citation

If you use this tool in your research or work, please consider citing:

```bibtex
@software{lbo_model_generator,
  title = {LBO Model Generator},
  author = {LBO Model Generator Team},
  year = {2024},
  license = {Apache-2.0},
  url = {https://github.com/SafetyMP/LBO-Model-Generator}
}
```

## Acknowledgments

- Built following investment banking industry standards
- AI-powered features powered by OpenAI
- Excel formatting based on best practices from top-tier financial institutions

