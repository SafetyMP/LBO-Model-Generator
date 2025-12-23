"""
Visualization functions for Streamlit app.

Includes enhanced charts: equity waterfall, returns attribution, tornado chart.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Optional
import plotly.graph_objects as go
import plotly.express as px


def create_equity_waterfall(results: Dict) -> go.Figure:
    """
    Create equity value waterfall chart showing value creation breakdown.

    Shows: Entry Equity → Operational Improvement → Multiple Expansion → Leverage → Exit Equity
    """
    entry_ev = results.get("entry_ev", 0)
    exit_ev = results.get("exit_ev", 0)
    entry_ebitda = results.get("entry_ebitda", 0)
    exit_ebitda = results.get("exit_ebitda", 0)
    entry_multiple = entry_ev / entry_ebitda if entry_ebitda > 0 else 0
    exit_multiple = exit_ev / exit_ebitda if exit_ebitda > 0 else 0
    equity_invested = results.get("equity_invested", 0)
    exit_equity_value = results.get("exit_equity_value", 0)

    # Calculate value creation components
    # 1. Entry Equity
    entry_equity = equity_invested

    # 2. Operational Improvement (EBITDA growth at entry multiple)
    ebitda_growth = exit_ebitda - entry_ebitda
    operational_value = ebitda_growth * entry_multiple

    # 3. Multiple Expansion (Exit multiple premium)
    multiple_expansion = (exit_multiple - entry_multiple) * exit_ebitda

    # 4. Debt Paydown (cash generation)
    debt_paid = results.get("debt_paid", 0) * 1_000_000

    # 5. Exit Equity
    exit_equity = exit_equity_value

    # Create waterfall data
    categories = [
        "Entry Equity",
        "Operational\nImprovement",
        "Multiple\nExpansion",
        "Debt Paydown",
        "Exit Equity",
    ]
    values = [entry_equity, operational_value, multiple_expansion, debt_paid, exit_equity]
    cumulative = [entry_equity]
    for i in range(1, len(values)):
        cumulative.append(cumulative[i - 1] + values[i])

    # Create waterfall chart
    fig = go.Figure()

    # Add bars
    colors = ["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728", "#9467bd"]
    for i, (cat, val, cum) in enumerate(zip(categories, values, cumulative)):
        if i == 0:
            # Starting point
            fig.add_trace(
                go.Bar(
                    x=[cat],
                    y=[val],
                    marker_color=colors[i],
                    name=cat,
                    text=[f"${val/1_000_000:.1f}M"],
                    textposition="outside",
                )
            )
        elif i < len(categories) - 1:
            # Intermediate steps
            fig.add_trace(
                go.Bar(
                    x=[cat],
                    y=[val],
                    marker_color=colors[i],
                    name=cat,
                    text=[f"${val/1_000_000:.1f}M"],
                    textposition="outside",
                )
            )
        else:
            # Final value
            fig.add_trace(
                go.Bar(
                    x=[cat],
                    y=[val],
                    marker_color=colors[i],
                    name=cat,
                    text=[f"${val/1_000_000:.1f}M"],
                    textposition="outside",
                )
            )

    fig.update_layout(
        title="Equity Value Waterfall",
        xaxis_title="",
        yaxis_title="Value ($)",
        barmode="group",
        height=500,
        showlegend=False,
    )

    return fig


def create_returns_attribution(results: Dict, inputs: Dict) -> go.Figure:
    """
    Create returns attribution chart showing IRR driver contributions.

    Shows contribution of: Revenue Growth, Margin Expansion, Multiple Expansion, Leverage, Debt Paydown
    """
    # This is a simplified attribution - in practice would need more detailed calculations
    # For now, show relative contributions based on available data

    irr = results.get("irr", 0)

    # Estimate contributions (simplified)
    # In a real implementation, would calculate from detailed model
    entry_multiple = inputs.get("entry_multiple", 10.0)
    exit_multiple = inputs.get("exit_multiple", 10.0)
    rev_growth = inputs.get("rev_growth", 0.05)
    leverage_ratio = inputs.get("leverage_ratio", 4.0)

    # Simplified attribution (would need more sophisticated calculation)
    multiple_contribution = abs(exit_multiple - entry_multiple) / entry_multiple * 0.3
    growth_contribution = rev_growth * 0.4
    leverage_contribution = min(leverage_ratio / 5.0, 1.0) * 0.2
    margin_contribution = 0.1

    drivers = ["Multiple\nExpansion", "Revenue\nGrowth", "Leverage", "Margin\nExpansion"]
    contributions = [
        multiple_contribution * irr,
        growth_contribution * irr,
        leverage_contribution * irr,
        margin_contribution * irr,
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=drivers,
                y=contributions,
                marker_color=["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728"],
                text=[f"{c/irr*100:.0f}%" if irr > 0 else "0%" for c in contributions],
                textposition="outside",
            )
        ]
    )

    fig.update_layout(
        title="IRR Attribution by Driver",
        xaxis_title="Value Driver",
        yaxis_title="IRR Contribution (%)",
        height=400,
    )

    return fig


def create_tornado_chart(sensitivity_results: list, base_irr: float, base_moic: float) -> go.Figure:
    """
    Create tornado chart showing sensitivity of IRR/MOIC to assumptions.

    Args:
        sensitivity_results: List of dicts with sensitivity analysis results
        base_irr: Base case IRR
        base_moic: Base case MOIC
    """
    if not sensitivity_results:
        return None

    # Convert to DataFrame
    df = pd.DataFrame(sensitivity_results)

    # Get variable name (first column that's not IRR or MOIC)
    var_col = None
    for col in df.columns:
        if col not in ["IRR", "MOIC"]:
            var_col = col
            break

    if var_col is None:
        return None

    # Calculate deviations from base
    df["IRR Deviation"] = (df["IRR"] - base_irr) * 100  # In percentage points
    df["MOIC Deviation"] = df["MOIC"] - base_moic

    # Sort by absolute IRR deviation
    df = df.sort_values("IRR Deviation", key=abs, ascending=False)

    # Create tornado chart
    fig = go.Figure()

    # Positive deviations (above base)
    above_base = df[df["IRR Deviation"] >= 0]
    if not above_base.empty:
        fig.add_trace(
            go.Bar(
                y=above_base[var_col],
                x=above_base["IRR Deviation"],
                orientation="h",
                name="Above Base",
                marker_color="#2ca02c",
                text=[f"+{d:.1f}pp" for d in above_base["IRR Deviation"]],
                textposition="outside",
            )
        )

    # Negative deviations (below base)
    below_base = df[df["IRR Deviation"] < 0]
    if not below_base.empty:
        fig.add_trace(
            go.Bar(
                y=below_base[var_col],
                x=below_base["IRR Deviation"],
                orientation="h",
                name="Below Base",
                marker_color="#d62728",
                text=[f"{d:.1f}pp" for d in below_base["IRR Deviation"]],
                textposition="outside",
            )
        )

    fig.update_layout(
        title="Tornado Chart: IRR Sensitivity",
        xaxis_title="IRR Deviation (percentage points)",
        yaxis_title=var_col,
        height=400,
        barmode="overlay",
    )

    return fig


def render_standard_charts(results: Dict):
    """Render standard financial statement charts."""
    if "financial_statements" not in results or results["financial_statements"].empty:
        return

    fs = results["financial_statements"]

    # Revenue and EBITDA Trends
    if "Revenue" in fs.columns and "Ebitda" in fs.columns:
        st.subheader("📈 Revenue and EBITDA Trends")
        st.line_chart(fs[["Revenue", "Ebitda"]])

    # Free Cash Flow
    if "Fcf" in fs.columns:
        st.subheader("💵 Free Cash Flow Generation")
        st.bar_chart(fs[["Fcf"]])

    # Coverage Ratios
    if "coverage_ratios" in results and not results["coverage_ratios"].empty:
        st.subheader("🛡️ Coverage Ratios")
        st.line_chart(results["coverage_ratios"])
