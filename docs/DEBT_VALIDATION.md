# Debt Schedule Validation and Payment Scenarios

## Overview

The LBO model now includes comprehensive debt schedule validation and payment scenario detection. This ensures the integrity of debt calculations and identifies different payment structures.

## Validation Features

### 1. Balance Equation Validation
- **Check**: Beginning Balance - Principal Paid = Ending Balance
- **Purpose**: Ensures debt schedule calculations are mathematically correct
- **Tolerance**: 0.01 (allows for rounding differences)

### 2. Principal Payment Validation
- **Check**: Principal paid does not exceed beginning balance
- **Purpose**: Prevents negative debt balances
- **Error Type**: Critical error

### 3. Ending Balance Validation
- **Check**: Ending balance is non-negative
- **Purpose**: Ensures debt cannot go negative
- **Error Type**: Critical error

### 4. Interest Calculation Validation
- **Check**: Interest = Beginning Balance × Interest Rate
- **Purpose**: Verifies interest is calculated correctly
- **Tolerance**: 0.01

### 5. Balance Continuity Validation
- **Check**: Year N Ending Balance = Year N+1 Beginning Balance
- **Purpose**: Ensures debt schedule flows correctly across years
- **Error Type**: Critical error

### 6. Payment Schedule Compliance
- **Amortizing Debt**: Validates principal matches expected amortization schedule
- **Bullet Debt**: Validates no payment until final year (unless cash flow sweep)
- **Cash Flow Sweep**: Detects when sweep increases principal payments

### 7. Total Debt Reconciliation
- **Check**: Sum of individual debt instruments = Total Debt on Balance Sheet
- **Purpose**: Ensures consistency across financial statements
- **Tolerance**: 0.01

## Payment Scenarios

The validation system automatically identifies and tracks different payment scenarios:

### Amortizing Debt Scenario
- **Description**: Debt that pays down principal evenly over time
- **Validation**: Principal should equal `debt.amount / amortization_periods` each year
- **Detection**: Automatically identified when `amortization_schedule == "amortizing"`

### Bullet Debt Scenario
- **Description**: Debt that pays no principal until final year
- **Validation**: Principal should be 0 until final year, then full balance
- **Detection**: Automatically identified when `amortization_schedule == "bullet"`

### Cash Flow Sweep Scenario
- **Description**: Excess cash used to pay down debt beyond scheduled payments
- **Validation**: Principal may exceed scheduled payment when sweep is active
- **Detection**: Automatically identified when `min_cash_balance > 0` and principal exceeds scheduled amount

### Mixed Debt Structure Scenario
- **Description**: Model contains both amortizing and bullet debt instruments
- **Validation**: Each instrument follows its own payment schedule
- **Detection**: Automatically identified when multiple debt types are present

## Usage

### Get Validation Results

```python
from lbo_model_generator import create_lbo_from_inputs

# Create model
model = create_lbo_from_inputs(config)

# Get validation results
validation = model.get_debt_schedule_validation()

# Check for errors
if validation['errors']:
    print("Errors found:")
    for error in validation['errors']:
        print(f"  - {error}")

# Check for warnings
if validation['warnings']:
    print("Warnings:")
    for warning in validation['warnings']:
        print(f"  - {warning}")

# Check payment scenarios
for scenario_type, details in validation['scenarios'].items():
    if details:
        print(f"{scenario_type} scenario: {details}")
```

### Validation Results Structure

```python
{
    'errors': [
        "Debt Name Year X: Error description",
        ...
    ],
    'warnings': [
        "Debt Name Year X: Warning description",
        ...
    ],
    'scenarios': {
        'amortizing': ['Debt Name 1', 'Debt Name 2', ...],
        'bullet': ['Debt Name 1', ...],
        'cash_flow_sweep': [
            "Debt Name Year X: Sweep details",
            ...
        ],
        'mixed_structure': [
            "Description of mixed structure",
            ...
        ]
    }
}
```

## Integration

The validation is automatically called during model reconciliation:

```python
def _reconcile_model(self):
    # ... other reconciliation checks ...
    
    # Validate debt schedule
    debt_validation = self._validate_debt_schedule()
    if debt_validation['errors']:
        for error in debt_validation['errors']:
            logger.error(f"Debt schedule validation error: {error}")
    if debt_validation['warnings']:
        for warning in debt_validation['warnings']:
            logger.warning(f"Debt schedule validation warning: {warning}")
```

## Test Scenarios

Comprehensive test scenarios are available in `tests/test_debt_validation.py`:

1. **Amortizing Debt Scenario**: Tests validation for amortizing debt
2. **Bullet Debt Scenario**: Tests validation for bullet debt
3. **Mixed Debt Structure Scenario**: Tests validation for mixed structures
4. **Cash Flow Sweep Scenario**: Tests validation when sweep is active

## Example Output

```
Validation Results:
  Errors: 0
  Warnings: 1
  Scenarios: ['amortizing', 'cash_flow_sweep']

Payment Scenarios:
  - amortizing: 1 item(s)
  - cash_flow_sweep: 4 item(s)

✓ Validation system is working correctly
```

## Notes

- Validation runs automatically during model reconciliation
- Errors are logged at ERROR level
- Warnings are logged at WARNING level
- Scenarios are logged at DEBUG level
- Validation can be called manually via `model.get_debt_schedule_validation()`

## Future Enhancements

Potential improvements:
1. Add validation for interest rate changes over time
2. Add validation for debt refinancing scenarios
3. Add validation for covenant compliance
4. Add validation for debt capacity limits
5. Add graphical validation reports

