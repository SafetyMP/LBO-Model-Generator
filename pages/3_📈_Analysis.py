"""
Analysis Page

Sensitivity analysis, scenario comparison, and enhanced visualizations.
"""

import streamlit as st

# IMPORTANT: st.set_page_config() must be the FIRST Streamlit command
st.set_page_config(
    page_title="Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
from streamlit_modules.app_config import initialize_session_state
from streamlit_modules.app_utils import calculate_sensitivity_analysis
from streamlit_modules.app_visualizations import (
    create_equity_waterfall,
    create_returns_attribution,
    create_tornado_chart,
    render_standard_charts
)
from streamlit_modules.app_analysis import run_break_even_analysis

# Initialize session state
initialize_session_state()

st.title("📈 Analysis")

if not st.session_state.current_results:
    st.info("👈 Please configure assumptions and calculate the model first.")
    st.stop()

results = st.session_state.current_results
inputs = st.session_state.current_inputs

# Enhanced Visualizations
st.subheader("🎨 Enhanced Visualizations")

viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Equity Waterfall", "Returns Attribution", "Standard Charts"])

with viz_tab1:
    st.markdown("**Equity Value Waterfall** - Shows value creation breakdown")
    try:
        fig = create_equity_waterfall(results)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not create equity waterfall: {str(e)}")
        st.info("💡 Install plotly: `pip install plotly`")

with viz_tab2:
    st.markdown("**Returns Attribution** - Shows IRR driver contributions")
    try:
        fig = create_returns_attribution(results, inputs)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not create returns attribution: {str(e)}")

with viz_tab3:
    render_standard_charts(results)

# Sensitivity Analysis
st.subheader("📊 Sensitivity Analysis")

sens_col1, sens_col2 = st.columns(2)
with sens_col1:
    show_sensitivity = st.checkbox("Show Sensitivity Analysis", value=False)
    sensitivity_variable = st.selectbox(
        "Variable to Analyze",
        ["Exit Multiple", "Entry Multiple", "Revenue Growth", "EBITDA Margin", "Leverage Ratio"],
        index=0
    )

with sens_col2:
    sensitivity_range = st.slider("Variation Range (%)", 10, 50, 20, 5)
    sensitivity_steps = st.slider("Number of Steps", 3, 11, 5, 2)

if show_sensitivity:
    with st.spinner("Calculating sensitivity analysis..."):
        try:
            sensitivity_results = calculate_sensitivity_analysis(
                base_results=results,
                variable=sensitivity_variable,
                base_entry_multiple=inputs.get('entry_multiple', 10.0),
                base_exit_multiple=inputs.get('exit_multiple', 10.0),
                base_rev_growth=inputs.get('rev_growth', 0.05),
                base_ebitda_margin=inputs.get('ebitda_margin', 0.20),
                base_leverage_ratio=inputs.get('leverage_ratio', 4.0),
                base_entry_ebitda=inputs.get('entry_ebitda', 10000.0),
                base_interest_rate=inputs.get('interest_rate', 0.08),
                base_tax_rate=inputs.get('tax_rate', 0.25),
                range_pct=sensitivity_range,
                steps=sensitivity_steps,
                dso=inputs.get('dso', 45.0),
                dio=inputs.get('dio', 30.0),
                dpo=inputs.get('dpo', 30.0),
                transaction_expenses_pct=inputs.get('transaction_expenses_pct', 0.03),
                financing_fees_pct=inputs.get('financing_fees_pct', 0.02),
            )

            if sensitivity_results:
                st.subheader(f"Sensitivity: {sensitivity_variable}")

                # Display table
                sens_df = pd.DataFrame(sensitivity_results)
                st.dataframe(sens_df, use_container_width=True)

                # Tornado Chart
                try:
                    base_irr = results['irr']
                    base_moic = results['moic']
                    tornado_fig = create_tornado_chart(sensitivity_results, base_irr, base_moic)
                    if tornado_fig:
                        st.plotly_chart(tornado_fig, use_container_width=True)
                except Exception:
                    st.info("💡 Tornado chart requires plotly. Install: `pip install plotly`")

                # Line charts
                viz_col1, viz_col2 = st.columns(2)
                with viz_col1:
                    st.subheader("IRR Sensitivity")
                    if 'IRR' in sens_df.columns and sensitivity_variable in sens_df.columns:
                        chart_data = sens_df.set_index(sensitivity_variable)[['IRR']]
                        st.line_chart(chart_data)

                with viz_col2:
                    st.subheader("MOIC Sensitivity")
                    if 'MOIC' in sens_df.columns and sensitivity_variable in sens_df.columns:
                        chart_data = sens_df.set_index(sensitivity_variable)[['MOIC']]
                        st.line_chart(chart_data)
            else:
                st.warning("No sensitivity results generated.")

        except Exception as sens_error:
            st.warning(f"Sensitivity analysis error: {str(sens_error)}")

# Debt Schedule
st.subheader("📉 Debt Schedule")
debt_df = results.get('debt_balance_over_time')
if debt_df is not None:
    if len(debt_df.columns) > 1:
        st.area_chart(debt_df)
        st.caption("💡 Chart shows debt breakdown by instrument")
    else:
        st.area_chart(debt_df)

    with st.expander("View Detailed Debt Schedule"):
        st.dataframe(debt_df, use_container_width=True)

# Break-Even Analysis
st.subheader("🎯 Break-Even Analysis")

break_even_tab1, break_even_tab2 = st.tabs(["Break-Even Calculator", "About"])

with break_even_tab1:
    st.markdown("**Calculate break-even values to achieve target IRR**")

    target_irr = st.slider(
        "Target IRR (%)",
        10.0, 50.0, 20.0, 1.0,
        help="Target IRR to achieve"
    ) / 100

    if st.button("Calculate Break-Even Values", type="primary"):
        try:
            break_even_results = run_break_even_analysis(inputs, target_irr)

            st.markdown("### Break-Even Results")

            col1, col2, col3 = st.columns(3)

            with col1:
                if break_even_results.get('exit_multiple'):
                    be_exit = break_even_results['exit_multiple']
                    current_exit = inputs.get('exit_multiple', 10.0)
                    diff = be_exit - current_exit
                    st.metric(
                        "Break-Even Exit Multiple",
                        f"{be_exit:.2f}x",
                        f"{diff:+.2f}x vs current"
                    )
                    if be_exit > current_exit:
                        st.warning(f"⚠️ Need {diff:.2f}x higher exit multiple")
                    else:
                        st.success(f"✅ Current exit multiple exceeds break-even by {abs(diff):.2f}x")

            with col2:
                if break_even_results.get('growth_rate'):
                    be_growth = break_even_results['growth_rate']
                    current_growth = inputs.get('rev_growth', 0.05)
                    diff = be_growth - current_growth
                    st.metric(
                        "Break-Even Growth Rate",
                        f"{be_growth:.1%}",
                        f"{diff:+.1%} vs current"
                    )
                    if be_growth > current_growth:
                        st.warning(f"⚠️ Need {diff:.1%} higher growth rate")
                    else:
                        st.success(f"✅ Current growth exceeds break-even by {abs(diff):.1%}")

            with col3:
                if break_even_results.get('margin'):
                    be_margin = break_even_results['margin']
                    current_margin = inputs.get('ebitda_margin', 0.20)
                    diff = be_margin - current_margin
                    st.metric(
                        "Break-Even EBITDA Margin",
                        f"{be_margin:.1%}",
                        f"{diff:+.1%} vs current"
                    )
                    if be_margin > current_margin:
                        st.warning(f"⚠️ Need {diff:.1%} higher margin")
                    else:
                        st.success(f"✅ Current margin exceeds break-even by {abs(diff):.1%}")

            # Summary
            st.markdown("### Summary")
            summary_points = []
            if break_even_results.get('exit_multiple'):
                be_exit = break_even_results['exit_multiple']
                current_exit = inputs.get('exit_multiple', 10.0)
                if be_exit <= current_exit:
                    summary_points.append(f"✅ Exit multiple is sufficient (need {be_exit:.2f}x, have {current_exit:.2f}x)")
                else:
                    summary_points.append(f"⚠️ Exit multiple needs to increase from {current_exit:.2f}x to {be_exit:.2f}x")

            if break_even_results.get('growth_rate'):
                be_growth = break_even_results['growth_rate']
                current_growth = inputs.get('rev_growth', 0.05)
                if be_growth <= current_growth:
                    summary_points.append(f"✅ Growth rate is sufficient (need {be_growth:.1%}, have {current_growth:.1%})")
                else:
                    summary_points.append(f"⚠️ Growth rate needs to increase from {current_growth:.1%} to {be_growth:.1%}")

            if break_even_results.get('margin'):
                be_margin = break_even_results['margin']
                current_margin = inputs.get('ebitda_margin', 0.20)
                if be_margin <= current_margin:
                    summary_points.append(f"✅ EBITDA margin is sufficient (need {be_margin:.1%}, have {current_margin:.1%})")
                else:
                    summary_points.append(f"⚠️ EBITDA margin needs to increase from {current_margin:.1%} to {be_margin:.1%}")

            for point in summary_points:
                st.markdown(f"• {point}")

        except Exception as e:
            st.error(f"Break-even analysis error: {str(e)}")
            st.exception(e)

with break_even_tab2:
    st.markdown("""
    ### About Break-Even Analysis

    Break-even analysis calculates the minimum values required for key assumptions to achieve a target IRR.

    **Break-Even Exit Multiple:**
    - The minimum exit multiple needed to achieve target IRR
    - Compares against your current exit multiple assumption
    - If break-even > current, you need multiple expansion

    **Break-Even Growth Rate:**
    - The minimum revenue growth rate needed to achieve target IRR
    - Compares against your current growth assumption
    - If break-even > current, you need higher growth

    **Break-Even EBITDA Margin:**
    - The minimum EBITDA margin needed to achieve target IRR
    - Compares against your current margin assumption
    - If break-even > current, you need margin expansion

    **How to Use:**
    1. Set your target IRR (default: 20%)
    2. Click "Calculate Break-Even Values"
    3. Review the results and compare to your current assumptions
    4. Adjust assumptions if break-even values exceed current values
    """)
