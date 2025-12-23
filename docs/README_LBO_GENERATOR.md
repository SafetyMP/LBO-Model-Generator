# LBO Model Generator

A comprehensive Python tool to generate Leveraged Buyout (LBO) financial models from user inputs.

## Features

- **Complete Financial Statements**: Generates Income Statement, Balance Sheet, and Cash Flow Statement
- **Debt Schedule**: Handles multiple debt instruments with different amortization schedules (bullet, amortizing, cash flow sweep)
- **Returns Analysis**: Calculates IRR and MOIC based on exit assumptions
- **Excel Export**: Produces formatted Excel files ready for analysis
- **Flexible Input**: Supports JSON configuration files or interactive command-line input

## Installation

```bash
pip install pandas numpy openpyxl
```

## Quick Start

### 1. Generate a Template

```bash
python lbo_input_generator.py --template
```

This creates `lbo_input_template.json` with default values you can edit.

### 2. Edit the Configuration

Edit `lbo_input_template.json` with your assumptions:

```json
{
  "entry_ebitda": 10000,
  "entry_multiple": 6.5,
  "revenue_growth_rate": [0.05, 0.05, 0.05, 0.05, 0.05],
  "debt_instruments": [
    {
      "name": "Senior Debt",
      "interest_rate": 0.08,
      "ebitda_multiple": 1.0,
      "amortization_schedule": "amortizing",
      "amortization_periods": 5
    }
  ],
  "exit_year": 5,
  "exit_multiple": 7.5
}
```

### 3. Generate the Model

```bash
python lbo_input_generator.py --input lbo_input_template.json --output my_lbo_model.xlsx
```

### Interactive Mode

```bash
python lbo_input_generator.py --interactive --output my_lbo_model.xlsx
```

## Configuration Parameters

### Transaction Details
- `entry_ebitda`: EBITDA at transaction close ($)
- `entry_multiple`: Enterprise value multiple (x EBITDA)
- `existing_debt`: Existing debt to be refinanced ($)
- `existing_cash`: Existing cash balance ($)
- `transaction_expenses_pct`: Transaction expenses as % of EV (default: 3%)
- `financing_fees_pct`: Financing fees as % of total debt (default: 2%)

### Debt Instruments
Each debt instrument can specify:
- `name`: Name of the debt instrument
- `interest_rate`: Annual interest rate (decimal, e.g., 0.08 for 8%)
- `ebitda_multiple`: Debt amount as multiple of EBITDA (or use `amount`)
- `amount`: Fixed debt amount ($) - use if not using EBITDA multiple
- `amortization_schedule`: "bullet", "amortizing", or "cash_flow_sweep"
- `amortization_periods`: Number of years for amortization (if applicable)

### Operating Assumptions
- `revenue_growth_rate`: List of annual growth rates (e.g., [0.05, 0.05, 0.05])
- `starting_revenue`: Starting revenue ($, 0 to estimate from EBITDA)
- `cogs_pct_of_revenue`: COGS as % of revenue (default: 70%)
- `sganda_pct_of_revenue`: SG&A as % of revenue (default: 15%)
- `capex_pct_of_revenue`: CapEx as % of revenue (default: 3%)
- `depreciation_pct_of_ppe`: Depreciation as % of PP&E (default: 10%)
- `tax_rate`: Corporate tax rate (default: 25%)

### Working Capital
- `days_sales_outstanding`: DSO (default: 45)
- `days_inventory_outstanding`: DIO (default: 30)
- `days_payable_outstanding`: DPO (default: 30)

### Exit Assumptions
- `exit_year`: Year of exit (default: 5)
- `exit_multiple`: Exit multiple (x EBITDA, default: 7.5)

### Optional
- `initial_ppe`: Starting PP&E balance ($)
- `initial_ar`: Starting accounts receivable ($)
- `initial_inventory`: Starting inventory ($)
- `initial_ap`: Starting accounts payable ($)
- `min_cash_balance`: Minimum cash balance requirement ($)
- `equity_amount`: Sponsor equity contribution ($, 0 to calculate)

## Output

The tool generates an Excel file with the following sheets:

1. **Sources & Uses**: Transaction financing structure
2. **Income Statement**: Multi-year P&L projections
3. **Balance Sheet**: Multi-year balance sheet projections
4. **Cash Flow**: Multi-year cash flow statement
5. **Debt Schedule**: Detailed debt repayment schedule
6. **Returns Analysis**: IRR and MOIC calculations

## Example Usage in Python

```python
from lbo_model_generator import create_lbo_from_inputs

config = {
    "entry_ebitda": 10000,
    "entry_multiple": 6.5,
    "revenue_growth_rate": [0.05, 0.05, 0.05, 0.05, 0.05],
    "debt_instruments": [
        {
            "name": "Senior Debt",
            "interest_rate": 0.08,
            "ebitda_multiple": 1.0,
            "amortization_schedule": "amortizing",
            "amortization_periods": 5
        },
        {
            "name": "Sub Debt",
            "interest_rate": 0.12,
            "ebitda_multiple": 2.0,
            "amortization_schedule": "bullet"
        }
    ],
    "exit_year": 5,
    "exit_multiple": 7.5
}

model = create_lbo_from_inputs(config)
model.export_to_excel("output.xlsx")

returns = model.calculate_returns()
print(f"MOIC: {returns['moic']:.2f}x")
print(f"IRR: {returns['irr']:.2f}%")
```

## Notes

- The model automatically balances the balance sheet each period
- Cash flow sweep functionality for senior debt can be enhanced
- IRR calculation uses simplified method (can be improved with more sophisticated algorithms)
- Working capital is calculated based on DSO/DIO/DPO assumptions
- Goodwill is calculated as purchase price minus net book value

## Limitations

- Cash flow sweep for debt repayment is simplified
- More sophisticated working capital modeling can be added
- Tax loss carryforwards not modeled
- Currency formatting in Excel can be enhanced

## License

Free to use and modify.

