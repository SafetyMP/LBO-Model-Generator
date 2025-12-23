# AI-Powered LBO Model Validator and Enhancement Suite

## Overview

The LBO Model Generator now includes a comprehensive AI-powered validation and enhancement suite that provides 10 different AI capabilities to improve model quality, debugging, and analysis.

## Features

### 1. Model Validation and Quality Assurance
Validates LBO assumptions for realism, consistency, and common errors.

```python
from lbo_model_generator import LBOModel, LBOAssumptions
from lbo_ai_validator import LBOModelAIValidator

model = LBOModel(assumptions)
validation = model.validate_with_ai(industry="Software")

if not validation["is_valid"]:
    print("Errors:", validation["errors"])
    print("Warnings:", validation["warnings"])
    print("Suggestions:", validation["suggestions"])
```

### 2. Output Review and Consistency Checks
Reviews generated Excel files for balance sheet balancing, cash flow reconciliation, and formula consistency.

```python
review = model.review_output_with_ai("model.xlsx")
print("Review findings:", review["warnings"])
```

### 3. Scenario Analysis Generation
Automatically generates High/Base/Low scenarios and sensitivity analysis.

```python
scenarios = model.generate_scenarios_with_ai(industry="Manufacturing")
print("High Case IRR:", scenarios["high_case"]["expected_irr"])
print("Sensitivity Matrix:", scenarios["sensitivity_matrix"])
```

### 4. Natural Language Query Interface
Ask questions about your model in plain English.

```python
answer = model.query_model_ai("Why is the IRR 15%?")
print(answer)

answer = model.query_model_ai("What drives the cash flow?")
print(answer)

answer = model.query_model_ai("How sensitive is MOIC to revenue growth?")
print(answer)
```

### 5. Market Benchmarking
Compares your model against industry benchmarks.

```python
benchmark = model.benchmark_against_market("Technology")
print("Industry Average Entry Multiple:", benchmark["industry_averages"]["entry_multiple"])
print("Deviations:", benchmark["deviations"])
print("Recommendations:", benchmark["recommendations"])
```

### 6. Documentation Generation
Automatically generates comprehensive model documentation.

```python
doc = model.generate_documentation_ai("model.xlsx")
with open("model_documentation.md", "w") as f:
    f.write(doc)
```

### 7. Error Diagnosis
AI-powered debugging and error diagnosis.

```python
try:
    model.export_to_excel("output.xlsx")
except Exception as e:
    diagnosis = model.diagnose_error_ai(str(e), traceback.format_exc())
    print("Root Cause:", diagnosis["root_cause"])
    print("Fix Suggestions:", diagnosis["fix_suggestions"])
```

### 8. Optimization Suggestions
Suggests optimal debt structures and deal terms.

```python
optimization = model.optimize_debt_structure_ai()
print("Recommended Debt Structure:", optimization["recommended_debt_structure"])
print("Expected IRR Improvement:", optimization["expected_irr_improvement"])
```

### 9. Dynamic Prompt Enhancement
Enhances business descriptions to improve AI recommendations.

```python
from lbo_ai_validator import LBOModelAIValidator

validator = LBOModelAIValidator()
enhanced = validator.enhance_business_description("Tech company with $10M revenue")
print("Enhanced Description:", enhanced["enhanced_description"])
print("Missing Information:", enhanced["missing_information"])
```

### 10. Real-Time Guidance
Provides contextual help during model building.

```python
help_text = validator.get_contextual_help(
    "revenue_growth_rate",
    {"entry_ebitda": 10000},
    field_name="revenue_growth_rate"
)
print(help_text)
```

## Command Line Usage

### Basic Validation
```bash
python lbo_input_generator.py \
    --input config.json \
    --output model.xlsx \
    --ai-validate \
    --industry "Software"
```

### Full AI Suite
```bash
python lbo_input_generator.py \
    --input config.json \
    --output model.xlsx \
    --ai-validate \
    --ai-review \
    --ai-scenarios \
    --ai-benchmark \
    --industry "SaaS Software" \
    --api-key $OPENAI_API_KEY
```

### Error Diagnosis
```bash
python lbo_input_generator.py \
    --input config.json \
    --output model.xlsx \
    --ai-diagnose
```

## Python API Examples

### Complete Workflow with AI
```python
from lbo_model_generator import create_lbo_from_inputs

# Load configuration
config = {...}  # Your LBO assumptions

# Create model
model = create_lbo_from_inputs(config)

# Validate assumptions
validation = model.validate_with_ai(industry="Technology")
if validation["is_valid"]:
    print("✓ Validation passed")
else:
    print("⚠️ Issues found:", validation["warnings"])

# Export with validation
model.export_to_excel(
    "model.xlsx",
    validate_with_ai=True,
    industry="Technology"
)

# Review output
review = model.review_output_with_ai("model.xlsx")
print("Review:", review["suggestions"])

# Generate scenarios
scenarios = model.generate_scenarios_with_ai(industry="Technology")
print("Scenarios:", scenarios)

# Benchmark
benchmark = model.benchmark_against_market("Technology")
print("Benchmark:", benchmark["recommendations"])

# Query model
answer = model.query_model_ai("What is the optimal exit year?")
print("AI Answer:", answer)

# Get optimization suggestions
optimization = model.optimize_debt_structure_ai()
print("Optimization:", optimization)
```

## Setup

1. Install OpenAI package:
```bash
pip install openai
```

2. Set API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or pass it directly:
```python
validator = LBOModelAIValidator(api_key='your-key')
```

## Cost Considerations

- Default model: `gpt-4o-mini` (cost-effective)
- Can switch to `gpt-4` for more advanced analysis:
```python
validator = LBOModelAIValidator(model="gpt-4")
```

## Error Handling

All AI methods gracefully handle errors and API unavailability:

```python
try:
    result = model.validate_with_ai()
except Exception as e:
    print(f"AI validation unavailable: {e}")
    # Continue without AI
```

## Best Practices

1. **Validate Early**: Run validation before generating Excel files
2. **Review Output**: Always review generated models for consistency
3. **Use Scenarios**: Generate scenarios to understand sensitivity
4. **Benchmark**: Compare against market to validate assumptions
5. **Query for Insights**: Use natural language queries to understand results
6. **Document**: Generate documentation for complex models
7. **Optimize**: Use optimization suggestions to improve deal structures

## Integration Points

The AI features are integrated at key points:
- Before model export (validation)
- After Excel generation (review)
- During error handling (diagnosis)
- On-demand (queries, scenarios, benchmarking)

## Notes

- All AI features are optional - models work without them
- API key can be set via environment variable or parameter
- Results include confidence scores and detailed explanations
- All methods return structured data for programmatic use

