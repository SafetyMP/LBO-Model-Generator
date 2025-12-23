"""
Advanced analysis functions for LBO model.

Includes break-even analysis and other advanced calculations.
"""

import streamlit as st
from typing import Dict, Tuple, Optional
from src.lbo_engine import calculate_lbo


def calculate_break_even_exit_multiple(
    entry_multiple: float,
    leverage_ratio: float,
    rev_growth: float,
    ebitda_margin: float,
    entry_ebitda: float,
    target_irr: float = 0.20,  # 20% target IRR
    interest_rate: float = 0.08,
    tax_rate: float = 0.25,
    dso: float = 45.0,
    dio: float = 30.0,
    dpo: float = 30.0,
    transaction_expenses_pct: float = 0.03,
    financing_fees_pct: float = 0.02,
    debt_instruments: Optional[list] = None,
    tolerance: float = 0.001,  # 0.1% tolerance
    max_iterations: int = 100,
) -> Optional[float]:
    """
    Calculate break-even exit multiple to achieve target IRR.

    Uses binary search to find exit multiple that achieves target IRR.

    Returns:
        Break-even exit multiple or None if not found
    """
    # Binary search bounds
    low = entry_multiple * 0.5  # Minimum reasonable exit multiple
    high = entry_multiple * 2.0  # Maximum reasonable exit multiple

    for _ in range(max_iterations):
        mid = (low + high) / 2

        try:
            result = calculate_lbo(
                entry_multiple=entry_multiple,
                leverage_ratio=leverage_ratio,
                rev_growth=rev_growth,
                ebitda_margin=ebitda_margin,
                entry_ebitda=entry_ebitda,
                exit_multiple=mid,
                interest_rate=interest_rate,
                tax_rate=tax_rate,
                dso=dso,
                dio=dio,
                dpo=dpo,
                transaction_expenses_pct=transaction_expenses_pct,
                financing_fees_pct=financing_fees_pct,
                debt_instruments=debt_instruments,
            )

            current_irr = result['irr']

            if abs(current_irr - target_irr) < tolerance:
                return mid

            if current_irr < target_irr:
                low = mid
            else:
                high = mid

        except Exception:
            # If calculation fails, adjust bounds
            low = mid
            continue

    # Return best estimate
    return (low + high) / 2


