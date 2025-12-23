"""
Streamlit App for LBO Deal Screener

Main entry point - redirects to multi-page structure.
"""

import streamlit as st

# IMPORTANT: st.set_page_config() must be the FIRST Streamlit command
st.set_page_config(
    page_title="LBO Deal Screener",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",  # Force sidebar to be open
)

from streamlit_modules.app_config import initialize_session_state, get_openai_api_key, AI_AVAILABLE

# Initialize
initialize_session_state()
OPENAI_API_KEY = get_openai_api_key()

# Show status for API key
if OPENAI_API_KEY:
    st.success("✅ OpenAI API key configured. AI features are enabled.")
else:
    st.warning(
        "⚠️ OpenAI API key not found. AI features will be disabled. Set OPENAI_API_KEY environment variable or configure in .streamlit/secrets.toml"
    )

# Main page content (will be shown if user navigates to home)
st.title("🚀 Professional LBO Deal Screener")

st.markdown(
    """
Welcome to the LBO Deal Screener! This tool helps you analyze leveraged buyout opportunities.

### Getting Started

1. **⚙️ Assumptions** - Configure your LBO model inputs
2. **📊 Dashboard** - View high-level results and key metrics
3. **📈 Analysis** - Explore sensitivity analysis and enhanced visualizations
4. **🤖 AI Features** - Get AI-powered insights and recommendations
5. **📊 Comparison** - Compare multiple scenarios side-by-side
6. **💾 Export** - Download Excel models and export configurations

### Quick Tips

- Start by loading a test case or configuring assumptions
- Use the sidebar in the Assumptions page to set your inputs
- Click "Calculate LBO Model" to run the analysis
- Navigate between pages using the sidebar menu

### Features

✅ Multiple debt instruments support
✅ Real-time validation feedback
✅ AI-powered analysis (requires API key)
✅ Enhanced visualizations
✅ Scenario comparison
✅ Excel export
"""
)

# Show current status
if st.session_state.current_results:
    st.success("✅ Model calculated! Navigate to Dashboard or Analysis to view results.")
else:
    st.info("👈 Go to the Assumptions page to configure and calculate your first model.")
