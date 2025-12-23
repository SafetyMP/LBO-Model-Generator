# Industry Standards Implementation

## Overview

The LBO Model Generator has been updated to follow industry-standard Excel formatting and structure based on recommendations from OpenAI's analysis of top-tier investment banking practices (Goldman Sachs, Morgan Stanley, JPMorgan).

## Key Changes

### 1. New Industry-Standard Template System

**Files Created:**
- `src/lbo_industry_standards.py` - Defines formatting standards, colors, fonts, and layout constants
- `src/lbo_industry_excel.py` - Implements industry-standard Excel export

**Key Features:**
- **Color Coding:**
  - Input cells: Light red (#FFC7CE)
  - Calculation cells: Light green (#C6EFCE)
  - Output cells: Light yellow (#FFEB9C)
  - Headers: Blue (#4472C4)

- **Font Standards:**
  - Font: Calibri
  - Body: 11pt
  - Headers: 14pt (bold)
  - Sections: 12pt (bold)

- **Sheet Organization:**
  Following industry-standard order:
  1. Cover
  2. Summary
  3. Assumptions
  4. Income Statement
  5. Cash Flow
  6. Balance Sheet
  7. Debt Schedule
  8. Returns Analysis

### 2. Updated Export Method

The `export_to_excel()` method now supports:
- `use_industry_standards=True` (default) - Uses new industry-standard format
- `use_industry_standards=False` - Uses legacy format for backward compatibility

### 3. Column Structure

Following industry standards:
- **3 Historical Years** (Year -3, Year -2, Year -1)
- **1 Transaction Year** (Transaction adjustments)
- **5 Projected Years** (Year 1 through Year 5)

### 4. Formula Standards

- Formulas wrapped in `IFERROR()` for error handling
- Absolute references for key inputs
- Relative references for calculations
- Formula cells protected from accidental changes

## Usage

### Basic Usage (Industry Standards - Default)

```python
from lbo_model_generator import create_lbo_from_inputs

config = {
    'entry_ebitda': 10000,
    'entry_multiple': 6.5,
    'revenue_growth_rate': [0.05] * 5,
    'starting_revenue': 50000,
    'exit_year': 5,
    'exit_multiple': 7.5
}

model = create_lbo_from_inputs(config)
model.export_to_excel('output.xlsx', company_name='My Company')
# Uses industry standards by default
```

### Legacy Format (Backward Compatibility)

```python
model.export_to_excel(
    'output.xlsx', 
    company_name='My Company',
    use_industry_standards=False  # Use legacy format
)
```

## Sheet Descriptions

### 1. Cover Sheet
- Company name and date
- Navigation hyperlinks to all sheets
- Key metrics summary (Entry EBITDA, MOIC, IRR, etc.)

### 2. Summary Sheet
- Executive summary with investment highlights
- Transaction summary
- Key return metrics

### 3. Assumptions Sheet
- All model inputs organized by category:
  - Transaction Assumptions
  - Operating Assumptions
  - Working Capital
  - Exit Assumptions
- Input cells formatted in light red

### 4. Income Statement
- Complete income statement with:
  - Revenue
  - COGS
  - Gross Profit
  - SG&A
  - EBITDA
  - Depreciation & Amortization
  - EBIT
  - Interest Expense
  - Pretax Income
  - Income Tax
  - Net Income
- Calculation cells formatted in light green

### 5. Cash Flow Statement
- Operating activities
- Investing activities
- Financing activities
- Net change in cash
- Beginning and ending cash balances

### 6. Balance Sheet
- Assets section
- Liabilities & Equity section
- All items properly formatted

### 7. Debt Schedule
- Detailed schedule for each debt instrument:
  - Beginning balance
  - Interest paid
  - Principal paid
  - Ending balance
- Total debt summary

### 8. Returns Analysis
- Exit year and EBITDA
- Exit enterprise value
- Exit equity value
- Equity invested
- MOIC and IRR

## Formatting Standards

### Cell Types

1. **Input Cells** (Light Red)
   - All assumption values
   - User-editable parameters
   - Formatted with `format_input_cell()`

2. **Calculation Cells** (Light Green)
   - All formulas and calculated values
   - Protected from accidental changes
   - Formatted with `format_calculation_cell()`

3. **Output Cells** (Light Yellow)
   - Key metrics and results
   - Formatted with `format_output_cell()`

### Borders and Alignment

- Thin borders for all cells
- Thick borders for section headers
- Double underline for total rows
- Right-aligned numbers
- Center-aligned headers

## Benefits

1. **Professional Appearance**
   - Matches formatting used at top investment banks
   - Client-ready presentation quality

2. **Clear Structure**
   - Logical sheet organization
   - Easy navigation with hyperlinks
   - Consistent formatting throughout

3. **Error Prevention**
   - Formula protection
   - Error handling with IFERROR
   - Clear distinction between inputs and calculations

4. **Maintainability**
   - Centralized formatting standards
   - Easy to update and extend
   - Consistent with industry best practices

## Migration Guide

### For Existing Code

The default behavior now uses industry standards. If you need the legacy format:

```python
# Old code (still works)
model.export_to_excel('output.xlsx', company_name='Company')

# Explicitly use legacy format if needed
model.export_to_excel('output.xlsx', company_name='Company', use_industry_standards=False)
```

### Breaking Changes

None. The legacy format is still available for backward compatibility.

## Testing

Test the industry-standard export:

```bash
cd lbo_model_generator
python3 -c "
from lbo_model_generator import create_lbo_from_inputs
config = {
    'entry_ebitda': 10000,
    'entry_multiple': 6.5,
    'revenue_growth_rate': [0.05] * 5,
    'starting_revenue': 50000,
    'exit_year': 5,
    'exit_multiple': 7.5
}
model = create_lbo_from_inputs(config)
model.export_to_excel('output/test_industry_standards.xlsx', company_name='Test Company')
print('✓ Industry-standard Excel file created!')
"
```

## References

The implementation is based on OpenAI's analysis of industry standards from:
- Goldman Sachs
- Morgan Stanley
- JPMorgan
- Other top-tier investment banks

Recommendations saved in: `/tmp/industry_standards_recommendations.json`