def calculate_break_even_growth_rate(
    entry_multiple: float,
    leverage_ratio: float,
    ebitda_margin: float,
    entry_ebitda: float,
    exit_multiple: float,
    target_irr: float = 0.20,
    interest_rate: float = 0.08,
    tax_rate: float = 0.25,
    dso: float = 45.0,
    dio: float = 30.0,
    dpo: float = 30.0,
    transaction_expenses_pct: float = 0.03,
    financing_fees_pct: float = 0.02,
    debt_instruments: Optional[list] = None,
    tolerance: float = 0.001,
    max_iterations: int = 100,
) -> Optional[float]:
    """
    Calculate break-even revenue growth rate to achieve target IRR.

    Returns:
        Break-even growth rate (as decimal) or None if not found
    """
    low = 0.0  # 0% growth
    high = 0.50  # 50% growth (upper bound)

    for _ in range(max_iterations):
        mid = (low + high) / 2

        try:
            result = calculate_lbo(
                entry_multiple=entry_multiple,
                leverage_ratio=leverage_ratio,
                rev_growth=mid,
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

            current_irr = result['irr']

            if abs(current_irr - target_irr) < tolerance:
                return mid

            if current_irr < target_irr:
                low = mid
            else:
                high = mid

        except Exception:
            low = mid
            continue

    return (low + high) / 2


def calculate_break_even_margin(
    entry_multiple: float,
    leverage_ratio: float,
    rev_growth: float,
    entry_ebitda: float,
    exit_multiple: float,
    target_irr: float = 0.20,
    interest_rate: float = 0.08,
    tax_rate: float = 0.25,
    dso: float = 45.0,
    dio: float = 30.0,
    dpo: float = 30.0,
    transaction_expenses_pct: float = 0.03,
    financing_fees_pct: float = 0.02,
    debt_instruments: Optional[list] = None,
    tolerance: float = 0.001,
    max_iterations: int = 100,
) -> Optional[float]:
    """
    Calculate break-even EBITDA margin to achieve target IRR.

    Returns:
        Break-even EBITDA margin (as decimal) or None if not found
    """
    low = 0.05  # 5% margin (minimum)
    high = 0.50  # 50% margin (maximum)

    for _ in range(max_iterations):
        mid = (low + high) / 2

        try:
            result = calculate_lbo(
                entry_multiple=entry_multiple,
                leverage_ratio=leverage_ratio,
                rev_growth=rev_growth,
                ebitda_margin=mid,
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

            current_irr = result['irr']

            if abs(current_irr - target_irr) < tolerance:
                return mid

            if current_irr < target_irr:
                low = mid
            else:
                high = mid

        except Exception:
            low = mid
            continue

    return (low + high) / 2


def run_break_even_analysis(
    inputs: Dict,
    target_irr: float = 0.20,
) -> Dict[str, Optional[float]]:
    """
    Run comprehensive break-even analysis.

    Returns:
        Dictionary with break-even values for exit multiple, growth rate, and margin
    """
    results = {}

    with st.spinner("Calculating break-even exit multiple..."):
        results['exit_multiple'] = calculate_break_even_exit_multiple(
            entry_multiple=inputs.get('entry_multiple', 10.0),
            leverage_ratio=inputs.get('leverage_ratio', 4.0),
            rev_growth=inputs.get('rev_growth', 0.05),
            ebitda_margin=inputs.get('ebitda_margin', 0.20),
            entry_ebitda=inputs.get('entry_ebitda', 10000.0),
            target_irr=target_irr,
            interest_rate=inputs.get('interest_rate', 0.08),
            tax_rate=inputs.get('tax_rate', 0.25),
            dso=inputs.get('dso', 45.0),
            dio=inputs.get('dio', 30.0),
            dpo=inputs.get('dpo', 30.0),
            transaction_expenses_pct=inputs.get('transaction_expenses_pct', 0.03),
            financing_fees_pct=inputs.get('financing_fees_pct', 0.02),
        )

    with st.spinner("Calculating break-even growth rate..."):
        results['growth_rate'] = calculate_break_even_growth_rate(
            entry_multiple=inputs.get('entry_multiple', 10.0),
            leverage_ratio=inputs.get('leverage_ratio', 4.0),
            ebitda_margin=inputs.get('ebitda_margin', 0.20),
            entry_ebitda=inputs.get('entry_ebitda', 10000.0),
            exit_multiple=inputs.get('exit_multiple', 10.0),
            target_irr=target_irr,
            interest_rate=inputs.get('interest_rate', 0.08),
            tax_rate=inputs.get('tax_rate', 0.25),
            dso=inputs.get('dso', 45.0),
            dio=inputs.get('dio', 30.0),
            dpo=inputs.get('dpo', 30.0),
            transaction_expenses_pct=inputs.get('transaction_expenses_pct', 0.03),
            financing_fees_pct=inputs.get('financing_fees_pct', 0.02),
        )

    with st.spinner("Calculating break-even margin..."):
        results['margin'] = calculate_break_even_margin(
            entry_multiple=inputs.get('entry_multiple', 10.0),
            leverage_ratio=inputs.get('leverage_ratio', 4.0),
            rev_growth=inputs.get('rev_growth', 0.05),
            entry_ebitda=inputs.get('entry_ebitda', 10000.0),
            exit_multiple=inputs.get('exit_multiple', 10.0),
            target_irr=target_irr,
            interest_rate=inputs.get('interest_rate', 0.08),
            tax_rate=inputs.get('tax_rate', 0.25),
            dso=inputs.get('dso', 45.0),
            dio=inputs.get('dio', 30.0),
            dpo=inputs.get('dpo', 30.0),
            transaction_expenses_pct=inputs.get('transaction_expenses_pct', 0.03),
            financing_fees_pct=inputs.get('financing_fees_pct', 0.02),
        )

    return results
