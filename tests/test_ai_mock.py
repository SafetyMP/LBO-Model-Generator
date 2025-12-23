"""
Mock test for AI recommendations (works without API key)
Demonstrates the expected structure and flow
"""

import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lbo_model_generator import create_lbo_from_inputs

print("=" * 80)
print("AI RECOMMENDATIONS TEST (MOCK)")
print("=" * 80)
print("\nThis demonstrates what AI recommendations would look like.")
print("To test with real AI, set OPENAI_API_KEY environment variable.\n")

# Simulated AI recommendations for a SaaS company
mock_ai_recommendations = {
    "entry_ebitda": 5250000,  # 35% of $15M revenue
    "entry_multiple": 8.5,  # High multiple for SaaS
    "revenue_growth_rate": [0.10, 0.09, 0.08, 0.07, 0.06],  # Declining growth
    "cogs_pct_of_revenue": 0.25,  # Low COGS for SaaS
    "sganda_pct_of_revenue": 0.40,  # High SG&A for growth
    "capex_pct_of_revenue": 0.02,  # Low CapEx for SaaS
    "tax_rate": 0.25,
    "days_sales_outstanding": 30.0,  # Low DSO for SaaS
    "days_inventory_outstanding": 0.0,  # No inventory
    "days_payable_outstanding": 15.0,  # Low DPO
    "exit_multiple": 10.0,  # Higher exit multiple
    "debt_instruments": [
        {
            "name": "Senior Debt",
            "ebitda_multiple": 1.5,
            "interest_rate": 0.075,
            "amortization_schedule": "amortizing",
            "amortization_periods": 5,
        },
        {
            "name": "Subordinated Debt",
            "ebitda_multiple": 2.0,
            "interest_rate": 0.12,
            "amortization_schedule": "bullet",
        },
    ],
    "exit_year": 5,
    "starting_revenue": 15000000,
}

print("MOCK AI RECOMMENDATIONS FOR SAAS COMPANY")
print("-" * 80)
print(
    f"""
Business: SaaS company with $15M ARR, 35% EBITDA margins

Recommended Parameters:
- Entry EBITDA: ${mock_ai_recommendations['entry_ebitda']:,.0f}
- Entry Multiple: {mock_ai_recommendations['entry_multiple']:.1f}x
- Exit Multiple: {mock_ai_recommendations['exit_multiple']:.1f}x
- Revenue Growth: {[f'{g*100:.1f}%' for g in mock_ai_recommendations['revenue_growth_rate']]}

Operating Metrics:
- COGS: {mock_ai_recommendations['cogs_pct_of_revenue']*100:.1f}% of revenue
- SG&A: {mock_ai_recommendations['sganda_pct_of_revenue']*100:.1f}% of revenue
- CapEx: {mock_ai_recommendations['capex_pct_of_revenue']*100:.1f}% of revenue

Working Capital:
- DSO: {mock_ai_recommendations['days_sales_outstanding']:.0f} days
- DIO: {mock_ai_recommendations['days_inventory_outstanding']:.0f} days (no inventory)
- DPO: {mock_ai_recommendations['days_payable_outstanding']:.0f} days

Debt Structure:
- Senior Debt: {mock_ai_recommendations['debt_instruments'][0]['ebitda_multiple']:.1f}x EBITDA,
  {mock_ai_recommendations['debt_instruments'][0]['interest_rate']*100:.1f}% interest, amortizing
- Subordinated Debt: {mock_ai_recommendations['debt_instruments'][1]['ebitda_multiple']:.1f}x EBITDA,
  {mock_ai_recommendations['debt_instruments'][1]['interest_rate']*100:.1f}% interest, bullet

Reasoning: SaaS companies typically command higher multiples due to recurring revenue,
scalability, and asset-light model. Conservative debt structure appropriate for growth
stage company.
"""
)

print("\n" + "=" * 80)
print("GENERATING LBO MODEL FROM MOCK AI RECOMMENDATIONS")
print("=" * 80)

try:
    model = create_lbo_from_inputs(mock_ai_recommendations)
    returns = model.calculate_returns()

    print("\n✓ Model generated successfully!")
    print("\nReturns Analysis:")
    print(f"  Exit Year:              {returns['exit_year']}")
    print(f"  Exit EBITDA:            ${returns['exit_ebitda']:,.0f}")
    print(f"  Exit Enterprise Value:  ${returns['exit_ev']:,.0f}")
    print(f"  Exit Equity Value:      ${returns['exit_equity_value']:,.0f}")
    print(f"  Equity Invested:        ${returns['equity_invested']:,.0f}")
    print(f"  MOIC:                   {returns['moic']:.2f}x")
    print(f"  IRR:                    {returns['irr']:.2f}%")

    # Export to Excel
    output_file = "test_ai_mock_recommendations.xlsx"
    model.export_to_excel(output_file)
    print(f"\n✓ Excel file created: {output_file}")

    # Show some key metrics
    print("\n" + "=" * 80)
    print("KEY METRICS FROM MODEL")
    print("=" * 80)
    print("\nYear 1:")
    print(f"  Revenue: ${model.income_statement.loc['Revenue', 1]:,.0f}")
    print(f"  EBITDA: ${model.income_statement.loc['EBITDA', 1]:,.0f}")
    print(
        f"  EBITDA Margin: {model.income_statement.loc['EBITDA', 1] / model.income_statement.loc['Revenue', 1] * 100:.1f}%"
    )

    print("\nYear 5:")
    print(f"  Revenue: ${model.income_statement.loc['Revenue', 5]:,.0f}")
    print(f"  EBITDA: ${model.income_statement.loc['EBITDA', 5]:,.0f}")
    print(
        f"  EBITDA Margin: {model.income_statement.loc['EBITDA', 5] / model.income_statement.loc['Revenue', 5] * 100:.1f}%"
    )
    print(
        f"  Revenue CAGR: {((model.income_statement.loc['Revenue', 5] / model.income_statement.loc['Revenue', 1]) ** (1/4) - 1) * 100:.1f}%"
    )

    print("\n" + "=" * 80)
    print("✓ MOCK AI TEST COMPLETE")
    print("=" * 80)
    print("\nTo test with real AI recommendations:")
    print("  1. Get API key from: https://platform.openai.com/api-keys")
    print("  2. Set: export OPENAI_API_KEY='your-api-key-here'")
    print("  3. Run: python3 test_lbo_generator.py")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback

    traceback.print_exc()
