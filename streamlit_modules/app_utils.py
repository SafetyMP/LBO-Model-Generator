"""
Utility functions for Streamlit app.
"""

import json
import streamlit as st
from typing import Dict, List, Optional
from src.lbo_engine import calculate_lbo


@st.cache_data
def load_test_case(config_path: str) -> Optional[Dict]:
    """Load test case configuration."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def calculate_sensitivity_analysis(
    base_results: Dict,
    variable: str,
    base_entry_multiple: float,
    base_exit_multiple: float,
    base_rev_growth: float,
    base_ebitda_margin: float,
    base_leverage_ratio: float,
    base_entry_ebitda: float,
    base_interest_rate: float,
    base_tax_rate: float,
    range_pct: int,
    steps: int,
    dso: float,
    dio: float,
    dpo: float,
    transaction_expenses_pct: float,
    financing_fees_pct: float,
) -> List[Dict]:
    """Calculate sensitivity analysis for a given variable."""
    results_list = []

    # Calculate variation range
    variation_range = range_pct / 100.0
    step_size = (2 * variation_range) / (steps - 1)

    # Generate values to test
    if variable == "Exit Multiple":
        base_value = base_exit_multiple
        values = [base_value * (1 - variation_range + i * step_size) for i in range(steps)]
        for val in values:
            try:
                result = calculate_lbo(
                    entry_multiple=base_entry_multiple,
                    leverage_ratio=base_leverage_ratio,
                    rev_growth=base_rev_growth,
                    ebitda_margin=base_ebitda_margin,
                    entry_ebitda=base_entry_ebitda,
                    exit_multiple=val,
                    interest_rate=base_interest_rate,
                    tax_rate=base_tax_rate,
                    dso=dso,
                    dio=dio,
                    dpo=dpo,
                    transaction_expenses_pct=transaction_expenses_pct,
                    financing_fees_pct=financing_fees_pct,
                )
                results_list.append({
                    "Exit Multiple": f"{val:.2f}x",
                    "IRR": result['irr'],
                    "MOIC": result['moic'],
                })
            except (KeyError, ValueError, TypeError):
                continue
            except Exception as e:
                st.warning(f"Skipping calculation for exit multiple {val:.2f}x: {str(e)}")
                continue

    elif variable == "Entry Multiple":
        base_value = base_entry_multiple
        values = [base_value * (1 - variation_range + i * step_size) for i in range(steps)]
        for val in values:
            try:
                result = calculate_lbo(
                    entry_multiple=val,
                    leverage_ratio=base_leverage_ratio,
                    rev_growth=base_rev_growth,
                    ebitda_margin=base_ebitda_margin,
                    entry_ebitda=base_entry_ebitda,
                    exit_multiple=base_exit_multiple,
                    interest_rate=base_interest_rate,
                    tax_rate=base_tax_rate,
                    dso=dso,
                    dio=dio,
                    dpo=dpo,
                    transaction_expenses_pct=transaction_expenses_pct,
                    financing_fees_pct=financing_fees_pct,
                )
                results_list.append({
                    "Entry Multiple": f"{val:.2f}x",
                    "IRR": result['irr'],
                    "MOIC": result['moic'],
                })
            except (KeyError, ValueError, TypeError):
                continue
            except Exception as e:
                st.warning(f"Skipping calculation for entry multiple {val:.2f}x: {str(e)}")
                continue

    elif variable == "Revenue Growth":
        base_value = base_rev_growth
        values = [max(0, base_value * (1 - variation_range + i * step_size)) for i in range(steps)]
        for val in values:
            try:
                result = calculate_lbo(
                    entry_multiple=base_entry_multiple,
                    leverage_ratio=base_leverage_ratio,
                    rev_growth=val,
                    ebitda_margin=base_ebitda_margin,
                    entry_ebitda=base_entry_ebitda,
                    exit_multiple=base_exit_multiple,
                    interest_rate=base_interest_rate,
                    tax_rate=base_tax_rate,
                    dso=dso,
                    dio=dio,
                    dpo=dpo,
                    transaction_expenses_pct=transaction_expenses_pct,
                    financing_fees_pct=financing_fees_pct,
                )
                results_list.append({
                    "Revenue Growth": f"{val*100:.1f}%",
                    "IRR": result['irr'],
                    "MOIC": result['moic'],
                })
            except (KeyError, ValueError, TypeError):
                continue
            except Exception as e:
                st.warning(f"Skipping calculation for revenue growth {val*100:.1f}%: {str(e)}")
                continue

    elif variable == "EBITDA Margin":
        base_value = base_ebitda_margin
        values = [max(0.01, min(0.99, base_value * (1 - variation_range + i * step_size))) for i in range(steps)]
        for val in values:
            try:
                result = calculate_lbo(
                    entry_multiple=base_entry_multiple,
                    leverage_ratio=base_leverage_ratio,
                    rev_growth=base_rev_growth,
                    ebitda_margin=val,
                    entry_ebitda=base_entry_ebitda,
                    exit_multiple=base_exit_multiple,
                    interest_rate=base_interest_rate,
                    tax_rate=base_tax_rate,
                    dso=dso,
                    dio=dio,
                    dpo=dpo,
                    transaction_expenses_pct=transaction_expenses_pct,
                    financing_fees_pct=financing_fees_pct,
                )
                results_list.append({
                    "EBITDA Margin": f"{val*100:.1f}%",
                    "IRR": result['irr'],
                    "MOIC": result['moic'],
                })
            except (KeyError, ValueError, TypeError):
                continue
            except Exception as e:
                st.warning(f"Skipping calculation for EBITDA margin {val*100:.1f}%: {str(e)}")
                continue

    elif variable == "Leverage Ratio":
        base_value = base_leverage_ratio
        values = [max(0.5, base_value * (1 - variation_range + i * step_size)) for i in range(steps)]
        for val in values:
            try:
                result = calculate_lbo(
                    entry_multiple=base_entry_multiple,
                    leverage_ratio=val,
                    rev_growth=base_rev_growth,
                    ebitda_margin=base_ebitda_margin,
                    entry_ebitda=base_entry_ebitda,
                    exit_multiple=base_exit_multiple,
                    interest_rate=base_interest_rate,
                    tax_rate=base_tax_rate,
                    dso=dso,
                    dio=dio,
                    dpo=dpo,
                    transaction_expenses_pct=transaction_expenses_pct,
                    financing_fees_pct=financing_fees_pct,
                )
                results_list.append({
                    "Leverage Ratio": f"{val:.2f}x",
                    "IRR": result['irr'],
                    "MOIC": result['moic'],
                })
            except (KeyError, ValueError, TypeError):
                continue
            except Exception as e:
                st.warning(f"Skipping calculation for leverage ratio {val:.2f}x: {str(e)}")
                continue

    return results_list


@st.cache_data
def cached_calculate_lbo(
    entry_multiple: float,
    leverage_ratio: float,
    rev_growth: float,
    ebitda_margin: float,
    entry_ebitda: float,
    exit_multiple: float,
    interest_rate: float,
    tax_rate: float,
    dso: float = 45.0,
    dio: float = 30.0,
    dpo: float = 30.0,
    transaction_expenses_pct: float = 0.03,
    financing_fees_pct: float = 0.02,
    debt_instruments: Optional[List[Dict]] = None,
) -> Dict:
    """Cached wrapper for calculate_lbo to improve performance."""
    return calculate_lbo(
        entry_multiple=entry_multiple,
        leverage_ratio=leverage_ratio,
        rev_growth=rev_growth,
        ebitda_margin=ebitda_margin,
        entry_ebitda=entry_ebitda,
        exit_multiple=exit_multiple,
        interest_rate=interest_rate,
        tax_rate=tax_rate,
        dso=dso,
        dio=dio,
        dpo=dpo,
        transaction_expenses_pct=transaction_expenses_pct,
        financing_fees_pct=financing_fees_pct,
        debt_instruments=debt_instruments,
    )
