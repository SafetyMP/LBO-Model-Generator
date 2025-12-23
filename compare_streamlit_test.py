"""
Compare Streamlit LBO calculation output with test case configurations.
"""

import json
import sys
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.lbo_engine import calculate_lbo

def load_test_case(filename):
    """Load test case configuration."""
    with open(filename, 'r') as f:
        return json.load(f)

def extract_streamlit_inputs(test_config):
    """Extract inputs that Streamlit would use from test config."""
    # Streamlit uses simplified inputs
    entry_multiple = float(test_config.get("entry_multiple", 10.0))

    # Calculate leverage ratio from debt instruments
    debt_instruments = test_config.get("debt_instruments", [])
    if debt_instruments:
        total_leverage = sum(d.get("ebitda_multiple", 0) for d in debt_instruments)
    else:
        total_leverage = 4.0

    # Revenue growth (use first year or average)
    rev_growth_list = test_config.get("revenue_growth_rate", [0.05])
    rev_growth = float(rev_growth_list[0]) if isinstance(rev_growth_list, list) else float(rev_growth_list)

    # EBITDA margin - need to calculate from revenue and EBITDA
    entry_ebitda = float(test_config.get("entry_ebitda", 10000))
    starting_revenue = float(test_config.get("starting_revenue", entry_ebitda * 5))
    ebitda_margin = entry_ebitda / starting_revenue if starting_revenue > 0 else 0.20

    # Other inputs
    entry_ebitda_val = entry_ebitda
    exit_multiple = float(test_config.get("exit_multiple", entry_multiple))
    num_years = int(test_config.get("exit_year", 5))

    # Interest rate - average from debt instruments
    if debt_instruments:
        total_debt = sum(d.get("ebitda_multiple", 0) * entry_ebitda for d in debt_instruments)
        weighted_rate = sum(
            (d.get("ebitda_multiple", 0) * entry_ebitda / total_debt * d.get("interest_rate", 0.08))
            for d in debt_instruments
        ) if total_debt > 0 else 0.08
        interest_rate = weighted_rate
    else:
        interest_rate = 0.08

    tax_rate = float(test_config.get("tax_rate", 0.25))

    # Working capital
    dso = float(test_config.get("days_sales_outstanding", 45.0))
    dio = float(test_config.get("days_inventory_outstanding", 30.0))
    dpo = float(test_config.get("days_payable_outstanding", 30.0))

    # Transaction fees
    transaction_expenses_pct = float(test_config.get("transaction_expenses_pct", 0.03))
    financing_fees_pct = float(test_config.get("financing_fees_pct", 0.02))

    # Debt instruments (for Streamlit's multiple debt support)
    # Need to convert ebitda_multiple to amount
    streamlit_debt_instruments = []
    for debt in debt_instruments:
        ebitda_multiple = debt.get("ebitda_multiple", 0)
        debt_amount = ebitda_multiple * entry_ebitda
        streamlit_debt_instruments.append({
            "name": debt.get("name", "Debt"),
            "amount": debt_amount,
            "interest_rate": debt.get("interest_rate", 0.08),
            "amortization_schedule": debt.get("amortization_schedule", "cash_flow_sweep"),
            "amortization_periods": debt.get("amortization_periods", num_years),
            "priority": debt.get("priority", 1)
        })

    return {
        "entry_multiple": entry_multiple,
        "leverage_ratio": total_leverage,
        "rev_growth": rev_growth,
        "ebitda_margin": ebitda_margin,
        "entry_ebitda": entry_ebitda_val,
        "exit_multiple": exit_multiple,
        "num_years": num_years,
        "interest_rate": interest_rate,
        "tax_rate": tax_rate,
        "dso": dso,
        "dio": dio,
        "dpo": dpo,
        "transaction_expenses_pct": transaction_expenses_pct,
        "financing_fees_pct": financing_fees_pct,
        "debt_instruments": streamlit_debt_instruments if streamlit_debt_instruments else None,
        "starting_revenue": starting_revenue
    }

