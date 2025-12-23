# AI-Powered LBO Model Recommendations

The LBO Model Generator now includes AI-powered recommendations using Large Language Models (LLMs) to analyze business descriptions and suggest appropriate LBO model parameters.

## Features

- **Natural Language Input**: Describe your business in plain English
- **Industry-Aware Recommendations**: AI considers industry characteristics, margins, and growth patterns
- **Intelligent Defaults**: Gets you started quickly with realistic assumptions
- **Transparent Reasoning**: Shows confidence level and explanation of recommendations

## Setup

### 1. Install OpenAI Package

```bash
pip install openai
```

### 2. Set API Key

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or pass it directly in code:
```python
from lbo_ai_recommender import LBOModelAIRecommender
recommender = LBOModelAIRecommender(api_key='your-api-key')
```

## Usage

### Command Line - Interactive Mode with AI

```bash
python lbo_input_generator.py --interactive --ai --output my_lbo.xlsx
```

This will prompt you to:
1. Describe your business
2. Optionally provide current revenue, EBITDA, and industry
3. Review AI recommendations
4. Use recommendations as defaults (you can still modify any value)

### Command Line - Direct AI Generation

```bash
python lbo_input_generator.py \
    --ai-description "SaaS company with $15M ARR, 40% EBITDA margins" \
    --ai-revenue 15000000 \
    --ai-ebitda 6000000 \
    --ai-industry "SaaS Software" \
    --output my_lbo.xlsx
```

### Python API

```python
from lbo_ai_recommender import recommend_lbo_parameters, LBOModelAIRecommender
from lbo_model_generator import create_lbo_from_inputs

# Get AI recommendations
business_description = """
TechCorp is a SaaS company providing project management software for mid-market
companies. Founded in 2018, they have grown to $15M ARR with 40% EBITDA margins.
The company serves 500+ customers with strong retention rates.
"""

recommendations = recommend_lbo_parameters(
    business_description,
    current_revenue=15_000_000,
    current_ebitda=6_000_000,
    industry="SaaS Software"
)

# Review recommendations
recommender = LBOModelAIRecommender()
print(recommender.explain_recommendations(recommendations))

# Generate model from recommendations
model = create_lbo_from_inputs(recommendations)
model.export_to_excel("ai_recommended_lbo.xlsx")
```

## What the AI Recommends

The AI analyzes your business description and provides recommendations for:

### Financial Metrics
- **Entry EBITDA**: Estimated based on business size and profitability
- **Entry Multiple**: Appropriate valuation multiple for industry/company
- **Exit Multiple**: Typical exit multiple (typically 0.5-1.5x higher than entry)

### Operating Assumptions
- **Revenue Growth**: Realistic growth rates based on business stage (mature: 2-5%, growth: 5-15%, high-growth: 15%+)
- **COGS %**: Cost structure appropriate for industry
- **SG&A %**: Operating expense ratios typical for the business model
- **CapEx %**: Capital intensity based on asset requirements

### Working Capital
- **Days Sales Outstanding (DSO)**: Payment terms typical for the industry
- **Days Inventory Outstanding (DIO)**: Inventory turnover for the business model
- **Days Payable Outstanding (DPO)**: Supplier payment terms

### Debt Structure
- **Senior Debt**: Typically 1-2x EBITDA at 6-8% interest
- **Subordinated Debt**: 1-3x EBITDA at 10-14% interest
- **Amortization Schedule**: Appropriate repayment structure

## Example Output

```
AI RECOMMENDATIONS SUMMARY
============================================================

Confidence Level: HIGH

Key Recommendations:
Based on the SaaS business model with strong margins and recurring revenue,
recommendations reflect high-growth software company characteristics with
conservative leverage given the asset-light model.

Recommended Parameters:
- Entry EBITDA: $6,000,000
- Entry Multiple: 8.5x
- Exit Multiple: 10.0x
- Revenue Growth (5-year avg): 8.2%

Operating Metrics:
- COGS: 25.0% of revenue
- SG&A: 35.0% of revenue
- CapEx: 2.0% of revenue

Working Capital:
- DSO: 30 days
- DIO: 0 days (no inventory)
- DPO: 15 days

Debt Structure:
- Senior Debt: 1.5x EBITDA, 7.5% interest, amortizing
- Subordinated Debt: 2.0x EBITDA, 12.0% interest, bullet
```

## Best Practices

1. **Provide Context**: The more detail in your business description, the better the recommendations
2. **Include Financials**: If you have current revenue or EBITDA, include them for better accuracy
3. **Specify Industry**: Mentioning the industry helps the AI apply relevant benchmarks
4. **Review Carefully**: AI recommendations are starting points - adjust based on your specific circumstances
5. **Market Conditions**: Consider current market conditions when using recommendations

## Limitations

- Recommendations are based on general industry patterns and may not reflect your specific situation
- Market conditions (interest rates, multiples) change over time
- Always validate recommendations against:
  - Recent comparable transactions
  - Industry reports and benchmarks
  - Professional financial advisors
  - Your company's unique circumstances

## Model Selection

By default, the system uses `gpt-4o-mini` for cost efficiency. You can specify a different model:

```python
recommender = LBOModelAIRecommender(model="gpt-4")
```

Available models:
- `gpt-4o-mini`: Fast and cost-effective (recommended)
- `gpt-4o`: More capable, higher cost
- `gpt-4`: Most capable, highest cost

## Cost Considerations

- Each recommendation call uses approximately 1,500-2,500 tokens
- GPT-4o-mini: ~$0.01-0.02 per recommendation
- GPT-4o: ~$0.05-0.10 per recommendation
- GPT-4: ~$0.15-0.30 per recommendation

## Troubleshooting

**Error: "OpenAI API key required"**
- Set `OPENAI_API_KEY` environment variable or pass `api_key` parameter

**Error: "AI recommendations not available"**
- Install OpenAI package: `pip install openai`

**Poor recommendations**
- Provide more detailed business description
- Include financial metrics if available
- Specify industry clearly
- Consider trying a different model (gpt-4o or gpt-4)

## Privacy

- Business descriptions are sent to OpenAI's API
- Review OpenAI's privacy policy: https://openai.com/policies/privacy-policy
- For sensitive information, consider using manual inputs instead

