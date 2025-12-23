# Quick Start Guide

## Installation

```bash
# Navigate to project directory
cd lbo_model_generator

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### 1. Generate a Template

```bash
python run.py --template
```

This creates `examples/lbo_input_template.json` that you can edit.

### 2. Generate Model from JSON

```bash
python run.py --input examples/lbo_input_template.json --output output/my_model.xlsx
```

### 3. Interactive Mode

```bash
python run.py --interactive
```

Follow the prompts to enter your assumptions.

### 4. AI-Powered Recommendations

```bash
# Set your OpenAI API key
export OPENAI_API_KEY='your-key-here'

# Generate from business description
python run.py \
    --ai-description "SaaS company with $10M revenue and 30% EBITDA margin" \
    --ai-industry "Software" \
    --output output/ai_model.xlsx
```

## Common Commands

```bash
# Basic model generation
python run.py --input examples/lbo_input_template.json --output output/model.xlsx

# With AI validation
python run.py \
    --input examples/lbo_input_template.json \
    --output output/model.xlsx \
    --ai-validate \
    --industry "Technology"

# Full AI suite
python run.py \
    --input examples/lbo_input_template.json \
    --output output/model.xlsx \
    --ai-validate \
    --ai-review \
    --ai-scenarios \
    --ai-benchmark \
    --industry "SaaS Software"

# Run tests
python tests/test_lbo_generator.py
```

## Project Structure

- `src/` - Source code
- `tests/` - Test files
- `docs/` - Documentation
- `examples/` - Example JSON files
- `output/` - Generated Excel files

## Next Steps

1. Read [README.md](README.md) for full documentation
2. Check [docs/README_LBO_GENERATOR.md](docs/README_LBO_GENERATOR.md) for detailed usage
3. See [docs/README_AI_VALIDATOR.md](docs/README_AI_VALIDATOR.md) for AI features

