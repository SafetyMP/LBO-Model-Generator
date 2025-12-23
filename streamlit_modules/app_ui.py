"""
UI components for Streamlit app.

Includes sidebar navigation and common UI elements.
"""

import streamlit as st
from streamlit_modules.app_config import initialize_session_state


def render_sidebar_navigation():
    """
    Render custom sidebar navigation menu.

    Note: Streamlit automatically generates page navigation from pages/ directory,
    but this provides additional navigation context.
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📑 Navigation")

    # Page links (Streamlit handles this automatically, but we can add context)
    pages_info = {
        "📊 Dashboard": "View results and key metrics",
        "⚙️ Assumptions": "Configure model inputs",
        "📈 Analysis": "Sensitivity and visualizations",
        "ℹ️ Help": "Documentation and guides",
    }

    for page, description in pages_info.items():
        st.sidebar.markdown(f"**{page}**")
        st.sidebar.caption(description)

    st.sidebar.markdown("---")


def render_sidebar_footer():
    """Render footer in sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.caption("LBO Deal Screener v2.0")
    st.sidebar.caption("Professional LBO analysis tool")

    # Show current model status
    if st.session_state.get('current_results'):
        st.sidebar.success("✅ Model Calculated")
    else:
        st.sidebar.info("👈 Configure & Calculate")


def add_sidebar_navigation_to_page():
    """
    Add navigation to sidebar.
    Call this at the top of each page to add consistent navigation.
    """
    # Navigation is automatically handled by Streamlit pages
    # This function can add additional navigation elements if needed
    pass
