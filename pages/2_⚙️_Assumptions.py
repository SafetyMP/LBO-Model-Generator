"""
Assumptions Configuration Page

Allows users to configure LBO model inputs.
"""

import streamlit as st

# IMPORTANT: st.set_page_config() must be the FIRST Streamlit command
st.set_page_config(
    page_title="Assumptions",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",  # Force sidebar to be open
)

from streamlit_modules.app_config import initialize_session_state, get_openai_api_key
from streamlit_modules.app_utils import load_test_case, cached_calculate_lbo
from streamlit_modules.app_performance import add_cache_management_ui

# Initialize session state
initialize_session_state()
OPENAI_API_KEY = get_openai_api_key()

st.title("⚙️ Assumptions")

# Test case selection
test_cases = {
    "AlphaCo": "AlphaCo_config.json",
    "DataCore": "DataCore_config.json",
    "SentinelGuard": "SentinelGuard_config.json",
    "VectorServe": "VectorServe_config.json",
}

selected_test = st.selectbox("Load Test Case (Optional):", ["None"] + list(test_cases.keys()))

# Load test case if selected
if selected_test != "None":
    test_config = load_test_case(test_cases[selected_test])
    if test_config:
        entry_multiple_val = float(test_config.get("entry_multiple", 10.0))
        leverage_ratio_val = (
            float(test_config.get("debt_instruments", [{}])[0].get("ebitda_multiple", 4.0))
            if test_config.get("debt_instruments")
            else 4.0
        )
        rev_growth_val = float(test_config.get("revenue_growth_rate", [0.05])[0])
        ebitda_margin_val = 0.20  # Default
        entry_ebitda_val = float(test_config.get("entry_ebitda", 10000.0))
        exit_multiple_val = float(test_config.get("exit_multiple", 10.0))
        interest_rate_val = (
            float(test_config.get("debt_instruments", [{}])[0].get("interest_rate", 0.08))
            if test_config.get("debt_instruments")
            else 0.08
        )
        tax_rate_val = float(test_config.get("tax_rate", 0.25))
    else:
        entry_multiple_val = 10.0
        leverage_ratio_val = 4.0
        rev_growth_val = 0.05
        ebitda_margin_val = 0.20
        entry_ebitda_val = 10000.0
        exit_multiple_val = 10.0
        interest_rate_val = 0.08
        tax_rate_val = 0.25
else:
    # Use defaults or session state
    entry_multiple_val = st.session_state.current_inputs.get("entry_multiple", 10.0)
    leverage_ratio_val = st.session_state.current_inputs.get("leverage_ratio", 4.0)
    rev_growth_val = st.session_state.current_inputs.get("rev_growth", 0.05)
    ebitda_margin_val = st.session_state.current_inputs.get("ebitda_margin", 0.20)
    entry_ebitda_val = st.session_state.current_inputs.get("entry_ebitda", 10000.0)
    exit_multiple_val = st.session_state.current_inputs.get("exit_multiple", 10.0)
    interest_rate_val = st.session_state.current_inputs.get("interest_rate", 0.08)
    tax_rate_val = st.session_state.current_inputs.get("tax_rate", 0.25)

