# Test Files Update - AI-Generated Company

## Overview

All test files have been updated to use an AI-generated company instead of hardcoded test inputs. This provides more realistic and varied test scenarios.

## AI-Generated Test Company

**Company:** TechWave Solutions  
**Industry:** Software as a Service (SaaS)  
**Description:** Mid-market SaaS company specializing in cloud-based project management software for SMEs

### Key Metrics
- **Current Revenue:** $35M
- **Current EBITDA:** $7M
- **Entry Multiple:** 6.0x
- **Entry EBITDA:** $7,000 (in thousands)
- **Revenue Growth:** 15% → 12% → 10% → 8% → 7% (5-year projection)
- **COGS:** 30% of revenue
- **SG&A:** 25% of revenue
- **CapEx:** 5% of revenue

### Debt Structure
- **Senior Debt:** 1.5x EBITDA, 7% interest, amortizing over 5 years
- **Subordinated Debt:** 2.0x EBITDA, 11% interest, bullet payment

## Files Updated

### 1. `test_lbo_generator.py`
- ✅ Updated `test_basic_lbo_model()` to use AI company
- ✅ Updated `test_balance_sheet_balancing()` to use AI company
- ✅ Updated `test_cash_flow_reconciliation()` to use AI company
- ✅ Updated `test_debt_schedule()` to use AI company
- ✅ Updated `test_ai_recommendations()` to use AI company
- ✅ Added `load_ai_test_company()` helper function
- ✅ Added `get_default_test_config()` fallback function

### 2. `test_ai_with_key.py`
- ✅ Updated to use AI-generated company from test fixture
- ✅ Loads company data from `ai_test_company.json`

### 3. `ai_test_company.json` (New)
- Test fixture containing AI-generated company data
- Includes full LBO configuration
- Can be regenerated with different companies for variety

## Benefits

1. **Realistic Scenarios** - Tests use industry-appropriate metrics
2. **Variety** - Easy to regenerate with different companies
3. **Consistency** - All tests use the same company data
4. **Maintainability** - Company data stored in one JSON file
5. **AI-Powered** - Leverages AI to create realistic test cases

## Usage

### Running Tests
```bash
python3 tests/test_lbo_generator.py
```

### Regenerating Test Company
To generate a new AI company for testing:

```python
import os
import sys
import json
sys.path.insert(0, 'src')
import openai
from lbo_ai_recommender import LBOModelAIRecommender

# Generate new company
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# ... generate company description ...

# Get LBO parameters
recommender = LBOModelAIRecommender()
recommendations = recommender.recommend_parameters(...)

# Save to ai_test_company.json
```

## Test Results

All tests pass with the AI-generated company:
- ✅ Basic LBO Model Generation
- ✅ Balance Sheet Balancing
- ✅ Cash Flow Reconciliation
- ✅ Debt Schedule
- ✅ AI Recommendations

## Company Profile: TechWave Solutions

**Business Model:**
- Recurring revenue model (85% subscriptions)
- 90% customer retention rate
- Diverse customer base across IT, construction, marketing

**Growth Prospects:**
- Projected 20% CAGR over 5 years
- Expansion into international markets
- New features and integrations planned

**LBO Characteristics:**
- Strong cash flow generation
- Predictable revenue streams
- Scalable business model
- Suitable for leveraged buyout

## Notes

- The AI company data is stored in `tests/ai_test_company.json`
- Tests automatically fall back to default config if file not found
- Company can be easily swapped for different test scenarios
- All financial metrics are in thousands (matching model format)

