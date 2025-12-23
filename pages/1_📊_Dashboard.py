"""
Main Dashboard Page

Displays high-level results, returns analysis, and key metrics.
"""

import streamlit as st

# IMPORTANT: st.set_page_config() must be the FIRST Streamlit command
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

from streamlit_modules.app_config import initialize_session_state
from streamlit_modules.app_utils import cached_calculate_lbo
from streamlit_modules.app_export import export_pdf_button

# Initialize session state
initialize_session_state()

st.title("📊 Dashboard")

# Note: Page navigation menu appears automatically in the sidebar
# Navigate between pages using the sidebar menu at the top

# Get results from session state
if st.session_state.current_results:
    results = st.session_state.current_results

    # Returns Analysis
    st.subheader("📊 Returns Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Equity IRR", f"{results['irr']:.1%}")
    col2.metric("MOIC", f"{results['moic']:.2f}x")
    col3.metric("Total Debt Paydown", f"${results['debt_paid']:.1f}M")

    # Exit Metrics
    st.subheader("💰 Exit Metrics")
    exit_col1, exit_col2, exit_col3, exit_col4 = st.columns(4)
    exit_col1.metric("Exit EV", f"${results['exit_ev']/1_000_000:.1f}M")
    exit_col2.metric("Exit Equity Value", f"${results['exit_equity_value']/1_000_000:.1f}M")
    exit_col3.metric("Exit Cash", f"${results['exit_cash']/1_000_000:.1f}M")
    exit_col4.metric("Equity Invested", f"{results['equity_invested']/1_000_000:.1f}M")

    # Entry vs Exit Comparison
    st.subheader("📈 Entry vs Exit Comparison")
    comp_col1, comp_col2, comp_col3 = st.columns(3)
    ev_change = ((results['exit_ev'] - results['entry_ev']) / results['entry_ev']) * 100
    comp_col1.metric("EV Change", f"{ev_change:+.1f}%",
                    f"${results['entry_ev']/1_000_000:.1f}M → ${results['exit_ev']/1_000_000:.1f}M")
    ebitda_change = ((results['exit_ebitda'] - results['entry_ebitda']) / results['entry_ebitda']) * 100
    comp_col2.metric("EBITDA Change", f"{ebitda_change:+.1f}%",
                    f"${results['entry_ebitda']/1_000_000:.1f}M → ${results['exit_ebitda']/1_000_000:.1f}M")

    # Get leverage ratio from inputs
    leverage_ratio = st.session_state.current_inputs.get('leverage_ratio', 4.0)
    debt_paydown_pct = (results['debt_paid'] * 1_000_000 / (results['entry_ev'] * leverage_ratio)) * 100 if leverage_ratio > 0 else 0
    comp_col3.metric("Debt Paydown %", f"{debt_paydown_pct:.1f}%")

    # PDF Export
    st.markdown("---")
    st.subheader("💾 Export")
    export_pdf_button(results, st.session_state.current_inputs)
else:
    st.info("👈 Please configure your assumptions in the Assumptions page to see results here.")
