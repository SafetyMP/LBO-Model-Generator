# Interactive Test Guide

## Overview

The Interactive Test tool allows you to test the LBO model generator with minimal input. You can provide as much or as little information as you have, and AI will intelligently fill in the missing details.

## Quick Start

```bash
cd lbo_model_generator
python3 interactive_test.py
```

## Prerequisites

1. **OpenAI API Key** (recommended for full functionality)
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```
   
   Without an API key, the tool will use default values instead of AI-generated ones.

2. **Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## What Information to Provide

### Required Information
**None!** You can run the test with zero input - AI will generate everything.

### Optional Information (Provide What You Have)

#### 1. Basic Company Information
- **Company Name**: Name of the company
  - Example: "TechWave Solutions"
  - If omitted: AI will generate a realistic company name

- **Industry Sector**: What industry the company operates in
  - Example: "SaaS Software", "Manufacturing", "Healthcare Services"
  - If omitted: AI will infer from business description

- **Business Description**: Description of what the company does
  - Example: "A SaaS company providing project management software for SMEs"
  - If omitted: AI will generate a detailed business description

#### 2. Financial Metrics (Optional)
- **Current Annual Revenue**: Company's current revenue in dollars
  - Example: 35000000 (for $35M)
  - If omitted: AI will estimate based on company description

- **Current EBITDA**: Company's current EBITDA in dollars
  - Example: 7000000 (for $7M)
  - If omitted: AI will estimate based on industry margins

## How It Works

### Step 1: Information Collection
The tool prompts you for information. You can:
- Enter values for fields you know
- Press Enter to skip fields (AI will generate them)
- Provide partial information (AI will infer the rest)

### Step 2: AI Generation
If you have an API key, AI will:
1. **Generate Missing Company Info**: Creates realistic company details based on what you provided
2. **Generate LBO Parameters**: Creates appropriate LBO model parameters based on the company profile

### Step 3: Model Generation
The tool:
1. Combines your input with AI-generated values
2. Creates a complete LBO model
3. Calculates returns (IRR, MOIC)
4. Optionally exports to Excel
5. Optionally runs AI validation

## Example Usage

### Minimal Input (AI Generates Everything)
```
Company Name: [press Enter]
Industry Sector: [press Enter]
Business Description: [press Enter]
Current Annual Revenue ($): [press Enter]
Current EBITDA ($): [press Enter]
```

AI will generate a complete realistic company profile.

### Partial Input (AI Fills Gaps)
```
Company Name: TechWave Solutions
Industry Sector: SaaS Software
Business Description: [press Enter]
Current Annual Revenue ($): 35000000
Current EBITDA ($): [press Enter]
```

AI will generate the business description and estimate EBITDA.

### Full Input (AI Still Provides LBO Parameters)
```
Company Name: TechWave Solutions
Industry Sector: SaaS Software
Business Description: Cloud-based project management software for SMEs
Current Annual Revenue ($): 35000000
Current EBITDA ($): 7000000
```

AI will still generate optimal LBO parameters (entry multiple, growth rates, debt structure, etc.)

## Output

The tool generates:
1. **Model Configuration Summary** - Shows what will be used
2. **LBO Model Results**:
   - Exit EBITDA
   - Exit Enterprise Value
   - Exit Equity Value
   - MOIC (Multiple on Invested Capital)
   - IRR (Internal Rate of Return)
3. **Excel Export** (optional) - Professional Excel file with all sheets
4. **AI Validation** (optional) - AI review of model assumptions

## Example Session

```
================================================================================
LBO Model Generator - Interactive Test
================================================================================

This tool allows you to test the LBO model generator with minimal input.
You can provide as much or as little information as you have.
AI will fill in the missing details based on what you provide.

✓ OpenAI API key found (format: sk-proj...Q3QA)

--------------------------------------------------------------------------------
📝 Company Information
--------------------------------------------------------------------------------
Provide as much information as you have. Press Enter to skip and let AI generate it.

Company Name: TechWave Solutions
Industry Sector: SaaS Software
Business Description: Cloud project management for SMEs
Current Annual Revenue ($): 35000000
Current EBITDA ($): [press Enter]

🤖 Using AI to Generate Missing Information
Analyzing provided information and generating realistic values...
✓ AI-generated information:
  - Current EBITDA: $7,000,000

📊 Getting AI-Generated LBO Parameters
✓ AI recommendations received:
  - Entry EBITDA: $7,000,000
  - Entry Multiple: 6.0x
  - Revenue Growth (Year 1): 15.0%
  - Debt Instruments: 2

📋 Model Configuration Summary
Company: TechWave Solutions
Industry: SaaS Software
Entry EBITDA: $7,000,000
Entry Multiple: 6.0x
Revenue Growth: 15.0% (Year 1)
Debt Instruments: 2

Generate LBO model with this configuration? (y/n) [y]: y

🔄 Generating LBO Model
✓ Model generated successfully!

Key Results:
  Exit Year: 5
  Exit EBITDA: $22,423,000
  Exit Enterprise Value: $156,961,000
  Exit Equity Value: $204,929,000
  Equity Invested: $18,500,000
  MOIC: 11.08x
  IRR: 61.77%

Export to Excel? (y/n) [y]: y
Output filename [output/interactive_test.xlsx]: output/techwave_lbo.xlsx

✓ Excel file created: output/techwave_lbo.xlsx
```

## Tips

1. **Start Simple**: Try with minimal input first to see how AI generates values
2. **Provide Industry**: Giving the industry helps AI generate more accurate assumptions
3. **Revenue vs EBITDA**: If you know revenue but not EBITDA, AI will estimate margins
4. **Review AI Output**: Always review AI-generated values before generating the model
5. **Use Validation**: Run AI validation to get feedback on your model assumptions

## Without API Key

If you don't have an OpenAI API key:
- The tool will still work
- It will use default values instead of AI-generated ones
- You'll need to provide more information manually
- AI validation will not be available

## Troubleshooting

**Error: "OPENAI_API_KEY not set"**
- Set the environment variable: `export OPENAI_API_KEY='your-key'`
- Or the tool will use defaults (less optimal)

**Error: "Invalid input"**
- Make sure numbers are entered without commas or currency symbols
- Example: `35000000` not `$35,000,000`

**Error: "Model generation failed"**
- Check that required fields have values
- Review the configuration summary before generating
- Try with different values

## Advanced Usage

### Save Configuration
After generation, you can save the configuration:
```python
# Configuration is available in final_config variable
# Save it for future use
```

### Batch Testing
You can modify the script to test multiple companies:
```python
companies = [
    {"company_name": "Company A", "industry": "SaaS"},
    {"company_name": "Company B", "industry": "Manufacturing"},
]
```

## Next Steps

After running the interactive test:
1. Review the Excel output
2. Check AI validation results (if run)
3. Adjust assumptions if needed
4. Re-run with different inputs
5. Compare results across different scenarios

