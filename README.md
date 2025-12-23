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

## Project Structure

```
lbo_model_generator/
├── src/                          # Source code modules
│   ├── lbo_model_generator.py    # Core LBO model logic (3,256 lines)
│   ├── lbo_input_generator.py    # CLI and input handling
│   ├── lbo_ai_recommender.py     # AI recommendations
│   ├── lbo_ai_validator.py       # AI validation and analysis
│   ├── lbo_constants.py           # Centralized constants
│   ├── lbo_exceptions.py         # Custom exceptions
│   ├── lbo_validation.py          # Input validation
│   ├── lbo_excel_template.py     # Legacy Excel template
│   ├── lbo_industry_standards.py  # Industry-standard formatting
│   └── lbo_industry_excel.py     # Industry-standard Excel export
├── tests/                        # Test suite
│   ├── test_lbo_generator.py     # Core functionality tests
│   ├── test_ai_mock.py           # Mock AI tests
│   ├── test_ai_with_key.py       # Real AI tests
│   └── ai_test_company.json      # Test data
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
git clone https://github.com/yourusername/lbo-model-generator.git
cd lbo-model-generator

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
  url = {https://github.com/yourusername/lbo-model-generator}
}
```

## Acknowledgments

- Built following investment banking industry standards
- AI-powered features powered by OpenAI
- Excel formatting based on best practices from top-tier financial institutions