# Sidebar for Inputs
with st.sidebar:
    st.header("Entry Assumptions")
    entry_multiple = st.slider(
        "Entry EBITDA Multiple",
        5.0,
        15.0,
        entry_multiple_val,
        0.5,
        help="Purchase price multiple. Typical range: 5-12x for most industries.",
    )
    leverage_ratio = st.slider(
        "Debt/EBITDA (Leverage)",
        2.0,
        7.0,
        leverage_ratio_val,
        0.1,
        help="Total debt as multiple of EBITDA. Typical range: 3-5x.",
    )

    st.header("Operating Projections")
    rev_growth = (
        st.slider(
            "Annual Revenue Growth (%)",
            0.0,
            20.0,
            rev_growth_val * 100,
            0.5,
            help="Expected annual revenue growth rate.",
        )
        / 100
    )
    ebitda_margin = (
        st.slider(
            "EBITDA Margin (%)",
            10.0,
            40.0,
            ebitda_margin_val * 100,
            0.5,
            help="EBITDA as percentage of revenue.",
        )
        / 100
    )

    st.header("Advanced Options")
    entry_ebitda = st.number_input(
        "Entry EBITDA ($)",
        min_value=1000.0,
        value=entry_ebitda_val,
        step=1000.0,
        help="Company's EBITDA at entry.",
    )
    exit_multiple = st.slider(
        "Exit EBITDA Multiple", 5.0, 15.0, exit_multiple_val, 0.5, help="Expected exit multiple."
    )

    # Debt Structure
    with st.expander("💳 Debt Structure", expanded=False):
        debt_structure_type = st.radio(
            "Debt Structure:",
            ["Single Instrument", "Senior + Subordinated"],
            help="Choose between single debt instrument or multiple tranches",
        )

        if debt_structure_type == "Single Instrument":
            interest_rate = (
                st.slider(
                    "Debt Interest Rate (%)",
                    4.0,
                    15.0,
                    interest_rate_val * 100,
                    0.5,
                    help="Weighted average interest rate on debt.",
                )
                / 100
            )
            debt_instruments = None
        else:
            st.markdown("**Senior Debt**")
            senior_pct = st.slider("Senior Debt (% of Total Debt)", 50.0, 90.0, 70.0, 5.0) / 100
            senior_rate = st.slider("Senior Interest Rate (%)", 4.0, 10.0, 7.0, 0.25) / 100
            senior_schedule = st.selectbox(
                "Senior Amortization", ["cash_flow_sweep", "amortizing", "bullet"], index=0
            )

            st.markdown("**Subordinated Debt**")
            sub_rate = st.slider("Subordinated Interest Rate (%)", 8.0, 15.0, 12.0, 0.25) / 100
            sub_schedule = st.selectbox(
                "Subordinated Amortization", ["bullet", "cash_flow_sweep", "amortizing"], index=0
            )

            debt_instruments = {
                "type": "multiple",
                "senior_pct": senior_pct,
                "senior_rate": senior_rate,
                "senior_schedule": senior_schedule,
                "sub_rate": sub_rate,
                "sub_schedule": sub_schedule,
            }
            interest_rate = (senior_rate * senior_pct) + (sub_rate * (1 - senior_pct))

    tax_rate = st.slider("Tax Rate (%)", 15.0, 35.0, tax_rate_val * 100, 0.5) / 100

    # Working Capital
    with st.expander("⚙️ Working Capital Assumptions"):
        dso = st.slider("Days Sales Outstanding (DSO)", 0.0, 365.0, 45.0, 5.0)
        dio = st.slider("Days Inventory Outstanding (DIO)", 0.0, 365.0, 30.0, 5.0)
        dpo = st.slider("Days Payable Outstanding (DPO)", 0.0, 365.0, 30.0, 5.0)

    # Transaction Costs
    with st.expander("💰 Transaction Costs"):
        transaction_expenses_pct = (
            st.slider("Transaction Expenses (% of EV)", 0.0, 10.0, 3.0, 0.5) / 100
        )
        financing_fees_pct = st.slider("Financing Fees (% of Total Debt)", 0.0, 5.0, 2.0, 0.5) / 100

    # Performance & Cache Management
    add_cache_management_ui()

# Calculate button
if st.button("🔄 Calculate LBO Model", type="primary", use_container_width=True):
    # Calculate debt instrument amounts if multiple instruments
    debt_instruments_list = None
    if (
        debt_instruments is not None
        and isinstance(debt_instruments, dict)
        and debt_instruments.get("type") == "multiple"
    ):
        total_debt = entry_ebitda * leverage_ratio
        senior_amount = total_debt * debt_instruments["senior_pct"]
        sub_amount = total_debt - senior_amount
        debt_instruments_list = [
            {
                "name": "Senior Debt",
                "amount": senior_amount,
                "interest_rate": debt_instruments["senior_rate"],
                "amortization_schedule": debt_instruments["senior_schedule"],
                "amortization_periods": 5,
                "priority": 1,
            },
            {
                "name": "Subordinated Debt",
                "amount": sub_amount,
                "interest_rate": debt_instruments["sub_rate"],
                "amortization_schedule": debt_instruments["sub_schedule"],
                "amortization_periods": 5,
                "priority": 2,
            },
        ]

    with st.spinner("Calculating LBO model..."):
        try:
            results = cached_calculate_lbo(
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
                debt_instruments=debt_instruments_list,
            )

            # Store in session state
            st.session_state.current_results = results
            st.session_state.current_inputs = {
                "entry_multiple": entry_multiple,
                "leverage_ratio": leverage_ratio,
                "rev_growth": rev_growth,
                "ebitda_margin": ebitda_margin,
                "entry_ebitda": entry_ebitda,
                "exit_multiple": exit_multiple,
                "interest_rate": interest_rate,
                "tax_rate": tax_rate,
                "dso": dso,
                "dio": dio,
                "dpo": dpo,
                "transaction_expenses_pct": transaction_expenses_pct,
                "financing_fees_pct": financing_fees_pct,
            }

            st.success("✅ Model calculated successfully! Navigate to Dashboard to see results.")
            st.balloons()

        except Exception as e:
            st.error(f"Error calculating LBO model: {str(e)}")
            st.exception(e)
