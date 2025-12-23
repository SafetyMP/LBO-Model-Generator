"""
Simplified LBO Engine for Streamlit App

Provides a simplified interface for calculating LBO returns and debt schedules.
"""

import pandas as pd
from typing import Dict, List
from .lbo_model_generator import LBOModel, LBOAssumptions, LBODebtStructure


def calculate_lbo(
    entry_multiple: float,
    leverage_ratio: float,
    rev_growth: float,
    ebitda_margin: float,
    entry_ebitda: float = None,
    starting_revenue: float = None,
    num_years: int = 5,
    exit_multiple: float = None,
    interest_rate: float = 0.08,
    tax_rate: float = 0.25,
    amortization_schedule: str = "cash_flow_sweep",
    dso: float = 45.0,
    dio: float = 30.0,
    dpo: float = 30.0,
    transaction_expenses_pct: float = 0.03,
    financing_fees_pct: float = 0.02,
    debt_instruments: List[Dict] = None,
) -> Dict:
    """
    Calculate LBO returns and debt schedule from simplified inputs.

    Args:
        entry_multiple: Entry EBITDA multiple (e.g., 10.0)
        leverage_ratio: Debt/EBITDA ratio (e.g., 4.0)
        rev_growth: Annual revenue growth rate as decimal (e.g., 0.05 for 5%)
        ebitda_margin: EBITDA margin as decimal (e.g., 0.20 for 20%)
        entry_ebitda: Entry EBITDA (if None, calculated from starting_revenue and margin)
        starting_revenue: Starting revenue (if None, calculated from entry_ebitda and margin)
        num_years: Number of projection years (default: 5)
        exit_multiple: Exit EBITDA multiple (default: same as entry_multiple)
        interest_rate: Interest rate on debt (default: 8%)
        tax_rate: Tax rate as decimal (default: 25%)
        amortization_schedule: Debt amortization schedule - "bullet", "amortizing", or "cash_flow_sweep" (default: "cash_flow_sweep")
        dso: Days Sales Outstanding (default: 45.0)
        dio: Days Inventory Outstanding (default: 30.0)
        dpo: Days Payable Outstanding (default: 30.0)
        transaction_expenses_pct: Transaction expenses as % of EV (default: 3%)
        financing_fees_pct: Financing fees as % of total debt (default: 2%)

    Returns:
        Dictionary with:
            - irr: Equity IRR as decimal (e.g., 0.3846 for 38.46%)
            - moic: Multiple on Invested Capital (e.g., 2.5x)
            - debt_paid: Total debt paid down in millions
            - debt_balance_over_time: DataFrame with debt balance by year
    """
    # Calculate entry_ebitda and starting_revenue if not provided
    if entry_ebitda is None and starting_revenue is None:
        # Default to $10M EBITDA
        entry_ebitda = 10000.0
        starting_revenue = entry_ebitda / ebitda_margin if ebitda_margin > 0 else 50000.0
    elif entry_ebitda is None:
        entry_ebitda = starting_revenue * ebitda_margin
    elif starting_revenue is None:
        starting_revenue = entry_ebitda / ebitda_margin if ebitda_margin > 0 else entry_ebitda * 5

    # Set exit multiple (default to entry multiple)
    if exit_multiple is None:
        exit_multiple = entry_multiple

    # Calculate total debt from leverage ratio
    total_debt = entry_ebitda * leverage_ratio

    # Create debt instruments
    if debt_instruments is None:
        # Default: single debt instrument
        debt_instrument = LBODebtStructure(
            name="Senior Debt",
            amount=total_debt,
            interest_rate=interest_rate,
            amortization_schedule=amortization_schedule,
            amortization_periods=num_years,
            priority=1,
        )
        debt_instruments_list = [debt_instrument]
    else:
        # Convert dict list to LBODebtStructure objects
        debt_instruments_list = []
        for i, debt_dict in enumerate(debt_instruments):
            debt = LBODebtStructure(
                name=debt_dict.get("name", f"Debt {i+1}"),
                amount=debt_dict.get("amount", 0),
                interest_rate=debt_dict.get("interest_rate", interest_rate),
                amortization_schedule=debt_dict.get("amortization_schedule", amortization_schedule),
                amortization_periods=debt_dict.get("amortization_periods", num_years),
                priority=debt_dict.get("priority", i + 1),
            )
            debt_instruments_list.append(debt)

    # Create revenue growth rate list
    revenue_growth_rate = [rev_growth] * num_years

    # Calculate COGS and SG&A from EBITDA margin
    # EBITDA = Revenue - COGS - SG&A - Depreciation
    # For simplicity, assume COGS = 70% of revenue, SG&A = 15% of revenue
    # This gives us ~15% EBITDA margin (adjustable via ebitda_margin parameter)
    # We'll use a more flexible approach: adjust COGS to achieve target margin
    cogs_pct = 0.70  # Base assumption
    sganda_pct = 0.15  # Base assumption

    # Adjust COGS to achieve target EBITDA margin
    # EBITDA margin = 1 - COGS% - SG&A% - Depreciation%
    # For simplicity, we'll keep SG&A fixed and adjust COGS
    target_total_costs = 1.0 - ebitda_margin
    # Reserve ~3% for depreciation and other items
    cogs_pct = max(0.50, min(0.85, target_total_costs - sganda_pct - 0.03))

    # Create assumptions
    assumptions = LBOAssumptions(
        entry_ebitda=entry_ebitda,
        entry_multiple=entry_multiple,
        existing_debt=0.0,
        existing_cash=0.0,
        transaction_expenses_pct=transaction_expenses_pct,
        financing_fees_pct=financing_fees_pct,
        debt_instruments=debt_instruments_list,
        revenue_growth_rate=revenue_growth_rate,
        starting_revenue=starting_revenue,
        cogs_pct_of_revenue=cogs_pct,
        sganda_pct_of_revenue=sganda_pct,
        tax_rate=tax_rate,
        days_sales_outstanding=dso,
        days_inventory_outstanding=dio,
        days_payable_outstanding=dpo,
        exit_year=num_years,
        exit_multiple=exit_multiple,
    )

    # Build model
    model = LBOModel(assumptions)

    # Calculate returns
    returns = model.calculate_returns()

    # Extract debt balance over time (by instrument and total)
    initial_debt = total_debt
    debt_balance_over_time = [initial_debt]  # Start with initial debt (Year 0 / Entry)

    # Get debt balance by instrument from debt schedule
    debt_by_instrument = {}
    if model.debt_schedule:
        for debt_name in model.debt_schedule.keys():
            debt_by_instrument[debt_name] = []
            # Add initial balance
            if (
                "ending_balance" in model.debt_schedule[debt_name]
                and len(model.debt_schedule[debt_name]["ending_balance"]) > 0
            ):
                # Initial balance is the first ending balance (or we can calculate from amount)
                initial_bal = model.debt_schedule[debt_name].get("amount", 0)
                if initial_bal == 0 and len(model.debt_schedule[debt_name]["ending_balance"]) > 0:
                    # Try to infer from first year's starting balance
                    initial_bal = model.debt_schedule[debt_name]["ending_balance"][0] + (
                        model.debt_schedule[debt_name].get("principal_payment", [0])[0]
                        if "principal_payment" in model.debt_schedule[debt_name]
                        else 0
                    )
                debt_by_instrument[debt_name].append(initial_bal)

                # Add balances for each year
                for year_idx, year in enumerate(model.years):
                    if year_idx < len(model.debt_schedule[debt_name]["ending_balance"]):
                        debt_balance = model.debt_schedule[debt_name]["ending_balance"][year_idx]
                        debt_by_instrument[debt_name].append(debt_balance)
                    else:
                        debt_by_instrument[debt_name].append(0.0)

    # Get total debt balance from balance sheet (more reliable)
    if "Total Debt" in model.balance_sheet.index:
        debt_balance_over_time = [initial_debt]
        for year in model.years:
            debt_balance = model.balance_sheet.loc["Total Debt", year]
            debt_balance_over_time.append(debt_balance)
    else:
        # Fallback: sum by instrument
        if debt_by_instrument:
            debt_balance_over_time = [initial_debt]
            for year_idx in range(len(model.years)):
                total = sum(
                    inst_balances[year_idx + 1] if year_idx + 1 < len(inst_balances) else 0
                    for inst_balances in debt_by_instrument.values()
                )
                debt_balance_over_time.append(total)
        else:
            # Last resort: use single instrument logic
            for year in model.years:
                if model.debt_schedule and "Senior Debt" in model.debt_schedule:
                    year_idx = year - 1
                    if year_idx < len(model.debt_schedule["Senior Debt"]["ending_balance"]):
                        debt_balance = model.debt_schedule["Senior Debt"]["ending_balance"][
                            year_idx
                        ]
                    else:
                        debt_balance = 0.0
                else:
                    debt_balance = 0.0
                debt_balance_over_time.append(debt_balance)

    # Calculate total debt paid (from entry to exit)
    final_debt = debt_balance_over_time[-1] if debt_balance_over_time else 0.0
    debt_paid = initial_debt - final_debt

    # Create DataFrame for debt balance over time
    # Include "Entry" as Year 0, then Years 1-N
    year_labels = ["Entry"] + [f"Year {i+1}" for i in range(len(debt_balance_over_time) - 1)]

    # Create debt DataFrame with total and by instrument
    debt_data = {"Total Debt": debt_balance_over_time}
    for debt_name, balances in debt_by_instrument.items():
        if len(balances) == len(debt_balance_over_time):
            debt_data[debt_name] = balances

    debt_df = pd.DataFrame(debt_data, index=year_labels)

    # Extract additional metrics from returns
    exit_ebitda = returns.get("exit_ebitda", 0)
    exit_ev = returns.get("exit_ev", 0)
    exit_debt = returns.get("exit_debt", 0)
    exit_cash = returns.get("exit_cash", 0)
    exit_equity_value = returns.get("exit_equity_value", 0)
    equity_invested = returns.get("equity_invested", 0)

    # Calculate entry metrics
    entry_ev = entry_ebitda * entry_multiple

    # Extract financial statement data for visualizations
    financial_data = {}
    if "Revenue" in model.income_statement.index:
        financial_data["revenue"] = [
            model.income_statement.loc["Revenue", year] for year in model.years
        ]
    if "EBITDA" in model.income_statement.index:
        financial_data["ebitda"] = [
            model.income_statement.loc["EBITDA", year] for year in model.years
        ]
    if "Net Income" in model.income_statement.index:
        financial_data["net_income"] = [
            model.income_statement.loc["Net Income", year] for year in model.years
        ]

    # Extract cash flow data
    if "Cash Flow from Operations" in model.cash_flow.index:
        financial_data["cfo"] = [
            model.cash_flow.loc["Cash Flow from Operations", year] for year in model.years
        ]
    if "Capital Expenditures" in model.cash_flow.index:
        financial_data["capex"] = [
            abs(model.cash_flow.loc["Capital Expenditures", year]) for year in model.years
        ]
        # Calculate FCF = CFO - CapEx
        if "cfo" in financial_data:
            financial_data["fcf"] = [
                cfo - capex for cfo, capex in zip(financial_data["cfo"], financial_data["capex"])
            ]

    # Extract working capital data
    if "Net Change in Working Capital" in model.cash_flow.index:
        financial_data["wc_change"] = [
            model.cash_flow.loc["Net Change in Working Capital", year] for year in model.years
        ]
    if "Change in Accounts Receivable" in model.cash_flow.index:
        financial_data["ar_change"] = [
            model.cash_flow.loc["Change in Accounts Receivable", year] for year in model.years
        ]
    if "Change in Inventory" in model.cash_flow.index:
        financial_data["inv_change"] = [
            model.cash_flow.loc["Change in Inventory", year] for year in model.years
        ]
    if "Change in Accounts Payable" in model.cash_flow.index:
        financial_data["ap_change"] = [
            model.cash_flow.loc["Change in Accounts Payable", year] for year in model.years
        ]

    # Extract balance sheet data for coverage ratios
    coverage_ratios = {}
    if (
        "EBITDA" in model.income_statement.index
        and "Interest Expense" in model.income_statement.index
    ):
        for year in model.years:
            ebitda = model.income_statement.loc["EBITDA", year]
            interest = model.income_statement.loc["Interest Expense", year]
            if interest > 0:
                coverage_ratios[f"interest_coverage_{year}"] = ebitda / interest
            else:
                coverage_ratios[f"interest_coverage_{year}"] = None

    # Extract debt service coverage (EBITDA / (Interest + Principal))
    if "Total Debt" in model.balance_sheet.index:
        for year_idx, year in enumerate(model.years):
            if year_idx > 0:
                prev_year = model.years[year_idx - 1]
                debt_repayment = (
                    model.balance_sheet.loc["Total Debt", prev_year]
                    - model.balance_sheet.loc["Total Debt", year]
                )
                interest = (
                    model.income_statement.loc["Interest Expense", year]
                    if "Interest Expense" in model.income_statement.index
                    else 0
                )
                ebitda = model.income_statement.loc["EBITDA", year]
                debt_service = interest + debt_repayment
                if debt_service > 0:
                    coverage_ratios[f"debt_service_coverage_{year}"] = ebitda / debt_service
                else:
                    coverage_ratios[f"debt_service_coverage_{year}"] = None

    # Create financial statements DataFrame
    financial_df = pd.DataFrame(
        {
            "Year": [f"Year {i+1}" for i in range(len(model.years))],
        },
        index=[f"Year {i+1}" for i in range(len(model.years))],
    )

    for key, values in financial_data.items():
        if len(values) == len(model.years):
            financial_df[key.title().replace("_", " ")] = values

    financial_df = financial_df.set_index("Year")

    # Create coverage ratios DataFrame
    coverage_df = pd.DataFrame(
        {
            "Year": [f"Year {i+1}" for i in range(len(model.years))],
        },
        index=[f"Year {i+1}" for i in range(len(model.years))],
    )

    interest_coverage = [
        coverage_ratios.get(f"interest_coverage_{year}", None) for year in model.years
    ]
    debt_service_coverage = [
        coverage_ratios.get(f"debt_service_coverage_{year}", None) for year in model.years
    ]

    if any(x is not None for x in interest_coverage):
        coverage_df["Interest Coverage"] = interest_coverage
    if any(x is not None for x in debt_service_coverage):
        coverage_df["Debt Service Coverage"] = debt_service_coverage

    coverage_df = coverage_df.set_index("Year")

    return {
        "irr": returns["irr"],
        "moic": returns["moic"],
        "debt_paid": debt_paid / 1_000_000,  # Convert to millions
        "debt_balance_over_time": debt_df,
        "debt_by_instrument": debt_by_instrument,
        # Exit metrics
        "exit_ebitda": exit_ebitda,
        "exit_ev": exit_ev,
        "exit_debt": exit_debt,
        "exit_cash": exit_cash,
        "exit_equity_value": exit_equity_value,
        "equity_invested": equity_invested,
        # Entry metrics
        "entry_ev": entry_ev,
        "entry_ebitda": entry_ebitda,
        # Financial statements
        "financial_statements": financial_df,
        # Coverage ratios
        "coverage_ratios": coverage_df,
        # Model reference for export
        "model": model,
    }
