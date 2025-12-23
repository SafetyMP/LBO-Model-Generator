"""
Help and Documentation Page

Comprehensive help system with guides, FAQs, and examples.
"""

import streamlit as st

# IMPORTANT: st.set_page_config() must be the FIRST Streamlit command
st.set_page_config(
    page_title="Help",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from streamlit_modules.app_config import initialize_session_state

# Initialize session state
initialize_session_state()

st.title("ℹ️ Help & Documentation")

help_tab1, help_tab2, help_tab3, help_tab4 = st.tabs([
    "Getting Started",
    "Understanding Metrics",
    "Best Practices",
    "FAQ"
])

with help_tab1:
    st.markdown("""
    ## Getting Started Guide

    ### Step 1: Configure Assumptions
    1. Navigate to the **⚙️ Assumptions** page
    2. Use the sidebar to set your LBO model inputs:
       - **Entry Assumptions**: Entry multiple, leverage ratio
       - **Operating Projections**: Revenue growth, EBITDA margin
       - **Advanced Options**: Entry EBITDA, exit multiple, tax rate
       - **Debt Structure**: Single or multiple instruments
       - **Working Capital**: DSO, DIO, DPO
       - **Transaction Costs**: Expenses and financing fees

    3. Click **"🔄 Calculate LBO Model"** to run the analysis

    ### Step 2: View Results
    1. Navigate to the **📊 Dashboard** page
    2. Review key metrics:
       - Equity IRR
       - MOIC (Multiple on Invested Capital)
       - Exit metrics (EV, Equity Value, Cash)
       - Entry vs Exit comparison

    ### Step 3: Analyze
    1. Go to the **📈 Analysis** page
    2. Explore:
       - Enhanced visualizations (waterfall, attribution, tornado charts)
       - Sensitivity analysis
       - Break-even analysis
       - Debt schedule

    ### Quick Tips
    - **Load Test Cases**: Use the dropdown in Assumptions to load example configurations
    - **Save Scenarios**: Use comparison features to save and compare multiple scenarios
    - **Export**: Download Excel models or JSON configurations
    """)

with help_tab2:
    st.markdown("""
    ## Understanding Key Metrics

    ### Returns Metrics

    **Equity IRR (Internal Rate of Return)**
    - The annualized return on equity investment
    - Typical target: 20-30% for LBOs
    - Formula: Discount rate where NPV of cash flows = 0

    **MOIC (Multiple on Invested Capital)**
    - Total return multiple (e.g., 2.5x means 2.5x return)
    - Typical target: 2.0-3.0x for 5-year hold
    - Formula: Exit Equity Value / Equity Invested

    ### Valuation Metrics

    **Entry/Exit Multiple**
    - Enterprise Value / EBITDA
    - Entry: Purchase price multiple
    - Exit: Expected sale multiple
    - Typical range: 5-12x depending on industry

    **Enterprise Value (EV)**
    - Total company value
    - Formula: Equity Value + Debt - Cash
    - Entry EV = Entry EBITDA × Entry Multiple
    - Exit EV = Exit EBITDA × Exit Multiple

    ### Debt Metrics

    **Leverage Ratio**
    - Total Debt / EBITDA
    - Typical range: 3-5x for most LBOs
    - Higher leverage = higher returns but higher risk

    **Debt Paydown**
    - Amount of debt paid down during hold period
    - Driven by free cash flow generation
    - Higher paydown = lower exit debt = higher equity value

    ### Operating Metrics

    **Revenue Growth**
    - Annual revenue growth rate
    - Typical range: 5-15% for mature companies
    - Higher growth = higher exit value

    **EBITDA Margin**
    - EBITDA / Revenue
    - Industry-specific (Software: 20-40%, Manufacturing: 10-20%)
    - Margin expansion = value creation

    ### Coverage Ratios

    **Interest Coverage**
    - EBITDA / Interest Expense
    - Measures ability to service debt
    - Target: >2.0x minimum

    **Debt Service Coverage**
    - EBITDA / (Interest + Principal Payments)
    - Measures ability to service all debt obligations
    - Target: >1.25x minimum
    """)

with help_tab3:
    st.markdown("""
    ## Best Practices

    ### Assumption Setting

    **Entry Multiple**
    - Research comparable transactions
    - Consider growth prospects
    - Factor in market conditions
    - Typical: 5-12x EBITDA

    **Leverage Ratio**
    - Match to cash flow generation
    - Consider industry norms
    - Factor in interest rate environment
    - Typical: 3-5x EBITDA

    **Revenue Growth**
    - Base on market size and company position
    - Consider historical performance
    - Factor in competitive dynamics
    - Be realistic about execution

    **EBITDA Margin**
    - Research industry benchmarks
    - Consider operational improvements
    - Factor in cost structure
    - Typical: 10-40% depending on industry

    **Exit Multiple**
    - Usually 0.5-1.5x higher than entry
    - Consider multiple expansion potential
    - Factor in market conditions
    - Research exit comparables

    ### Analysis Best Practices

    **Sensitivity Analysis**
    - Test key assumptions
    - Identify value drivers
    - Understand risk factors
    - Use tornado charts to prioritize

    **Break-Even Analysis**
    - Calculate minimum values needed
    - Compare to current assumptions
    - Identify gaps
    - Adjust strategy if needed

    **Scenario Planning**
    - Create Base/High/Low cases
    - Test downside scenarios
    - Understand probability of outcomes
    - Plan for different outcomes

    ### Common Pitfalls

    ❌ **Overly Optimistic Growth**
    - Unrealistic growth assumptions
    - Solution: Base on market research

    ❌ **Ignoring Working Capital**
    - Forgetting working capital needs
    - Solution: Set realistic DSO/DIO/DPO

    ❌ **Aggressive Leverage**
    - Too much debt relative to cash flow
    - Solution: Ensure adequate coverage ratios

    ❌ **Unrealistic Exit Multiple**
    - Assuming significant multiple expansion
    - Solution: Be conservative, base on comparables
    """)

with help_tab4:
    st.markdown("""
    ## Frequently Asked Questions

    ### General Questions

    **Q: What is an LBO?**
    A: A Leveraged Buyout (LBO) is a transaction where a company is acquired using a significant amount of debt, with the company's assets and cash flows used as collateral.

    **Q: What is the typical hold period?**
    A: Most LBOs have a 3-7 year hold period, with 5 years being most common.

    **Q: What are typical target returns?**
    A: Target IRR is typically 20-30%, with MOIC of 2.0-3.0x for a 5-year hold.

    ### Technical Questions

    **Q: How is IRR calculated?**
    A: IRR is the discount rate that makes the net present value of all cash flows equal to zero. It's calculated iteratively using the cash flows from equity investment to exit.

    **Q: What is the difference between IRR and MOIC?**
    A: IRR is time-weighted (annualized return), while MOIC is a simple multiple. A 2.5x MOIC over 5 years = ~20% IRR.

    **Q: How does leverage affect returns?**
    A: Higher leverage increases returns (more debt = less equity = higher returns on equity) but also increases risk (higher interest expense, lower coverage ratios).

    **Q: What is a cash flow sweep?**
    A: A cash flow sweep uses excess free cash flow to pay down debt, reducing interest expense and increasing equity value over time.

    ### Using the Tool

    **Q: How do I load a test case?**
    A: In the Assumptions page, use the "Load Test Case" dropdown at the top to select from pre-configured examples.

    **Q: Can I save my scenarios?**
    A: Yes! Use the comparison features to save scenarios and compare them side-by-side.

    **Q: How do I export results?**
    A: The tool supports Excel export (full model) and JSON export (configuration). Look for export buttons in the relevant sections.

    **Q: What if I get an error?**
    A: Check that all inputs are within reasonable ranges. Review validation warnings. If issues persist, check the error message for specific guidance.

    ### AI Features

    **Q: Do I need an API key for AI features?**
    A: Yes, AI features require an OpenAI API key. Set it in `.streamlit/secrets.toml` or as an environment variable.

    **Q: What AI features are available?**
    A: AI validation, natural language queries, market benchmarking, and scenario generation.

    ### Advanced Questions

    **Q: Can I model multiple debt instruments?**
    A: Yes! In the Debt Structure section, select "Senior + Subordinated" to configure multiple tranches.

    **Q: How do I interpret break-even analysis?**
    A: Break-even analysis shows the minimum values needed to achieve your target IRR. If break-even > current, you need to improve that assumption.

    **Q: What is a tornado chart?**
    A: A tornado chart shows which assumptions have the greatest impact on returns, sorted by magnitude of impact.
    """)

    st.markdown("---")
    st.markdown("### Still Have Questions?")
    st.info("💡 Check the other help tabs for more detailed information, or review the tooltips on each input field.")