def run_comparison(test_case_name, test_config_file):
    """Run comparison for a test case."""
    print(f"\n{'='*80}")
    print(f"COMPARISON: {test_case_name}")
    print(f"{'='*80}\n")

    # Load test case
    test_config = load_test_case(test_config_file)
    company_name = test_config.get("company_name", test_case_name)

    print(f"Company: {company_name}")
    print(f"Test Config File: {test_config_file}\n")

    # Extract Streamlit inputs
    inputs = extract_streamlit_inputs(test_config)

    print("Streamlit Input Parameters:")
    print(f"  Entry Multiple: {inputs['entry_multiple']:.2f}x")
    print(f"  Leverage Ratio: {inputs['leverage_ratio']:.2f}x")
    print(f"  Revenue Growth: {inputs['rev_growth']:.1%}")
    print(f"  EBITDA Margin: {inputs['ebitda_margin']:.1%}")
    print(f"  Entry EBITDA: ${inputs['entry_ebitda']:,.0f}")
    print(f"  Exit Multiple: {inputs['exit_multiple']:.2f}x")
    print(f"  Number of Years: {inputs['num_years']}")
    print(f"  Interest Rate: {inputs['interest_rate']:.2%}")
    print(f"  Tax Rate: {inputs['tax_rate']:.1%}")
    if inputs['debt_instruments']:
        print(f"  Debt Instruments: {len(inputs['debt_instruments'])} tranches")
        for i, debt in enumerate(inputs['debt_instruments'], 1):
            debt_amount = debt.get('amount', 0)
            leverage_ratio = debt_amount / inputs['entry_ebitda'] if inputs['entry_ebitda'] > 0 else 0
            print(f"    {i}. {debt['name']}: ${debt_amount:,.0f} ({leverage_ratio:.2f}x) @ {debt['interest_rate']:.2%}")
    print()

    # Run Streamlit calculation
    print("Running Streamlit LBO calculation...")
    try:
        results = calculate_lbo(
            entry_multiple=inputs['entry_multiple'],
            leverage_ratio=inputs['leverage_ratio'],
            rev_growth=inputs['rev_growth'],
            ebitda_margin=inputs['ebitda_margin'],
            entry_ebitda=inputs['entry_ebitda'],
            exit_multiple=inputs['exit_multiple'],
            num_years=inputs['num_years'],
            interest_rate=inputs['interest_rate'],
            tax_rate=inputs['tax_rate'],
            dso=inputs['dso'],
            dio=inputs['dio'],
            dpo=inputs['dpo'],
            transaction_expenses_pct=inputs['transaction_expenses_pct'],
            financing_fees_pct=inputs['financing_fees_pct'],
            debt_instruments=inputs['debt_instruments'] if inputs['debt_instruments'] else None,
            starting_revenue=inputs['starting_revenue']
        )

        print("✅ Calculation successful!\n")

        # Display key results
        print("Key Results:")
        print(f"  Equity IRR: {results['irr']:.2%}")
        print(f"  MOIC: {results['moic']:.2f}x")
        print(f"  Total Debt Paydown: ${results['debt_paid']:,.0f}")
        print(f"  Exit EBITDA: ${results.get('exit_ebitda', 0):,.0f}")
        print(f"  Exit EV: ${results.get('exit_ev', 0):,.0f}")
        print(f"  Exit Equity Value: ${results.get('exit_equity_value', 0):,.0f}")
        print(f"  Equity Invested: ${results.get('equity_invested', 0):,.0f}")

        # Financial statements summary
        if 'income_statement' in results:
            is_df = results['income_statement']
            print(f"\nIncome Statement Summary:")
            if isinstance(is_df, pd.DataFrame) and len(is_df) > 0:
                print(f"  Year 1 Revenue: ${is_df.loc['Revenue', 1]:,.0f}" if 'Revenue' in is_df.index and 1 in is_df.columns else "  N/A")
                print(f"  Year 1 EBITDA: ${is_df.loc['EBITDA', 1]:,.0f}" if 'EBITDA' in is_df.index and 1 in is_df.columns else "  N/A")
                print(f"  Year {inputs['num_years']} Revenue: ${is_df.loc['Revenue', inputs['num_years']]:,.0f}" if 'Revenue' in is_df.index and inputs['num_years'] in is_df.columns else "  N/A")
                print(f"  Year {inputs['num_years']} EBITDA: ${is_df.loc['EBITDA', inputs['num_years']]:,.0f}" if 'EBITDA' in is_df.index and inputs['num_years'] in is_df.columns else "  N/A")

        # Debt schedule summary
        if 'debt_balance_over_time' in results:
            debt_df = results['debt_balance_over_time']
            if isinstance(debt_df, pd.DataFrame) and len(debt_df) > 0:
                print(f"\nDebt Schedule Summary:")
                initial_debt = debt_df.iloc[0, 0] if len(debt_df.columns) > 0 else 0
                final_debt = debt_df.iloc[-1, -1] if len(debt_df.columns) > 0 else 0
                print(f"  Initial Debt: ${initial_debt:,.0f}")
                print(f"  Final Debt: ${final_debt:,.0f}")
                print(f"  Debt Paydown: ${initial_debt - final_debt:,.0f}")

        return results

    except Exception as e:
        print(f"❌ Error calculating LBO: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Run comparisons for all test cases."""
    test_cases = {
        "AlphaCo": "AlphaCo_config.json",
        "DataCore": "DataCore_config.json",
        "SentinelGuard": "SentinelGuard_config.json",
        "VectorServe": "VectorServe_config.json",
    }

    print("="*80)
    print("STREAMLIT vs TEST CASE COMPARISON")
    print("="*80)
    print("\nThis script compares the Streamlit LBO calculation output")
    print("with the test case configurations to verify consistency.\n")

    all_results = {}

    for name, config_file in test_cases.items():
        if Path(config_file).exists():
            results = run_comparison(name, config_file)
            all_results[name] = results
        else:
            print(f"\n⚠️  Test case file not found: {config_file}")

    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}\n")

    for name, results in all_results.items():
        if results:
            print(f"{name}:")
            print(f"  IRR: {results['irr']:.2%}")
            print(f"  MOIC: {results['moic']:.2f}x")
            print()
        else:
            print(f"{name}: ❌ Calculation failed\n")

if __name__ == "__main__":
    main()
